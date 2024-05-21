from fastchan import parallel_ops as po
from tqdm import tqdm
import time


def p(x: int):
    return range(x)


def f(x):
    time.sleep(0.001)
    return x + 1


# dp = po.ParMap(range(10000), f, num_threads=10)
dp = po.ParFlatMap(range(1000), p, num_threads=10)
dp = po.ParMap(dp, f, num_threads=100)


for x in tqdm(dp):
    print(f"recv: {x}")
