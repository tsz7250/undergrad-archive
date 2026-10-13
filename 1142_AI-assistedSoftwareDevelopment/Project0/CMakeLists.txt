cmake_minimum_required(VERSION 3.15)
project(TwoSum LANGUAGES CXX VERSION 1.0.0)

# Set C++20 standard globally
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Create a library for TwoSum implementations
add_library(twosum_lib
    src/TwoSumArray.cpp
    src/TwoSumHashTable.cpp
)

# Add include directories so consumers can find headers
target_include_directories(twosum_lib PUBLIC src)

# Create the main interactive executable
add_executable(solution src/main.cpp)

# Link the executable with the library
target_link_libraries(solution PRIVATE twosum_lib)

# Create the test executable
add_executable(test_twosum tests/test_twosum.cpp)

# Link the test executable with the library
target_link_libraries(test_twosum PRIVATE twosum_lib)

# Enable testing
enable_testing()

# Register the executable as a CTest test
add_test(NAME AllTests COMMAND test_twosum)
