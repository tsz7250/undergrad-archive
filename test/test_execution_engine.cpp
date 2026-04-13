#include <gtest/gtest.h>
#include "execution_engine.h"
#include "storage.h"
#include "hash_index.h"
#include "query_parser.h"

using namespace csv_db;

class ExecutionEngineTest : public ::testing::Test {
protected:
    StorageLayer storage;
    HashIndexBuilder index_builder;
    ExecutionEngine* engine;

    void SetUp() override {
        storage.clear();
        storage.setColumnNames({"Name", "Age", "Grade"});

        // Add test data
        storage.addRow({{"Name", "Alice"}, {"Age", "20"}, {"Grade", "A"}});
        storage.addRow({{"Name", "Bob"}, {"Age", "20"}, {"Grade", "B"}});
        storage.addRow({{"Name", "Charlie"}, {"Age", "19"}, {"Grade", "A"}});
        storage.addRow({{"Name", "David"}, {"Age", "21"}, {"Grade", "A"}});
        storage.addRow({{"Name", "Eve"}, {"Age", "20"}, {"Grade", "C"}});

        index_builder.buildIndices(storage);
        engine = new ExecutionEngine(storage, index_builder);
    }

    void TearDown() override { delete engine; }
};

// UT-06: Single condition with equality
TEST_F(ExecutionEngineTest, SingleConditionEquality) {
    // SELECT * FROM data WHERE Grade = A
    auto condition = ASTNode::makeLeaf("Grade", "=", "A");
    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 3);  // Alice, Charlie, David
}

// UT-06: Single condition with less than
TEST_F(ExecutionEngineTest, SingleConditionLessThan) {
    // SELECT * FROM data WHERE Age < 20
    auto condition = ASTNode::makeLeaf("Age", "<", "20");
    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 1);  // Charlie
    EXPECT_EQ(results[0]["Name"], "Charlie");
}

// UT-06: Single condition with greater than
TEST_F(ExecutionEngineTest, SingleConditionGreaterThan) {
    // SELECT * FROM data WHERE Age > 20
    auto condition = ASTNode::makeLeaf("Age", ">", "20");
    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 1);  // David
}

// UT-06: AND operation (intersection)
TEST_F(ExecutionEngineTest, ANDOperation) {
    // SELECT * FROM data WHERE Grade = A AND Age = 20
    auto left = ASTNode::makeLeaf("Grade", "=", "A");
    auto right = ASTNode::makeLeaf("Age", "=", "20");
    auto condition = ASTNode::makeAndNode(left, right);

    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 1);  // Only Alice
    EXPECT_EQ(results[0]["Name"], "Alice");
}

// UT-06: OR operation (union)
TEST_F(ExecutionEngineTest, OROperation) {
    // SELECT * FROM data WHERE Grade = B OR Grade = C
    auto left = ASTNode::makeLeaf("Grade", "=", "B");
    auto right = ASTNode::makeLeaf("Grade", "=", "C");
    auto condition = ASTNode::makeOrNode(left, right);

    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 2);  // Bob and Eve
}

// UT-06: Complex AND/OR expression
TEST_F(ExecutionEngineTest, ComplexExpression) {
    // SELECT * FROM data WHERE (Grade = A AND Age = 20) OR (Grade = B AND Age =
    // 20)
    auto and1_left = ASTNode::makeLeaf("Grade", "=", "A");
    auto and1_right = ASTNode::makeLeaf("Age", "=", "20");
    auto and1 = ASTNode::makeAndNode(and1_left, and1_right);

    auto and2_left = ASTNode::makeLeaf("Grade", "=", "B");
    auto and2_right = ASTNode::makeLeaf("Age", "=", "20");
    auto and2 = ASTNode::makeAndNode(and2_left, and2_right);

    auto condition = ASTNode::makeOrNode(and1, and2);

    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 2);  // Alice and Bob
}

// UT-06: Empty result set
TEST_F(ExecutionEngineTest, EmptyResultSet) {
    // SELECT * FROM data WHERE Grade = Z
    auto condition = ASTNode::makeLeaf("Grade", "=", "Z");
    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 0);
}

// UT-06: Select specific columns
TEST_F(ExecutionEngineTest, SelectSpecificColumns) {
    // SELECT Name, Age FROM data WHERE Grade = A
    auto condition = ASTNode::makeLeaf("Grade", "=", "A");
    ParsedQuery query;
    query.select_columns.push_back("Name");
    query.select_columns.push_back("Age");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 3);
    EXPECT_EQ(results[0].size(), 2);  // Only 2 columns
    EXPECT_TRUE(results[0].find("Name") != results[0].end());
    EXPECT_TRUE(results[0].find("Age") != results[0].end());
    EXPECT_TRUE(results[0].find("Grade") == results[0].end());
}

// UT-06: Select all columns
TEST_F(ExecutionEngineTest, SelectAllColumns) {
    // SELECT * FROM data WHERE Age >= 20
    auto condition = ASTNode::makeLeaf("Age", ">=", "20");
    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 4);  // Alice, Bob, David, Eve
    EXPECT_EQ(results[0].size(), 3);  // All columns
}

// UT-06: Not equal operator
TEST_F(ExecutionEngineTest, NotEqualOperator) {
    // SELECT * FROM data WHERE Grade != A
    auto condition = ASTNode::makeLeaf("Grade", "!=", "A");
    ParsedQuery query;
    query.select_columns.push_back("*");
    query.where_condition = condition;

    auto results = engine->execute(query);

    EXPECT_EQ(results.size(), 2);  // Bob and Eve
}
