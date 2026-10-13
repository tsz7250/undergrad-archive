#ifndef CSV_MINIDB_EXECUTION_ENGINE_H
#define CSV_MINIDB_EXECUTION_ENGINE_H

#include "types.h"
#include "storage.h"
#include "hash_index.h"
#include <string>
#include <vector>
#include <map>
#include <memory>

namespace csv_db {

/**
 * @class ExecutionEngine
 * @brief Executes parsed queries against indexed data
 *
 * Responsibilities (SDS-M005):
 * - Execute queries based on AST
 * - Use hash indices for fast lookups
 * - Perform set operations (intersection for AND, union for OR)
 * - Extract result rows and specified columns
 *
 * Query execution flow:
 * 1. Parse WHERE condition (AST)
 * 2. For each simple condition, use hash index to find matching RowIDs
 * 3. Combine results using AND (intersection) or OR (union)
 * 4. Extract specified columns from result rows
 */
class ExecutionEngine {
public:
    /**
     * @brief Constructor
     * @param storage Reference to StorageLayer
     * @param index Reference to HashIndexBuilder
     */
    ExecutionEngine(const StorageLayer& storage, const HashIndexBuilder& index)
        : storage_(storage), index_(index) {}

    ~ExecutionEngine() = default;

    /**
     * @brief Execute a parsed query and return result rows
     * @param query The parsed query
     * @return Vector of result rows (each row as column -> value map)
     */
    std::vector<std::map<std::string, std::string>> execute(
        const ParsedQuery& query);

private:
    const StorageLayer& storage_;
    const HashIndexBuilder& index_;

    /**
     * @brief Evaluate WHERE condition AST and return matching RowIDs
     * @param condition The AST node to evaluate
     * @return Sorted vector of matching RowIDs
     */
    std::vector<RowID> evaluateCondition(const std::shared_ptr<ASTNode>& condition);

    /**
     * @brief Evaluate a leaf node (comparison)
     * @return Vector of RowIDs matching the comparison
     */
    std::vector<RowID> evaluateLeaf(const std::shared_ptr<ASTNode>& leaf);

    /**
     * @brief Evaluate AND node (set intersection)
     */
    std::vector<RowID> evaluateAnd(const std::shared_ptr<ASTNode>& and_node);

    /**
     * @brief Evaluate OR node (set union)
     */
    std::vector<RowID> evaluateOr(const std::shared_ptr<ASTNode>& or_node);

    /**
     * @brief Extract specified columns from result RowIDs
     */
    std::vector<std::map<std::string, std::string>> extractColumns(
        const std::vector<RowID>& row_ids,
        const std::vector<std::string>& select_columns);
};

}  // namespace csv_db

#endif  // CSV_MINIDB_EXECUTION_ENGINE_H
