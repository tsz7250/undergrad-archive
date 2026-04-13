#include "storage.h"
#include <algorithm>
#include <stdexcept>

namespace csv_db {

void StorageLayer::clear() {
    rows_.clear();
    columns_.clear();
    next_row_id_ = 0;
}

RowID StorageLayer::addRow(const std::map<std::string, std::string>& row_data) {
    Row row;
    row.id = next_row_id_;
    row.values = row_data;
    rows_.push_back(row);
    return next_row_id_++;
}

const Row* StorageLayer::getRow(RowID row_id) const {
    if (row_id >= rows_.size()) {
        return nullptr;
    }
    return &rows_[row_id];
}

size_t StorageLayer::getColumnIndex(const std::string& column_name) const {
    auto it = std::find(columns_.begin(), columns_.end(), column_name);
    if (it == columns_.end()) {
        return std::string::npos;
    }
    return std::distance(columns_.begin(), it);
}

bool StorageLayer::hasColumn(const std::string& column_name) const {
    return std::find(columns_.begin(), columns_.end(), column_name) != columns_.end();
}

}  // namespace csv_db
