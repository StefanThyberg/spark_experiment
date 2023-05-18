# spark_experiment

This is intended to be a local experiment to run Spark with Scala and set up several local Spark nodes through Docker. There are then two apps, one for analyzing bus positioning data (main.py) and another one to run an analysis counting different words in a text.

# Data installation

The bus data in main.py comes from http://web.mta.info/developers/MTA-Bus-Time-historical-data.html and needs to be placed into data with the filename referred to in apps/mta.py. The word_counter.py needs the same with an appropriately large text, in my case I used the collected works of Shakespeare from the Gutenberg project at https://www.gutenberg.org/ebooks/100

# Library installation

The lib directory needs to contain a jar for processing MTA information, for the mta.py script(mta-processing.jar, which I found here: https://github.com/mvillarrealb/docker-spark-cluster), as well as a library for accessing Postgresql (postgresql-42.2.22.jar)

# How to use

1. Insert the above data and libraries into their respective folders.

2. run `docker build -t cluster-apache-spark:3.0.2 .` (this can take about 40 min because the download from apache is slow) to build the base image

3. run `docker compose up -d` and let the nodes start up

4. Create a database called "word_data" in the postgres database

5. run `docker container exec -it spark_experiment-spark-master-1 /bin/bash` to get into the shell of the master spark node

6. finally, submit the word_counter job to spark by running `/opt/spark/bin/spark-submit --master spark://spark-master:7077 --jars /opt/spark-lib/postgresql-42.2.22.jar --driver-memory 1G --executor-memory 1G /opt/spark-apps/word_counter.py`

7. Check the database for results