#include "TwoSumHashTable.h"
#include <unordered_map>
#include <utility>

std::vector<int> twoSumHashTable(const std::vector<int>& nums, int target) {
    std::unordered_map<int, int> numMap;
    
    for (int i = 0; i < nums.size(); ++i) {
        int complement = target - nums[i];
        if (numMap.find(complement) != numMap.end()) {
            int idx1 = numMap[complement];
            int idx2 = i;
            if (idx1 > idx2) std::swap(idx1, idx2);
            return {idx1, idx2};
        }
        numMap[nums[i]] = i;
    }
    
    return {}; // No solution
}
