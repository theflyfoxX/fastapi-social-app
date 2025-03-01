# **Graph Alert Simulator Backend Architecture**

**Date:** March 1, 2025  

## **Table of Contents**
1. Introduction  
2. System Architecture Overview  
3. Notification System  
4. Filtering Mechanism  
5. Applying Changes  
6. Graph Exporting as JPG  
7. API Endpoints & Functionalities  
8. Database Schema & Models  
9. Code Snippets  
10. Testing & Optimization Strategies  
11. Connecting Backend with Frontend  
12. Caching and Notification Handling  
13. Conclusion  

---

## **1. Introduction**
This document outlines the **Graph Alert Simulator Backend**, focusing on:
- Fetching **historical alert data** from a database.
- Allowing users to **filter and visualize** data in a graph.
- **Notifying users** via Email/SMS when machine conditions reach a threshold.
- **Downloading graphs** as JPG for reports or analysis.

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

## **3. Notification System (Parag. 1 - Notify User)**
Users receive notifications via **Email or SMS** based on the settings assigned by an **admin**.  
- The **admin** determines which users are eligible for notifications.  
- Users will be **notified when a machine with a specific UUID reaches a certain threshold** for a selected `tag_code` (either **Temperature (°C)** or **Pressure (P)**).  
- The notification system ensures that only **authorized users** receive alerts when a predefined condition is met.  

---

## **4. Filtering Mechanism (Parag. 2 - Filtering)**  

### **Frontend & Backend Logic**  

1. **Retrieve and map inputs for dropdowns:**  
   - Fetch available options dynamically for each input field (`machine-uuid`, `tag_codes`, etc.).
   - Populate dropdowns based on **valid machine-tag associations**.

2. **Conditions for Inputs:**  

   - **Tag Codes Validation:**  
     - Machines may only have **one valid tag_code** (either `TEMP` or `PRESSURE`).
     - If a user selects an **invalid tag_code** (one that does not exist for the selected machine), an **error alert** should be displayed.

   - **Date Inputs Validation:**  
     - Users can select a **start date** and an **end date** freely.  
     - The **start date must always be earlier than the end date** (`start_date < end_date`).  
     - If this condition is violated, an **error alert** should appear.

   - **Apply Button Logic:**  
     - The **"Apply Changes"** button should remain **disabled** until **all conditions** are satisfied (valid machine UUID, tag_code, and date range).

---

## **5. Applying Changes (Parag. 3 - Apply Changes)**
Once all conditions are met and the user clicks **"Apply Changes"**:  
1. The frontend triggers an **API request** to fetch **filtered data** from **PostgreSQL**.  
2. The retrieved data is then **displayed on a graph** where:  
   - The **X-axis** represents the **time interval** between `start_datetime` and `end_datetime`.  
   - The **Y-axis** represents the selected **tag_code** value (`TEMP °C` or `Pressure P`).  

---

## **6. Graph Exporting as JPG (Parag. 4 - Download Graph)**
- Users should have the ability to **download the generated graph** as a **JPG file**.  
- When clicking the **"Download Graph"** button:  
  1. The system should **convert the current graph into a JPG image**.  
  2. The file should be **automatically downloaded** to the user's device.  

---

## **7. API Endpoints & Functionalities**

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

## **8. Database Schema & Models**
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

## **9. Testing & Optimization Strategies**

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

## **10. Connecting Backend with Frontend**
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

## **11. Caching and Notification Handling**
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

## **12. Conclusion**
This document presents a **structured backend architecture** for a **Graph Alert Simulator**, ensuring:
- **Efficient data retrieval** from PostgreSQL.
- **Real-time notifications** for alerts.
- **Seamless integration** with a React frontend.
- **Optimized performance** via Redis caching.
