# Alert Simulation System Backend Architecture

## 1. Introduction
This document outlines the architecture of the **Alert Simulation System**, a backend service that processes historical machine tag data to identify when a defined alert condition was met. The system does not trigger real alerts but allows users to visualize past alert conditions based on stored data.

## 2. System Overview
The backend is responsible for:
- Retrieving **historical machine tag data** within a defined timeframe.
- **Evaluating conditions** to determine when an alert threshold was crossed.
- Formatting **response data as JSON** for frontend visualization.
- **Ensuring performance** by handling up to **2000 data points per request**.

## 3. Input Data & User-Defined Conditions
Users can specify:
- **Start & End Time:** Data range (maximum **one week**).
- **Tags:** Parameters like `temperature`, `pressure`.
- **Logic Statement:** Condition (e.g., `Tag1 > 10 AND Tag2 < 50`).
- **Max Data Points:** Limit of **2000** matches per graph.

## 4. Historical Data Retrieval
### Data Source
Uses **CosmosDB** to store and fetch machine tag history.

### API to Fetch Data
```python
async def get_machine_tags_history(
    db, 
    machine, 
    start_datetime, 
    end_datetime, 
    tag_ids, 
    limit=10000
):
    historical_data = await db.fetch(
        machine_id=machine,
        start_time=start_datetime,
        end_time=end_datetime,
        tags=tag_ids,
        max_records=limit
    )
    return historical_data
```

## 5. Evaluating Alert Conditions
The function `evaluate_alert_condition()` checks if a tag value violates a given condition.

### Processing Historical Data
```python
matches = []
last_known_values = {}

for data_point in historical_data:
    timestamp = data_point.timestamp
    tag_name = data_point.tag
    tag_value = data_point.value

    last_known_values[tag_name] = tag_value

    condition_met = evaluate_alert_condition(tag_name, tag_value, user_defined_conditions)
    
    if condition_met:
        matches.append({
            "timestamp": timestamp,
            "tag_name": tag_name,
            "value": tag_value
        })
```

## 6. Formatting Data for Frontend
Once processed, the backend formats data as JSON for the frontend to visualize.

### Example JSON Response
```json
{
  "alert_id": "2d537e04-0139-4740-9a69-dadbd95d5984",
  "matches": [
    { "timestamp": "2025-02-25T14:00:00Z", "tag_name": "TEMP", "value": -1 },
    { "timestamp": "2025-02-25T14:05:00Z", "tag_name": "TEMP", "value": 3 }
  ]
}
```

## 7. Testing and Validation
To ensure system reliability, the backend undergoes rigorous testing:
- **Accuracy Testing:** Validate detection logic against expected results.
- **Performance Testing:** Ensure smooth processing for large data sets.
- **Edge Case Handling:** Test missing values, extreme inputs, and invalid data.

## 8. Conclusion
This architecture provides a scalable backend for **alert simulation**, enabling users to visualize alert conditions efficiently. It ensures fast processing, structured data output, and optimized performance.
