import psycopg2
import time

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432",
)

cur = conn.cursor()

total_records = 100000
record_partition = 10000
print(f"Starting stress testing : {total_records} inserts.")

start_time = time.time()

for i in range(total_records):
    cur.execute(
        "INSERT INTO policies_mst(status, policy_name) VALUES (%s, %s)",
        (f"Applied - {i}", f"Stress_test_policy - {i}"),
    )
    if i % record_partition == 0:
        # commit the data in batches
        conn.commit()
        print(
            f"Inserted {i} records... | time taken : {round(time.time() - start_time, 2)}"
        )

conn.commit()
end_time = time.time()

print(f"Source DB finish, Time taken : {round(end_time - start_time, 2)} seconds")
cur.close()
conn.close()
