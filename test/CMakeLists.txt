cmake_minimum_required(VERSION 3.10)

# Enable testing
enable_testing()

# Find GTest
find_package(GTest CONFIG REQUIRED)

# Include directory for headers
include_directories(${CMAKE_SOURCE_DIR}/include)

# Test source files
set(TEST_SOURCES
    test_csv_parser.cpp
    test_storage.cpp
    test_hash_index.cpp
    test_query_parser.cpp
    test_execution_engine.cpp
    test_type_inference.cpp
    ../src/csv_parser.cpp
    ../src/storage.cpp
    ../src/hash_index.cpp
    ../src/query_parser.cpp
    ../src/execution_engine.cpp
)

# Create test executable
add_executable(csv_db_tests ${TEST_SOURCES})

# Link dependencies
target_link_libraries(csv_db_tests 
    PRIVATE 
    GTest::gtest 
    GTest::gtest_main
    unofficial::vincentlaucsb-csv-parser::csv  # csv-parser library
)

# Register tests with ctest
add_test(NAME csv_db_tests COMMAND csv_db_tests)
