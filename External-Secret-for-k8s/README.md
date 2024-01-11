***External Secrets***
External secret management for Kubernetes

****Installing with Helm****
The default install options will automatically install and manage the CRDs as part of your helm release. If you do not want the CRDs to be automatically upgraded and managed, you must set the installCRDs option to false. (e.g. --set installCRDS=false)

Uncomment the relevant line in the next steps to disable the automatic install of CRDs.

**Option** 1️⃣: Install from chart repository
helm repo add external-secrets https://charts.external-secrets.io
```shell
helm install external-secrets \
   external-secrets/external-secrets \
    -n external-secrets \
    --create-namespace \
  # --set installCRDs=false
```

**Create Iam Role Service Account ,IAM Policy**

1-) Create iam policy (*External-Secret-Policy*) to attace it to iam role.
    
```shell
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetResourcePolicy",
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret",
                "secretsmanager:ListSecretVersionIds"
            ],
            "Resource": [
                "arn:aws:secretsmanager:eu-central-1:${AWS_Account_ID}:secret:*"
            ]
        }
    ]
}
```
2-) Create **IAM Role Service Account** ,attache previous IAM Policy to it.
- Create Service Account IAMRole "[REF](https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html)."
```shell
   eksctl create iamserviceaccount --name secret-manager-sa --namespace external-secrets --cluster ${Cluster_Name} --profile ${AWS_profile_name} --region ${Region_name} --role-name External-Secret-Role \
       --attach-policy-arn arn:aws:iam::${Account_ID}:policy/External-Secret-Policy --approve
```

***Create ClusterSecretStore***
   **Note** we create Cluster Secret Store because we want it to have access on all namespaces

```shell
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
  name: global-secret-store
spec:
  provider:
    aws:
      auth:
        jwt:
          serviceAccountRef:
            name: secret-manager-sa
            namespace: external-secrets
      region: ${AWS_Region}
      service: SecretsManager
```
****To Test that working well***
1-) Create Secret Manager on AWS account Ex with name : test-eso , put any key , value.
2-) then create your external-secret resources in k8s

```shell
 ---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: test-eso
  namespace: default
spec:
  dataFrom:
    - extract:
        conversionStrategy: Default
        decodingStrategy: None
        key: test-eso
  refreshInterval: 10s
  secretStoreRef:
    kind: ClusterSecretStore
    name: global-secret-store
  target:
    creationPolicy: Owner
    deletionPolicy: Retain
    name: test-eso
```
3-) to see your create k8s secret 
```shell
 kubectl get secrets/test-eso
```

🎉 We are done - now we should have external secret in K8s. 🎉
