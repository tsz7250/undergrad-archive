#include <gtest/gtest.h>
#include "utils.h"

using namespace csv_db;

class TypeInferenceTest : public ::testing::Test {};

// UT-05: Infer integer field
TEST_F(TypeInferenceTest, InferIntegerField) {
    std::vector<std::string> values = {"10", "20", "30", "40", "50"};
    FieldType type = inferFieldType(values);
    EXPECT_EQ(type, FieldType::INTEGER);
}

// UT-05: Infer floating point field
TEST_F(TypeInferenceTest, InferFloatingPointField) {
    std::vector<std::string> values = {"10.5", "20.3", "30.1"};
    FieldType type = inferFieldType(values);
    EXPECT_EQ(type, FieldType::FLOATING_POINT);
}

// UT-05: Infer string field
TEST_F(TypeInferenceTest, InferStringField) {
    std::vector<std::string> values = {"Alice", "Bob", "Charlie"};
    FieldType type = inferFieldType(values);
    EXPECT_EQ(type, FieldType::STRING);
}

// UT-05: Mixed with mostly integers
TEST_F(TypeInferenceTest, MostlyIntegers) {
    std::vector<std::string> values = {"10", "20", "30", "forty"};
    FieldType type = inferFieldType(values, 0.75);  // 75% threshold
    EXPECT_EQ(type, FieldType::INTEGER);
}

// UT-05: Mixed with mostly strings
TEST_F(TypeInferenceTest, MostlyStrings) {
    std::vector<std::string> values = {"Alice", "Bob", "20", "Charlie"};
    FieldType type = inferFieldType(values, 0.5);  // 50% threshold
    EXPECT_EQ(type, FieldType::STRING);
}

// UT-05: Empty values
TEST_F(TypeInferenceTest, EmptyValues) {
    std::vector<std::string> values;
    FieldType type = inferFieldType(values);
    EXPECT_EQ(type, FieldType::STRING);  // Default
}

// UT-05: Single value integer
TEST_F(TypeInferenceTest, SingleIntegerValue) {
    std::vector<std::string> values = {"42"};
    FieldType type = inferFieldType(values);
    EXPECT_EQ(type, FieldType::INTEGER);
}

// UT-05: With empty strings
TEST_F(TypeInferenceTest, WithEmptyStrings) {
    std::vector<std::string> values = {"10", "", "20", "", "30"};
    FieldType type = inferFieldType(values, 0.6);
    EXPECT_EQ(type, FieldType::INTEGER);
}

// UT-05: Negative numbers
TEST_F(TypeInferenceTest, NegativeNumbers) {
    std::vector<std::string> values = {"-10", "-20", "-30"};
    FieldType type = inferFieldType(values);
    EXPECT_EQ(type, FieldType::INTEGER);
}

// UT-05: Scientific notation
TEST_F(TypeInferenceTest, FloatingPointVariants) {
    std::vector<std::string> values = {"1.5", "2.5", "3.5"};
    FieldType type = inferFieldType(values);
    EXPECT_EQ(type, FieldType::FLOATING_POINT);
}
