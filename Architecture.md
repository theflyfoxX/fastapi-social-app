# Deep Dive into Alert Simulation System Backend Architecture

## 1. Understanding the Problem

The **Alert Simulation System** is a backend service that allows users to analyze **historical machine tag data** and detect when certain conditions were met. Unlike a real-time alert system, this simulation does not trigger live notifications but instead provides **a retrospective view of machine events** for better analysis and decision-making.

### **Key Concept: When Should an Alert be Logged?**

- Consider a machine that must maintain **a temperature above 0°C**.
- On **March 1, 2025, at 6:00 PM**, the temperature dropped **below 0°C**.
- At **6:01 PM**, the temperature returned to normal.
- The system should only log **this exact moment when the condition was met** and display it visually.

This ensures that unnecessary data points are not included, making the visualization **clear, precise, and efficient**.

---

## 2. Enhancing the System with Additional Features

### **What Was Missing?**

- The **original design focused** only on fetching historical data.
- It lacked **multiple alert conditions per tag**.
- No implementation for **storing and retrieving past simulations**.
- Missing **metadata for alerts** (severity, frequency, resolution time, etc.).
- No **custom visualization filters** for better graph representation.

### **What We Will Improve?**

- **Allow multiple threshold conditions per tag** (e.g., both upper and lower bounds).
- **Introduce metadata** for alerts (e.g., machine health status, frequency of violations).
- **Allow real-time tagging of anomalies** and let users annotate findings.

---

## 3. Improved Data Model

### **Database Schema (PostgreSQL)**

```sql
CREATE TABLE machine_alerts (
    id UUID PRIMARY KEY,
    machine_id UUID NOT NULL,
    tag_code TEXT NOT NULL,
    value FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    condition_met BOOLEAN DEFAULT FALSE,
    severity TEXT CHECK (severity IN ('low', 'medium', 'high')),
    notes TEXT
);
```

### **Improvements Over the Old Design**

- **Condition\_met column** ensures we only log violations.
- **Severity column** helps users prioritize issues.
- **Notes column** allows users to annotate events.

---

## 4. Advanced Data Retrieval and Filtering

### **Improved API Endpoint**

```python
from fastapi import FastAPI, Query
from typing import List
from datetime import datetime

app = FastAPI()

@app.get("/api/alert-simulator/data")
async def get_alert_data(
    machine_id: str,
    start_datetime: datetime,
    end_datetime: datetime,
    tag_codes: List[str] = Query([]),
    min_value: float = None,
    max_value: float = None
):
    query = "SELECT * FROM machine_alerts WHERE machine_id = :machine_id AND timestamp BETWEEN :start AND :end"
    
    if tag_codes:
        query += " AND tag_code IN (:tag_codes)"
    if min_value:
        query += " AND value >= :min_value"
    if max_value:
        query += " AND value <= :max_value"

    data = await fetch_from_db(query, machine_id, start_datetime, end_datetime, tag_codes, min_value, max_value)
    return {"data": data}
```

### **Enhancements**

- **Min and max values filtering** allows flexible querying.
- **Dynamic query construction** improves efficiency.

---

## 5. Enhanced Condition Evaluation

### **Old vs New Approach**

- Previously, we only checked for **one threshold condition per tag**.
- Now, we allow **multiple conditions per tag**.

### **New Evaluation Logic**

```python
def evaluate_conditions(tag_name, tag_value, conditions):
    for condition in conditions:
        operator, threshold = condition["operator"], condition["value"]
        
        if operator == ">" and tag_value > threshold:
            return True
        elif operator == "<" and tag_value < threshold:
            return True
        elif operator == "==" and tag_value == threshold:
            return True
        elif operator == "!=" and tag_value != threshold:
            return True
    return False
```

### **Why This is Better?**

- Allows **custom conditions per tag**.
- Supports **multiple logical operators**.
- More flexible and scalable.

---

## 6. Optimized JSON Response for Frontend

### **New JSON Format**

```json
{
  "machine_id": "123e4567-e89b-12d3-a456-426614174000",
  "alerts": [
    {
      "timestamp": "2025-03-01T18:00:00Z",
      "tag_code": "TEMP",
      "value": -1,
      "severity": "high",
      "condition": "value < 0",
      "notes": "Temperature dropped below safe limit."
    }
  ]
}
```

### **New Features**

- **Severity field** helps prioritize alerts.
- **Notes field** allows user annotations.
- **Machine ID included** for better tracking.

## 7. Testing & Validation Strategies

### **New Test Cases to Cover**

- **Multiple conditions per tag**.
- **Handling missing data points**.
- **Testing with large datasets (> 2000 records).**
- **Edge cases like invalid timestamps, out-of-range values.**

### **Automated API Test Example**

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_alert_fetch():
    response = client.get("/api/alert-simulator/data", params={
        "machine_id": "123e4567-e89b-12d3-a456-426614174000",
        "start_datetime": "2025-03-01T00:00:00",
        "end_datetime": "2025-03-02T00:00:00"
    })
    assert response.status_code == 200
```

---

## 8. Conclusion

This **new and improved architecture** introduces:

- **More powerful filtering options**.
- **Custom alert conditions per tag**.
- **More insightful JSON responses for better frontend visualization**.

