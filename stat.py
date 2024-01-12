import re

flag = False

dask_time = []
other_time = []

with open("./time.txt", "r") as f:
    for line in f:
        line = line.strip()

        if flag:
            time = line.split(" ")[0]
            match = re.search(r"(\d+\.\d+)", time)
            if match is None:
                flag = False
                continue
            if "dask" in line:
                dask_time.append(float(match.group(1)))
            else:
                other_time.append(float(match.group(1)))

        if "slowest durations" in line:
            flag = True

print("##################################################")
print("Time Report")
print("##################################################")
print(f"dask took {sum(dask_time):.2f}s")
print(f"other took {sum(other_time):.2f}s")
print(f"ratio is {sum(dask_time)/(sum(other_time) + sum(dask_time)):.2f}s")
print(f"total time is {sum(dask_time) + sum(other_time):.2f}s")
