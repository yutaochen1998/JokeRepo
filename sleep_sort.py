from multiprocessing.pool import ThreadPool
import time
import random

def sleep_sort(nums):
    shift = min(nums)
    scale = max(nums) - shift
    schedule = [((number - shift) / scale / 10 , number) for number in nums]
    pool = ThreadPool(len(nums))
    res = []
    def thread_sleep(params):
        sleep_time, number = params
        time.sleep(sleep_time)
        return number
    for number in pool.imap_unordered(thread_sleep, schedule):
        res.append(number)
    return res

if __name__ == "__main__":
    nums = [random.randint(1, 10)*random.random() for _ in range(10)]
    print(nums)
    print(sleep_sort(nums))

    # print('pr test')
    # yutao's PR test
