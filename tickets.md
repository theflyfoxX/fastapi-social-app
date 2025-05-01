# Alert Simulation System - Development Tickets

## **Ticket 1: Implement Historical Data Retrieval Endpoint**

### **Task:** Develop the `GET /alerts/{alert_id}/simulate-alert-triggers` endpoint.

#### **Subtasks:**

- Integrate with **Cosmos DB** to fetch historical tag data using the `get_machine_tags_history` function.
- Implement **filtering** based on machine ID, timeframe (max one week), and selected tags.
- Set up **pagination or limit** for data retrieval (maximum **2000 matches per request** to avoid system overload).
- Implement **error handling** for:
  - Exceeding data limits.
  - Invalid or missing parameters.
  - Unavailable historical data.

## **Ticket 2: Develop Alert Condition Evaluation Logic**

### **Task:** Implement `evaluate_alert_condition` function to check user-defined conditions against historical tag values.

#### **Subtasks:**

- Define logic to evaluate **single or multiple conditions** (e.g., `Tag1 > 50 AND Tag2 < 20`).
- Support **logical operators** (`AND`, `OR`, `<=`, `>=`, `!=`, etc.).
- Implement handling for **missing tag values** by using the **last known value**.
- Optimize evaluation performance to **handle large datasets efficiently**.

## **Ticket 3: Setup Simulation Start and Status Endpoints**

### **Task:** Develop API endpoints to start a simulation and track its progress.

#### **Subtasks:**

- Implement **`POST /alerts/{alert_id}/simulate-alert-triggers`** to initiate a simulation asynchronously.
- Generate and return a unique **simulation ID** for tracking.
- Develop **`GET /alerts/simulations/{simulation_id}/status`** to check the simulation’s progress.
- Ensure correct handling of different **simulation states** (`IN_PROGRESS`, `COMPLETED`, `FAILED`).

## **Ticket 4: Format Data for Visualization**

### **Task:** Structure response data in a frontend-friendly JSON format for graph plotting.

#### **Subtasks:**

- Convert processed data into a structured **JSON format**.
- Include **timestamps, tag values, and machine ID** for better traceability.
- Ensure each tag has a **unique color assignment** for clear graph visualization.
- Implement an **API response validation function** to check formatting.

## **Ticket 5: Implement Simulation Results Retrieval**

### **Task:** Develop the `GET /alerts/simulate-alert-triggers/{simulation_id}` endpoint to return simulation results.

#### **Subtasks:**

- Fetch stored results linked to `simulation_id`.
- Ensure the response includes only **timestamps when conditions were met**.
- Optimize database queries for **efficient data retrieval**.
- Handle scenarios where no alerts match the user-defined conditions.

## **Ticket 6: Implement Edge Case Handling & Performance Optimization**

### **Task:** Ensure the system handles unexpected inputs and scales efficiently.

#### **Subtasks:**

- **Performance Testing:** Simulate large datasets and optimize query execution times.
- **Edge Case Handling:**
  - Missing or corrupt tag data.
  - Extreme values (e.g., very high/low temperature readings).
  - Invalid timestamps or data types.
- Implement **logging & monitoring** to track API usage and errors.

## **Ticket 7: Develop Unit & Integration Tests for API Endpoints**

### **Task:** Create comprehensive tests to validate API functionality and data accuracy.

#### **Subtasks:**

- Write **unit tests** for:
  - `get_machine_tags_history` function.
  - `evaluate_alert_condition` logic.
  - JSON formatting validation.
- Develop **integration tests** to:
  - Simulate user requests and validate responses.
  - Test API endpoints with real Cosmos DB queries.
  - Ensure correct handling of concurrent requests.
- Automate tests using **pytest & FastAPI’s TestClient**
