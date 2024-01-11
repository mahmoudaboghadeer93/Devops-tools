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
