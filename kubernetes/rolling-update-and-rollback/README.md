# Kubernetes Deployments: Rolling Updates and Rollbacks

This guide explains **how to update** your Kubernetes applications **without downtime** and **rollback** safely if needed.

> **Note:**  
> The examples use the images:
> - `13angs/containerize-backend-app:v0.0.1` (initial version)  
> - `13angs/containerize-backend-app:latest` (updated version)

---

## 📦 Rolling Updates (Zero-Downtime Deployments)

- **What**: Gradually replaces old Pods with new ones.
- **How**:
  - Kubernetes creates a new ReplicaSet.
  - It slowly updates Pods while keeping the app available.
  - Health checks (`liveness` and `readiness probes`) ensure only healthy Pods serve traffic.
- **Important Settings**:
  - `maxSurge`: Max extra Pods during update (default: 25%).
  - `maxUnavailable`: Max unavailable Pods during update (default: 25%).
  - `minReadySeconds`: Wait time for a Pod to be considered ready.

### Example Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend-app
  template:
    metadata:
      labels:
        app: backend-app
    spec:
      containers:
      - name: backend-container
        image: 13angs/containerize-backend-app:v0.0.1 # initial version
        ports:
        - containerPort: 8080
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
```

**Deploy it**:

```bash
kubectl apply -f deployment.yaml
```

**Monitor rollout**:

```bash
kubectl rollout status deployment/backend-app
```

---

## 🚀 Updating the Deployment

To update the app to the `latest` version:

**Option 1: Modify YAML**

- Change image to `13angs/containerize-backend-app:latest` in `deployment.yaml`.
- Apply the update:

```bash
kubectl apply -f deployment.yaml
```

**Option 2: Command Line Update**

```bash
kubectl set image deployment/backend-app backend-container=13angs/containerize-backend-app:latest
```

**Annotate the change cause**:

```bash
kubectl annotate deployment/backend-app kubernetes.io/change-cause="Updated image to latest" --overwrite
```

---

## 🔁 Rollbacks (Revert Deployments)

- **What**: Quickly revert to a previous Deployment if something goes wrong.
- **How**:
  - Kubernetes stores Deployment history.
  - Rollback to a previous revision easily.

**Rollback to previous version**:

```bash
kubectl rollout undo deployment/backend-app
```

**Rollback to specific revision**:

```bash
kubectl rollout undo deployment/backend-app --to-revision=2
```

**Annotate the rollback cause**:

```bash
kubectl annotate deployment/backend-app kubernetes.io/change-cause="Rollback to v0.0.1 due to issues in latest" --overwrite
```

**View rollout history**:

```bash
kubectl rollout history deployment/backend-app
```

---

## ✅ Best Practices

- Always **monitor** deployments.
- Use **readiness probes** to catch bad deployments early.
- Always **annotate** update and rollback reasons.
- Be prepared for **quick rollbacks**.