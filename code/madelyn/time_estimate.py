import numpy as np

file_data = np.load("./cache/timing_probest/times_high_10000.npz", allow_pickle=True)

times = file_data["inline_times"]

print("time length", len(times))
time_sum = 0

for time in times:
    print(time/3600)
    time_sum = time_sum + time

print("hours: ", time_sum / 3600)


