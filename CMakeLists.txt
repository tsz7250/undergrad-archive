cmake_minimum_required(VERSION 3.10)
# vcpkg toolchain integration
set(CMAKE_TOOLCHAIN_FILE "${CMAKE_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")

project(CSVMiniDB LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find csv-parser
find_package(unofficial-vincentlaucsb-csv-parser CONFIG REQUIRED)

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
target_link_libraries(csv_mini_db PRIVATE unofficial::vincentlaucsb-csv-parser::csv)

# Add tests subdirectory
add_subdirectory(test)
