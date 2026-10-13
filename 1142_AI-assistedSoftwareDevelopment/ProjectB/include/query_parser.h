#ifndef CSV_MINIDB_QUERY_PARSER_H
#define CSV_MINIDB_QUERY_PARSER_H

#include "types.h"
#include <string>
#include <vector>
#include <memory>
#include <stdexcept>

namespace csv_db {

/**
 * @class QueryParser
 * @brief Parses SQL-like query strings into AST
 *
 * Responsibilities (SDS-M004):
 * - Parse SQL-like query syntax
 * - Generate Abstract Syntax Tree (AST)
 * - Support SELECT clause with column selection
 * - Support WHERE clause with conditions
 * - Handle AND/OR logical combinations
 * - Handle comparison operators: =, <, >, <=, >=, !=
 *
 * Grammar (simplified):
 * query    ::= SELECT select_list FROM table WHERE where_condition
 * select_list ::= '*' | column (',' column)*
 * where_condition ::= or_expr
 * or_expr  ::= and_expr ('OR' and_expr)*
 * and_expr ::= comparison ('AND' comparison)*
 * comparison ::= column op value
 * op       ::= '=' | '<' | '>' | '<=' | '>=' | '!='
 *
 * Example: "SELECT Name, Age FROM data WHERE Grade = 'A' AND Age < '20'"
 */
class QueryParser {
public:
    QueryParser() = default;
    ~QueryParser() = default;

    /**
     * @brief Parse a query string
     * @param query_str The query string to parse
     * @return ParsedQuery structure containing SELECT columns and WHERE AST
     * @throws std::runtime_error if query syntax is invalid
     */
    ParsedQuery parse(const std::string& query_str);

private:
    // Tokenization and lexical analysis
    std::vector<std::string> tokens_;
    size_t current_token_;

    /**
     * @brief Tokenize the query string
     */
    void tokenize(const std::string& query_str);

    /**
     * @brief Get current token
     */
    std::string currentToken() const;

    /**
     * @brief Consume current token and advance
     */
    std::string consumeToken();

    /**
     * @brief Peek at current token without consuming
     */
    std::string peekToken() const;

    /**
     * @brief Check if current token matches given string (case-insensitive)
     */
    bool match(const std::string& expected);

    /**
     * @brief Check if end of tokens reached
     */
    bool isAtEnd() const;

    /**
     * @brief Throw parse error
     */
    void error(const std::string& message);

    // Parser methods (recursive descent)
    std::vector<std::string> parseSelectClause();
    std::shared_ptr<ASTNode> parseWhereClause();

    std::shared_ptr<ASTNode> parseOrExpression();
    std::shared_ptr<ASTNode> parseAndExpression();
    std::shared_ptr<ASTNode> parseComparison();
};

}  // namespace csv_db

#endif  // CSV_MINIDB_QUERY_PARSER_H
