# Deploy AWS Load Balancer Controller on AWS EKS.

Application Load Balancer (ALB) within AWS EKS.
Buckle up as i introduce you to the incredible AWS Load Balancer Controller, a Kubernetes controller specifically designed to effortlessly handle Elastic Load Balancers for your Kubernetes cluster.

**Prerequisites**

**IAM Permissions**
 You need to set up IAM permissions to allow the AWS Load Balancer Controller to manage ALB resources.
 There are two ways to set up IAM permissions:
    using IAM roles for ServiceAccounts 
    **or**
    attaching IAM policies directly to the worker node IAM roles.

Option 1: Using IAM roles for ServiceAccounts (*recommended*):

1. Create an IAM OIDC provider for your EKS cluster:
   ```bash
      eksctl utils associate-iam-oidc-provider \
      --profile <profile-name> \
      --region <region-code> \
      --cluster <your-cluster-name> \
      --approve
   ```
   
2. Download the IAM policy for the AWS Load Balancer Controller:

   ```bash
     curl -o iam-policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json
   ```

3. Create an IAM policy called AWSLoadBalancerControllerIAMPolicy:

```bash
aws iam create-policy \
    --profile <profile-name> \
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam-policy.json
```

 Take note of the policy ARN that is returned.

 4. Create an IAM role and ServiceAccount for the AWS Load Balancer Controller, using the ARN from the previous step:

```bash
eksctl create iamserviceaccount \
    --cluster=<your-cluster-name> \
    --profile <profile-name> \
    --region <region-code> \
    --namespace=kube-system \
    --name=aws-load-balancer-controller \
    --attach-policy-arn=arn:aws:iam::<YOUR_AWS_ACCOUNT_ID>:policy/AWSLoadBalancerControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --approve
```

Option 2: Setting up IAM manually:

If you choose not to use IAM roles for ServiceAccounts, 
you can manually apply the IAM policies from the following URL: https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.2.1/docs/install/iam_policy.json.


***Deploy the Controller to the Cluster via Helm:***

1. Add the EKS chart repo to Helm:
   
   ```bash
    helm repo add eks https://aws.github.io/eks-charts
   ```

2. Install the TargetGroupBinding CRDs:

   ```bash
    kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller/crds?ref=master"
   ```
3. Install the AWS Load Balancer controller, if using iamserviceaccount (as our case here):
   
    **NOTE:**
   
      The clusterName value must be set either via the values.yaml or the Helm command line. The <k8s-cluster-name> in the command
      below should be replaced with name of your k8s cluster before running it.
   
   ```bash
      helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=<k8s-cluster-name> --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
   ```
   
**OR**

3. Install the AWS Load Balancer controller, if not using iamserviceaccount(Not our Case):

  ```bash
     helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=<k8s-cluster-name>
  ```

      🎉 We are done - now we should have AWS ALB Controller in K8s. 🎉



***Certificate Discovery***

TLS certificates for ALB Listeners can be automatically discovered with hostnames from Ingress resources if the alb.ingress.kubernetes.io/certificate-arn annotation is not specified.

The controller will attempt to discover TLS certificates from the tls field in Ingress and host field in Ingress rules.

*Discover via Ingress tls*

  *EX:*
  
  ```bash
    apiVersion: extensions/v1beta1
    kind: Ingress
    metadata:
    namespace: default
    name: ingress
    annotations:
      kubernetes.io/ingress.class: alb
      alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    spec:
      tls:
      - hosts:
        - www.example.com
      rules:
      - http:
          paths:
          - path: /users/*
            backend:
              serviceName: user-service
              servicePort: 80
  ```

*Discover via Ingress rule host*

  *EX:*
  
  ```bash
     apiVersion: extensions/v1beta1
     kind: Ingress
     metadata:
     namespace: default
     name: ingress
     annotations:
       kubernetes.io/ingress.class: alb
       alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
     spec:
     rules:
     - host: dev.example.com
       http:
         paths:
         - path: /users/*
         backend:
           serviceName: user-service
           servicePort: 80
  ```


| NGINX Ingress Annotation                               | ALB Ingress Annotation                                      | Description                                                                                         |
|--------------------------------------------------------|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------------|
| `nginx.ingress.kubernetes.io/configuration-snippet`    | N/A                                                          | No direct equivalent. Manual configuration may be required.                                         |
| `nginx.ingress.kubernetes.io/force-ssl-redirect`       | N/A                                                          | No direct equivalent. SSL redirection is managed differently in AWS ALB.                            |
| `nginx.ingress.kubernetes.io/proxy-body-size`          | N/A                                                          | No direct equivalent. ALB has default maximum request size limit. Adjust application accordingly.    |
| `nginx.ingress.kubernetes.io/proxy-connect-timeout`    | `alb.ingress.kubernetes.io/backend-connection-idle-timeout` | Sets idle timeout for connections between ALB and backend servers.                                  |
| `nginx.ingress.kubernetes.io/proxy-read-timeout`       | `alb.ingress.kubernetes.io/backend-read-timeout`            | Sets maximum time ALB waits for response from backend server.                                        |
| `nginx.ingress.kubernetes.io/proxy-request-buffering`  | N/A                                                          | No direct equivalent. ALB does not buffer entire request bodies by default.                          |
| `nginx.ingress.kubernetes.io/proxy-send-timeout`       | `alb.ingress.kubernetes.io/backend-timeout`                | Sets maximum time ALB waits for backend ser



[***Certificate Discovery REF***](https://github.com/aws/eks-charts/tree/master/stable/aws-load-balancer-controller)

[***REF***](https://github.com/aws/eks-charts/tree/master/stable/aws-load-balancer-controller)

[***Helm chart***](https://artifacthub.io/packages/helm/aws/aws-load-balancer-controller)

