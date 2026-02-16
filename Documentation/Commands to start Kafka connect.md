--to start the confluent services
taukir@Taukir-Predator:~$confluent local services start

--to stop the confluent services
taukir@Taukir-Predator:~$confluent local services stop

--to see the list of topics
taukir@Taukir-Predator:~$ kafka-topics --bootstrap-server localhost:9092 --list

--to install the kafdrop in wsl
taukir@Taukir-Predator:~$ curl -LO https://github.com/obsidiandynamics/kafdrop/releases/download/4.0.1/kafdrop-4.0.1.jar

--to run the kafdrop portal
taukir@Taukir-Predator:~$ java --add-opens=java.base/sun.nio.ch=ALL-UNNAMED \
 -jar kafdrop-4.0.1.jar \
 --kafka.brokerConnect=localhost:9092

--to access KafDrop
http://localhost:9000/

--Update the config file to connector in kafka
taukir@Taukir-Predator:~$curl -X POST -H "Content-Type: application/json" --data @data_transfer_config.json http://localhost:8083/connectors

--to delete the connector
taukir@Taukir-Predator:~$curl -X DELETE http://localhost:8083/connectors/deparments-transfer-data-jdbc-source-connector-v1

--to check the list of connectors - plugins
http://localhost:8083/connector-plugins

--to see the list of connector
http://localhost:8083/connectors

--to check the status of connector
http://localhost:8083/connectors/deparments-transfer-data-jdbc-source-connector-v1/status

--to see the live messages comming into the topic
taukir@Taukir-Predator:~$confluent local services kafka consume department-transfer-data-v1 --from-beginning

===================================================================================

To start from starting

1.  Turn On WSL terminal in the system

2.  Start the Infrastructure:

    > taukir@Taukir-Predator:~$ confluent local services start

3.  Start your Database

    > Postgres DB

4.  After infrastructure starts working

    > check the Kafka JDBC connector [that connects Postgres > Kafka Topic] status is running or not, by following:
    > Url : http://localhost:8083/connectors/deparments-transfer-data-jdbc-source-connector-v1/status

    --JDBC Connector
    {

        > If connector is not running then
        > taukir@Taukir-Predator:~$ curl -X POST -H "Content-Type: application/json" --data @data_transfer_config.json http://localhost:8083/connectors

        > Current IP for my system is used in Connector's config file
        > Kafka Connect - config file > connection.url [ip address is used to map port Postgres server] [windows postgres server -> WSL Kafka cluster & kafka Connect]
        > ip address used in config file :
            "connection.url": "jdbc:postgresql://172.20.128.1:5432/postgres"

    }

    --Elastic Search Sink Connect
    {

        > If sink connector is not running then
        > taukir@Taukir-Predator:~$ curl -X POST -H "Content-Type: application/json" --data @elastic_search-sink-config.json http://localhost:8083/connectors

        > check the status of elastic Search sink connector
        >> http://localhost:8083/connectors/elastic_search-sink-v1/status

            > is status comes failed, check following

            1. if Elastic search 9.X.X is used, then elastic sink connector is not able to communicate with Elastic search, so giving error : 400 : ElasticSinkSearchException.

            2. Ksql by defaults create topic name in UpperCase, and elastic search is case sensitive, so elastic search sink connector not able to link Ksql 's topic to ES index.

    }

5.  GUI to View Kafka Cluster > KafDrop

    > taukir@Taukir-Predator:~$ java --add-opens=java.base/sun.nio.ch=ALL-UNNAMED \
    > -jar kafdrop-4.0.1.jar \
    > --kafka.brokerConnect=localhost:9092

6.  To stream the messages live in terminal:

    > taukir@Taukir-Predator:~$ confluent local services kafka consume department-transfer-data-v1 --from-beginning

    \*\*department-transfer-data-v1 : Topic mentioned in config File / Topic name showing in KafDrop

7.  To see the logs that what are queries fire from kafka connect, to debug

    > # Look for the SELECT statement the connector is using
    >
    > taukir@Taukir-Predator:~$ confluent local services connect log | grep -i "SELECT"

8.  To update the config file in wsl

    > taukir@Taukir-Predator:~$ nano data_transfer_config.json

9.  To Start the ksqlDB (for data transforming)

    > taukir@Taukir-Predator:~$ksql

10. Check the list of streams

    > taukir@Taukir-Predator:~$ show streams

11. To create a stream

    > show stream
    > if streams is not working > refer to Ksql document
