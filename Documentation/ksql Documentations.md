ksql Documentations

--check that ksql is running in system or not

> http://localhost:8088/info

--how to start ksql

> taukir@Taukir-Predator:~$ksql

--show list of streams
taukir@Taukir-Predator:~$show streams

--create a stream (just like table in sql) for existing topic
ksql> CREATE STREAM st_dept_stream (
department_id INT,
department_name VARCHAR,
changed_date VARCHAR,
new_column1 VARCHAR,
new_column2 VARCHAR) WITH (
KAFKA_TOPIC = 'department-transfer-data-v1',
VALUE_FORMAT = 'JSON');

--create a enchanced stream to make updated data
ksql>
CREATE STREAM st_dept_enriched
WITH(KAFKA_TOPIC='st_dept_enriched', VALUE_FORMAT='JSON')
AS SELECT *,
'MyGlobal-Corp-IN' AS company_name,
TIMESTAMPTOSTRING(ROWTIME, 'yyyy-MM-dd HH:mm:ss') as processed_at
FROM st_dept_stream;

--to see the changes live in the enriched stream
SELECT * FROM st_dept_enriched EMIT CHANGES;