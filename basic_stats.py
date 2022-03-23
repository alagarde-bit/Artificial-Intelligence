def avg(nums: list()):
    sum=0
    count=0
    for num in nums:
        sum = num + sum
        count = count + num
        avg = sum / count
    return avg

def l_sqr(nums: list()):
    nums = [num ** 2 for num in nums]
    return nums
    
def var(nums: list()):
    n = len(nums)
    mean = sum(nums) / n
    deviations_sq = [(num-mean)**2 for num in nums]
    var = sum(deviations_sq)/n
    return var
