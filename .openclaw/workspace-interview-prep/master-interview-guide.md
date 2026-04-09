# Rishabh's ML Interview Master Guide

Based on:
- Andersen technical screening feedback
- FAANG ML System Design frameworks (Backprop, Exponent, Towards Data Science)
- Chip Huyen's "Designing Machine Learning Systems"

---

## PART 1: Your 5 Critical Weaknesses (FIX THESE FIRST)

### WEAKNESS 1: Outlier Handling ❌

**What you said:** "Outliers would be good to exclude"

**Why it's wrong:** Outliers can be valid rare events (fraud, equipment failures, viral content). Default deletion loses signal.

**Correct approach (investigation first):**
1. **Understand the outlier:** Domain knowledge, visualization, statistical tests
2. **Is it data error?** → Fix pipeline
3. **Is it genuine rare event?** → Keep it, handle specially

**Handling options (not deletion):**
| Method | When to use |
|--------|-------------|
| **Robust losses** | Huber loss, Tukey loss—less sensitive to outliers |
| **Winsorizing/capping** | Clip extreme values at percentiles (e.g., 1st and 99th) |
| **Transformations** | Log transform, Box-Cox to reduce skew |
| **Separate modeling** | Isolation Forest, LOF for anomaly detection |
| **Robust scalers** | RobustScaler (uses median/IQR, not mean/std) |

**Interview answer:**
"I wouldn't automatically remove outliers. First, I'd investigate—are these data errors, or genuine rare events like fraud? If genuine, I'd consider robust losses, winsorizing at the 99th percentile, or separate anomaly detection models depending on the use case."

---

### WEAKNESS 2: Batch vs Online Inference ❌

**What you said:** "Online inference uses more RAM over time"

**Why it's wrong:** Both load the model once. Memory doesn't accumulate per request.

**Correct distinction:**

| Aspect | Batch Inference | Online (Real-time) Inference |
|--------|----------------|------------------------------|
| **Latency requirement** | Minutes/hours acceptable | Milliseconds (often <100ms) |
| **Throughput** | High (millions/batch) | Per-request |
| **Cost optimization** | Resource utilization | Meeting SLA |
| **Memory pattern** | Model loaded once | Model loaded once |
| **Use cases** | Overnight reports, precomputed recs | Fraud detection, search ranking, live predictions |

**Key insight:** Most production systems use **hybrid approaches**:
- Batch: Candidate generation, precompute most recommendations
- Online: Ranking, real-time user context

**Interview answer:**
"The key difference isn't memory—both load the model once. It's latency SLA versus throughput optimization. Batch optimizes for cost per prediction with high throughput. Online optimizes for low latency per request. Most systems use hybrid: batch for candidates, online for ranking with real-time signals."

---

### WEAKNESS 3: SageMaker Endpoints ❌

**What you said:** "Endpoints mainly for testing"

**Why it's wrong:** Endpoints are production HTTPS hosting infrastructure.

**SageMaker endpoint lifecycle:**
```
Model Artifacts → Endpoint Config → Endpoint
                      ↓
              Production Variants (A/B testing)
                      ↓
              Autoscaling Policies
                      ↓
              Data Capture (for monitoring)
```

**Endpoint types:**
| Type | Use case |
|------|----------|
| **Real-time** | Synchronous, low latency (<100ms) |
| **Asynchronous** | Large payloads, doesn't need immediate response |
| **Serverless** | Variable traffic, pay per inference |
| **Batch Transform** | Offline batch inference |

**Deployment strategies:**
- **Blue/green:** Zero-downtime switchover
- **Canary:** Route small % traffic to new version
- **A/B testing:** Compare model variants

**Interview answer:**
"SageMaker endpoints are managed HTTPS inference hosting. The lifecycle is: model artifacts → endpoint configuration → endpoint. I can deploy multiple variants for A/B testing, configure autoscaling on InvocationsPerInstance, and enable data capture for monitoring. For a high-traffic model, I'd use multi-model endpoints or separate endpoints with traffic shifting for canary deployments."

---

### WEAKNESS 4: Model Monitoring ❌

**What you did:** Mixed with general logging/testing and resource debugging

**What they wanted:** The 4 dimensions with concrete metrics and actions

**Chip Huyen's 4 artifacts to monitor (from book):**

#### 1. Accuracy-Related Metrics
- Classification: Accuracy, Precision, Recall, F1, AUC-ROC
- Regression: MAE, RMSE, R²
- Ranking: NDCG, Precision@k

**Ground truth delays:**
- **Short feedback loop:** Minutes (clicks, recommendations)
- **Long feedback loop:** Weeks/months (fraud—dispute window)

#### 2. Predictions
- Distribution shifts (KS-test)
- Unusual patterns (all same prediction)
- Confidence score drift

#### 3. Features
- **Validation:** Min/max, regex, schema (Great Expectations, Deequ)
- **Drift:** Distribution changes
- **Warning:** Most feature drift is benign—alert fatigue is real

#### 4. Raw Inputs
- Schema changes
- Encoding changes
- Upstream pipeline issues

**The 3 types of data distribution shifts:**
| Shift | Changes | Stays Same | Example |
|-------|---------|------------|---------|
| **Covariate** | P(X) | P(Y\|X) | New user demographic |
| **Label** | P(Y) | P(X\|Y) | Fraud rate spikes |
| **Concept** | P(Y\|X) | P(X) | Post-COVID house prices |

**Interview answer:**
"I monitor 4 artifacts: accuracy metrics (when ground truth available), predictions (for drift), features (validation + distribution), and raw inputs. For drift detection, I use KS-test for predictions and watch for covariate shift (input changes), label shift (output changes), and concept drift (relationship changes). Alerts trigger actions: investigate → rollback or retrain."

---

### WEAKNESS 5: LSTM Fundamentals ❌

**What you missed:** Cell state vs hidden state, gate mechanics, historical context

**Correct LSTM explanation:**

**Problem with vanilla RNNs:** Vanishing gradients in long sequences

**LSTM solution:** Gated mechanism with two state vectors:
- **Cell state (Cₜ):** Long-term memory (runs through entire chain with minimal changes)
- **Hidden state (hₜ):** Short-term memory/output at each step

**Three gates:**
1. **Forget gate:** What to discard from cell state
2. **Input gate:** What new info to store in cell state  
3. **Output gate:** What from cell state to output as hidden state

**Key points for interview:**
- LSTM is an **RNN variant** (not the first recurrent model)
- Invented in 1997 by Hochreiter & Schmidhuber
- **Today:** Transformers dominate (self-attention, parallelizable, better long-range dependencies)
- **Still useful:** Small datasets, resource-constrained environments, sequential data where order matters

**Interview answer:**
"An LSTM is a type of RNN that uses a cell state and hidden state. The cell state acts as long-term memory, while the hidden state is the short-term output. Three gates—forget, input, and output—control information flow, solving the vanishing gradient problem in long sequences. LSTMs were invented in 1997, but today Transformers are preferred for most tasks due to self-attention and parallelization. I'd still use LSTMs for small datasets or resource-constrained environments."

---

## PART 2: ML System Design Interview Framework (40 Minutes)

### Minute 0-5: Problem Clarification

**Ask:**
- WHO is the user?
- WHAT is the business goal?
- SCALE: QPS, data volume, latency SLA?
- CONSTRAINTS: Privacy, budget, timeline?

**Example:**
"Before designing, I need to understand: Who are we recommending to? What's the business objective—engagement, revenue, or diversity? What's the scale—DAU, QPS? What's the latency requirement? Any privacy constraints with user data?"

### Minute 5-10: ML Task Formulation

**Define:**
- Task type: Classification, regression, ranking, generation?
- Success metrics: Offline (AUC, NDCG) + Online (CTR, revenue)
- Baseline: What's the simple thing that works?

**Example:**
"This is a ranking problem. Offline, I'll use NDCG@10. Online, I'll A/B test click-through rate and dwell time. My baseline is popularity-based recommendations."

### Minute 10-20: Data & Features

**Cover:**
- **Sources:** Existing vs new collection
- **Labels:** Explicit (ratings) vs implicit (clicks, dwell time)
- **Features:** User, item, context, interaction
- **Quality:** Missing values, outliers, bias, cold start

**Example:**
"For features, I'll use: user demographics, historical interactions, item metadata, and real-time context. I'll handle cold start with content-based features for new users."

### Minute 20-30: Model & Training

**Cover:**
- Architecture: Justify your choice
- Training: Batch vs online, distributed?
- Evaluation: Cross-validation, temporal split for time-series

**Example:**
"I'll start with a two-tower neural network for candidate generation, then a lightGBM ranker. This balances recall and precision. I'll use temporal split since this is time-series data."

### Minute 30-38: Deployment & Monitoring

**Cover:**
- Serving: Batch vs online, caching
- Testing: A/B test design
- Monitoring: The 4 dimensions + alerts + actions

**Example:**
"For serving, I'll precompute recommendations in batch and cache them, with an online layer for real-time personalization. I'll run a 2-week A/B test. For monitoring, I'll track prediction drift, feature validation, and accuracy metrics when labels arrive."

### Minute 38-40: Summary & Trade-offs

**Recap:**
- Key decisions and why
- What you'd do with more time
- How to scale

**Example:**
"To summarize: batch candidate generation, online ranking, 2-week A/B testing, and 4-dimension monitoring. With more time, I'd add diversity constraints and explore reinforcement learning for exploration."

---

## PART 3: Practice Questions (Target Your Weaknesses)

### Outlier Handling Questions

**Q1:** "You find 5% of your training data are outliers. What do you do?"

*Bad answer:* "Remove them."

*Good answer:* "First, I'd investigate—are these data errors or genuine rare events? For data errors, I'd fix the pipeline. For genuine outliers like fraud, I'd consider robust losses, winsorizing at 99th percentile, or separate anomaly detection models depending on the business impact."

---

### Batch vs Online Questions

**Q2:** "Design an ad click prediction system. Batch or online inference?"

*Bad answer:* "Online because batch uses less RAM."

*Good answer:* "Ad click prediction needs <50ms latency, so online inference. However, I'd use a hybrid: batch precompute candidate ads, then online ranking with real-time user context. Both approaches load the model once—the difference is latency SLA vs throughput optimization."

---

### SageMaker Questions

**Q3:** "How do you deploy a model handling 10k QPS with 99.99% uptime?"

*Bad answer:* "Use endpoints for testing."

*Good answer:* "I'd use SageMaker real-time endpoints with multi-model deployment. Configure autoscaling on InvocationsPerInstance, enable data capture for monitoring, and implement blue/green deployment for zero-downtime updates. The endpoint lifecycle is: model artifacts → endpoint config → endpoint with production variants."

---

### Monitoring Questions

**Q4:** "What metrics do you monitor for a production fraud model?"

*Bad answer:* "Logs, errors, CPU usage."

*Good answer:* "I monitor 4 artifacts: (1) Accuracy—precision/recall when fraud labels arrive after dispute window, (2) Predictions—distribution drift via KS-test, (3) Features—validation and drift detection, (4) Raw inputs—schema changes. I watch for covariate shift (new transaction patterns), label shift (fraud rate changes), and concept drift (fraudsters adapting). Alerts trigger investigation, rollback, or retraining."

---

### LSTM Questions

**Q5:** "Explain LSTM vs Transformer."

*Bad answer:* "LSTM is the first recurrent model. It has gates."

*Good answer:* "An LSTM is a type of RNN with cell state (long-term memory) and hidden state (short-term output), controlled by three gates. It solved vanishing gradients in vanilla RNNs. However, Transformers use self-attention, are parallelizable, and handle long-range dependencies better. Today I'd use Transformers for most tasks, but LSTMs for small data or resource constraints."

---

## PART 4: Full System Design Questions

### Q6: Design YouTube Video Recommendations

**Key points:**
- Two-stage: candidate generation (two-tower NN) + ranking (LightGBM/NN)
- Features: watch history, likes, dwell time, demographics
- Hybrid serving: batch for candidates, online for ranking
- Evaluation: NDCG offline, CTR/dwell time online
- Monitoring: prediction drift, feature validation, degenerate feedback loops

### Q7: Design Stripe Fraud Detection

**Key points:**
- Real-time: <50ms latency requirement
- Features: transaction velocity, amount patterns, device fingerprint
- Model: Gradient boosting (XGBoost/LightGBM) for interpretability + NN ensemble
- Labels: Confirmed fraud after dispute window (long feedback loop)
- Monitoring: High precision to minimize false positives (customer friction)

### Q8: Design Instagram Explore Ranking

**Key points:**
- Multi-objective: engagement + diversity + freshness
- Cold start: content-based signals for new items
- Degenerate feedback loops: measure popularity diversity
- A/B testing: Control for network effects

---

## PART 5: Quick Reference Cards

### Card 1: When to Use What Model

| Problem | Start With | Scale To |
|---------|-----------|----------|
| Tabular | XGBoost/LightGBM | Neural net if massive |
| Text | Logistic + TF-IDF | BERT fine-tuning |
| Image | ResNet/EfficientNet | Vision Transformer |
| Recommendations | Matrix factorization | Two-tower NN |
| Sequence | LSTM/GRU | Transformer |

### Card 2: Monitoring Checklist

- [ ] Accuracy metrics (when ground truth available)
- [ ] Prediction distribution drift (KS-test)
- [ ] Feature validation (schema, ranges)
- [ ] Feature distribution shifts
- [ ] Latency percentiles (p50, p95, p99)
- [ ] Error rates
- [ ] Business metric correlation
- [ ] Automated rollback triggers

### Card 3: Shift Types

| Type | P(X) | P(Y) | P(Y\|X) | P(X\|Y) |
|------|------|------|---------|---------|
| Covariate | Changes | Changes | Same | - |
| Label | - | Changes | - | Same |
| Concept | Same | Changes | Changes | - |

### Card 4: SageMaker Components

| Component | Purpose |
|-----------|---------|
| Processing Jobs | Data preprocessing |
| Training Jobs | Distributed training |
| Endpoints | Real-time inference |
| Batch Transform | Offline inference |
| Model Monitor | Drift detection |
| Pipelines | ML workflow orchestration |

---

## PART 6: Study Schedule

### Week 1: Fix Your Weaknesses
- [ ] Read this guide thoroughly
- [ ] Write out answers to the 5 weakness questions
- [ ] Practice explaining LSTM with cell/hidden states

### Week 2: Deep Dive Monitoring
- [ ] Review Chip Huyen Chapter 8 summary
- [ ] Practice the monitoring interview template
- [ ] Understand KS-test, covariate/label/concept drift

### Week 3: System Design Framework
- [ ] Practice 2 full system design questions with timer
- [ ] Draw architecture diagrams
- [ ] Focus on the 40-minute structure

### Week 4: Mock Interviews
- [ ] Do 3+ mock interviews
- [ ] Get feedback
- [ ] Refine weak areas

---

## Final Checklist (Before Your Interview)

Can you fluently explain:
- [ ] Outlier handling: investigation first, then robust losses/winsorizing/separate models
- [ ] Batch vs online: latency vs throughput, not memory
- [ ] SageMaker: endpoint lifecycle, deployment strategies, autoscaling
- [ ] Monitoring: 4 artifacts, 3 shift types, actionable alerts
- [ ] LSTM: cell state, hidden state, gates, RNN variant, vs Transformers
- [ ] 40-minute framework: Problem → Data → Model → Eval → Deploy → Monitor

---

*Good luck. You've got this.*
