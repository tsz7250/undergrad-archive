#include <iostream>
#include <vector>
#include <cassert>
#include "src/TwoSumArray.h"
#include "src/TwoSumHashTable.h"

void checkTestCase(const std::string& name, const std::vector<int>& nums, int target, const std::vector<int>& expected) {
    std::cout << "[TEST] " << name << " ... ";
    std::vector<int> resArray = twoSumArray(nums, target);
    std::vector<int> resHash = twoSumHashTable(nums, target);

    if (resArray == expected && resHash == expected) {
        std::cout << "PASS" << std::endl;
    } else {
        std::cout << "FAIL" << std::endl;
        std::cerr << "  Expected: [";
        for (size_t i=0; i<expected.size(); ++i) std::cerr << expected[i] << (i+1==expected.size()?"":",");
        std::cerr << "]" << std::endl;
        std::cerr << "  TwoSumArray: [";
        for (size_t i=0; i<resArray.size(); ++i) std::cerr << resArray[i] << (i+1==resArray.size()?"":",");
        std::cerr << "]" << std::endl;
        std::cerr << "  TwoSumHashTable: [";
        for (size_t i=0; i<resHash.size(); ++i) std::cerr << resHash[i] << (i+1==resHash.size()?"":",");
        std::cerr << "]" << std::endl;
        exit(1);
    }
}

int main() {
    std::cout << "Running Tests for Two Sum" << std::endl;
    std::cout << "-----------------------------------" << std::endl;

    // Normal positive
    checkTestCase("Normal Case", {2, 7, 11, 15}, 9, {0, 1});

    // Negative numbers
    checkTestCase("Negative Numbers", {-3, 4, 3, 90}, 0, {0, 2});

    // Duplicates
    checkTestCase("Duplicates", {3, 3}, 6, {0, 1});

    // No solution
    checkTestCase("No Solution", {1, 2, 3}, 7, {});

    std::cout << "-----------------------------------" << std::endl;
    std::cout << "ALL TESTS PASSED!" << std::endl;
    return 0;
}
