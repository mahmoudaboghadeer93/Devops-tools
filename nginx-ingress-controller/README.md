***If you have Helm, you can deploy the ingress controller with the following command:***
this for default ELB type (classic).
```shell
 helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
```
**OR**
this for NLB type 
```shell
helm upgrade --install ingress-nginx ingress-nginx \                                       
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"="nlb"
```

***If you want a full list of values that you can set, while installing with Helm, then run:***

```shell
helm show values ingress-nginx --repo https://kubernetes.github.io/ingress-nginx
```

***If you don't have Helm or if you prefer to use a YAML manifest, you can run the following command instead:***

I'm using NLB here

```shell
kubectl apply -f nginx-all.yaml
```

[***RFC***](https://kubernetes.github.io/ingress-nginx/deploy/)

[***Helm chart***](https://artifacthub.io/packages/helm/bitnami/nginx-ingress-controller)

