# Week 6 Assignment: Docker Microservices System & Study Notes

This project uses Docker and Docker Compose to build a three-tier microservice architecture featuring an **Nginx** reverse proxy server, a **Python (Flask)** backend web application, and a **PostgreSQL** relational database.

---

## 1. System Architecture

```text
[ Browser (localhost:8080) ]
             │
             ▼
[ Nginx Reverse Proxy ] (Port 8080 -> 80)
             │
             ▼ (Internal Network: app_net)
[ Python Flask Web App ] (Port 5000)
             │
             ▼ (Internal Network: app_net)
[ PostgreSQL 15 Database ] (Port 5432 + Persistent Volume)