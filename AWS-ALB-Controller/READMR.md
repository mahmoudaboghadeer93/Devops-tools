**Deploy AWS Load Balancer Controller AWS EKS.** 

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
    --policy-name AWSLoadBalancerControllerIAMPolicy \
    --policy-document file://iam-policy.json
```

 Take note of the policy ARN that is returned.

 4. Create an IAM role and ServiceAccount for the AWS Load Balancer Controller, using the ARN from the previous step:

```bash
eksctl create iamserviceaccount \
    --cluster=<your-cluster-name> \
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
    kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"
   ```
3. Install the AWS Load Balancer controller, if using iamserviceaccount (as our case here):
    # NOTE: The clusterName value must be set either via the values.yaml or the Helm command line. The <k8s-cluster-name> in the command
    # below should be replaced with name of your k8s cluster before running it.
   
   ```bash
      helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=<k8s-cluster-name> --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
   ```
   
**OR**

3. Install the AWS Load Balancer controller, if not using iamserviceaccount(Not our Case):

  ```bash
     helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=<k8s-cluster-name>
  ```


[***Helm chart***](https://artifacthub.io/packages/helm/aws/aws-load-balancer-controller)
