# Adding User Access to K8s Cluster using Service Account Role and Role Binding

Follow these steps to grant user access to a Kubernetes (k8s) cluster using Service Account Role and Role Binding:

1. **Create Namespace:** Create a namespace named "users" to centralize all users or service accounts.

    ```bash
    kubectl create namespace users
    ```

2. **Create Secret:** Generate a secret for the service account to obtain the Token and ca.crt required for authentication.

    ```bash
    kubectl create secret generic <SECRET_NAME> \
      --namespace=users \
      --from-file=token=<PATH_TO_TOKEN_FILE> \
      --from-file=ca.crt=<PATH_TO_CA_FILE>
    ```

    Replace `<SECRET_NAME>`, `<PATH_TO_TOKEN_FILE>`, and `<PATH_TO_CA_FILE>` with your preferred secret name and file paths.

3. **Create Role:** Define a Role inside the namespace where you want the user to have access. Specify the privileges you want to grant.

    ```bash
    kubectl apply -f role-definition.yaml
    ```

    Customize the `role-definition.yaml` file to specify the desired permissions.

4. **Create Role Binding:** Establish a Role Binding in the same namespace as the role to bind the Service Account with the Role.

    ```bash
    kubectl apply -f role-binding.yaml
    ```

    Adjust the `role-binding.yaml` file to reference the previously created role.

5. **Run Script:** Execute the `add-new-user.sh` script after customizing environment variables. This script generates a kube-config file that users can use to access the Kubernetes cluster.

    ```bash
    chmod +x add-new-user.sh
    ./add-new-user.sh
    ```

    Ensure to customize environment variables inside the script and use the generated kube-config file to access k8s.

Feel free to reach out for any questions or assistance. Happy Kubernetes user access management! 👩‍💻🚀

