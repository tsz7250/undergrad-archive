#include <iostream>
#include <vector>
#include "TwoSumArray.h"
#include "TwoSumHashTable.h"

int main() {
    std::cout << "=== Two Sum ===" << std::endl;
    
    int n;
    std::cout << "Enter the number of elements: ";
    if (!(std::cin >> n) || n <= 0) {
        std::cerr << "Invalid input or size must be > 0." << std::endl;
        return 1;
    }

    std::vector<int> nums(n);
    std::cout << "Enter " << n << " integers: ";
    for (int i = 0; i < n; ++i) {
        if (!(std::cin >> nums[i])) {
            std::cerr << "Invalid input for array element." << std::endl;
            return 1;
        }
    }

    int target;
    std::cout << "Enter the target sum: ";
    if (!(std::cin >> target)) {
        std::cerr << "Invalid input for target." << std::endl;
        return 1;
    }

    // Call the two sum functions
    std::vector<int> resultArray = twoSumArray(nums, target);
    std::vector<int> resultHash = twoSumHashTable(nums, target);

    std::cout << "\n[TwoSumArray Result]: ";
    if (!resultArray.empty()) {
        std::cout << "Indices " << resultArray[0] << " and " << resultArray[1] << std::endl;
    } else {
        std::cout << "No solution found." << std::endl;
    }

    std::cout << "[TwoSumHashTable Result]: ";
    if (!resultHash.empty()) {
        std::cout << "Indices " << resultHash[0] << " and " << resultHash[1] << std::endl;
    } else {
        std::cout << "No solution found." << std::endl;
    }

    return 0;
}