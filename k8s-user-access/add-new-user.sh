#!/bin/bash

cluster_name=${cluster-name}
context_name=${cluster-context}
user_name=${new-user}   
secret_name=${secretName-for-serviceAcoount}

#name=$(kubectl get secrets --namespace=users -o json | jq -r '.items[] | select(.metadata.name | test("${user_name}-reader-token")).metadata.name')

server=$(kubectl config view --minify --output jsonpath='{.clusters[*].cluster.server}')
ca=$(kubectl get secret/$secret_name --namespace=users -o jsonpath='{.data.ca\.crt}')
token=$(kubectl get secret/$secret_name --namespace=users -o jsonpath='{.data.token}' | base64 --decode)

echo "
apiVersion: v1
kind: Config
clusters:
- name: ${cluster_name}
  cluster:
    certificate-authority-data: ${ca}
    server: ${server}
contexts:
- name: ${context_name}
  context:
    cluster: ${cluster_name}
    user: ${user_name}
current-context: ${context_name}
users:
- name: ${user_name}
  user:
    token: ${token}
" > ${user_name}-kubeconfig.yml
