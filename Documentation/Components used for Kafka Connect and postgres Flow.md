Components used for Flow

[
Postgres Table [Windows] > Kafka Connect > Kafka Topic [WSL > Ubuntu] > KSQL > Kakfa Sink Connect > Elastic Search
]

1. PostgreSQL (The Source)
   This is the System of Record. It lives on Windows host. It holds the departments table and acts as the "source of truth" where data originates.

2. Apache Kafka (The Backbone)
   The event streaming platform itself. It manages the Topics (like clean-data-departments) and ensures that messages are stored durably and in the correct order.

3. Kafka Connect (The Bridge)
   This is the "worker" or the "engine", where more time is spent, configuring. It has two main parts:

The Framework: A part of Kafka designed specifically to move data in and out.

The JDBC Source Connector: The specific "plugin" that knows how to speak SQL to Postgres and translate it into Kafka events.

4. Confluent CLI (The Control Center)
   Its used to manage the environment. It’s the tool that allows you to:

Start and stop the services (confluent local services start).

Watch the data stream (confluent local services kafka consume).

Check the health of the system.

5. Kafdrop (The Visualizer)
   This is Web UI. While Kafka is "invisible" (it runs in the background), Kafdrop gave you a browser-based window to see the topics, check message counts, and inspect the JSON payloads without using the command line.

6. The Transformation Layer (Stream Processing)
   ksqlDB Server: The software that allows you to write SQL against Kafka topics.
   ksqlDB CLI: The terminal where CREATE STREAM commands are implemented.

   Technical Detail: ksqlDB is actually running Kafka Streams code in the background, but it lets you use SQL so you don't have to write Java code.

7. The Search & Analytics Layer (Sink)
   Elasticsearch Sink Connector: The plugin that takes data from the enriched Kafka topic and sends it to ES.

Elasticsearch (v8.x): search engine and document store.

The "Hidden" Player: WSL 2

+1
Don't forget Windows Subsystem for Linux. It acted as the virtualization layer that allowed, Linux-based Kafka tools to coexist and communicate with Windows-based Postgres database.
