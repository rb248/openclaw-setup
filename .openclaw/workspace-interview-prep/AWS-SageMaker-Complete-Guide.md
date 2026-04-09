# AWS SageMaker AI Developer Guide - Complete Interview Reference

**Compiled from:** AWS SageMaker AI Documentation (docs.aws.amazon.com/sagemaker)  
**Last Updated:** December 2024 (SageMaker AI rebrand)  
**Purpose:** ML System Design Interview Preparation

---

## Table of Contents

1. [What is Amazon SageMaker AI?](#1-what-is-amazon-sagemaker-ai)
2. [SageMaker Processing Jobs](#2-sagemaker-processing-jobs)
3. [Batch Transform](#3-batch-transform-for-inference)
4. [Deploy Models for Inference](#4-deploy-models-for-inference)
5. [Real-Time Endpoints](#5-real-time-endpoints)
6. [Autoscaling](#6-autoscaling)
7. [Blue/Green Deployments](#7-bluegreen-deployments)
8. [Model Monitor](#8-model-monitor)
9. [Data Capture](#9-data-capture)
10. [Interview Answer Templates](#10-interview-answer-templates)

---

## 1. What is Amazon SageMaker AI?

**Definition:** Amazon SageMaker AI is a fully managed machine learning (ML) service. With SageMaker AI, data scientists and developers can quickly and confidently build, train, and deploy ML models into a production-ready hosted environment.

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **SageMaker AI** | Build, train, and deploy ML and foundation models |
| **SageMaker Lakehouse** | Unify data access across S3 data lakes, Redshift |
| **Data and AI Governance** | Discover, govern, and collaborate with SageMaker Catalog |
| **SQL Analytics** | Amazon Redshift SQL engine |
| **Data Processing** | Athena, EMR, Glue for data prep |
| **Unified Studio** | Single development environment |
| **Bedrock** | Build generative AI applications |

### Important Rename Notice (December 2024)
On December 03, 2024, Amazon SageMaker was renamed to **Amazon SageMaker AI**. Legacy namespaces remain unchanged:
- `sagemaker` API namespaces
- AWS CLI commands with `sagemaker`
- Service endpoints containing `sagemaker`
- CloudFormation resources with `AWS::SageMaker`

---

## 2. SageMaker Processing Jobs

**Purpose:** Run data pre/post processing, feature engineering, and model evaluation on fully-managed infrastructure.

### How It Works

```
┌─────────────────┐
│   Your Script   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│   Input Data    │────▶│ Processing Job  │
│   (S3/Athena/   │     │                 │
│   Redshift)     │     │ • Launches      │
└─────────────────┘     │   instances     │
                        │ • Processes     │
┌─────────────────┐     │   data          │
│  Output Data    │◀────│ • Releases      │
│     (S3)        │     │   resources     │
└─────────────────┘     └─────────────────┘
```

### Use Cases
- Data preprocessing and cleaning
- Feature engineering
- Model evaluation
- Distributed processing with Spark

### Key Features
- **Fully managed infrastructure:** No servers to manage
- **Built-in containers:** scikit-learn, Spark
- **Bring your own container:** Custom processing logic
- **Integration:** Works with S3, Athena, Redshift

### API
```python
# CreateProcessingJob API
# Or use SageMaker Python SDK
```

### Monitoring
- CloudWatch logs and metrics
- CPU, GPU, memory, disk metrics
- Event logging

---

## 3. Batch Transform for Inference

**Purpose:** Get inferences from large datasets without a persistent endpoint.

### When to Use
- Preprocess datasets (remove noise/bias)
- Large dataset inference
- No persistent endpoint needed
- Associate input records with inferences

### How It Works

```
Input Files (S3)          Compute Instances          Output Files (S3)
┌─────────────┐           ┌───────────────┐         ┌───────────────┐
│ input1.csv  │──────────▶│  Instance 1   │────────▶│input1.csv.out │
│ input2.csv  │──────────▶│  Instance 2   │────────▶│input2.csv.out │
│ input3.csv  │──────────▶│  Instance 3   │────────▶│input3.csv.out │
└─────────────┘           └───────────────┘         └───────────────┘
```

**Key Points:**
- S3 objects partitioned by key and mapped to instances
- Each input file processed separately
- Output files have same name + `.out` extension
- Predictions in same order as input records

### Parameters

| Parameter | Description | Default/Max |
|-----------|-------------|-------------|
| `SplitType` | How to split input (None, Line) | None |
| `BatchStrategy` | SingleRecord or MultiRecord | - |
| `MaxPayloadInMB` | Max payload size | 100 MB |
| `MaxConcurrentTransforms` | Max parallel transforms | - |
| `AssembleWith` | Output format (None, Line) | None |

**Note:** `MaxConcurrentTransforms * MaxPayloadInMB` must not exceed 100 MB.

### Optimization Tips
- Set `MaxConcurrentTransforms` = number of compute workers
- Use `SplitType=Line` for CSV files
- Use `AssembleWith=Line` for readable output

---

## 4. Deploy Models for Inference

### Deployment Options

| Option | Latency | Use Case |
|--------|---------|----------|
| **Real-time inference** | Milliseconds | Interactive, low latency requirements |
| **Serverless Inference** | Higher (cold start) | Variable/sporadic traffic |
| **Asynchronous inference** | Minutes | Large payloads (up to 1GB), long processing (up to 1 hour) |
| **Batch Transform** | N/A | Offline batch processing |

### Cost Optimization

| Feature | Description |
|---------|-------------|
| **SageMaker Neo** | Optimize models for Inferentia chips |
| **Autoscaling** | Dynamic resource adjustment based on traffic |

### Deployment Approaches

1. **JumpStart in Studio** - Low-code, pre-trained models
2. **ModelBuilder (Python SDK)** - Fine-grained control
3. **CloudFormation (IaC)** - Production scale, CI/CD

---

## 5. Real-Time Endpoints

### Endpoint Lifecycle

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Model Artifact │────▶│ Endpoint Config │────▶│    Endpoint     │
│   (in S3)       │     │ (instance type, │     │  (live HTTPS    │
│                 │     │  model variant) │     │   hosting)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Key APIs

| API | Purpose |
|-----|---------|
| `CreateModel` | Register model artifacts in S3 |
| `CreateEndpointConfig` | Define instance type and initial instance count |
| `CreateEndpoint` | Deploy live endpoint |
| `UpdateEndpoint` | Update with new config (uses blue/green) |

### Endpoint Types

| Type | Best For | Billing |
|------|----------|---------|
| **Real-time** | Synchronous, low latency | Per instance-hour |
| **Asynchronous** | Large payloads, no immediate response | Per instance-hour |
| **Serverless** | Variable traffic | Per inference |
| **Batch Transform** | Offline processing | Per instance-hour |

---

## 6. Autoscaling

**Purpose:** Dynamically adjust compute resources based on incoming traffic.

### Prerequisites
1. Endpoint must exist
2. Register model as scalable target
3. Define scaling policy

### Scaling Policy Types

#### 1. Target Tracking (Recommended)

```python
{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
        "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"
    }
}
```

**How it works:**
- Choose CloudWatch metric and target value
- Auto scaling creates/manages alarms
- Calculates scaling adjustment
- Adds/removes instances to keep metric at target

#### 2. Step Scaling
- Advanced configuration
- Specify exact instances under specific conditions
- **Required** to scale out from zero

### Key Metrics for Autoscaling

| Metric | Description |
|--------|-------------|
| `InvocationsPerInstance` | Average invocations per instance per minute |
| `ConcurrentRequestsPerModel` | Concurrent requests per model (high-res) |
| `ConcurrentRequestsPerCopy` | Concurrent requests per copy (high-res) |

### Scaling Limits

```python
{
    "MinCapacity": 1,   # At least 1
    "MaxCapacity": 10   # Test with expected traffic
}
```

### Cooldown Periods
- **Default:** 300 seconds (5 minutes) for scale-in and scale-out
- **Purpose:** Prevent rapid fluctuations (thrashing)
- **Adjust:** 
  - Increase if adding/removing too quickly
  - Decrease if not responding fast enough

### Schedule-Based Scaling
- Create scheduled actions for specific times
- One-time or recurring
- Managed via AWS CLI or API only

### IAM Permissions Required

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sagemaker:DescribeEndpoint",
                "sagemaker:DescribeEndpointConfig",
                "sagemaker:UpdateEndpointWeightsAndCapacities",
                "application-autoscaling:*",
                "cloudwatch:PutMetricAlarm"
            ],
            "Resource": "*"
        }
    ]
}
```

### Service-Linked Role
- `AWSServiceRoleForApplicationAutoScaling_SageMakerEndpoint`
- Created automatically
- Grants permissions to describe alarms, monitor capacity, scale resources

---

## 7. Blue/Green Deployments

**Purpose:** Zero-downtime deployments with automatic rollback.

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                     Deployment Start                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────┐    ┌─────────────────┐
│   Blue Fleet    │    │   Green Fleet   │
│  (current)      │    │   (new model)   │
│  100% traffic   │    │   0% traffic    │
└────────┬────────┘    └─────────────────┘
         │                     │
         │              ┌──────┴──────┐
         │              │  Provision  │
         │              └──────┬──────┘
         │                     │
         ▼                     ▼
┌─────────────────┐    ┌─────────────────┐
│   Blue Fleet    │◀───│   Green Fleet   │
│   X% traffic    │    │   Y% traffic    │
└─────────────────┘    └────────┬────────┘
                                │
                    ┌───────────┴───────────┐
                    │    Baking Period      │
                    │  (Monitor with CW     │
                    │    alarms)            │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Alarms Trip?        │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    │ YES       │        NO │
                    ▼                       ▼
            ┌───────────────┐      ┌───────────────┐
            │ Auto-Rollback │      │ Shift 100%    │
            │ to Blue       │      │ to Green      │
            └───────────────┘      └───────┬───────┘
                                           │
                                  ┌────────┴────────┐
                                  │ Final Baking    │
                                  │ Period          │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌───────────────┐
                                  │ Terminate     │
                                  │ Blue Fleet    │
                                  └───────────────┘
```

### Traffic Shifting Modes

| Mode | Description | Pros | Cons | Use When |
|------|-------------|------|------|----------|
| **All at once** | 100% shift in one step | Fastest, cheapest | 100% blast radius if broken | Low risk updates |
| **Canary** | Small % (≤50%) → rest | Confines blast radius | Two fleets longer | Balanced safety/speed |
| **Linear** | Equal steps over time | Minimum risk | Longest duration/cost | High risk updates |

### Configuration Example (Canary)

```python
{
    "EndpointName": "my-endpoint",
    "EndpointConfigName": "new-config",
    "DeploymentConfig": {
        "BlueGreenUpdatePolicy": {
            "TrafficRoutingConfiguration": {
                "Type": "CANARY",
                "CanarySize": {
                    "Type": "CAPACITY_PERCENT",
                    "Value": 30  # 30% to canary
                },
                "WaitIntervalInSeconds": 600  # 10 min baking
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
}
```

### Key Terms

| Term | Definition |
|------|------------|
| **Baking period** | Time to monitor green fleet before proceeding |
| **Canary** | Small portion of green fleet receiving traffic |
| **Blue fleet** | Old/current model fleet |
| **Green fleet** | New/updated model fleet |
| **Auto-rollback** | Automatic revert if alarms trip |

### Billing Note
For multi-stage deployments with baking periods, you're billed for **both fleets** during the update. For all-at-once with no baking, billed for one fleet.

---

## 8. Model Monitor

**Purpose:** Automatic monitoring of ML model quality in production.

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

### Steps to Enable

1. **Enable Data Capture** - Log inputs and outputs
2. **Create Baseline** - Compute metrics and constraints from training data
3. **Create Schedule** - Specify data collection frequency and analysis
4. **Inspect Reports** - Watch for violations and CloudWatch notifications

### Monitoring Types

| Type | Monitors |
|------|----------|
| **Data quality** | Input data drift (schema, distribution) |
| **Model quality** | Prediction accuracy (vs ground truth) |
| **Bias drift** | Fairness metrics in production |
| **Feature attribution** | Feature importance drift (SHAP values) |

### Limitations
- Only **single-model endpoints** (not multi-model)
- Computes metrics on **tabular data only**
- Input images/text not analyzed directly (outputs can be)

---

## 9. Data Capture

**Purpose:** Log inputs to endpoint and inference outputs to S3.

### Use Cases
- Training data collection
- Debugging
- Monitoring

### Enable at Endpoint Creation

```python
data_capture_config = {
    "EnableCapture": True,
    "InitialSamplingPercentage": 100,  # % of requests
    "DestinationS3Uri": "s3://bucket/capture/",
    "CaptureOptions": [
        {"CaptureMode": "Input"},
        {"CaptureMode": "Output"}
    ],
    "CaptureContentTypeHeader": {
        "CsvContentTypes": ["text/csv"],
        "JsonContentTypes": ["application/json"]
    }
}
```

### Key Points
- Captures both inputs and predictions to S3
- **Stops capturing** at high disk usage (>75%)
- Used for monitoring, debugging, retraining

### Baseline Creation

From training data, compute:
- Statistics (mean, std, min, max, completeness)
- Constraints (expected ranges, types)

Example constraint:
```json
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
            "BaselineStatistics": "s3://bucket/statistics.json",
            "MonitoringOutputs": [
                {"S3Output": {"S3Uri": "s3://bucket/reports/"}}
            ]
        }
    }
}
```

---

## 10. Interview Answer Templates

### Q1: "How do you deploy a model with 99.99% uptime?"

**Answer:**
"I'd use SageMaker real-time endpoints with blue/green deployment. The endpoint lifecycle is: model artifacts → endpoint config → endpoint. For updates, I'd use canary traffic shifting—route 30% traffic to the new fleet, monitor with CloudWatch alarms during the baking period, then shift 100% if successful. If alarms trip (latency, error rate), auto-rollback to the old fleet. This ensures zero downtime."

### Q2: "How do you handle traffic spikes?"

**Answer:**
"I'd configure autoscaling with target tracking on InvocationsPerInstance. Set a target of 70 invocations per instance per minute, with min=2 and max=20 instances. Include cooldown periods (300s default) to prevent thrashing. I'd also set up CloudWatch alarms to alert if we're hitting max capacity."

### Q3: "How do you monitor model quality in production?"

**Answer:**
"I'd use SageMaker Model Monitor. First, enable Data Capture to log inputs and outputs to S3. Create a baseline from training data with statistics and constraints. Set up a monitoring schedule—hourly or daily—to compare production data against the baseline. Monitor four dimensions: data quality (input drift), model quality (accuracy with ground truth), bias drift, and feature attribution drift. Violations trigger CloudWatch alerts for investigation."

### Q4: "Walk me through a safe model update."

**Answer:**
"I'd use blue/green deployment with canary traffic shifting. First, create a new endpoint config with the updated model. Use UpdateEndpoint with DeploymentConfig specifying CANARY type, 30% canary size, and 10-minute baking period. Set CloudWatch alarms on model latency and error rate. If alarms trip during baking, auto-rollback to the blue fleet. If successful, shift remaining traffic and terminate old fleet after final baking period."

### Q5: "Explain the SageMaker inference options."

**Answer:**
"SageMaker offers four inference options: Real-time for low-latency synchronous predictions, Asynchronous for large payloads up to 1GB with near-real-time requirements, Serverless for variable traffic without infrastructure management, and Batch Transform for offline processing of large datasets. For user-facing applications, I typically use Real-time endpoints with autoscaling and blue/green deployments."

### Q6: "What's the difference between batch transform and real-time endpoints?"

**Answer:**
"Batch Transform is for offline inference on large datasets without a persistent endpoint—ideal for preprocessing or periodic reports. Real-time endpoints are for low-latency synchronous predictions—ideal for user-facing applications. Batch transform processes S3 files in parallel and outputs to S3, while real-time endpoints serve HTTPS requests with millisecond latency."

---

## Quick Reference Tables

### SageMaker Components

| Component | Purpose |
|-----------|---------|
| **Processing Jobs** | Data preprocessing, feature engineering |
| **Training Jobs** | Distributed model training |
| **Endpoints** | Real-time inference hosting |
| **Batch Transform** | Offline batch inference |
| **Model Monitor** | Drift and quality monitoring |
| **Pipelines** | ML workflow orchestration |

### Autoscaling Metrics

| Metric | When to Use |
|--------|-------------|
| `InvocationsPerInstance` | General purpose (target tracking) |
| `ConcurrentRequestsPerModel` | High-resolution monitoring |
| `ConcurrentRequestsPerCopy` | Multi-model endpoints |

### Deployment Strategies

| Strategy | Risk Level | Cost | Speed |
|----------|-----------|------|-------|
| All at once | High | Low | Fast |
| Canary | Medium | Medium | Medium |
| Linear | Low | High | Slow |

---

## Common Interview Mistakes to Avoid

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

❌ **Wrong:** "Batch transform is for real-time"  
✅ **Right:** "Batch transform is offline; use real-time endpoints for low latency"

---

## Architecture Example: Production Setup

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
│  │   (Drift)   │  │  (Accuracy) │──▶│     Alarms          │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

**Document compiled from:**  
- https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html  
- https://docs.aws.amazon.com/sagemaker/latest/dg/processing-job.html  
- https://docs.aws.amazon.com/sagemaker/latest/dg/batch-transform.html  
- https://docs.aws.amazon.com/sagemaker/latest/dg/deploy-model.html  
- https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html  
- https://docs.aws.amazon.com/sagemaker/latest/dg/deployment-guardrails-blue-green.html  
- https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html  
- https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-data-capture.html

**Last Updated:** April 2025  
**Version:** SageMaker AI (December 2024 rebrand)
