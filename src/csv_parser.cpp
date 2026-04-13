#include "csv_parser.h"
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <algorithm>

namespace csv_db {

std::vector<std::map<std::string, std::string>>
CSVParser::parseFile(const std::string& file_path) {
    std::vector<std::map<std::string, std::string>> rows;
    column_names_.clear();

    // Open file
    std::ifstream file(file_path);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + file_path);
    }

    std::string line;

    // Read header line
    if (!std::getline(file, line)) {
        if (file.eof()) {
            // Empty file - throw exception
            throw std::runtime_error("Empty CSV file: " + file_path);
        }
        throw std::runtime_error("Failed to read header from file: " + file_path);
    }

    // Parse header (simple comma-separated, no quote handling for now)
    // TODO: Implement proper CSV parsing with quote handling
    std::stringstream header_ss(line);
    std::string column;
    while (std::getline(header_ss, column, ',')) {
        // Trim whitespace
        column.erase(0, column.find_first_not_of(" \t\r\n"));
        column.erase(column.find_last_not_of(" \t\r\n") + 1);
        column_names_.push_back(column);
    }

    if (column_names_.empty()) {
        throw std::runtime_error("No columns found in CSV header");
    }

    // Read data rows
    size_t row_index = 0;
    while (std::getline(file, line)) {
        if (line.empty()) continue;  // Skip empty lines

        std::map<std::string, std::string> row;
        std::stringstream row_ss(line);
        std::string field;
        size_t col_index = 0;

        while (std::getline(row_ss, field, ',') && col_index < column_names_.size()) {
            // Trim whitespace
            field.erase(0, field.find_first_not_of(" \t\r\n"));
            field.erase(field.find_last_not_of(" \t\r\n") + 1);

            // Remove surrounding quotes if present
            if (field.length() >= 2 && field.front() == '"' && field.back() == '"') {
                field = field.substr(1, field.length() - 2);
            }

            row[column_names_[col_index]] = field;
            col_index++;
        }

        // Handle case where row has fewer columns than header
        for (size_t i = col_index; i < column_names_.size(); ++i) {
            row[column_names_[i]] = "";
        }

        rows.push_back(row);
        row_index++;
    }

    file.close();
    return rows;
}

}  // namespace csv_db
