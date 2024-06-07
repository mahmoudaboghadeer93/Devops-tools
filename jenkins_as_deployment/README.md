### deploy and Configure Jenkins on EKs ###

# deploy Jenkins

1️⃣ First Deploy EFS-Driver aadd-ons as "[here](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html)."

2️⃣ Create efs storage (for jenkins) with security group that allow port 2049 for VPC CIDR of k8s as "[here](https://aws.amazon.com/blogs/storage/deploying-jenkins-on-amazon-eks-with-amazon-efs/)."

3️⃣ Create Storage class ,PV, PVC after you changed the "volumeHandle: ID-of-EFS" inside PV.

    ```shell
      kubectl apply -f storage/ 
    ````
     
4️⃣ Create RBAC (service account, cluster role, role binding , secret) that give the jenkins access for k8s resources , use this service account with jenkins deployment.

    ```shell
      kubectl apply -f RBAC/ 
    ````

5️⃣ Deploy Jenkins resources (don't forget to use latest image of Jenkins, also change the jenkins domain to your own one):

    ```shell
      kubectl apply -f jenkins-server/ 
    ````

6️⃣ Open up a web browser, trigger your jenkins url!
    
   * User: admin
   * Password:
    To get the password for the admin user, run the following command:

    - printf $(kubectl get secret jenkins -o jsonpath="{.data.jenkins-admin-
password}" | base64 --decode);echo   

*🎉 Now we have jenkins server  🎉*


# Configure Jenkins to deploy apps on k8s

   1️⃣ Install kuberenetes cloud plugin , other needed plugins as here
   
   2️⃣ Configure kuberenetes Cloud :
   
      - Go to Manage Jenkins → Clouds → Add new cloud
      
      - Provide Cloud name as kubernetes and type as Kubernetes.

[      ![img (1)](https://github.com/mahmoudaboghadeer93/Devops-tools/assets/69244659/b3bee7f2-d922-4665-8b43-ecb0867edb88)
](https://github.com/mahmoudaboghadeer93/Devops-tools/blob/add-readme-for-jenkins/jenkins_as_deployment/image%20(1).png)


  - Click create and edit cloud details by expanding Kubernetes Cloud Details.
      
  - Add URL of the Kubernetes API server in Kubernetes URL and namespace in kubernetes namespace.

    If you don’t know Kubernetes API server URL use :

    '''shell
       kubectl cluster-info 
    ''''

 -  Check Disable https certificate check.

 -  Use token of secret for your jenkins service account(jenkins-admin) which created in above (step 4️⃣ for deploy Jenkins)
    and use it to create jenkins credentials using (**Note:** this step we can skip it if the jenkins in same k8s):
          **Steps**:  add → jenkins → select kind as secret text → fill the details → Add.

[      [![image](https://github.com/mahmoudaboghadeer93/Devops-tools/assets/69244659/018e1934-c010-4063-82e0-13157f9585cd)](https://github.com/mahmoudaboghadeer93/Devops-tools/blob/add-readme-for-jenkins/jenkins_as_deployment/creds1.png)]

 - Use created credentials and click Test Connection.

[     [ ![image](https://github.com/mahmoudaboghadeer93/Devops-tools/assets/69244659/280b375a-86b3-483c-84bf-442a5798a23e)](https://github.com/mahmoudaboghadeer93/Devops-tools/blob/add-readme-for-jenkins/jenkins_as_deployment/creds-test.png)]

 - Add jenkins service private URL in Jenkins URL and leave rest as default and click Save.
      
    You can get jenkins-service private URL using
   
    '''shell
        kubectl get svc -n jenkins 
    ''''



-----
## Learn more from REF:

For more detailed documentation, please refer to:

"[efs-csi](https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html)."
"[deploying-jenkins-on-amazon-eks-with-amazon-efs](https://aws.amazon.com/blogs/storage/deploying-jenkins-on-amazon-eks-with-amazon-efs/)."
"[deployment-with-efs](https://www.eksworkshop.com/docs/fundamentals/storage/efs/deployment-with-efs)."
