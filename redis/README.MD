 Redis(R) is an open source, advanced key-value store. It is often referred to as a data structure server since keys can contain strings, hashes, lists, sets and sorted sets.
 
 ## Installation

 Deploying Redis® architecture standalone Not replication with only one instance for 
 - Multiple databases 
 - Single write/read point (single master)

 ```
 helm repo add bitnami https://charts.bitnami.com/bitnami

 helm install staging bitnami/redis --version 16.13.2 -n redisdb --set architecture="standalone" --set auth.enabled=false

 ```

[Overview of chart and installation parameters&reg;](https://github.com/bitnami/charts/blob/main/bitnami/redis/README.md)
