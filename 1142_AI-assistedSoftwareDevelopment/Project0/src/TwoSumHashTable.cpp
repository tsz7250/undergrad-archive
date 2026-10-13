#include "TwoSumHashTable.h"
#include <unordered_map>
#include <utility>

std::vector<int> twoSumHashTable(const std::vector<int>& nums, int target) {
    std::unordered_map<int, int> numMap;
    
    for (std::size_t i = 0; i < nums.size(); ++i) {
        int complement = target - nums[i];
        if (numMap.find(complement) != numMap.end()) {
            int idx1 = numMap[complement];
            int idx2 = static_cast<int>(i);
            if (idx1 > idx2) std::swap(idx1, idx2);
            return {idx1, idx2};
        }
        numMap[nums[i]] = static_cast<int>(i);
    }
    
    return {}; // No solution
}
