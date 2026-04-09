# ML Monitoring Deep Dive - Chip Huyen's Framework

## Your Monitoring Weakness (From Feedback)

**What you did:** Mixed monitoring with general logging/testing and resource debugging
**What they wanted:** The 4 dimensions of ML monitoring with concrete metrics and actions

---

## The 4 Artifacts to Monitor (In Order of Importance)

### 1. Accuracy-Related Metrics (Closest to Business)
**What to track:**
- Classification: Accuracy, Precision, Recall, F1, AUC-ROC
- Regression: MAE, RMSE, R²
- Ranking: NDCG, MRR, Precision@k

**Key insight:** These require ground truth labels, which are often delayed
- **Short feedback loops:** Minutes (recommendations, clicks)
- **Long feedback loops:** Weeks/months (fraud detection—dispute window)

**Example answer for interview:**
"For a fraud detection model, I'd track precision and recall at different thresholds. Since ground truth labels arrive after the dispute window (1-3 months), I'd also use proxy metrics like the rate of user disputes as an early warning signal."

---

### 2. Predictions (Most Common to Monitor)
**Why monitor predictions:**
- Low dimensional (easy to visualize)
- Summary statistics straightforward
- Distribution shifts in predictions indicate input distribution shifts (if model weights haven't changed)

**What to check:**
- Distribution shifts (use KS-test for 1D data)
- Unusual patterns (e.g., predicting all False for 10 minutes)
- Confidence scores drifting

**Statistical methods:**
- **Kolmogorov-Smirnov (KS) test:** Non-parametric, works on 1D data
- **Maximum Mean Discrepancy (MMD):** Kernel-based, for multivariate data
- **Least-Squares Density Difference:** Alternative for distribution comparison

---

### 3. Features (Industry Focus)
**Feature validation ("unit tests for data"):**
- Min/max/median within expected ranges
- Values match regex patterns
- Values belong to predefined sets
- Cross-feature constraints (e.g., arrival_time > departure_time)

**Tools:**
- **Great Expectations** (open source)
- **Deequ** (AWS)
- **TensorFlow Data Validation**

**Warning:** Feature shifts don't always mean model degradation. Feature drift is often benign. Alert fatigue is real.

---

### 4. Raw Inputs (Hardest but Most Fundamental)
**Challenges:**
- Multiple sources, formats, structures
- Often managed by data platform teams
- ML engineers may not have direct access

**When to monitor:**
- When you suspect upstream data pipeline issues
- Schema changes
- Encoding changes (e.g., emoji encoding)

---

## The 3 Types of Data Distribution Shifts

| Shift Type | What Changes | What Stays Same | Example |
|------------|--------------|-----------------|---------|
| **Covariate Shift** | P(X) changes | P(Y\|X) same | More women over 40 in training data |
| **Label Shift** | P(Y) changes | P(X\|Y) same | Breast cancer prevalence changes |
| **Concept Drift** | P(Y\|X) changes | P(X) same | House prices drop post-COVID for same features |

**Memory aid:**
- **Covariate shift:** Input distribution changes
- **Label shift:** Output distribution changes  
- **Concept drift:** Relationship between input/output changes

---

## Causes of ML System Failures

### Software System Failures (60% of failures at Google)
1. Dependency failure
2. Deployment failure
3. Hardware failure
4. Downtime/crashing

### ML-Specific Failures (40% but more dangerous)

#### 1. Production Data ≠ Training Data
**Why:**
- Real-world data distribution ≠ training distribution
- World isn't stationary (trends, seasons, events)

**Examples:**
- COVID changed "Wuhan" search intent
- Competitor pricing changes affect your price predictions
- Celebrity mention causes user surge

#### 2. Edge Cases
**Outlier:** Data differs significantly from other examples
**Edge case:** Model performs significantly worse on an example

**Key point:** Not all outliers are edge cases. A jaywalker on a highway is an outlier, but not an edge case if your self-driving car handles it correctly.

#### 3. Degenerate Feedback Loops
**Definition:** System's outputs influence the feedback used to train the next iteration

**Example (Recommendation system):**
1. Song A ranked slightly higher than Song B
2. Users click A more because it's shown first
3. Model gets more positive feedback for A
4. Model ranks A even higher
5. **Result:** Rich get richer, filter bubbles

**Detection:**
- Measure popularity diversity of outputs
- Check hit rate across popularity buckets
- Track if recommendations become more homogeneous over time

**Fixes:**
1. **Randomization:** Show random items to new content (TikTok approach)
2. **Contextual bandits:** Intelligent exploration
3. **Positional features:** Model learns position bias separately from true quality

---

## Monitoring Toolbox

### 1. Logs
**What to log:**
- Function calls, inputs, outputs
- Errors, stack traces
- Unusual events (long inputs, NaNs)

**Distributed tracing:**
- Give each process a unique ID
- Track request across 20-30 hops in microservices
- Search logs by ID when debugging

**Processing:**
- **Batch:** Spark, Hadoop (periodic)
- **Stream:** Kafka, Kinesis, Flink SQL (real-time)

### 2. Dashboards
**Purpose:**
- Visualize relationships
- Make monitoring accessible to non-engineers

**Warning:** Dashboard rot is real. Pick the right metrics.

### 3. Alerts
**Components:**
1. **Description:** What's happening, timestamp, service
2. **Policy:** Condition (e.g., accuracy < 90% for 10 minutes)
3. **Notification:** Email, Slack, PagerDuty

**Actionable alerts:** Include mitigation instructions or runbook

**Alert fatigue:** Too many trivial alerts desensitize people to critical ones

---

## Observability vs Monitoring

| Monitoring | Observability |
|------------|---------------|
| Passive: track external outputs | Active: infer internal state from outputs |
| Aggregated metrics | Fine-grained, sliceable metrics |
| When something goes wrong | Why something went wrong |

**Observability = Instrumentation:**
- Add timers to functions
- Count NaNs in features
- Track input transformations
- Log with tags/keywords for later slicing

**Example queries observability enables:**
- "Show users where model A was wrong in last hour, grouped by zip code"
- "Show outlier requests in last 10 minutes"
- "Show intermediate outputs for this input"

---

## Interview Answer Template: Model Monitoring

When asked "How do you monitor a production ML model?" use this structure:

### 1. Operational Metrics (Software Health)
"First, I monitor system health: latency p50/p99, throughput, error rates, CPU/GPU utilization, memory usage. I set SLOs like 99.99% uptime and <200ms p50 latency."

### 2. ML-Specific Metrics (4 Artifacts)
**Accuracy metrics:**
"I track [precision/recall/F1/RMSE] depending on the task. I need ground truth labels, which come from [user feedback/dispute window]."

**Predictions:**
"I monitor prediction distributions for drift using KS-test. Sudden changes in prediction patterns can indicate upstream issues."

**Features:**
"I validate features using Great Expectations—checking ranges, schemas, cross-feature constraints."

**Raw inputs:**
"When possible, I monitor raw inputs for schema changes or encoding issues."

### 3. Data Distribution Shifts
"I watch for:
- **Covariate shift:** Input distribution changes (e.g., new user demographic)
- **Label shift:** Output distribution changes (e.g., fraud rate spikes)
- **Concept drift:** Relationship changes (e.g., post-COVID housing prices)"

### 4. Alerting & Actions
"I set alerts for metric thresholds with actionable runbooks. When alerted, I can:
- Rollback to previous model version
- Trigger retraining pipeline
- Investigate feature pipeline issues"

### 5. Observability
"I instrument the system to answer questions like 'Which feature contributed most to wrong predictions in the last hour?'"

---

## Key Takeaways for Your Interview

1. **Don't mix ML monitoring with general logging.** They're separate concerns.

2. **Always mention the 4 artifacts:** Accuracy → Predictions → Features → Raw inputs

3. **Ground truth labels are often delayed.** Have proxy metrics for early warning.

4. **Know the 3 shift types:** Covariate, Label, Concept

5. **Degenerate feedback loops matter** for recommender systems—mention popularity bias.

6. **Alert fatigue is real.** Don't monitor everything; monitor what matters.

7. **Observability > Monitoring.** Being able to investigate beats just detecting.

---

## Quick Reference: When to Retrain

| Trigger | Action |
|---------|--------|
| Performance degradation detected | Investigate cause first |
| Confirmed data distribution shift | Retrain/fine-tune on new data |
| Scheduled (weekly/monthly) | Retrain regardless of drift |
| Feature schema change | May need full retrain from scratch |
| New class added | Must retrain (label schema change) |

---

## Practice Question

**Q: "You deployed a fraud detection model 6 months ago. Recently, false negative rate increased by 15%. Walk me through your investigation."**

**A:**
1. **Check operational metrics:** Is the system up? Latency normal? Rule out infra issues.

2. **Check prediction distribution:** Has the fraud score distribution shifted? KS-test between recent and training data.

3. **Check feature drift:** Which features changed? Use feature validation tools.

4. **Check for concept drift:** Are fraudsters using new techniques? Same transaction patterns now have different fraud probability.

5. **Check for covariate shift:** New merchant types? New geographic regions? Input distribution changed.

6. **Check feedback loop:** Are we missing fraud labels because the model is letting fraud through undetected? Degenerate loop.

7. **Action:** If confirmed drift → retrain on recent data with fraud labels from dispute window.

---

*Source: Designing Machine Learning Systems by Chip Huyen, Chapter 8*
