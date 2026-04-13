cmake_minimum_required(VERSION 3.10)
project(CSVMiniDB LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# vcpkg toolchain integration (optional, for documentation)
# set(CMAKE_TOOLCHAIN_FILE "${CMAKE_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")

# Find csv-parser
find_package(csv-parser CONFIG REQUIRED)

# Include directory for all targets
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

# Main executable
add_executable(csv_mini_db 
    src/main.cpp
    src/csv_parser.cpp
    src/storage.cpp
    src/hash_index.cpp
    src/query_parser.cpp
    src/execution_engine.cpp
)

# Link csv-parser to main executable
# target_link_libraries(csv_mini_db PRIVATE csv::csv)
target_link_libraries(csv_mini_db PRIVATE csv)

# Add tests subdirectory
add_subdirectory(test)
