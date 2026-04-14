#ifndef CSV_MINIDB_TYPES_H
#define CSV_MINIDB_TYPES_H

#include <string>
#include <vector>
#include <map>
#include <memory>
#include <cstddef>

namespace csv_db {

/**
 * @file types.h
 * @brief Core type definitions for CSV Mini Database
 */

// ============================================================================
// Basic Types
// ============================================================================

/// Unique identifier for each row
using RowID = size_t;

/// A single row with column -> value mapping
struct Row {
    RowID id;
    std::map<std::string, std::string> values;
};

// ============================================================================
// Hash Index Type
// ============================================================================

/**
 * Hash Index Structure:
 * index[column_name][column_value] = {rowid1, rowid2, ...}
 *
 * Supports O(1) exact match queries
 */
using HashIndex = std::map<std::string, std::map<std::string, std::vector<RowID>>>;

// ============================================================================
// Query AST (Abstract Syntax Tree)
// ============================================================================

/**
 * @class ASTNode
 * @brief Represents a node in the query Abstract Syntax Tree
 *
 * Supports binary AND/OR operations and leaf-level comparisons.
 * Example: "WHERE Grade = 'A' AND Age < '20'"
 * generates:
 *   AND
 *  /   \
 * =     <
 */
struct ASTNode {
    enum Type {
        Leaf,   ///< Leaf node: column op value
        AND,    ///< Logical AND node
        OR      ///< Logical OR node
    };

    Type type;

    // For Leaf nodes only:
    std::string column;        ///< Column name being compared
    std::string op;            ///< Comparison operator: =, <, >, <=, >=, !=
    std::string value;         ///< Value being compared against

    // For AND/OR nodes:
    std::shared_ptr<ASTNode> left;   ///< Left child node
    std::shared_ptr<ASTNode> right;  ///< Right child node

    // Constructors
    ASTNode() : type(Leaf), left(nullptr), right(nullptr) {}

    explicit ASTNode(Type t) : type(t), left(nullptr), right(nullptr) {}

    static std::shared_ptr<ASTNode> makeLeaf(const std::string& col,
                                              const std::string& o,
                                              const std::string& val) {
        auto node = std::make_shared<ASTNode>(Leaf);
        node->column = col;
        node->op = o;
        node->value = val;
        return node;
    }

    static std::shared_ptr<ASTNode> makeAndNode(std::shared_ptr<ASTNode> l,
                                                 std::shared_ptr<ASTNode> r) {
        auto node = std::make_shared<ASTNode>(AND);
        node->left = l;
        node->right = r;
        return node;
    }

    static std::shared_ptr<ASTNode> makeOrNode(std::shared_ptr<ASTNode> l,
                                                std::shared_ptr<ASTNode> r) {
        auto node = std::make_shared<ASTNode>(OR);
        node->left = l;
        node->right = r;
        return node;
    }
};

// ============================================================================
// Query Structure
// ============================================================================

/**
 * @struct ParsedQuery
 * @brief Represents a parsed SQL-like query
 *
 * Example: SELECT Name, Age FROM data WHERE Grade = 'A' AND Age < '20'
 */
struct ParsedQuery {
    std::vector<std::string> select_columns;  ///< Columns to return (or "*" for all)
    std::shared_ptr<ASTNode> where_condition; ///< WHERE condition tree

    ParsedQuery() : where_condition(nullptr) {}
};

// ============================================================================
// Field Type Inference
// ============================================================================

enum class FieldType {
    STRING,
    INTEGER,
    FLOATING_POINT
};

}  // namespace csv_db

#endif  // CSV_MINIDB_TYPES_H
