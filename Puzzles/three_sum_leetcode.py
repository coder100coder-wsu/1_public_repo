from typing import List

def threeSum(nums: List[int]) -> List[List[int]]:
    index_1 = 0
    index_2 = 0
    index_3 = 0
    list_of_lists =[]
    sum_to_zero = 0
    for i in range(0, len(nums)):
        sum_to_zero = nums[i]
        # print("delta= ", delta)
        for j in range(i+1, len(nums)):
            if delta == nums[j]:
                index_2 = j
                index_1 = i
                break
        list_of_lists
    return list_of_lists


print(twoSum(nums=[2, 7, 11, 15], target=9))
print(twoSum(nums=[3, 2, 4], target=6))
print(twoSum(nums=[3, 3], target=6))
