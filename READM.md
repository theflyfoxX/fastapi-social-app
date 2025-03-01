# **Graph Alert Simulator Backend Architecture**

**Date:** March 1, 2025

## **Table of Contents**
1. Introduction  
2. System Architecture Overview  
3. API Endpoints & Functionalities  
4. Database Schema & Models  
5. Code Snippets  
6. Testing & Optimization Strategies  
7. Connecting Backend with Frontend  
8. Caching and Notification Handling  
9. Conclusion  

---

## **1. Introduction**
This document outlines the architecture, API design, and implementation details of the **Graph Alert Simulator Backend**.  
The system:
- Fetches **alert history data** from a database.
- **Processes and filters** data for visualization.
- **Notifies users** via email/SMS if conditions are met.

---

## **2. System Architecture Overview**
The **backend** is built using:
- **FastAPI** – Lightweight and fast backend framework.
- **PostgreSQL** – Stores historical alert data.
- **Azure Notification Services** – Handles real-time email/SMS alerts.
- **Redis** – Caches frequently accessed data.

### **Workflow**
1. The user applies **filters (machine_id, date range, tag_code)**.
2. The **backend fetches data** from PostgreSQL.
3. The **data is displayed in a graph**.
4. If conditions are met (e.g., **high temperature or pressure**), a **notification is sent**.
5. The graph can be **downloaded as a JPG**.

---

## **3. API Endpoints & Functionalities**

### **Fetching Historical Alert Data**
- **Endpoint:** `GET /api/alert-simulator/data`
- **Purpose:** Retrieve filtered alert data.
- **Query Parameters:**
  - `machine_id` (UUID, required)
  - `start_datetime` (ISO datetime, required)
  - `end_datetime` (ISO datetime, required)
  - `tag_codes` (List[str], optional)

---

### **Exporting Graph as JPG**
- **Endpoint:** `GET /api/alert-simulator/export-jpg`
- **Purpose:** Export the displayed graph as a JPG file.

---

### **Sending Notifications**
- **Endpoint:** `POST /api/alert-simulator/notify`
- **Purpose:** Send email/SMS alerts based on conditions.
- **Body:**
  ```json
  {
    "user_id": "UUID",
    "machine_id": "UUID",
    "tag_code": "TEMP",
    "value": 95.0,
    "threshold": 90.0
  }
  ```

---

## **4. Database Schema & Models**
The system stores alert history in **PostgreSQL** with the following schema:

### **Table: alerts**
| Column | Type | Description |
|---------|------|-------------|
| id | UUID (Primary Key) | Unique record ID |
| machine_id | UUID (Foreign Key) | Machine Identifier |
| tag_code | TEXT | Data type (TEMP / PRESSURE) |
| value | FLOAT | Recorded value |
| timestamp | TIMESTAMP | Time of record |
| user_id | UUID (Foreign Key) | User assigned to alert |
| notification_sent | BOOLEAN | Whether a notification was sent |

---

## **5. Code Snippets**

### **Fetching Alert Data**
```python
from fastapi import FastAPI, Query
from datetime import datetime

app = FastAPI()

@app.get("/api/alert-simulator/data")
async def get_alert_data(
    machine_id: str,
    start_datetime: datetime,
    end_datetime: datetime,
    tag_codes: list[str] = Query([]),
):
    data = fetch_data_from_db(machine_id, start_datetime, end_datetime, tag_codes)
    return {"data": data}
```

---

### **Exporting Graph as JPG**
```python
import matplotlib.pyplot as plt
from fastapi.responses import FileResponse

@app.get("/api/alert-simulator/export-jpg")
async def export_graph():
    plt.figure(figsize=(6,4))
    plt.plot([1,2,3], [90, 100, 80], label="Temp °C")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.legend()
    plt.savefig("graph.jpg")
    return FileResponse("graph.jpg")
```

---

### **Sending Notifications**
```python
from azure.communication.email import EmailClient

def send_notification(user_email, message):
    email_client = EmailClient("your-azure-connection-string")
    email_client.send(
        from_email="alerts@yourdomain.com",
        to_email=user_email,
        subject="Alert Notification",
        body=message
    )
```

---

## **6. Testing & Optimization Strategies**

### **Unit Tests**
- Validate API responses for:
  - Correct filtering of data.
  - Error handling (invalid machine_id, date ranges).
  - Graph generation.

### **Integration Tests**
- Verify database interactions:
  - Correctly retrieving data.
  - Handling large datasets.

### **Performance Optimization**
- **Redis caching** for frequently accessed queries.
- **Asynchronous processing** for high-volume requests.

---

## **7. Connecting Backend with Frontend**
The **React frontend** interacts with FastAPI using `axios` for API calls.  

Example **fetch request** in React:
```javascript
import axios from "axios";
const fetchData = async () => {
  const response = await axios.get("/api/alert-simulator/data", {
    params: {
      machine_id: "1234",
      start_datetime: "2025-03-01T00:00:00",
      end_datetime: "2025-03-07T00:00:00",
      tag_codes: ["TEMP"]
    }
  });
  console.log(response.data);
};
```

---

## **8. Caching and Notification Handling**
### **Redis for Caching**
```python
import redis
cache = redis.Redis(host="localhost", port=6379, db=0)

def get_cached_data(key):
    if cache.exists(key):
        return cache.get(key)
    return None
```

### **Azure Notification Service**
- Handles **real-time notifications** for critical alerts.
- Admin sets notification preferences for users.

---

## **9. Conclusion**
This document presents a **structured backend architecture** for a **Graph Alert Simulator**, ensuring:
- **Efficient data retrieval** from PostgreSQL.
- **Real-time notifications** for alerts.
- **Seamless integration** with a React frontend.
- **Optimized performance** via Redis caching.
