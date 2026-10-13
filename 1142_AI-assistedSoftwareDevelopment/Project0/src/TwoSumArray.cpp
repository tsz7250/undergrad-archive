#include "TwoSumArray.h"
#include <algorithm>
#include <utility>

std::vector<int> twoSumArray(const std::vector<int>& nums, int target) {
    if (nums.empty()) return {};
    
    // Store original indices
    std::vector<std::pair<int, int>> sortedNums;
    sortedNums.reserve(nums.size());
    for (int i = 0; i < nums.size(); ++i) {
        sortedNums.push_back({nums[i], i});
    }
    
    // Sort array by value in O(n log n)
    std::sort(sortedNums.begin(), sortedNums.end(), [](const auto& a, const auto& b) {
        return a.first < b.first;
    });
    
    // Two-pointer approach
    int left = 0;
    int right = sortedNums.size() - 1;
    
    while (left < right) {
        int sum = sortedNums[left].first + sortedNums[right].first;
        if (sum == target) {
            int idx1 = sortedNums[left].second;
            int idx2 = sortedNums[right].second;
            // Ensure returning smaller index first to avoid flakiness in testing
            if (idx1 > idx2) std::swap(idx1, idx2);
            return {idx1, idx2};
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    
    return {}; // No solution
}
