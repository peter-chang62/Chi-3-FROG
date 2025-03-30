import time

# Using time.time()
start_time = time.time()
for _ in range(10_000_000):
    pass
end_time = time.time()
print(f"time.time() duration: {end_time - start_time:.6f} seconds")

# Using time.perf_counter_ns()
start_ns = time.perf_counter_ns()
for _ in range(10_000_000):
    pass
end_ns = time.perf_counter_ns()
print(f"time.perf_counter_ns() duration: {(end_ns - start_ns) / 1e9:.6f} seconds")
