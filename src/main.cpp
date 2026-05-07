#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include "TwoSumArray.h"
#include "TwoSumHashTable.h"

int main() {
    std::cout << "=== Two Sum Solver ===\n";
    std::cout << "Enter the target sum: ";
    std::string line;
    if (!std::getline(std::cin, line)) return 1;
    
    int target;
    std::istringstream issTarget(line);
    if (!(issTarget >> target)) {
        std::cerr << "Invalid input for target.\n";
        return 1;
    }

    std::cout << "Enter the array of numbers (separated by spaces on a single line): ";
    if (!std::getline(std::cin, line)) return 1;

    std::vector<int> nums;
    std::istringstream issNums(line);
    int num;
    while (issNums >> num) {
        nums.push_back(num);
    }

    if (nums.empty()) {
        std::cout << "No numbers entered.\n";
        return 0;
    }

    std::cout << "\nSolving Two Sum for target " << target << " with array of size " << nums.size() << "...\n";

    std::vector<int> resArray = twoSumArray(nums, target);
    std::vector<int> resHash = twoSumHashTable(nums, target);

    auto printArray = [](const std::vector<int>& v) {
        if (v.empty()) {
            std::cout << "[] (No solution found)";
        } else {
            std::cout << "[" << v[0] << ", " << v[1] << "]";
        }
    };

    std::cout << "Result from TwoSumArray (O(n log n)): ";
    printArray(resArray);
    std::cout << "\n";

    std::cout << "Result from TwoSumHashTable (O(n)):     ";
    printArray(resHash);
    std::cout << "\n";

    return 0;
}