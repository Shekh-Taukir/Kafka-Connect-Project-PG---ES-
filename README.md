# Kafka-Connect-Project-PG--ES

## Postgres to Elasticsearch Pipeline via Kafka Connect

This project implements a reliable data bridge between PostgreSQL and Elasticsearch. It uses the Kafka Connect framework to automate the ingestion and indexing process without writing custom producer/consumer code.

==================================================

🔄 Data Flow
Extract: The JDBC Source Connector polls Postgres for new or updated rows using an incrementing ID or a timestamp column.

Transport: Records are published as structured JSON/Avro messages into a dedicated Kafka topic.

Load: The Elasticsearch Sink Connector consumes these messages and indexes them into an ES index for full-text search.

==================================================

🛠️ Tech Stack
Source: PostgreSQL

Orchestration: Apache Kafka & Kafka Connect

Connectors: \* confluentinc/kafka-connect-jdbc (Source)

confluentinc/kafka-connect-elasticsearch (Sink)

Destination: Elasticsearch & Kibana
