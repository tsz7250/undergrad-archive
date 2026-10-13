#include "hash_index.h"
#include <algorithm>

namespace csv_db {

void HashIndexBuilder::buildIndices(const StorageLayer& storage) {
    index_.clear();

    // Build index for each column
    for (const auto& column : storage.getColumnNames()) {
        buildColumnIndex(column, storage);
    }
}

void HashIndexBuilder::buildColumnIndex(const std::string& column,
                                        const StorageLayer& storage) {
    // Create entry for this column if not exists
    if (index_.find(column) == index_.end()) {
        index_[column] = std::map<std::string, std::vector<RowID>>();
    }

    // Iterate through all rows and build the index
    for (const auto& row : storage.getAllRows()) {
        auto it = row.values.find(column);
        if (it != row.values.end()) {
            const std::string& value = it->second;
            index_[column][value].push_back(row.id);
        }
    }

    // Sort RowID vectors for efficient set operations (intersection/union)
    for (auto& value_list : index_[column]) {
        std::sort(value_list.second.begin(), value_list.second.end());
    }
}

std::vector<RowID> HashIndexBuilder::lookup(const std::string& column,
                                            const std::string& value) const {
    auto col_it = index_.find(column);
    if (col_it == index_.end()) {
        return std::vector<RowID>();  // Column not indexed
    }

    auto value_it = col_it->second.find(value);
    if (value_it == col_it->second.end()) {
        return std::vector<RowID>();  // Value not found
    }

    return value_it->second;
}

bool HashIndexBuilder::hasColumnIndex(const std::string& column) const {
    return index_.find(column) != index_.end();
}

std::vector<std::string> HashIndexBuilder::getUniqueValues(
    const std::string& column) const {
    std::vector<std::string> values;

    auto col_it = index_.find(column);
    if (col_it == index_.end()) {
        return values;  // Column not indexed
    }

    for (const auto& value_list : col_it->second) {
        values.push_back(value_list.first);
    }

    return values;
}

}  // namespace csv_db
