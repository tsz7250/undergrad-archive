#include <gtest/gtest.h>
#include "hash_index.h"
#include "storage.h"

using namespace csv_db;

class HashIndexTest : public ::testing::Test {
protected:
    StorageLayer storage;
    HashIndexBuilder index_builder;

    void SetUp() override {
        storage.clear();
        storage.setColumnNames({"ID", "Name", "Age", "Gender", "Grade", "GPA", "Department", "Email"});

        // Add test data
        storage.addRow({{"ID", "1"}, {"Name", "Alice"}, {"Age", "20"}, {"Gender", "Female"}, {"Grade", "A"}, {"GPA", "3.8"}, {"Department", "CS"}, {"Email", "alice@example.com"}});
        storage.addRow({{"ID", "2"}, {"Name", "Bob"}, {"Age", "20"}, {"Gender", "Male"}, {"Grade", "B"}, {"GPA", "3.2"}, {"Department", "Physics"}, {"Email", "bob@example.com"}});
        storage.addRow({{"ID", "3"}, {"Name", "Charlie"}, {"Age", "19"}, {"Gender", "Male"}, {"Grade", "A"}, {"GPA", "3.9"}, {"Department", "CS"}, {"Email", "charlie@example.com"}});
        storage.addRow({{"ID", "4"}, {"Name", "David"}, {"Age", "21"}, {"Gender", "Male"}, {"Grade", "A"}, {"GPA", "3.5"}, {"Department", "Math"}, {"Email", "david@example.com"}});

        index_builder.clear();
    }
};

// UT-03: Build indices
TEST_F(HashIndexTest, BuildIndices) {
    index_builder.buildIndices(storage);

    EXPECT_TRUE(index_builder.hasColumnIndex("Name"));
    EXPECT_TRUE(index_builder.hasColumnIndex("Age"));
    EXPECT_TRUE(index_builder.hasColumnIndex("Grade"));
    EXPECT_TRUE(index_builder.hasColumnIndex("GPA"));
}

// UT-03: Lookup exact match
TEST_F(HashIndexTest, LookupExactMatch) {
    index_builder.buildIndices(storage);

    auto result = index_builder.lookup("Name", "Alice");
    EXPECT_EQ(result.size(), 1);
    EXPECT_EQ(result[0], 0);
}

// UT-03: Lookup multiple matches
TEST_F(HashIndexTest, LookupMultipleMatches) {
    index_builder.buildIndices(storage);

    auto result = index_builder.lookup("Age", "20");
    EXPECT_EQ(result.size(), 2);
    // Results should be sorted
    EXPECT_EQ(result[0], 0);
    EXPECT_EQ(result[1], 1);
}

// UT-03: Lookup with no matches
TEST_F(HashIndexTest, LookupNoMatches) {
    index_builder.buildIndices(storage);

    auto result = index_builder.lookup("Name", "NonExistent");
    EXPECT_EQ(result.size(), 0);
}

// UT-03: Multiple duplicate values
TEST_F(HashIndexTest, MultipleDuplicateValues) {
    index_builder.buildIndices(storage);

    auto result = index_builder.lookup("Grade", "A");
    EXPECT_EQ(result.size(), 3);  // Alice, Charlie, David
    EXPECT_EQ(result[0], 0);
    EXPECT_EQ(result[1], 2);
    EXPECT_EQ(result[2], 3);
}

// UT-03: Get unique values
TEST_F(HashIndexTest, GetUniqueValues) {
    index_builder.buildIndices(storage);

    auto values = index_builder.getUniqueValues("Grade");
    EXPECT_EQ(values.size(), 2);  // A and B
    // Values might be in any order due to map traversal
}

// UT-03: Column not indexed returns empty
TEST_F(HashIndexTest, NonindexedColumnReturnsEmpty) {
    // Don't build indices
    auto result = index_builder.lookup("Name", "Alice");
    EXPECT_EQ(result.size(), 0);
}

// UT-03: Indices are sorted
TEST_F(HashIndexTest, IndicesSorted) {
    storage.clear();
    storage.setColumnNames({"ID"});

    // Add in non-sequential order
    storage.addRow({{"ID", "1"}});
    storage.addRow({{"ID", "2"}});
    storage.addRow({{"ID", "1"}});
    storage.addRow({{"ID", "3"}});
    storage.addRow({{"ID", "1"}});

    index_builder.buildIndices(storage);

    auto result = index_builder.lookup("ID", "1");
    EXPECT_EQ(result.size(), 3);
    // Results should be in sorted order
    EXPECT_LT(result[0], result[1]);
    EXPECT_LT(result[1], result[2]);
}

// UT-03: Clear indices
TEST_F(HashIndexTest, ClearIndices) {
    index_builder.buildIndices(storage);
    EXPECT_TRUE(index_builder.hasColumnIndex("Name"));

    index_builder.clear();
    EXPECT_FALSE(index_builder.hasColumnIndex("Name"));
}
