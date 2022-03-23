import sys
nums = sys.argv[1]
high_count = 0
num = nums[0]
for n in nums:

    num_count = nums.count(n)
    if(num_count > high_count):
        high_count = num_count
        num = n
print(num)




   


