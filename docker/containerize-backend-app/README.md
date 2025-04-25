# 🐳 Containerize backend app

## 📄 Description

This is a simple Python-based REST API built with Flask and containerized using Docker. It returns a basic JSON response and serves as an introductory example for containerizing backend applications. The goal is to demonstrate how to package an application and its dependencies into a portable Docker container — a key step before deploying to platforms like Kubernetes.

---

## 📁 Project Structure

```
flask-api/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
└── Dockerfile          # Docker instructions to build the container image
```

---

## 🚀 Getting Started (Run Locally)

To run this project on your local machine:

1. Clone this repository.
2. Make sure Docker is installed and running.
3. Follow the instructions below to build and run the application inside a container.

---

## 🔧 Build the Docker Image

Use the following command in the terminal (in the project root directory):

```bash
docker build -t flask-api:latest .
```

### Explanation

- `docker build`: Docker command to create an image from the Dockerfile.
- `-t flask-api:latest`: Tags the image as `flask-api` with the `latest` tag.
- `.`: The current directory is used as the build context.

To confirm the image was built successfully:

```bash
docker images
```

---

## ▶️ Run the Container

Start the container with this command:

```bash
docker run -d -p 5000:5000 flask-api:latest
```

### Explanation

- `-d`: Detached mode (runs in background).
- `-p 5000:5000`: Maps port 5000 on your machine to port 5000 inside the container.
- `flask-api:latest`: Name of the Docker image.

Then, access the application by visiting:

```
http://localhost:5000
```

Expected response:

```json
{"message": "Hello, World!"}
```

---

## 🧹 Cleanup

Stop the running container:

```bash
docker ps        # Find the container ID
docker stop <container_id>
```

Remove the container:

```bash
docker rm <container_id>
```
