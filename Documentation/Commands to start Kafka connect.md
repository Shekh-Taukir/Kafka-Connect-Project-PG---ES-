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

--Update the config file to JDBC connector in kafka
taukir@Taukir-Predator:~$curl -X POST -H "Content-Type: application/json" --data @data_transfer_config.json http://localhost:8083/connectors

--update/start the Elastic search sink connector in kafka
taukir@Taukir-Predator:~$curl -X POST -H "Content-Type: application/json" --data @elastic_search-sink-config.json http://localhost:8083/connectors

--update/start the elastic search sink connector for csv data in kafka
taukir@Taukir-Predator:~$curl -X POST -H "Content-Type: application/json" --data @elastic_search_csv_raw_data_config.json http://localhost:8083/connectors

--update/start the Spooler Source Connector in kafka
taukir@Taukir-Predator:~$curl -X POST -H "Content-Type: application/json" --data @spooler_config_v1.json http://localhost:8083/connectors

--to update/create the schema in kafka schema registry
taukir@Taukir-Predator:~$curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
 --data "{\"schema\": $(jq -Rs . < spooler_csv_schema_v1.json), \"schemaType\": \"JSON\"}" \
 http://localhost:8081/subjects/csv_raw_data-value/versions

--to check the subjects (schema registry for default schemas)
http://localhost:8081/subjects

--to check the content of subject
http://localhost:8081/subjects/csv_raw_data-value/versions/latest

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

--to see the logs for Connector issue
taukir@Taukir-Predator:~$confluent local services connect log -f

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

12. TO check the data in elastic search

    > [GET] curl http://192.168.0.10:9200/st_dept_enriched/_search?pretty

12.1. To create a index in elastic search

    >  curl -X PUT "192.168.0.4:9200/st_csv_raw_data_enriched"

12.2 get list of indexes

    > http://192.168.0.4:9200/_cat/indices?v

12.3 To delete index from elastic search

> curl -XDELETE 'http://localhost:9200/st_csv_raw_data_enriched'

13. To apply sort in ES result based on department_id
    > [POST] curl http://192.168.0.10:9200/st_dept_enriched/_search?pretty
    > {
        "query": {
            "match_all": {}
        },
        "sort": [
            {
            "DEPARTMENT_ID": {
                "order": "desc"
            }
            }
        ]
        }

===================================================================================

1.  if adding any new plugins directory in wsl like

    > elastic search
    > spooldir

    > then place that directory at

        /confluent-8.1.1/share/java/

2.  If any plugins are added in the system for confluent, then need to restart the confluent services

3.  If need to set the schema for csv file for a topic, then need to create a differnt csv.json file, and upload that to connect portals subject

    > if error occurs on running the curl like command jq not found then run this command
    > taukir@Taukir-Predator:~$sudo apt install jq -y

4.  To access wsl files in windows

    > run below command in cmd
    > explorer.exe \\wsl$
