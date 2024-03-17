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

***Notes:***

***1-) also if you don't use Cloudfront in front of ELB ,you use ACM on AWS ELB side so***
 - change the following values inside ingress-nginx-controller service ([***Issue***](https://github.com/kubernetes/ingress-nginx/issues/5206)
   
   **appProtocol: from https to http**
   
   **targetPort: from https to http**
      
<img width="301" alt="image" src="https://github.com/mahmoudaboghadeer93/Devops-tools/assets/69244659/a941fe46-a614-4ba8-a6bf-a02a3656c05f">


**The Nginx ingress controller can export Prometheus metrics.**

```shell
helm upgrade --install ingress-nginx ingress-nginx \                                       
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"="nlb" --set controller.metrics.enabled=true
```

You can add Prometheus annotations to the metrics service using controller.metrics.service.annotations. Alternatively, if you use the Prometheus Operator, you can enable ServiceMonitor creation using controller.metrics.serviceMonitor.enabled.

[***RFC***](https://kubernetes.github.io/ingress-nginx/deploy/)

[***Helm chart***](https://artifacthub.io/packages/helm/bitnami/nginx-ingress-controller)

