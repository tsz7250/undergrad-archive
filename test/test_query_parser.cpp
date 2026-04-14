#include <gtest/gtest.h>
#include "query_parser.h"

using namespace csv_db;

class QueryParserTest : public ::testing::Test {
protected:
    QueryParser parser;
};

// UT-04: Basic query parsing
TEST_F(QueryParserTest, ParseBasicQuery) {
    std::string query = "SELECT * FROM data WHERE Name = Alice";
    ParsedQuery result = parser.parse(query);

    EXPECT_EQ(result.select_columns.size(), 1);
    EXPECT_EQ(result.select_columns[0], "*");
    ASSERT_NE(result.where_condition, nullptr);
    EXPECT_EQ(result.where_condition->type, ASTNode::Leaf);
    EXPECT_EQ(result.where_condition->column, "Name");
    EXPECT_EQ(result.where_condition->op, "=");
    EXPECT_EQ(result.where_condition->value, "Alice");
}

// UT-04: Parse multiple columns
TEST_F(QueryParserTest, ParseMultipleColumns) {
    std::string query = "SELECT Name, Age, Grade FROM data WHERE Age = 20";
    ParsedQuery result = parser.parse(query);

    EXPECT_EQ(result.select_columns.size(), 3);
    EXPECT_EQ(result.select_columns[0], "Name");
    EXPECT_EQ(result.select_columns[1], "Age");
    EXPECT_EQ(result.select_columns[2], "Grade");
}

// UT-04: Parse AND condition
TEST_F(QueryParserTest, ParseANDCondition) {
    std::string query = "SELECT * FROM data WHERE Grade = A AND Age = 20";
    ParsedQuery result = parser.parse(query);

    ASSERT_NE(result.where_condition, nullptr);
    EXPECT_EQ(result.where_condition->type, ASTNode::AND);
    EXPECT_NE(result.where_condition->left, nullptr);
    EXPECT_NE(result.where_condition->right, nullptr);
}

// UT-04: Parse OR condition
TEST_F(QueryParserTest, ParseORCondition) {
    std::string query = "SELECT * FROM data WHERE Grade = A OR Grade = B";
    ParsedQuery result = parser.parse(query);

    ASSERT_NE(result.where_condition, nullptr);
    EXPECT_EQ(result.where_condition->type, ASTNode::OR);
}

// UT-04: Parse mixed AND/OR with precedence
TEST_F(QueryParserTest, ParseMixedANDOR) {
    std::string query =
        "SELECT * FROM data WHERE Grade = A AND Age = 20 OR Name = Bob";
    ParsedQuery result = parser.parse(query);

    ASSERT_NE(result.where_condition, nullptr);
    // OR has lower precedence, so root should be OR
    EXPECT_EQ(result.where_condition->type, ASTNode::OR);
    // Left child should be AND
    EXPECT_EQ(result.where_condition->left->type, ASTNode::AND);
}

// UT-04: Parse comparison operators
TEST_F(QueryParserTest, ParseComparisonOperators) {
    std::vector<std::string> queries = {
        "SELECT * FROM data WHERE Age = 20",
        "SELECT * FROM data WHERE Age < 25",
        "SELECT * FROM data WHERE Age > 18",
        "SELECT * FROM data WHERE Age <= 20",
        "SELECT * FROM data WHERE Age >= 18",
        "SELECT * FROM data WHERE Grade != A"};

    std::vector<std::string> expected_ops = {"=", "<", ">", "<=", ">=",
                                              "!="};

    for (size_t i = 0; i < queries.size(); ++i) {
        ParsedQuery result = parser.parse(queries[i]);
        EXPECT_EQ(result.where_condition->op, expected_ops[i])
            << "Failed for query: " << queries[i];
    }
}

// UT-04: Parse quoted values
TEST_F(QueryParserTest, ParseQuotedValues) {
    std::string query = "SELECT * FROM data WHERE Name = 'Alice'";
    ParsedQuery result = parser.parse(query);

    EXPECT_EQ(result.where_condition->value, "Alice");
}

// UT-04: Parse double quoted values
TEST_F(QueryParserTest, ParseDoubleQuotedValues) {
    std::string query = "SELECT * FROM data WHERE Name = \"Bob\"";
    ParsedQuery result = parser.parse(query);

    EXPECT_EQ(result.where_condition->value, "Bob");
}

// UT-04: Invalid syntax - missing SELECT
TEST_F(QueryParserTest, InvalidSyntaxMissingSelect) {
    std::string query = "* FROM data WHERE Age = 20";
    EXPECT_THROW(parser.parse(query), std::runtime_error);
}

// UT-04: Invalid syntax - missing WHERE
TEST_F(QueryParserTest, InvalidSyntaxMissingWhere) {
    std::string query = "SELECT * FROM data Age = 20";
    EXPECT_THROW(parser.parse(query), std::runtime_error);
}

// UT-04: Complex nested expression
TEST_F(QueryParserTest, ComplexNestedExpression) {
    std::string query =
        "SELECT Name FROM data WHERE (Grade = A AND Age < 25) OR (Grade = B AND "
        "Age > 18)";
    ParsedQuery result = parser.parse(query);

    ASSERT_NE(result.where_condition, nullptr);
    // Root should be OR
    EXPECT_EQ(result.where_condition->type, ASTNode::OR);
}
