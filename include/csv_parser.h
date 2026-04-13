#ifndef CSV_MINIDB_CSV_PARSER_H
#define CSV_MINIDB_CSV_PARSER_H

#include "types.h"
#include <string>
#include <vector>
#include <map>
#include <memory>

namespace csv_db {

/**
 * @class CSVParser
 * @brief Reads and parses CSV files
 *
 * Responsibilities (SDS-M001):
 * - Read CSV file from disk
 * - Parse rows and columns
 * - Handle quoted fields and escaped characters
 * - Support standard CSV format (comma-separated, quoted fields)
 *
 * Input: File path
 * Output: std::vector<std::map<std::string, std::string>>
 *         (each row as a map, keys are column names, values are field values)
 */
class CSVParser {
public:
    CSVParser() = default;
    ~CSVParser() = default;

    /**
     * @brief Parse a CSV file and return parsed rows
     * @param file_path Path to the CSV file
     * @return Vector of rows (each row is a map of column -> value)
     * @throws std::runtime_error if file cannot be read or parsed
     */
    std::vector<std::map<std::string, std::string>>
    parseFile(const std::string& file_path);

    /**
     * @brief Get column names from the last parsed file
     * @return Vector of column names in order
     */
    const std::vector<std::string>& getColumnNames() const {
        return column_names_;
    }

private:
    std::vector<std::string> column_names_;
};

}  // namespace csv_db

#endif  // CSV_MINIDB_CSV_PARSER_H
