#!/bin/bash

cluster_name=promize-cluster
context_name=promize-context
user_name=admin-user
secret_name=admin-token

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
