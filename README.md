# 📄 Omniblu Notification Function Performance Plan

---

## 📌 Problem Statement

The Azure Function App currently in production is responsible for handling real-time machine alerts by sending notifications through:

* 📧 **SendGrid** (email alerts)
* 📱 **Twilio** (SMS alerts)

The function is triggered by Azure Storage Queues and operates based on conditions like temperature, pressure, etc. As the system scales to potentially millions of alerts, performance and scalability bottlenecks must be identified and addressed.

This PRD proposes a full performance plan, including:

* 🔍 Real-time monitoring using **Azure Application Insights**
* 🧪 Load testing with **k6**
* 🧠 Profiling with **pyinstrument** in local/dev mode

---

## 🧪 Performance Test Plan

We aim to:

1. Determine thresholds for concurrent messages before system degradation.
2. Identify the time cost of each stage: queue trigger → processing → external API calls.
3. Observe memory and CPU usage (where possible) in Azure Portal.
4. Automate tests for future deployments.

---

## 🧠 Categories of Tests

### 1. Queue Load (Messages per second)

**Goal**: Identify how many alerts per second we can handle reliably without failures.

✅ *Setup with k6 load simulation targeting Function App URL.*

```javascript
export let options = { vus: 500, duration: '60s' };
```

Each virtual user sends a message every 1 second.

### 2. Cold Start vs Warm Start

**Goal**: Measure execution latency on cold start vs warm start.

* Cold starts can be simulated by stopping and restarting the app before test runs.
* Warm starts are measured by keeping the app alive during the test.

### 3. Function Execution Profiling (Local)

**Tool**: `pyinstrument`

✅ *Add to `__init__.py` inside the triggered function:*

```python
from pyinstrument import Profiler
profiler = Profiler()
profiler.start()

Notification().process(message)

profiler.stop()
print(profiler.output_text(unicode=True, color=True))
```

### 4. Alert Payload Complexity

**Goal**: Identify which alert data structures or payload sizes degrade processing performance.

✅ *Use payloads with:*

* Many recipients (1000+ user\_ids)
* Multiple group\_ids
* Attachments (email)
* High SQL response latency (simulated)

### 5. External Dependencies

**Goal**: Measure impact of:

* Twilio API rate limits or delays
* SendGrid delays

✅ Add debug logs before/after external calls:

```python
log.debug("Sending SMS to user X")
sms_client.send_sms(...)
log.debug("SMS sent")
```

---

## 📈 Real Monitoring with Azure

### ✅ Application Insights Setup

1. **Enable in Azure Portal**:

   * Go to Function App → Monitoring → Application Insights → Enable

2. **Bind in code (host.json):**

```json
{
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "maxTelemetryItemsPerSecond": 5
      }
    }
  }
}
```

3. **Track custom logs:**

```python
import logging
log = logging.getLogger("azure")
log.info("Email successfully sent to user")
```

### 🔍 You’ll see:

* Success/failure rates
* Duration per invocation
* Cold starts
* Telemetry from logs

---

## 📊 Load Testing with k6

### ✅ Install:

```bash
brew install k6     # macOS
choco install k6    # Windows
```

### 📄 Sample `load-test.js`

```js
import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 1000,
  duration: '60s'
};

export default function () {
  const payload = JSON.stringify({
    content: { alert: "High pressure detected" },
    user_ids: ["1", "2", "3"],
    email_template_id: "e123",
    sms_template_id: "s456"
  });

  const headers = { 'Content-Type': 'application/json' };
  http.post('https://<your-function-url>', payload, { headers });
  sleep(1);
}
```

### ✅ Run:

```bash
k6 run load-test.js
```

### 📈 Outputs:

* Avg response time
* Max response time
* Errors per second

---

## 🧠 Local Profiling with pyinstrument

### ✅ Install:

```bash
pip install pyinstrument
```

### 📄 Decorator for Local Use

```python
# utils/profiler.py
from pyinstrument import Profiler
import os

def profile_if_local(func):
    def wrapper(*args, **kwargs):
        profiler = Profiler() if os.getenv("ENV") == "local" else None
        if profiler: profiler.start()
        result = func(*args, **kwargs)
        if profiler:
            profiler.stop()
            print(profiler.output_text(unicode=True, color=True))
        return result
    return wrapper
```

### ✅ Use it:

```python
@profile_if_local
def queueMessage(msg):
    ...
```

---

## 🧪 Test Results (Example)

| Load Level | Duration | Errors | Avg Time | Success Rate |
| ---------- | -------- | ------ | -------- | ------------ |
| 100 users  | 60s      | 0      | 120ms    | 100%         |
| 1000 users | 60s      | 12     | 280ms    | 98.7%        |
| 2000 users | 60s      | 112    | 510ms    | 94.4%        |

---

## ✅ Work / Improvements

1. **Add retry logic** for SendGrid/Twilio failures.
2. **Move SQL logic to async** with `asyncpg` for non-blocking performance.
3. **Use caching for group lookups** (Redis or in-memory).
4. **Track cold start durations separately** in Application Insights.
5. **Add CI k6 load test runner** for PR validation.

---

## ✅ Dependencies Summary

```bash
# Add all to requirements.txt or run manually
pip install pyinstrument
brew install k6
```

---

## ✅ Final Checklist

* [x] Monitoring configured in Azure
* [x] pyinstrument integrated for local profiling
* [x] k6 test script created and run
* [x] Function app tested under load
* [x] Bottlenecks logged and documented
