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

**Create Iam Role Service Account**
1-) create iam policy (*External-Secret-Policy*) to attace it to iam role.
    
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
2-) Create IAM Role (*External-Secret-Role*) ,attache previous IAM Policy to it and use this Role in Service Account.
3-) Create K8s Service Account 
```shell
 apiVersion: v1
kind: ServiceAccount
metadata:
  name: secret-manager-sa
  namespace: external-secrets
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::${AWS_Account_ID}:role/External-Secret-Role
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
