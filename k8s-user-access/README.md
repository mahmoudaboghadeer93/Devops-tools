# Adding User Access to K8s Cluster using Service Account Role and Role Binding

Follow these steps to grant user access to a Kubernetes (k8s) cluster using Service Account Role and Role Binding:

1. **Create Namespace:** Create a namespace named "users" to centralize all users or service accounts.

    ```bash
    kubectl create namespace users
    ```

2. **Create Service Account:** Create service account per user you want to have access to K8s, EX:.

    ```bash
    kubectl apply -f sa.yaml
    ```
    
3. **Create Secret:** Generate a secret for the service account to obtain the Token and ca.crt required for authentication.

    ```bash
    kubectl apply -f secret.yaml
    ```

4. **Create Role:** Define a Role inside the namespace where you want the user to have access. Specify the privileges you want to grant.

    ```bash
    kubectl apply -f role.yaml
    ```

    Customize the `role.yaml` file to specify the desired permissions ,above one it is just example.

5. **Create Role Binding:** Establish a Role Binding in the same namespace as the role to bind the Service Account with the Role.

    ```bash
    kubectl apply -f role-bind.yaml
    ```

    Adjust the `role-bind.yaml` file to reference the previously created role.

5. **Run Script:** Execute the `add-new-user.sh` script after customizing environment variables. This script generates a kube-config file that users can use to access the Kubernetes cluster.

    ```bash
    chmod +x add-new-user.sh
    ./add-new-user.sh
    ```

    Ensure to customize environment variables inside the script and use the generated kube-config file to access k8s.

Feel free to reach out for any questions or assistance. Happy Kubernetes user access management! 👩‍💻🚀

