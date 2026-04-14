#include "csv_parser.h"
#include "storage.h"
#include "hash_index.h"
#include "query_parser.h"
#include "execution_engine.h"
#include "utils.h"
#include <iostream>
#include <string>
#include <vector>
#include <iomanip>

using namespace csv_db;

/**
 * @brief Print usage information
 */
void printUsage(const char* program_name) {
    std::cout << "CSV Mini Database Query Engine\n\n";
    std::cout << "Usage: " << program_name << " <csv_file> <query>\n\n";
    std::cout << "Example:\n";
    std::cout << "  " << program_name
              << " data.csv \"SELECT * FROM data WHERE Age > 20\"\n";
    std::cout << "  " << program_name
              << " students.csv \"SELECT Name, Grade FROM students WHERE Grade = "
                 "'A' AND Age < '30'\"\n";
}

/**
 * @brief Format and print results as a table
 */
void printResults(
    const std::vector<std::string>& columns,
    const std::vector<std::map<std::string, std::string>>& rows) {
    if (rows.empty()) {
        std::cout << "No results found.\n";
        return;
    }

    // Determine column widths
    std::map<std::string, size_t> col_widths;
    for (const auto& col : columns) {
        col_widths[col] = col.length();
    }

    for (const auto& row : rows) {
        for (const auto& col : columns) {
            auto it = row.find(col);
            if (it != row.end()) {
                col_widths[col] =
                    std::max(col_widths[col], it->second.length());
            }
        }
    }

    // Print header
    for (size_t i = 0; i < columns.size(); ++i) {
        if (i > 0) std::cout << " | ";
        std::cout << std::left << std::setw(col_widths[columns[i]])
                  << columns[i];
    }
    std::cout << "\n";

    // Print separator
    for (size_t i = 0; i < columns.size(); ++i) {
        if (i > 0) std::cout << "-+-";
        std::cout << std::string(col_widths[columns[i]], '-');
    }
    std::cout << "\n";

    // Print rows
    for (const auto& row : rows) {
        for (size_t i = 0; i < columns.size(); ++i) {
            if (i > 0) std::cout << " | ";
            auto it = row.find(columns[i]);
            std::string value = (it != row.end()) ? it->second : "";
            std::cout << std::left << std::setw(col_widths[columns[i]])
                      << value;
        }
        std::cout << "\n";
    }

    std::cout << "\nTotal rows: " << rows.size() << "\n";
}

int main(int argc, char* argv[]) {
    // Check command line arguments
    if (argc != 3) {
        printUsage(argv[0]);
        return 1;
    }

    std::string csv_file = argv[1];
    std::string query_string = argv[2];

    try {
        // Step 1: Parse CSV file
        std::cout << "Loading CSV file: " << csv_file << "\n";
        CSVParser parser;
        auto parsed_rows = parser.parseFile(csv_file);
        std::cout << "  Loaded " << parsed_rows.size() << " rows\n";

        // Step 2: Load into storage layer
        std::cout << "Storing data in memory...\n";
        StorageLayer storage;
        storage.setColumnNames(parser.getColumnNames());
        for (const auto& row : parsed_rows) {
            storage.addRow(row);
        }
        std::cout << "  Storage layer ready\n";

        // Step 3: Build hash indices
        std::cout << "Building hash indices...\n";
        HashIndexBuilder index_builder;
        index_builder.buildIndices(storage);
        std::cout << "  Hash indices ready\n";

        // Step 4: Parse query
        std::cout << "Parsing query: " << query_string << "\n";
        QueryParser query_parser;
        ParsedQuery parsed_query = query_parser.parse(query_string);
        std::cout << "  Query parsed successfully\n";

        // Step 5: Execute query
        std::cout << "Executing query...\n";
        ExecutionEngine engine(storage, index_builder);
        auto results = engine.execute(parsed_query);
        std::cout << "  Query executed\n";

        // Step 6: Display results
        std::cout << "\nResults:\n";
        std::cout << "=========\n";

        // Determine which columns to display
        std::vector<std::string> display_columns;
        if (parsed_query.select_columns.size() == 1 &&
            parsed_query.select_columns[0] == "*") {
            display_columns = storage.getColumnNames();
        } else {
            display_columns = parsed_query.select_columns;
        }

        printResults(display_columns, results);

        return 0;

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
}
