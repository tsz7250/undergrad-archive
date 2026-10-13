#include <gtest/gtest.h>
#include "csv_parser.h"
#include <fstream>
#include <stdexcept>
#include <sstream>

using namespace csv_db;

class CSVParserTest : public ::testing::Test {
protected:
    // Helper to create temporary CSV file
    std::string createTestCSV(const std::string& content) {
        static int counter = 0;
        std::string filename = "test_" + std::to_string(counter++) + ".csv";
        std::ofstream file(filename);
        file << content;
        file.close();
        return filename;
    }

    void TearDown() override {
        // Clean up test files (optional)
    }
};

// UT-01: Basic CSV parsing (comma-separated, no quotes)
TEST_F(CSVParserTest, ParseBasicCSV) {
    std::string csv_content = "Name,Age,Grade\nAlice,20,A\nBob,19,B\n";
    std::string filename = createTestCSV(csv_content);

    CSVParser parser;
    auto rows = parser.parseFile(filename);

    EXPECT_EQ(rows.size(), 2);
    EXPECT_EQ(rows[0]["Name"], "Alice");
    EXPECT_EQ(rows[0]["Age"], "20");
    EXPECT_EQ(rows[0]["Grade"], "A");
    EXPECT_EQ(rows[1]["Name"], "Bob");
    EXPECT_EQ(rows[1]["Age"], "19");
    EXPECT_EQ(rows[1]["Grade"], "B");
}

// UT-01: Parse quoted fields
TEST_F(CSVParserTest, ParseQuotedFields) {
    std::string csv_content = R"(Name,Description,Price
"Alice Smith","Product for Alice",100.50
"Bob Jones","Product with ""quotes""",200.00
)";
    std::string filename = createTestCSV(csv_content);

    CSVParser parser;
    auto rows = parser.parseFile(filename);

    EXPECT_EQ(rows.size(), 2);
    EXPECT_EQ(rows[0]["Name"], "Alice Smith");
    EXPECT_EQ(rows[0]["Description"], "Product for Alice");
}

// UT-01: Empty fields and missing columns
TEST_F(CSVParserTest, ParseEmptyFields) {
    std::string csv_content = "Name,Age,Grade\nAlice,20,\nBob,,B\n";
    std::string filename = createTestCSV(csv_content);

    CSVParser parser;
    auto rows = parser.parseFile(filename);

    EXPECT_EQ(rows.size(), 2);
    EXPECT_EQ(rows[0]["Grade"], "");
    EXPECT_EQ(rows[1]["Age"], "");
}

// UT-01: Column names preserved
TEST_F(CSVParserTest, ColumnNamesPreserved) {
    std::string csv_content = "First_Name,Last_Name,Email\nJohn,Doe,john@example.com\n";
    std::string filename = createTestCSV(csv_content);

    CSVParser parser;
    auto rows = parser.parseFile(filename);
    auto columns = parser.getColumnNames();

    EXPECT_EQ(columns.size(), 3);
    EXPECT_EQ(columns[0], "First_Name");
    EXPECT_EQ(columns[1], "Last_Name");
    EXPECT_EQ(columns[2], "Email");
}

// UT-01: File not found
TEST_F(CSVParserTest, FileNotFound) {
    CSVParser parser;
    EXPECT_THROW(parser.parseFile("nonexistent_file.csv"),
                 std::runtime_error);
}

// UT-01: Empty file
TEST_F(CSVParserTest, EmptyFile) {
    std::string filename = createTestCSV("");
    CSVParser parser;
    EXPECT_THROW(parser.parseFile(filename), std::runtime_error);
}
