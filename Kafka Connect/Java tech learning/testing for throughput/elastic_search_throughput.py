import time
import requests


def of_get_current_es_count():
    cur_count_res = requests.get(
        "http://192.168.0.4:9200/kt_dbz_policies_proc_json_sr/_count"
    )
    curr_count = cur_count_res.json()["count"]
    return curr_count


start_time = time.time()

records = 100000
sleep_time_duration = 0.1

print(f"Waiting for elasticsearch to reach {records} records...")

curr_count = of_get_current_es_count()

print(f"Current count of elastic search : {curr_count}")

while True:
    temp_count = of_get_current_es_count()
    if temp_count - curr_count >= records:
        break
    time.sleep(sleep_time_duration)

end_time = time.time()
time_duration = end_time - start_time

print(f"total time for {records} rows : {time_duration:.2f} seconds ")
print(f"Throughput : {records / time_duration:.2f} rows/sec")
