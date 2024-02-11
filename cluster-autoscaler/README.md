***Deploy Cluster Autoscaler***

```shell
# Deploy the Cluster Autoscaler to your cluster
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml

# Add the cluster-autoscaler.kubernetes.io/safe-to-evict annotation to the deployment
kubectl -n kube-system annotate deployment.apps/cluster-autoscaler cluster-autoscaler.kubernetes.io/safe-to-evict="false"
```
***Edit Cluster Autoscaler Deployment to add Cluster name and two more parameters***

```shell
kubectl -n kube-system edit deployment.apps/cluster-autoscaler
```

***- Add cluster name***

```shell
# Before Change
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/<YOUR CLUSTER NAME>

# After Change
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/eksdemo1
```

***Add two more parameters***

```shell
        - --balance-similar-node-groups
        - --skip-nodes-with-system-pods=false
```
***Sample for reference***

```shell
    spec:
      containers:
      - command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/eksdemo1
        - --balance-similar-node-groups
        - --skip-nodes-with-system-pods=false
```

***Set the Cluster Autoscaler Image related to our current EKS Cluster version:***

 - Open https://github.com/kubernetes/autoscaler/releases
 - Find our release version (example: 1.28.n) and update the same.
 - Our Cluster version is 1.28 and our cluster autoscaler version is 1.18.2 as per above releases link
```shell
# Template
# Update Cluster Autoscaler Image Version
kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=us.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v1.XY.Z


# Update Cluster Autoscaler Image Version
kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=us.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v1.28.2
```

[***RFC***]([https://www.stacksimplify.com/aws-eks/aws-eks-kubernetes-autoscaling/learn-to-master-cluster-autoscaler-on-aws-eks/])

