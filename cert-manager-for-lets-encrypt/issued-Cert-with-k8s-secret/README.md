## cert-manager for nginx controller

  **cert-manager is the easiest way to automatically manage certificates in Kubernetes and OpenShift clusters.**
  
***Steps***

   1️⃣ **Install Cert-Manager CRDs**

   ```bash 
        kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.15.3/cert-manager.crds.yaml
   ```

   2️⃣ **Install Cert-Manager Using Helm** 
   
     Cert Manager is used to provision SSL Certificates to Kubernetes Clusters (https://github.com/cert-manager/cert-manager) To install cert-manager simply run :
     
   ```bash 
        helm repo add jetstack https://charts.jetstack.io
        helm repo update
        helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace --version v1.15.3
   ```

   ***list iteams*** 

   ```bash    
        kubectl get pods -n cert-manager
   ```

   3️⃣ **Create Secret of Certificates (Key,FullChain):**
       
   ```bash 
        kubectl create secret tls wildcard-cert-domain-com --cert=STAR.X.io-FullChain.crt --key=STAR.X.io.key -n NameSpace_Name
   ```

   4️⃣ **Configure Ingress Resources:** (will generate also certificate with same name of secret)

        Annotate your Ingress resources to use the appropriate TLS secrets:

   ```bash   
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: example-ingress-demo
          namespace: NameSpace_Name
          annotations:
            nginx.ingress.kubernetes.io/ssl-redirect=true
        spec:
          rules:
          - host: 'portal.x.com'
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
            - 'portal.x.com'
            secretName: wildcard-cert-domain-com #same name of created secret of certificates
   ```

**another wildcard domain Example**

   ```bash   
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: example-ingress-demo
          namespace: NameSpace_Name
          annotations:
            nginx.ingress.kubernetes.io/ssl-redirect=true
        spec:
          rules:
          - host: '*.x.com'
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
            - '*.x.com'
            secretName: wildcard-cert-domain-com #same name of created secret of certificates
   ```
   
**SSL takes a few minutes to issue. The issued Certificate is stored in the secret wildcard-cert-secret-example-tls. On opening https://portal.demo.x.io**

***Congratulations, you can now connect to your page securely via https…****

[cert-manager-Docs](https://cert-manager.io/docs/tutorials/acme/dns-validation/)

[Cert-manager-resources](https://github.com/cert-manager/cert-manager)
