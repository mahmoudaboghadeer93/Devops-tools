## cert-manager for nginx controller

  **cert-manager is the easiest way to automatically manage certificates in Kubernetes and OpenShift clusters.**
  
***Steps***

   1️⃣ **Install Cert-Manager CRDs**

   ```bash 
        kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.15.3/cert-manager.crds.yaml
   ```

   2️⃣ **Install Cert-Manager Using Helm** 
   
   Cert Manager is used to provision SSL Certificates to Kubernetes Clusters (https://github.com/cert-manager/cert-manager)
           To install cert-manager simply run :
     
   ```bash 
        helm repo add jetstack https://charts.jetstack.io
        helm repo update
        helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.15.3
   ```

   ***list iteams*** 

   ```bash    
        kubectl get pods -n cert-manager
   ```

   3️⃣ **Create a Secret with AWS Credentials (or other cloud provider for DNS like Alicloud):**

       Store the AWS credentials in a Kubernetes secret:
   
   ```bash    
        kubectl create secret generic route53-credentials-secret --from-literal=aws-access-key-id=YOUR_ACCESS_KEY_ID --from-literal=aws-secret-access-key=YOUR_SECRET_ACCESS_KEY -n cert-manager
   ```
  
   4️⃣ **Create a ClusterIssuer for DNS-01 Challenge:**

        Create the ClusterIssuer for Let's Encrypt using DNS-01 challenge with Route 53. Here’s the updated cluster-issuer.yaml:
        
   ```bash   
      apiVersion: cert-manager.io/v1
      kind: ClusterIssuer
      metadata:
        name: letsencrypt-dns
      spec:
        acme:
          server: https://acme-v02.api.letsencrypt.org/directory
          email: <your-email>
          privateKeySecretRef:
            name: letsencrypt-dns
          solvers:
          - dns01:
              route53:
                region: eu-central-1 # Use the appropriate region for your Route 53 hosted zone
                accessKeyIDSecretRef:
                  name: route53-credentials-secret
                  key: aws-access-key-id
                secretAccessKeySecretRef:
                  name: route53-credentials-secret
                  key: aws-secret-access-key
   ```

  **Then**
  
   ```bash    
        kubectl apply -f cluster-issuer.yaml
   ```

   **Then**
   
   ```bash 
        kubectl apply -f certificates.yaml
   ```

   6️⃣ **Configure Ingress Resources:** (will generate also certificate with same name of secret)

        Annotate your Ingress resources to use the appropriate TLS secrets:

   ```bash   
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: example-ingress-demo
          namespace: default
          annotations:
            cert-manager.io/cluster-issuer: letsencrypt-dns
        spec:
          rules:
          - host: 'portal.demo.x.io'
            http:
              paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: your-service
                    port:
                      number: 80
          tls:
          - hosts:
            - 'portal.demo.x.io'
            secretName: wildcard-cert-secret-example-tls #same name exist in certificate
   ```

**another wildcard domain Example**

   ```bash   
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: example-ingress-demo
          namespace: default
          annotations:
            cert-manager.io/cluster-issuer: letsencrypt-dns
        spec:
          rules:
          - host: '*.demo.x.io'
            http:
              paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: your-service
                    port:
                      number: 80
          tls:
          - hosts:
            - '*.demo.x.io'
            secretName: wildcard-cert-secret-example-tls #same name exist in certificate
   ```
   
**SSL takes a few minutes to issue. The issued Certificate is stored in the secret wildcard-cert-secret-example-tls. On opening https://portal.demo.x.io**

***Congratulations, you can now connect to your page securely via https…****

[cert-manager-Docs](https://cert-manager.io/docs/tutorials/acme/dns-validation/)

[Cert-manager-resources](https://github.com/cert-manager/cert-manager)
