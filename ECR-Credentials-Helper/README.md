Keeping AWS Registry pull credentials fresh in Kubernetes

1-) Create K8s secret that contain all envs 
```shell
            - AWS_ACCESS_KEY_ID: ###################
            - AWS_ACCOUNT: ###################
            - AWS_REGION: ###################
            - AWS_SECRET_ACCESS_KEY: ###################==
            - DOCKER_SECRET_NAME: ###################==
```
```shell
kubectl apply -f secret.yaml
```    
2-) Create K8s CronJob to create secret for ECR credentials (mount the above created Secret to this cronjob)
   - The CronJob runs with a Service Account that is allowed to delete and update secrets
```shell
kubectl apply -f cronjob.yaml
```       
