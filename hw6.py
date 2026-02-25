def twosum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

# тестирование
nums = [2, 7, 11, 15]
target = 9
result = twosum(nums, target)
print(result)

print(twosum([3, 2, 4], 6))
print(twosum([3, 3], 6))