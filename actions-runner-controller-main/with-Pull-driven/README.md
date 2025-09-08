
# Actions Runner Controller (ARC) (Github APP with Pull driven)

- I'm using pull driven (not webhook driven) autoscaling, because the k8s cluster in not externally accessible and webhook can’t be used, no public endpoint.

[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/6061/badge)](https://bestpractices.coreinfrastructure.org/projects/6061)
[![awesome-runners](https://img.shields.io/badge/listed%20on-awesome--runners-blue.svg)](https://github.com/jonico/awesome-runners)
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/actions-runner-controller)](https://artifacthub.io/packages/search?repo=actions-runner-controller)

GitHub Actions automates the deployment of code to different environments, including production. The environments contain the `GitHub Runner` software which executes the automation. `GitHub Runner` can be run in GitHub-hosted cloud or self-hosted environments. Self-hosted environments offer more control of hardware, operating system, and software tools. They can be run on physical machines, virtual machines, or in a container. Containerized environments are lightweight, loosely coupled, highly efficient and can be managed centrally. However, they are not straightforward to use.

`Actions Runner Controller (ARC)` makes it simpler to run self hosted environments on Kubernetes(K8s) cluster.

With ARC you can :

- **Deploy self hosted runners on Kubernetes cluster** with a simple set of commands.
- **Auto scale runners** based on demand.
- **Setup across GitHub Enterprise editions**.

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

<sub> *note:- This command uses v1.9.1. Please replace with a later version, if available.</sub>

>You may also install cert-manager using Helm. For instructions, see "[Installing with Helm](https://cert-manager.io/docs/installation/helm/#installing-with-helm)."

2️⃣ Build docker image that will be used on Runner Deployment using this customized Dockerfile:

```shell
FROM summerwind/actions-runner:latest
RUN sudo apt update -y \
  && sudo apt install ${Package_Name} \
  && sudo rm -rf /var/lib/apt/lists/*
````

3️⃣ Next, Create a Github App for ARC to authenticate with GitHub.

- Login to your GitHub account and follow steps "[Here](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app)."

**Required Permissions for Repository Runners:**
**Repository Permissions**

- Actions (**read**)
- Administration (**read** / **write**)
- Metadata (**read**)
- Checks (**read**) (if you are going to use Webhook Driven Scaling)

**Required Permissions for Organization Runners:**

**Repository Permissions**

- Actions (**read**)
- Administration (**read** / **write**)
- Metadata (**read**)

***Organization Permissions***

- Self-hosted runners (**read** / **write**)

**Create GitHub Apps on your organization(as our case)**
You will see an App ID on the page of the GitHub App you created as follows, the value of this App ID will be used later.

<img width="887" alt="image" src="https://user-images.githubusercontent.com/69244659/195363463-97cf18d3-af2f-40cb-ad1c-0168144ca2a0.png">

Download the private key file by pushing the "Generate a private key" button at the bottom of the GitHub App page. This file will also be used later.

<img width="749" alt="image" src="https://user-images.githubusercontent.com/69244659/195359460-27f9ab53-9dcb-4f9d-bc24-3359c737593c.png">

Go to the "Install App" tab on the left side of the page and install the GitHub App that you created for your account or organization.

<img width="746" alt="image" src="https://user-images.githubusercontent.com/69244659/195360347-c9fc5cf0-85a3-4995-bdfc-990118c85fef.png">

When the installation is complete, you will be taken to a URL in one of the following formats, the last number of the URL will be used as the Installation ID later (For example, if the URL ends in settings/installations/8775, then the Installation ID is 8775).

### Deploy and Configure ARC

1️⃣ Deploy  and configure ARC components on your K8s cluster. we use official Helm Chart with some customization for GHE.

##### Create namespace actions-runner-system for ARC:

```shell
kubectl create ns actions-runner-system
````
   
##### Configure GitHub App as K8s secret that will be used by ARC Deployments:

```shell
kubectl create secret generic controller-manager \
    -n actions-runner-system \
    --from-literal=github_app_id=${APP_ID} \
    --from-literal=github_app_installation_id=${INSTALLATION_ID} \
    --from-file=github_app_private_key=${PRIVATE_KEY_FILE_PATH}
````
  
##### Add repository

```shell
helm repo add actions-runner-controller https://actions-runner-controller.github.io/actions-runner-controller
```

##### Install Helm chart

```shell
helm upgrade --install --namespace actions-runner-system \
             --set=githubEnterpriseServerURL=${GHE_URL}\
             --set=runnerGithubURL=${GHE_URL}\
             --set=githubURL="${GHE_API}"\
             --set=githubUploadURL="${GHE_API}"\
             --wait actions-runner-controller actions-runner-controller/actions-runner-controller
```


2️⃣ Create the GitHub self hosted runners deployment, HPA and configure to run against your organization.

Create a `runnerdeployment.yaml` file and copy the following YAML contents into it:

```yaml
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  name: ${runner_deployment_name}
  namespace: ${Namespace_name}
spec:
  template:
    spec:
      image: image_name_you_build_it_using_customized_Dockerfile
      dockerdWithinRunnerContainer: true     
      organization: ${Org_Name}
      labels:
       - ${label_name}
      group: ${group_name}
---
apiVersion: actions.summerwind.dev/v1alpha1
kind: HorizontalRunnerAutoscaler
metadata:
  name: runner-deployment-autoscaler
  namespace: ${Namespace_name}
spec:
spec:
  maxReplicas: 15
  metrics:
    - repositoryNames:
        - repo_name
      type: TotalNumberOfQueuedAndInProgressWorkflowRuns
  minReplicas: 1
  scaleDownDelaySecondsAfterScaleOut: 120
  scaleTargetRef:
    kind: RunnerDeployment
    name: arc-runner-deployment
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
runner-deployment-test-2475h595fr   mumoshu/actions-runner-controller-ci   Running

$ kubectl get pods
NAME                           READY   STATUS    RESTARTS   AGE
runner-deployment-test-2475ht2qbr 2/2     Running   0          1m
````

Also, this runner has been registered directly to the organization, you can see it in organization settings. For more information, see "[Checking the status of a self-hosted runner - GitHub Docs](https://docs.github.com/en/actions/hosting-your-own-runners/monitoring-and-troubleshooting-self-hosted-runners#checking-the-status-of-a-self-hosted-runner)."

:two: You are ready to execute workflows against this self-hosted runner. For more information, see "[Using self-hosted runners in a workflow - GitHub Docs](https://docs.github.com/en/actions/hosting-your-own-runners/using-self-hosted-runners-in-a-workflow#using-self-hosted-runners-in-a-workflow)."

There is also a quick start guide to get started on Actions, For more information, please refer to "[Quick start Guide to GitHub Actions](https://docs.github.com/en/actions/quickstart)."
-----

## Learn more from our REF:

For more detailed documentation, please refer to "[Detailed Documentation](https://github.com/actions-runner-controller/actions-runner-controller/blob/master/docs/detailed-docs.md)."
