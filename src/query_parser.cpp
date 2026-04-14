#include "query_parser.h"
#include "utils.h"
#include <algorithm>
#include <sstream>

namespace csv_db {

ParsedQuery QueryParser::parse(const std::string& query_str) {
    tokens_.clear();
    current_token_ = 0;

    tokenize(query_str);

    ParsedQuery result;

    // Expect SELECT keyword
    if (!match("SELECT")) {
        error("Expected SELECT keyword");
    }

    // Parse SELECT clause
    result.select_columns = parseSelectClause();

    // Expect FROM keyword
    if (!match("FROM")) {
        error("Expected FROM keyword");
    }

    // Skip table name (we don't use it, just consume it)
    consumeToken();

    // Expect WHERE keyword
    if (!match("WHERE")) {
        error("Expected WHERE keyword");
    }

    // Parse WHERE condition
    result.where_condition = parseWhereClause();

    return result;
}

void QueryParser::tokenize(const std::string& query_str) {
    // Simple tokenization by whitespace and operators
    std::string current;
    std::vector<std::string> operators = {"=", "<", ">", "<=", ">=", "!="};

    for (size_t i = 0; i < query_str.length(); ++i) {
        char c = query_str[i];

        if (std::isspace(c)) {
            if (!current.empty()) {
                tokens_.push_back(current);
                current.clear();
            }
        } else if (c == '(' || c == ')' || c == ',') {
            if (!current.empty()) {
                tokens_.push_back(current);
                current.clear();
            }
            tokens_.push_back(std::string(1, c));
        } else if (c == '=' || c == '<' || c == '>' || c == '!') {
            if (!current.empty()) {
                tokens_.push_back(current);
                current.clear();
            }

            // Handle multi-character operators
            if (c == '<' && i + 1 < query_str.length() && query_str[i + 1] == '=') {
                tokens_.push_back("<=");
                i++;
            } else if (c == '>' && i + 1 < query_str.length() &&
                       query_str[i + 1] == '=') {
                tokens_.push_back(">=");
                i++;
            } else if (c == '!' && i + 1 < query_str.length() &&
                       query_str[i + 1] == '=') {
                tokens_.push_back("!=");
                i++;
            } else {
                tokens_.push_back(std::string(1, c));
            }
        } else if (c == '\'' || c == '"') {
            // Handle quoted strings
            if (!current.empty()) {
                tokens_.push_back(current);
                current.clear();
            }
            char quote = c;
            std::string quoted;
            i++;
            while (i < query_str.length() && query_str[i] != quote) {
                quoted += query_str[i];
                i++;
            }
            tokens_.push_back(quoted);
        } else {
            current += c;
        }
    }

    if (!current.empty()) {
        tokens_.push_back(current);
    }
}

std::string QueryParser::currentToken() const {
    if (isAtEnd()) return "";
    return tokens_[current_token_];
}

std::string QueryParser::consumeToken() {
    if (isAtEnd()) {
        error("Unexpected end of query");
    }
    return tokens_[current_token_++];
}

std::string QueryParser::peekToken() const {
    if (isAtEnd()) return "";
    return tokens_[current_token_];
}

bool QueryParser::match(const std::string& expected) {
    std::string current = toLower(currentToken());
    std::string exp = toLower(expected);
    if (current == exp) {
        consumeToken();
        return true;
    }
    return false;
}

bool QueryParser::isAtEnd() const { return current_token_ >= tokens_.size(); }

void QueryParser::error(const std::string& message) {
    throw std::runtime_error("Query parse error: " + message +
                             " at token: " + currentToken());
}

std::vector<std::string> QueryParser::parseSelectClause() {
    std::vector<std::string> columns;

    if (match("*")) {
        columns.push_back("*");
    } else {
        // Parse column list
        columns.push_back(consumeToken());

        while (match(",")) {
            columns.push_back(consumeToken());
        }
    }

    return columns;
}

std::shared_ptr<ASTNode> QueryParser::parseWhereClause() {
    return parseOrExpression();
}

std::shared_ptr<ASTNode> QueryParser::parseOrExpression() {
    auto left = parseAndExpression();

    while (match("OR")) {
        auto right = parseAndExpression();
        left = ASTNode::makeOrNode(left, right);
    }

    return left;
}

std::shared_ptr<ASTNode> QueryParser::parseAndExpression() {
    auto left = parseComparison();

    while (match("AND")) {
        auto right = parseComparison();
        left = ASTNode::makeAndNode(left, right);
    }

    return left;
}

std::shared_ptr<ASTNode> QueryParser::parseComparison() {
    // Handle parentheses
    if (match("(")) {
        auto expr = parseOrExpression();
        if (!match(")")) {
            error("Expected closing parenthesis");
        }
        return expr;
    }

    // Parse: column op value
    std::string column = consumeToken();

    // Check for operator
    std::string op = currentToken();
    std::vector<std::string> valid_ops = {"=", "<", ">", "<=", ">=", "!="};
    if (std::find(valid_ops.begin(), valid_ops.end(), op) == valid_ops.end()) {
        error("Expected comparison operator, got: " + op);
    }
    consumeToken();

    std::string value = consumeToken();

    return ASTNode::makeLeaf(column, op, value);
}

}  // namespace csv_db
