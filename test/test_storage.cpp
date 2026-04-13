#include <gtest/gtest.h>
#include "storage.h"

using namespace csv_db;

class StorageLayerTest : public ::testing::Test {
protected:
    StorageLayer storage;

    void SetUp() override {
        storage.clear();
        storage.setColumnNames({"Name", "Age", "Grade"});
    }
};

// UT-02: Add rows and assign RowID
TEST_F(StorageLayerTest, AddRowsAssignRowID) {
    std::map<std::string, std::string> row1 = {
        {"Name", "Alice"}, {"Age", "20"}, {"Grade", "A"}};
    std::map<std::string, std::string> row2 = {
        {"Name", "Bob"}, {"Age", "19"}, {"Grade", "B"}};

    RowID id1 = storage.addRow(row1);
    RowID id2 = storage.addRow(row2);

    EXPECT_EQ(id1, 0);
    EXPECT_EQ(id2, 1);
    EXPECT_EQ(storage.getRowCount(), 2);
}

// UT-02: Get row by RowID
TEST_F(StorageLayerTest, GetRowByID) {
    std::map<std::string, std::string> row = {
        {"Name", "Alice"}, {"Age", "20"}, {"Grade", "A"}};
    RowID id = storage.addRow(row);

    const Row* retrieved = storage.getRow(id);
    ASSERT_NE(retrieved, nullptr);
    EXPECT_EQ(retrieved->id, id);
    EXPECT_EQ(retrieved->values["Name"], "Alice");
    EXPECT_EQ(retrieved->values["Age"], "20");
}

// UT-02: Get all rows
TEST_F(StorageLayerTest, GetAllRows) {
    storage.addRow({{"Name", "Alice"}, {"Age", "20"}, {"Grade", "A"}});
    storage.addRow({{"Name", "Bob"}, {"Age", "19"}, {"Grade", "B"}});

    const auto& all_rows = storage.getAllRows();
    EXPECT_EQ(all_rows.size(), 2);
}

// UT-02: Row ID sequential from 0
TEST_F(StorageLayerTest, RowIDSequential) {
    for (int i = 0; i < 10; ++i) {
        std::map<std::string, std::string> row = {
            {"Name", "Person" + std::to_string(i)},
            {"Age", std::to_string(20 + i)},
            {"Grade", "A"}};
        RowID id = storage.addRow(row);
        EXPECT_EQ(id, i);
    }
}

// UT-02: Clear storage
TEST_F(StorageLayerTest, ClearStorage) {
    storage.addRow({{"Name", "Alice"}, {"Age", "20"}, {"Grade", "A"}});
    EXPECT_EQ(storage.getRowCount(), 1);

    storage.clear();
    EXPECT_EQ(storage.getRowCount(), 0);
}

// UT-02: Column names
TEST_F(StorageLayerTest, ColumnNames) {
    const auto& columns = storage.getColumnNames();
    EXPECT_EQ(columns.size(), 3);
    EXPECT_EQ(columns[0], "Name");
    EXPECT_EQ(columns[1], "Age");
    EXPECT_EQ(columns[2], "Grade");
}

// UT-02: Get column index
TEST_F(StorageLayerTest, GetColumnIndex) {
    EXPECT_EQ(storage.getColumnIndex("Name"), 0);
    EXPECT_EQ(storage.getColumnIndex("Age"), 1);
    EXPECT_EQ(storage.getColumnIndex("Grade"), 2);
    EXPECT_EQ(storage.getColumnIndex("NonExistent"), std::string::npos);
}

// UT-02: Has column
TEST_F(StorageLayerTest, HasColumn) {
    EXPECT_TRUE(storage.hasColumn("Name"));
    EXPECT_TRUE(storage.hasColumn("Age"));
    EXPECT_FALSE(storage.hasColumn("NonExistent"));
}

// UT-02: Get nonexistent row returns nullptr
TEST_F(StorageLayerTest, GetNonexistentRow) {
    storage.addRow({{"Name", "Alice"}, {"Age", "20"}, {"Grade", "A"}});
    const Row* row = storage.getRow(999);
    EXPECT_EQ(row, nullptr);
}
