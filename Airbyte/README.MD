# Airbyte 

 
 ## Installation stpes

 Deploying Redis® architecture standalone Not replication with only one instance for 
 - Multiple databases 
 - Single write/read point (single master)

    ```bash
        helm repo add airbyte https://airbytehq.github.io/helm-charts
        helm repo update
        kubectl create namespace airbyte
        helm install --values values.yaml preprod-airbyte airbyte/airbyte -n airbyte
    ```

#For Upgrade:

    ```bash
        helm upgrade --install --values values.yaml preprod-airbyte airbyte/airbyte -n airbyte
    ```
