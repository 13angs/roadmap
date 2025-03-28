# 🟢 MongoDB ReplicaSet on Kubernetes

This repository helps you deploy a **highly available MongoDB ReplicaSet** on Kubernetes using:

✅ StatefulSets  
✅ Headless Service  
✅ Persistent Volumes  
✅ Secure Authentication  
✅ Automated ReplicaSet initialization

---

## 🚀 Quick Overview

You'll deploy:

- A 3-node MongoDB ReplicaSet
- Automatic ReplicaSet initialization
- Secure authentication via Kubernetes Secrets
- Data persistence with Persistent Volume Claims (PVCs)
- Failover-ready MongoDB cluster

---

## 🧩 Folder Structure

```
.
├── README.md
└── k8s-manifests/
    ├── configmap.yaml       # Contains init script for ReplicaSet
    ├── secret.yaml          # Stores MongoDB root credentials
    ├── service.yaml         # Headless Service for MongoDB discovery
    └── statefulset.yaml     # MongoDB StatefulSet (3 replicas)
```

---

## ⚙️ Prerequisites

- Kubernetes cluster (Minikube, kind, GKE, EKS, etc.)
- `kubectl` configured
- `openssl` installed
- Basic understanding of Kubernetes and MongoDB

---

## ✨ Deployment Steps (Step-by-Step)

### 1️⃣ Generate the MongoDB `keyfile`

This keyfile is used for internal authentication between MongoDB nodes.

```bash
openssl rand -base64 756 > keyfile
```

---

### 2️⃣ Create the Kubernetes Secret for the keyfile

```bash
kubectl create secret generic mongo-keyfile --from-file=keyfile=./keyfile
```

---

### 3️⃣ Create the Kubernetes Secret for MongoDB root credentials

The provided `secret.yaml` sets:
- Username: `root`
- Password: `password`

> **Note:** You can change these by updating the `secret.yaml` file and base64-encoding your own values.

```bash
kubectl apply -f k8s-manifests/secret.yaml
```

---

### 4️⃣ Deploy MongoDB ReplicaSet Manifests

This will deploy:
- `ConfigMap`: ReplicaSet initialization script
- `Service`: Headless service for DNS-based discovery
- `StatefulSet`: 3 MongoDB pods

```bash
kubectl apply -f k8s-manifests/
```

---

### 5️⃣ Check the Status

```bash
kubectl get pods
kubectl logs -f mongodb-0
```

Make sure all pods (`mongodb-0`, `mongodb-1`, `mongodb-2`) are up and ready.

---

## ✅ What happens behind the scenes?

- `mongodb-0` automatically initializes the ReplicaSet and creates the root user.
- `mongodb-1` and `mongodb-2` wait for the ReplicaSet to be ready and then join.
- All nodes restart with `--keyFile` to enable internal authentication.
- The ReplicaSet will elect a PRIMARY automatically.

---

## 🧪 Testing the ReplicaSet

### Connect to the Primary:

```bash
kubectl exec -it mongodb-0 -- mongosh -u root -p password --authenticationDatabase admin
```

### Check ReplicaSet Status:

```js
rs.status()
```

You should see all 3 nodes and the elected `PRIMARY`.

---

## 💡 Tips

- To simulate failover:  
  Delete the PRIMARY pod and watch the election happen automatically.
  
  ```bash
  kubectl delete pod mongodb-0
  ```

- To adjust storage:  
  Edit the `storage` size in `statefulset.yaml` under `volumeClaimTemplates`.

- To change root user/password:  
  Update `secret.yaml` (base64 encode them!) and re-apply.

---

## ❤️ Why StatefulSet?

- Stable Network IDs (`mongodb-0`, `mongodb-1`, `mongodb-2`)
- Persistent storage across restarts
- Supports ordered, graceful rolling updates

---

## 🧩 Components Summary

| Component       | Description                               |
|-----------------|-------------------------------------------|
| ConfigMap       | Automates ReplicaSet initiation           |
| Secret          | Stores root credentials securely          |
| Headless Service| Enables pod DNS discovery                 |
| StatefulSet     | Deploys and manages the MongoDB pods      |
| PVC             | Ensures data is persisted across restarts |

---

Feel free to copy-paste, tweak, or extend this to suit your team or project needs.