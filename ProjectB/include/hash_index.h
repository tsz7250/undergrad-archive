#ifndef CSV_MINIDB_HASH_INDEX_H
#define CSV_MINIDB_HASH_INDEX_H

#include "types.h"
#include "storage.h"
#include <string>
#include <vector>
#include <map>

namespace csv_db {

/**
 * @class HashIndexBuilder
 * @brief Builds and manages hash indices for efficient query execution
 *
 * Responsibilities (SDS-M003):
 * - Create hash index for each column
 * - Support O(1) exact-match lookups
 * - Map column values to lists of RowIDs
 *
 * Index structure:
 * index[column_name][value] = {rowid1, rowid2, ...}
 *
 * Time complexity for building: O(n*m) where n=rows, m=columns
 */
class HashIndexBuilder {
public:
    HashIndexBuilder() = default;
    ~HashIndexBuilder() = default;

    /**
     * @brief Build indices for all columns from storage layer
     * @param storage Reference to StorageLayer containing data
     */
    void buildIndices(const StorageLayer& storage);

    /**
     * @brief Get the hash index (read-only)
     * @return Const reference to the hash index
     */
    const HashIndex& getIndex() const { return index_; }

    /**
     * @brief Clear all indices
     */
    void clear() { index_.clear(); }

    /**
     * @brief Lookup value in a column
     * @param column Column name
     * @param value Value to search for
     * @return Vector of RowIDs matching the value, or empty vector if not found
     */
    std::vector<RowID> lookup(const std::string& column,
                              const std::string& value) const;

    /**
     * @brief Check if a column has an index
     */
    bool hasColumnIndex(const std::string& column) const;

    /**
     * @brief Get all unique values for a column
     * @return Vector of unique values, or empty if column not indexed
     */
    std::vector<std::string> getUniqueValues(const std::string& column) const;

private:
    HashIndex index_;  ///< Main index structure

    /**
     * @brief Build index for a single column
     */
    void buildColumnIndex(const std::string& column, const StorageLayer& storage);
};

}  // namespace csv_db

#endif  // CSV_MINIDB_HASH_INDEX_H
