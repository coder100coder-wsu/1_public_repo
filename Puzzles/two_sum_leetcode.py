from typing import List


def twoSum(nums: List[int], target: int) -> List[int]:
    index_1 = 0
    index_2 = 0
    for i in range(0, len(nums)):
        delta = target - nums[i]
        # print("delta= ", delta)
        for j in range(i+1, len(nums)):
            if delta == nums[j]:
                index_2 = j
                index_1 = i
                break
    return [index_1, index_2]


print(twoSum(nums=[2, 7, 11, 15], target=9))
print(twoSum(nums=[3, 2, 4], target=6))
print(twoSum(nums=[3, 3], target=6))
