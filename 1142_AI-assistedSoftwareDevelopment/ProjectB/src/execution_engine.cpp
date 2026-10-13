#include "execution_engine.h"
#include "utils.h"
#include <algorithm>
#include <stdexcept>

namespace csv_db {

std::vector<std::map<std::string, std::string>> ExecutionEngine::execute(
    const ParsedQuery& query) {
    // Evaluate WHERE condition to get matching RowIDs
    std::vector<RowID> matching_rows;

    if (query.where_condition) {
        matching_rows = evaluateCondition(query.where_condition);
    } else {
        // No WHERE clause, return all rows
        for (size_t i = 0; i < storage_.getRowCount(); ++i) {
            matching_rows.push_back(i);
        }
    }

    // Extract specified columns
    return extractColumns(matching_rows, query.select_columns);
}

std::vector<RowID> ExecutionEngine::evaluateCondition(
    const std::shared_ptr<ASTNode>& condition) {
    if (!condition) {
        return std::vector<RowID>();
    }

    switch (condition->type) {
        case ASTNode::Leaf:
            return evaluateLeaf(condition);
        case ASTNode::AND:
            return evaluateAnd(condition);
        case ASTNode::OR:
            return evaluateOr(condition);
        default:
            throw std::runtime_error("Unknown AST node type");
    }
}

std::vector<RowID> ExecutionEngine::evaluateLeaf(
    const std::shared_ptr<ASTNode>& leaf) {
    const std::string& column = leaf->column;
    const std::string& op = leaf->op;
    const std::string& value = leaf->value;

    std::vector<RowID> result;

    // Check if column exists
    if (!storage_.hasColumn(column)) {
        throw std::runtime_error("Column not found: " + column);
    }

    // For "=" operator, use hash index for O(1) lookup
    if (op == "=") {
        return index_.lookup(column, value);
    }

    // For other operators, scan all rows
    // TODO: Consider optimizing with type-aware comparisons
    for (const auto& row : storage_.getAllRows()) {
        auto it = row.values.find(column);
        if (it != row.values.end()) {
            const std::string& row_value = it->second;

            // Infer field type from column (could be cached)
            // For now, try numeric comparison first
            bool matches = false;

            // Try numeric comparison
            try {
                double row_val_num = std::stod(row_value);
                double query_val_num = std::stod(value);

                if (op == "<") {
                    matches = row_val_num < query_val_num;
                } else if (op == ">") {
                    matches = row_val_num > query_val_num;
                } else if (op == "<=") {
                    matches = row_val_num <= query_val_num;
                } else if (op == ">=") {
                    matches = row_val_num >= query_val_num;
                } else if (op == "!=") {
                    matches = row_val_num != query_val_num;
                }
            } catch (...) {
                // Fall back to string comparison
                if (op == "<") {
                    matches = row_value < value;
                } else if (op == ">") {
                    matches = row_value > value;
                } else if (op == "<=") {
                    matches = row_value <= value;
                } else if (op == ">=") {
                    matches = row_value >= value;
                } else if (op == "!=") {
                    matches = row_value != value;
                }
            }

            if (matches) {
                result.push_back(row.id);
            }
        }
    }

    // Sort for set operations
    std::sort(result.begin(), result.end());
    return result;
}

std::vector<RowID> ExecutionEngine::evaluateAnd(
    const std::shared_ptr<ASTNode>& and_node) {
    auto left_result = evaluateCondition(and_node->left);
    auto right_result = evaluateCondition(and_node->right);

    // Intersection (AND operation)
    return setIntersection(left_result, right_result);
}

std::vector<RowID> ExecutionEngine::evaluateOr(
    const std::shared_ptr<ASTNode>& or_node) {
    auto left_result = evaluateCondition(or_node->left);
    auto right_result = evaluateCondition(or_node->right);

    // Union (OR operation)
    return setUnion(left_result, right_result);
}

std::vector<std::map<std::string, std::string>> ExecutionEngine::extractColumns(
    const std::vector<RowID>& row_ids,
    const std::vector<std::string>& select_columns) {
    std::vector<std::map<std::string, std::string>> result;

    for (RowID row_id : row_ids) {
        const Row* row = storage_.getRow(row_id);
        if (!row) continue;

        std::map<std::string, std::string> result_row;

        if (select_columns.size() == 1 && select_columns[0] == "*") {
            // Select all columns
            result_row = row->values;
        } else {
            // Select specified columns
            for (const auto& col : select_columns) {
                auto it = row->values.find(col);
                if (it != row->values.end()) {
                    result_row[col] = it->second;
                } else {
                    result_row[col] = "";  // Missing column value
                }
            }
        }

        result.push_back(result_row);
    }

    return result;
}

}  // namespace csv_db
