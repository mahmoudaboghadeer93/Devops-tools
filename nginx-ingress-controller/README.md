***If you have Helm, you can deploy the ingress controller with the following command:***

```shell
 helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```
***If you want a full list of values that you can set, while installing with Helm, then run:***

```shell
helm show values ingress-nginx --repo https://kubernetes.github.io/ingress-nginx
```

***If you don't have Helm or if you prefer to use a YAML manifest, you can run the following command instead:***

```shell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
```

***RFC***

 https://kubernetes.github.io/ingress-nginx/deploy/
