## cert-manager for nginx controller

  **cert-manager is the easiest way to automatically manage certificates in Kubernetes and OpenShift clusters.**
  
***Steps***

   1️⃣ **Install Cert-Manager** 
     Cert Manager is used to provision SSL Certificates to Kubernetes Clusters (https://github.com/cert-manager/cert-manager)

     To install cert-manager simply run -
     
     bash ``` 
         kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.15.1/cert-manager.yaml

     ````

     list iteams 

     bash ```
         kubectl get pods -n cert-manager
     ```
  
   2️⃣ **we configure a Cluster Issuer LetsEncrypt** ( in our case to issue SSLs on the Fly. Create a file called cluster-issuer.yaml )

   bash ``` 
      apiVersion: cert-manager.io/v1
      kind: ClusterIssuer
      metadata:
        name: letsencrypt-prod
      spec:
        acme:
          server: https://acme-v02.api.letsencrypt.org/directory
          email: <your-mail>
          privateKeySecretRef:
            name: letsencrypt-prod
          solvers:
            - http01:
                ingress:
                  class: nginx
     ```

   3️⃣ **Update the ingress to use SSL**
   
   bash ```
      apiVersion: networking.k8s.io/v1
      kind: Ingress
      metadata:
        name: test-ingress
        annotations:
         kubernetes.io/ingress.class: nginx
         cert-manager.io/cluster-issuer: letsencrypt-prod
      
      spec:
        rules:
        - host: www.domain.net
          http:
            paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: test-svc
                    port:
                      number: 80
            
        tls:
            - hosts:
                - www.domain.net
              secretName: tls-2048-bilgicloud
   ```
    
   
