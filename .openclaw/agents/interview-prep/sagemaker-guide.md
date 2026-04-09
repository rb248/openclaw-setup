# AWS SageMaker Developer Guide - Interview Essentials

**Source:** AWS SageMaker AI Documentation  
**Key sections:** Endpoints, Autoscaling, Blue/Green Deployments, Model Monitor

---

## 1. SageMaker Endpoint Lifecycle

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Model Artifact │────▶│ Endpoint Config │────▶│    Endpoint     │
│   (in S3)       │     │ (instance type, │     │  (live HTTPS    │
│                 │     │  model variant) │     │   hosting)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**Key APIs:**
- `CreateModel` - Register model artifacts
- `CreateEndpointConfig` - Define instance type and initial count
- `CreateEndpoint` - Deploy live endpoint
- `UpdateEndpoint` - Update with new config (uses blue/green by default)

---

## 2. Endpoint Types

| Type | Use Case | Latency | Billing |
|------|----------|---------|---------|
| **Real-time** | Synchronous predictions | Milliseconds | Per instance-hour |
| **Asynchronous** | Large payloads, no immediate response needed | Minutes | Per instance-hour |
| **Serverless** | Variable/sporadic traffic | Higher (cold start) | Per inference |
| **Batch Transform** | Offline batch inference | N/A | Per instance-hour |

**Interview tip:** Most production systems use **real-time endpoints** for user-facing predictions.

---

## 3. Autoscaling (Application Auto Scaling)

### Prerequisites
- Endpoint must exist
- Register model as scalable target
- Define scaling policy

### Scaling Policy Types

**1. Target Tracking (Recommended)**
```python
# Keep InvocationsPerInstance at ~70
{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
        "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"
    }
}
```

**2. Step Scaling**
- Advanced configuration
- Specify exact instances under specific conditions
- Required to scale out from zero

### Key Metrics for Autoscaling

| Metric | Description |
|--------|-------------|
| `InvocationsPerInstance` | Average invocations per instance per minute |
| `ConcurrentRequestsPerModel` | Concurrent requests per model (high-res) |
| `ConcurrentRequestsPerCopy` | Concurrent requests per copy (high-res) |

### Scaling Limits
```python
{
    "MinCapacity": 1,  # At least 1
    "MaxCapacity": 10  # Adjust based on traffic testing
}
```

### Cooldown Periods
- **Default:** 300 seconds (5 minutes) for scale-in and scale-out
- **Purpose:** Prevent rapid fluctuations
- **Adjust:** Increase if adding/removing too quickly; decrease if not responding fast enough

### IAM Permissions Required
```json
{
    "Action": [
        "sagemaker:DescribeEndpoint",
        "sagemaker:DescribeEndpointConfig",
        "sagemaker:UpdateEndpointWeightsAndCapacities",
        "application-autoscaling:*",
        "cloudwatch:PutMetricAlarm"
    ]
}
```

---

## 4. Blue/Green Deployments (Deployment Guardrails)

**What it is:** Zero-downtime deployment with automatic rollback capabilities

**How it works:**
1. Provision new fleet (green) with updates
2. Shift traffic from old fleet (blue) to green
3. Monitor during baking period
4. If alarms trip → auto-rollback to blue
5. If successful → terminate blue fleet

### Traffic Shifting Modes

| Mode | Description | Pros | Cons | Use When |
|------|-------------|------|------|----------|
| **All at once** | 100% traffic shift in one step | Fastest, cheapest | 100% blast radius if broken | Low risk updates |
| **Canary** | Small % (e.g., 30%) → rest | Confines blast radius | Two fleets running longer | Balanced safety/speed |
| **Linear** | Equal steps over time (e.g., 25% × 4) | Minimum risk | Longest duration, cost | High risk updates |

### Key Configuration Parameters

```python
{
    "BlueGreenUpdatePolicy": {
        "TrafficRoutingConfiguration": {
            "Type": "CANARY",  # or "ALL_AT_ONCE", "LINEAR"
            "CanarySize": {
                "Type": "CAPACITY_PERCENT",
                "Value": 30  # 30% to canary
            },
            "WaitIntervalInSeconds": 600  # 10 min baking period
        },
        "TerminationWaitInSeconds": 600,  # Wait before killing blue
        "MaximumExecutionTimeoutInSeconds": 1800  # 30 min max
    },
    "AutoRollbackConfiguration": {
        "Alarms": [
            {"AlarmName": "ModelLatencyAlarm"},
            {"AlarmName": "ErrorRateAlarm"}
        ]
    }
}
```

### Baking Period
- Time to monitor green fleet before proceeding
- If CloudWatch alarms trip → automatic rollback
- Builds confidence before full traffic shift

### Auto-Rollback Alarms
Monitor during baking period:
- Model latency (p99)
- Error rate (5xx)
- Custom business metrics

---

## 5. Model Monitor

**Purpose:** Automatic monitoring of model quality in production

### How It Works
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Data Capture │────▶│   Baseline   │────▶│  Schedule   │
│  (inputs/     │     │  (constraints│     │  (compare   │
│   outputs)    │     │   + stats)   │     │   to base)  │
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                                  ▼
                                           ┌──────────────┐
                                           │   Reports    │
                                           │  (violations,│
                                           │   CloudWatch)│
                                           └──────────────┘
```

### Monitoring Types

| Type | What It Monitors |
|------|------------------|
| **Data quality** | Input data drift (schema, distribution) |
| **Model quality** | Prediction accuracy (vs ground truth) |
| **Bias drift** | Fairness metrics in production |
| **Feature attribution** | Feature importance drift (SHAP values) |

### Data Capture

**Enable at endpoint creation:**
```python
data_capture_config = {
    "EnableCapture": True,
    "InitialSamplingPercentage": 100,  # % of requests to capture
    "DestinationS3Uri": "s3://bucket/capture/",
    "CaptureOptions": [
        {"CaptureMode": "Input"},
        {"CaptureMode": "Output"}
    ]
}
```

**Key points:**
- Captures both inputs and predictions to S3
- Stops capturing at high disk usage (>75%)
- Used for monitoring, debugging, retraining

### Baseline Creation

From training data, compute:
- Statistics (mean, std, min, max, etc.)
- Constraints (expected ranges, types)

```python
# Example constraint
{
    "feature_name": "age",
    "inferred_type": "Integral",
    "completeness": 1.0,
    "num_constraints": {
        "min_value": 18,
        "max_value": 100
    }
}
```

### Monitoring Schedule

```python
{
    "MonitoringScheduleName": "my-schedule",
    "MonitoringScheduleConfig": {
        "ScheduleConfig": {
            "ScheduleExpression": "cron(0 * ? * * *)"  # Hourly
        },
        "MonitoringJobDefinition": {
            "BaselineConstraints": "s3://bucket/constraints.json",
            "BaselineStatistics": "s3://bucket/statistics.json"
        }
    }
}
```

### Limitations

- Only supports **single-model endpoints** (not multi-model)
- Computes metrics on **tabular data only**
- Input images/text not analyzed directly (outputs can be)

---

## 6. Interview Answer Templates

### Q: "How do you deploy a model with 99.99% uptime?"

**Answer:**
"I'd use SageMaker real-time endpoints with blue/green deployment. The endpoint lifecycle is: model artifacts → endpoint config → endpoint. For updates, I'd use canary traffic shifting—route 30% traffic to the new fleet, monitor with CloudWatch alarms during the baking period, then shift 100% if successful. If alarms trip (latency, error rate), auto-rollback to the old fleet. This ensures zero downtime."

### Q: "How do you handle traffic spikes?"

**Answer:**
"I'd configure autoscaling with target tracking on InvocationsPerInstance. Set a target of 70 invocations per instance per minute, with min=2 and max=20 instances. Include cooldown periods (300s default) to prevent thrashing. I'd also set up CloudWatch alarms to alert if we're hitting max capacity."

### Q: "How do you monitor model quality in production?"

**Answer:**
"I'd use SageMaker Model Monitor. First, enable Data Capture to log inputs and outputs to S3. Create a baseline from training data with statistics and constraints. Set up a monitoring schedule—hourly or daily—to compare production data against the baseline. Monitor four dimensions: data quality (input drift), model quality (accuracy with ground truth), bias drift, and feature attribution drift. Violations trigger CloudWatch alerts for investigation."

### Q: "Walk me through a safe model update."

**Answer:**
"I'd use blue/green deployment with canary traffic shifting. First, create a new endpoint config with the updated model. Use UpdateEndpoint with DeploymentConfig specifying CANARY type, 30% canary size, and 10-minute baking period. Set CloudWatch alarms on model latency and error rate. If alarms trip during baking, auto-rollback to the blue fleet. If successful, shift remaining traffic and terminate old fleet after final baking period."

---

## 7. Key Terms Quick Reference

| Term | Definition |
|------|------------|
| **Endpoint** | Live HTTPS endpoint serving predictions |
| **Production Variant** | A model version on an endpoint |
| **Blue/Green** | Zero-downtime deployment with two fleets |
| **Canary** | Test small % of traffic on new fleet first |
| **Baking Period** | Monitoring time before committing to shift |
| **Target Tracking** | Autoscaling to keep metric at target value |
| **Data Capture** | Logging inputs/outputs to S3 |
| **Baseline** | Reference statistics/constraints from training |
| **Drift** | Change in data or model behavior over time |
| **Auto-rollback** | Automatic revert if alarms trip |

---

## 8. Architecture Example: Production Setup

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Request                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   SageMaker Endpoint                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Production Variant A (current model)               │   │
│  │  - ml.m5.xlarge instances                           │   │
│  │  - Autoscaling: 2-10 instances                      │   │
│  │  - Target: 70 invocations/instance                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Capture                            │
│              (inputs + outputs → S3)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Model Monitor                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │ Data Quality│  │Model Quality│  │    CloudWatch       │ │
│  │   (drift)   │  │  (accuracy) │──▶│     Alarms          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. Common Interview Mistakes to Avoid

❌ **Wrong:** "Endpoints are for testing"  
✅ **Right:** "Endpoints are managed HTTPS hosting with autoscaling and monitoring"

❌ **Wrong:** "Autoscaling based on CPU"  
✅ **Right:** "Target tracking on InvocationsPerInstance, with min/max limits"

❌ **Wrong:** "Deploy new model directly"  
✅ **Right:** "Blue/green with canary or linear traffic shifting"

❌ **Wrong:** "Monitor with general logs"  
✅ **Right:** "Data Capture + Model Monitor for data quality and model quality"

❌ **Wrong:** "Update endpoint immediately"  
✅ **Right:** "Baking period with auto-rollback alarms"

---

*Source: AWS SageMaker AI Developer Guide*
