#ifndef CSV_MINIDB_UTILS_H
#define CSV_MINIDB_UTILS_H

#include "types.h"
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <sstream>

namespace csv_db {

// ============================================================================
// String Utilities
// ============================================================================

/**
 * @brief Trim leading and trailing whitespace from a string
 * @param str Input string
 * @return Trimmed string
 */
inline std::string trim(const std::string& str) {
    size_t first = str.find_first_not_of(" \t\n\r");
    if (first == std::string::npos) return "";
    size_t last = str.find_last_not_of(" \t\n\r");
    return str.substr(first, (last - first + 1));
}

/**
 * @brief Split a string by delimiter
 * @param str Input string
 * @param delimiter Single character delimiter
 * @return Vector of substrings
 *
 * Example: split("a,b,c", ',') -> ["a", "b", "c"]
 */
inline std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> result;
    std::stringstream ss(str);
    std::string item;
    while (std::getline(ss, item, delimiter)) {
        result.push_back(item);
    }
    return result;
}

/**
 * @brief Convert string to lowercase
 */
inline std::string toLower(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c) { return std::tolower(c); });
    return result;
}

/**
 * @brief Convert string to uppercase
 */
inline std::string toUpper(const std::string& str) {
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(),
                   [](unsigned char c) { return std::toupper(c); });
    return result;
}

/**
 * @brief Check if string contains only numeric characters (and optionally decimal point)
 */
inline bool isNumeric(const std::string& str, bool allow_decimal = false) {
    if (str.empty()) return false;
    bool has_dot = false;
    for (size_t i = 0; i < str.length(); ++i) {
        char c = str[i];
        if (i == 0 && (c == '-' || c == '+')) continue;  // Allow sign at start
        if (allow_decimal && c == '.' && !has_dot) {
            has_dot = true;
            continue;
        }
        if (!std::isdigit(static_cast<unsigned char>(c))) return false;
    }
    return true;
}

/**
 * @brief Check if string is an integer
 */
inline bool isInteger(const std::string& str) {
    if (str.empty()) return false;
    for (size_t i = 0; i < str.length(); ++i) {
        char c = str[i];
        if (i == 0 && (c == '-' || c == '+')) continue;
        if (!std::isdigit(static_cast<unsigned char>(c))) return false;
    }
    return true;
}

/**
 * @brief Check if string is floating point
 */
inline bool isFloatingPoint(const std::string& str) {
    return isNumeric(str, true) && str.find('.') != std::string::npos;
}

// ============================================================================
// Type Inference
// ============================================================================

/**
 * @brief Infer field type based on sample values
 * @param values Vector of string values from a column
 * @param threshold Percentage threshold (0.0-1.0) for type detection
 * @return Inferred FieldType
 *
 * Logic:
 * - If > threshold of values are integers -> INTEGER
 * - Else if > threshold are floating point -> FLOATING_POINT
 * - Else -> STRING
 *
 * Default threshold is 0.8 (80%)
 */
inline FieldType inferFieldType(const std::vector<std::string>& values,
                                  double threshold = 0.8) {
    if (values.empty()) return FieldType::STRING;

    int int_count = 0;
    int float_count = 0;

    for (const auto& val : values) {
        std::string trimmed = trim(val);
        if (trimmed.empty()) continue;  // Ignore empty values

        if (isInteger(trimmed)) {
            int_count++;
        } else if (isFloatingPoint(trimmed)) {
            float_count++;
        }
    }

    double total = static_cast<double>(values.size());
    if (int_count > 0 && int_count / total >= threshold) {
        return FieldType::INTEGER;
    }
    if ((int_count + float_count) > 0 &&
        (int_count + float_count) / total >= threshold) {
        return FieldType::FLOATING_POINT;
    }

    return FieldType::STRING;
}

// ============================================================================
// Set Operations on RowID Vectors
// ============================================================================

/**
 * @brief Compute intersection (AND operation) of two sorted RowID vectors
 * @param a First sorted vector
 * @param b Second sorted vector
 * @return Intersection as sorted vector
 */
inline std::vector<RowID> setIntersection(const std::vector<RowID>& a,
                                           const std::vector<RowID>& b) {
    std::vector<RowID> result;
    std::set_intersection(a.begin(), a.end(), b.begin(), b.end(),
                          std::back_inserter(result));
    return result;
}

/**
 * @brief Compute union (OR operation) of two sorted RowID vectors
 * @param a First sorted vector
 * @param b Second sorted vector
 * @return Union as sorted vector (with duplicates removed)
 */
inline std::vector<RowID> setUnion(const std::vector<RowID>& a,
                                     const std::vector<RowID>& b) {
    std::vector<RowID> result;
    std::set_union(a.begin(), a.end(), b.begin(), b.end(),
                   std::back_inserter(result));
    return result;
}

/**
 * @brief Ensure a RowID vector is sorted (required for set operations)
 */
inline void sortRowIDs(std::vector<RowID>& rows) {
    std::sort(rows.begin(), rows.end());
}

// ============================================================================
// Comparison Utilities
// ============================================================================

/**
 * @brief Compare two values based on field type and operator
 * @param lhs Left-hand side value (from data)
 * @param op Operator: "=", "<", ">", "<=", ">=", "!="
 * @param rhs Right-hand side value (from query)
 * @param field_type Type of the field
 * @return true if comparison succeeds
 */
inline bool compareValues(const std::string& lhs, const std::string& op,
                          const std::string& rhs, FieldType field_type) {
    if (op == "=") {
        return lhs == rhs;
    }

    if (field_type == FieldType::STRING) {
        // String comparison
        if (op == "<") return lhs < rhs;
        if (op == ">") return lhs > rhs;
        if (op == "<=") return lhs <= rhs;
        if (op == ">=") return lhs >= rhs;
        if (op == "!=") return lhs != rhs;
    } else if (field_type == FieldType::INTEGER || field_type == FieldType::FLOATING_POINT) {
        // Numeric comparison
        try {
            double lhs_num = std::stod(lhs);
            double rhs_num = std::stod(rhs);
            if (op == "<") return lhs_num < rhs_num;
            if (op == ">") return lhs_num > rhs_num;
            if (op == "<=") return lhs_num <= rhs_num;
            if (op == ">=") return lhs_num >= rhs_num;
            if (op == "!=") return lhs_num != rhs_num;
        } catch (...) {
            // Fallback to string comparison if conversion fails
            if (op == "<") return lhs < rhs;
            if (op == ">") return lhs > rhs;
            if (op == "<=") return lhs <= rhs;
            if (op == ">=") return lhs >= rhs;
            if (op == "!=") return lhs != rhs;
        }
    }

    return false;
}

}  // namespace csv_db

#endif  // CSV_MINIDB_UTILS_H
