
# Actions Runner Controller (ARC)

[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/6061/badge)](https://bestpractices.coreinfrastructure.org/projects/6061)
[![awesome-runners](https://img.shields.io/badge/listed%20on-awesome--runners-blue.svg)](https://github.com/jonico/awesome-runners)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/actions-runner-controller)](https://artifacthub.io/packages/search?repo=actions-runner-controller)

GitHub Actions automates the deployment of code to different environments, including production. The environments contain the `GitHub Runner` software which executes the automation. `GitHub Runner` can be run in GitHub-hosted cloud or self-hosted environments. Self-hosted environments offer more control of hardware, operating system, and software tools. They can be run on physical machines, virtual machines, or in a container. Containerized environments are lightweight, loosely coupled, highly efficient and can be managed centrally. However, they are not straightforward to use.

`Actions Runner Controller (ARC)` makes it simpler to run self hosted environments on Kubernetes(K8s) cluster.

With ARC you can :

- **Deploy self hosted runners on Kubernetes cluster** with a simple set of commands.
- **Auto scale runners** based on demand.
- **Setup across GitHub**.

## Overview

For an overview of ARC, please refer to "[ARC Overview](https://github.com/actions-runner-controller/actions-runner-controller/blob/master/docs/Actions-Runner-Controller-Overview.md)."



## Getting Started

ARC can be setup with just a few steps.

In this section we will setup prerequisites, deploy ARC into a K8s cluster, and then run GitHub Action workflows on that cluster.

### Prerequisites


:one: Install cert-manager in your cluster. For more information, see "[cert-manager](https://cert-manager.io/docs/installation/)."

```shell
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml 
```

<sub> *note:- This command uses v1.13.1. Please replace with a later version, if available.</sub>

>You may also install cert-manager using Helm. For instructions, see "[Installing with Helm](https://cert-manager.io/docs/installation/helm/#installing-with-helm)."

2️⃣ Build docker image that will be used on Runner Deployment using this customized Dockerfile:

```shell
FROM summerwind/actions-runner-dind-rootless:ubuntu-22.04
RUN sudo apt update -y \
  && sudo apt install ${Package_Name} \
  && sudo rm -rf /var/lib/apt/lists/*
````
3️⃣ Authenticate the Action Runner Controller with GitHub
First, we need to set up a mechanism to authenticate the action runner controller to GitHub. This can be done in two ways:

**PAT (Personal Access Token)**
**Using GitHub App**
We will use the **GithubApp** method for authentication.

**Create GitHub Apps for your organization**
- Login to your GitHub account and follow steps "[Here](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app)."
- Select the below-mentioned permission for this app and hit the “Create GitHub App” button at the bottom of the page to create a GitHub App.

**Required Permissions for Organization Runners:**

**Repository Permissions**

- Actions (**read only**)
- Administration (**read only** / **write**)
- Metadata (**read only**)
- Checks (**read only**) (if you are going to use Webhook Driven Scaling)
- Pull requests (**read only**)

***Organization Permissions***

- Self-hosted runners (**read** / **write**)
- Webhooks (**read** / **write**)

You will see an App ID on the page of the GitHub App you created as follows, the value of this App ID will be used later.

<img width="695" alt="Screenshot 2023-12-26 at 2 23 03 PM" src="https://github.com/mahmoudaboghadeer93/actions-runner-controller/assets/69244659/229439b9-0377-458d-a08b-b1399a3d315e">


Download the private key file by pushing the "Generate a private key" button at the bottom of the GitHub App page. This file will also be used later.

<img width="749" alt="image" src="https://user-images.githubusercontent.com/69244659/195359460-27f9ab53-9dcb-4f9d-bc24-3359c737593c.png">

Go to the "Install App" tab on the left side of the page and install the GitHub App that you created for your account or organization.

<img width="746" alt="image" src="https://user-images.githubusercontent.com/69244659/195360347-c9fc5cf0-85a3-4995-bdfc-990118c85fef.png">

When the installation is complete, you will be taken to a URL in one of the following formats, the last number of the URL will be used as the Installation ID later (For example, if the URL ends in settings/installations/8775, then the Installation ID is 8775).

### Deploy and Configure ARC

1️⃣ Deploy  and configure ARC components on your K8s cluster. we use official Helm Chart with some customization for GHE.

##### Create namespace actions-runner-system for ARC:

```shell
kubectl create ns arc-system
````
   
##### Configure GitHub App as K8s secret that will be used by ARC Deployments:

```shell
kubectl create secret generic controller-manager \
    -n arc-system \
    --from-literal=github_app_id=${APP_ID} \
    --from-literal=github_app_installation_id=${INSTALLATION_ID} \
    --from-file=github_app_private_key=${PRIVATE_KEY_FILE_PATH}
````

##### Install the Action Runner Controller (ARC)

```shell
helm repo add actions-runner-controller https://actions-runner-controller.github.io/actions-runner-controller
```
```shell
helm repo update
```
```shell
helm upgrade --install --namespace arc-system \
             -f values.yaml
             --wait actions-runner-controller actions-runner-controller/actions-runner-controller 
```
**or for specific nodegroup**
```shell
helm upgrade --install --namespace arc-system \
             -f values.yaml
             --wait actions-runner-controller actions-runner-controller/actions-runner-controller  --set nodeSelector.role=monitor
```

***create an Ingress to expose actions-runner-controller-github-webhook-server:***
  **arc-webhook-server-ing.yaml**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: actions-runner-controller-github-webhook-server
  namespace: actions-runner-system
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/backend-protocol: "HTTP"
spec:
  ingressClassName: nginx
  rules:
    - host: github-webhook.ccx.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: actions-runner-controller-github-webhook-server
                port:
                  number: 80 
```
Then create this resource on your cluster with the following command:
```shell
kubectl apply -n arc-system -f arc-webhook-server-ing.yaml
```
***Configure Autoscaling***
You can automatically adjust the number of self-hosted runners in your environment based on pull-driven or webhook-driven scaling metrics.
- Pull-driven Scaling
Pull-driven scaling performance is bound by the sync period/polling interval. Initially, we started using pull-driven scaling. But we ended up with a slow/cold starting period issue.

For performance improvement, we tried to reduce the polling interval. However, it ended up in an API rate limit issue.

So, we switched to webhook-driven scaling for better performance.

- Webhook-driven Scaling
Webhook-driven scaling is performed based on the number of webhook events from GitHub.

***Webhook-driven Scaling Architecture***

<img width="753" alt="image" src="https://github.com/mahmoudaboghadeer93/actions-runner-controller/assets/69244659/609f111e-d5eb-4fa0-bf0e-5c5ae7fcdab7">

The benefit of auto-scaling on webhooks compared to pull-driven scaling is that ARC is immediately notified of the scaling need.
Webhook events are processed by a separate webhook server. The webhook server receives workflow_job webhook events and scales RunnerDeployments/RunnerSets by updating HRAs configured for the webhook trigger.

***Register the webhook server to GitHub***

- Go to your GitHub organization settings and click on Add Webhook
- In the payload URL, add the https endpoint you deployed with the runner controller for your webhook server
- In content type, select application/JSON
- Under the secret button, add a random string that we will use as a webhook secret (YOUR_WEBHOOK_SECRET)
- Keep SSL verification on for webhook
- Select the events for which you would like to trigger this webhook.
For this example, let’s select individual events. Opt for Workflow job and workflow runs
<img width="688" alt="image" src="https://github.com/mahmoudaboghadeer93/actions-runner-controller/assets/69244659/31276f4d-f7d2-44be-89b2-dea767056ec8">
<img width="687" alt="image" src="https://github.com/mahmoudaboghadeer93/actions-runner-controller/assets/69244659/de956b46-1b17-4161-bb00-aa9bedf3fb6b">

***kubectl command to create secret for webhook token***
```shell
kubectl create secret generic github-selfhosted-webhook-token -n arc-system --from-literal=SELFHOSTED_GITHUB_WEBHOOK_SECRET_TOKEN=${YOUR_WEBHOOK_SECRET}
```


2️⃣ Create the GitHub self hosted runners deployment, HPA and configure to run against your organization.

Create a `runnerdeployment.yaml` file and copy the following YAML contents into it:

```yaml
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  annotations:
    karpenter.sh/do-not-evict: "true"
  name: arc-runner-deployment
  namespace: arc-system
spec:
  template:
    spec:
      image: summerwind/actions-runner-dind-rootless:ubuntu-22.04 #or one you created using above Dockerfile in Prerequisites 2️⃣ 
      dockerdWithinRunnerContainer: true     
      organization: ${github-organization-name}
      labels:
       - arc-runner
      ephemeral: true
      resources:
        limits:
          cpu: 1024m
          memory: 2Gi
        requests:
          cpu: 1024m
          memory: 2Gi
---
apiVersion: actions.summerwind.dev/v1alpha1
kind: HorizontalRunnerAutoscaler
metadata:
  name: runner-autoscaler
  namespace: arc-system
spec:
  maxReplicas: 3
  minReplicas: 0
  scaleTargetRef:
    kind: RunnerDeployment
    name: arc-runner-deployment
  scaleDownDelaySecondsAfterScaleOut: 60
  scaleUpTriggers:
  - duration: 30m
    githubEvent:
      workflowJob: {}
````
Apply this file to your K8s cluster.
```shell
kubectl apply -f runnerdeployment.yaml
````

*🎉 We are done - now we should have self hosted runners running in K8s configured to your organization.  🎉*

Next - lets verify our setup and execute some workflows.

### Verify and Execute Workflows

:one: Verify that your setup is successful:
```shell

$ kubectl get runners
NAME                             REPOSITORY                             STATUS
arc-runner-deployment-2475h595fr   mumoshu/actions-runner-controller-ci   Running

$ kubectl get pods
NAME                           READY   STATUS    RESTARTS   AGE
arc-runner-deployment-2475ht2qbr 2/2     Running   0          1m
````

Also, this runner has been registered directly to the organization, you can see it in organization settings. For more information, see "[Checking the status of a self-hosted runner - GitHub Docs](https://docs.github.com/en/actions/hosting-your-own-runners/monitoring-and-troubleshooting-self-hosted-runners#checking-the-status-of-a-self-hosted-runner)."

:two: You are ready to execute workflows against this self-hosted runner. For more information, see "[Using self-hosted runners in a workflow - GitHub Docs](https://docs.github.com/en/actions/hosting-your-own-runners/using-self-hosted-runners-in-a-workflow#using-self-hosted-runners-in-a-workflow)."

There is also a quick start guide to get started on Actions, For more information, please refer to "[Quick start Guide to GitHub Actions](https://docs.github.com/en/actions/quickstart)."
-----
## Learn more from our REF:

For more detailed documentation, please refer to "[Detailed Documentation](https://github.com/actions-runner-controller/actions-runner-controller/blob/master/docs/detailed-docs.md)."

