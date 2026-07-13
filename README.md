# Employee Management System - CI/CD Pipeline

A full-stack Employee Management System built to demonstrate a complete, production-style Devops pipeline, from code commit to automated testing, containerization, and deployment on Kubernetes.

## Project Overview

This projects is not just a web application; it is a demonstration of real CI/CD (Continuous Integration / Continuous Delivery) pipeline. Every code push is automatically tested, packaged into a Docker container, pushed to Docker Hub, and deployed, with zero manual steps after `git push`.

## Architecture
Developer's Laptop
|
| git push
v
GitHub Repository (source of truth)
|
| triggers (via webhook)
v
Jenkins CI/CD Server
|
|-- Checkout latest code
|-- Install Python dependencies
|-- Run automated tests (pytest); if any fail, pipeline stops here
|-- Build Docker image
|-- Push image to Docker Hub
|-- Deploy container
|
v
Running Application (localhost:5000)
|
v
Kubernetes Deployment (2+ replicas, auto-scaling, self-healing)

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Application | Python + Flask | Web framework |
| Database | SQLite + SQLAlchemy | Data persistence |
| Testing | pytest, pytest-flask | Automated testing (8 tests) |
| Containerization | Docker | Packaging the app |
| Orchestration | Kubernetes (kind) | Scaling and self-healing |
| CI/CD | Jenkins | Pipeline automation |
| Registry | Docker Hub | Image storage |
| Version Control | Git + GitHub | Source control, pipeline-as-code |

## Features

- Add, view, edit, delete, and search employees
- Duplicate email validation
- Fully automated test suite (8 tests covering all core functionality)
- Automated CI/CD pipeline; every push is tested, built, and deployed automatically
- Kubernetes deployment with horizontal scaling and self-healing

## Getting Started (Local Setup)

### Prerequisites
- Python 3.11+
- Docker Desktop
- Git

### Run locally without Docker
```bash
pip install -r requirements.txt
python run.py
```
Visit `http://localhost:5000`

### Run with Docker
```bash
docker build -t employee-management .
docker run -d -p 5000:5000 employee-management
```

### Run tests
```bash
pytest tests/ -v
```

## CI/CD Pipeline

The `Jenkinsfile` in this repository defines a six-stage pipeline:

1. **Checkout** - pulls the latest code from GitHub
2. **Install Dependencies** - installs all Python packages
3. **Run Tests** - runs all 8 automated tests; pipeline stops here if any fail
4. **Build Docker Image** - packages the tested code into a Docker image
5. **Push to Docker Hub** - publishes the image so it can be deployed anywhere
6. **Deploy** - runs the container, making the app live

Jenkins reads this pipeline definition directly from GitHub (Pipeline-as-Code via SCM), so any change to the `Jenkinsfile` is automatically picked up on the next build, with no manual Jenkins reconfiguration required.

## GitHub Webhook (Automatic Trigger)

The pipeline is designed to trigger automatically whenever code is pushed to GitHub, using a GitHub webhook that notifies Jenkins the moment new commits arrive, removing the need to manually click "Build Now."

Since Jenkins runs on `localhost` in this local development setup, `ngrok` is used to create a temporary public URL that GitHub can reach. Because free `ngrok` URLs change on every restart, the webhook is demonstrated via a recorded walkthrough (available separately) showing: a code push, followed by the GitHub webhook firing, followed by Jenkins automatically starting a build. In this recording, GitHub's "Recent Deliveries" log is also shown as confirmation that the webhook successfully reached Jenkins.

## Kubernetes Deployment

The `k8s/` folder contains:
- `deployment.yaml` - defines the app deployment (2 replicas by default)
- `service.yaml` - exposes the app via a NodePort service

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl port-forward service/emp-cicd-service 7070:5000
```

Kubernetes automatically handles:
- **Scaling** - `kubectl scale deployment emp-cicd-app --replicas=5`
- **Self-healing** - automatically restarts any pod that crashes or is manually deleted, maintaining the desired replica count at all times

## Team and Roles

| Member | Role | Responsibilities |
|---|---|---|
| Member 1 | Application Developer | Flask app, database, CRUD routes, pytest tests |
| Member 2 | Docker Engineer | Dockerfile, containerization, Docker Hub |
| Member 3 | CI/CD and Kubernetes Engineer | Jenkins pipeline, GitHub integration, Kubernetes deployment |

## Project Structure
Employee_Management_cicd/
├── app/                    Flask application
├── tests/                  Automated test suite
├── k8s/                    Kubernetes deployment and service configs
├── Dockerfile              Container build instructions
├── docker-compose.yml      Multi-container orchestration
├── Jenkinsfile             CI/CD pipeline definition
├── requirements.txt        Python dependencies
└── run.py                  Application entry point
# Last updated: webhook test
# retry
## retry
# webhook retest
# clean webhook test
# retest after jenkins restart
# test after job recreation
# test after manual build 1 completed
# direct build list test
# retest after jenkins restart
