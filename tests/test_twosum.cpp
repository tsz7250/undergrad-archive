#include <iostream>
#include <vector>
#include <cassert>
#include <algorithm>
#include <string>
#include <chrono>
#include "TwoSumArray.h"
#include "TwoSumHashTable.h"

// Helper function to compare actually returned indices to expected ignoring order
bool compareResult(const std::vector<int>& actual, const std::vector<int>& expected) {
    if (actual.size() != expected.size()) {
        return false;
    }
    if (actual.empty()) {
        return true;
    }
    std::vector<int> actual_sorted = actual;
    std::vector<int> expected_sorted = expected;
    std::sort(actual_sorted.begin(), actual_sorted.end());
    std::sort(expected_sorted.begin(), expected_sorted.end());
    return actual_sorted == expected_sorted;
}

void printResult(const std::string& name, const std::vector<int>& nums, int target, const std::vector<int>& expected, const std::vector<int>& actual) {
    std::cout << "[" << name << "] Target: " << target << " | Expected: ";
    if (expected.empty()) std::cout << "[]";
    else std::cout << "[" << expected[0] << ", " << expected[1] << "]";
    std::cout << " | Actual: ";
    if (actual.empty()) std::cout << "[]";
    else std::cout << "[" << actual[0] << ", " << actual[1] << "]";
    
    if (compareResult(actual, expected)) {
        std::cout << " -> PASS\n";
    } else {
        std::cout << " -> FAIL\n";
    }
}

bool runTestCase(const std::string& testName, const std::vector<int>& nums, int target, const std::vector<int>& expected) {
    std::cout << "--- " << testName << " ---\n";
    
    std::vector<int> resArray = twoSumArray(nums, target);
    std::vector<int> resHash = twoSumHashTable(nums, target);

    printResult("TwoSumArray", nums, target, expected, resArray);
    printResult("TwoSumHashTable", nums, target, expected, resHash);

    bool arrayPass = compareResult(resArray, expected);
    bool hashPass = compareResult(resHash, expected);

    if (!arrayPass || !hashPass) {
        std::cerr << "Test failed: " << testName << std::endl;
        return false;
    }
    return true;
}

void runPerformanceTest(int size) {
    std::cout << "--- Performance Test (N = " << size << ") ---\n";
    std::vector<int> nums(size);
    for (int i = 0; i < size; ++i) {
        nums[i] = i + 1;
    }
    // We set target such that the solution is at the very end of the array.
    // This forces both algorithms to process almost the entire array (worst-case).
    int target = nums[size - 2] + nums[size - 1]; 

    // Benchmark TwoSumArray
    auto startArray = std::chrono::steady_clock::now();
    std::vector<int> resArray = twoSumArray(nums, target);
    auto endArray = std::chrono::steady_clock::now();
    auto durationArray = std::chrono::duration_cast<std::chrono::microseconds>(endArray - startArray).count();

    // Benchmark TwoSumHashTable
    auto startHash = std::chrono::steady_clock::now();
    std::vector<int> resHash = twoSumHashTable(nums, target);
    auto endHash = std::chrono::steady_clock::now();
    auto durationHash = std::chrono::duration_cast<std::chrono::microseconds>(endHash - startHash).count();

    // Verify correctness: Ensure they return exactly 2 indices and their values sum up to target
    bool arrayCorrect = (resArray.size() == 2) && (nums[resArray[0]] + nums[resArray[1]] == target);
    bool hashCorrect = (resHash.size() == 2) && (nums[resHash[0]] + nums[resHash[1]] == target);

    if (!arrayCorrect || !hashCorrect) {
        std::cerr << "Performance test failed! Incorrect result.\n";
    }

    std::cout << "TwoSumArray (O(n log n)) time: " << durationArray << " us\n";
    std::cout << "TwoSumHashTable (O(n)) time:     " << durationHash << " us\n";
}

int main() {
    std::cout << "=== Running Two Sum Automated Tests ===\n\n";

    bool allPassed = true;

    // Test Case 1: Normal cases
    allPassed &= runTestCase("Test 1: Normal Case", {2, 7, 11, 15}, 9, {0, 1});

    // Test Case 2: Negative numbers
    allPassed &= runTestCase("Test 2: Negative Numbers", {-3, 4, 3, 90}, 0, {0, 2});

    // Test Case 3: Duplicate values
    allPassed &= runTestCase("Test 3: Duplicate Values", {3, 3}, 6, {0, 1});

    // Test Case 4: No solution
    allPassed &= runTestCase("Test 4: No Solution", {1, 2, 3}, 7, {});

    // Test Case 5: Extreme bounds
    allPassed &= runTestCase("Test 5: Extreme Bounds", {1000000000, -1000000000}, 0, {0, 1});

    std::cout << "\n=== Running Performance Tests ===\n\n";
    runPerformanceTest(10000);
    runPerformanceTest(100000);
    runPerformanceTest(1000000);

    std::cout << "\n=======================================\n";
    if (allPassed) {
        std::cout << "ALL TESTS PASSED SUCCESSFULLY.\n";
        return 0; // Success exit code
    } else {
        std::cerr << "SOME TESTS FAILED. PLEASE CHECK OUTPUT.\n";
        return 1; // Error exit code
    }
}
