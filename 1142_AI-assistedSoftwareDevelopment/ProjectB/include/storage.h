#ifndef CSV_MINIDB_STORAGE_H
#define CSV_MINIDB_STORAGE_H

#include "types.h"
#include <string>
#include <vector>
#include <map>

namespace csv_db {

/**
 * @class StorageLayer
 * @brief Manages in-memory storage of parsed CSV data
 *
 * Responsibilities (SDS-M002):
 * - Store parsed data in memory
 * - Assign unique RowID to each row
 * - Maintain column information
 * - Support row access by RowID
 *
 * Data structure:
 * - rows: vector of Row structs indexed by RowID
 * - columns: list of column names in order
 */
class StorageLayer {
public:
    StorageLayer() : next_row_id_(0) {}
    ~StorageLayer() = default;

    /**
     * @brief Clear all stored data and reset RowID counter
     */
    void clear();

    /**
     * @brief Add a row to storage and assign RowID
     * @param row_data Map of column -> value
     * @return Assigned RowID
     */
    RowID addRow(const std::map<std::string, std::string>& row_data);

    /**
     * @brief Get row by RowID
     * @param row_id The RowID to retrieve
     * @return Pointer to the Row struct, nullptr if not found
     */
    const Row* getRow(RowID row_id) const;

    /**
     * @brief Get all rows
     * @return Const reference to the rows vector
     */
    const std::vector<Row>& getAllRows() const { return rows_; }

    /**
     * @brief Get column names
     * @return Vector of column names
     */
    const std::vector<std::string>& getColumnNames() const { return columns_; }

    /**
     * @brief Get total number of rows
     */
    size_t getRowCount() const { return rows_.size(); }

    /**
     * @brief Set column names (typically from CSV header)
     */
    void setColumnNames(const std::vector<std::string>& columns) {
        columns_ = columns;
    }

    /**
     * @brief Get index of a column by name
     * @return Column index, or std::string::npos if not found
     */
    size_t getColumnIndex(const std::string& column_name) const;

    /**
     * @brief Check if a column exists
     */
    bool hasColumn(const std::string& column_name) const;

private:
    std::vector<Row> rows_;              ///< All rows indexed by RowID
    std::vector<std::string> columns_;   ///< Column names in order
    RowID next_row_id_;                  ///< Counter for assigning RowIDs
};

}  // namespace csv_db

#endif  // CSV_MINIDB_STORAGE_H
