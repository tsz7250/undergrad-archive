cmake_minimum_required(VERSION 3.10)
project(CSVMiniDB LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# vcpkg toolchain integration (optional, for documentation)
# set(CMAKE_TOOLCHAIN_FILE "${CMAKE_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")

# Find csv-parser
find_package(csv-parser CONFIG REQUIRED)

add_executable(csv_mini_db src/main.cpp)

# Link csv-parser
# target_link_libraries(csv_mini_db PRIVATE csv::csv)
target_link_libraries(csv_mini_db PRIVATE csv)

# GoogleTest (for未來測試)
# enable_testing()
# find_package(GTest CONFIG REQUIRED)
# add_executable(tests test/test_main.cpp)
# target_link_libraries(tests PRIVATE GTest::gtest_main)
# add_test(NAME AllTests COMMAND tests)
