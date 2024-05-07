import threading
import multiprocessing
import json
import math
import random
import os
from typing import List

def sample_generator(size: int) -> List[dict]:
    sample = []

    name_sample = [
            "Ada Lovelance",
            "Alan Turing",
            "Charles Babbel",
            "Edsger W. Dijkstra",
            "von Neumann",
            ]

    name_sample_size = len(name_sample)

    for i in range(size):
        name_idx = int(name_sample_size * random.random())
        sample.append({
            "id": i,
            "name": name_sample[name_idx],
            "rand_int": int(4096 * random.random()),
            "rand_float": 4096 * random.random(),
            })

    return sample

def write_sample(sample: List[dict]):
    sample_json = open("assets/input/sample.json", "w")

    sample_json.write(json.dumps(sample))

    sample_json.close()

def read_sample() -> str:
    sample_json = open("assets/input/sample.json", "r")

    sample_bytes = sample_json.read()

    sample_json.close()

    return str(sample_bytes)

async def write_csv(idx: int, begin: int, end: int, dataset: List[dict], separator: str = ",") -> None:
    file_path = f"assets/output/part-{idx}.csv"
    wipe_file(file_path)

    csv_file = open(file_path, "a")

    for data in dataset[begin:end]:
        columns = []

        for keys in data.keys():
            columns.append(str(data[keys]))

        csv_file.write(separator.join(columns)+"\n")

    print(f"INFO: thread {idx+1} writting [{begin}:{end}]")

def wipe_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)

# Simulating an I/O operation
write_sample(sample_generator(100000))
data = json.loads(read_sample())
data_size = len(data)

threads = multiprocessing.cpu_count()
slice_size = data_size / threads

slices_per_thread = [ math.floor(slice_size) ] * threads

reminder = data_size % threads
if reminder != 0:
    for i in range(reminder):
        slices_per_thread[i] += 1


print(f"Lines: {len(data)}")
print(f"Threads: {threads}")
print(f"Lines/Threads: {slice_size}")
print(f"Reminder: {reminder}")
print(f"Slices per thread: {slices_per_thread}")

thread_handlers = []

b = 0
for idx in range(threads):
    e = b + slices_per_thread[idx]

    print(f"[{idx}]{b}:{e}")

    t = write_csv(idx, b, e, data)
    thread_handlers.append(t)

    print(t)
    break
    # t = threading.Thread(target=write_csv, args=[idx, b, e, data])
    # t.start()

    b = e
exit(0)

for thread_handler in thread_handlers:
    thread_handler.join()
