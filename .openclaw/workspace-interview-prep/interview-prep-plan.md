# ML System Design Interview Prep - Rishabh

## Your Specific Weaknesses (From Andersen Feedback)

### 1. Outlier Detection & Handling
**What you said:** "Outliers would be good to exclude"
**What they wanted:** Investigation-first approach—are they fraud? sensor failures? genuine rare events?
**Correct framework:**
- **Investigate first:** Domain knowledge, visualization, statistical tests
- **Options:** Robust losses (Huber, Tukey), winsorizing/capping, transformations (log, Box-Cox)
- **Separate modeling:** Isolation Forest, LOF for anomaly detection
- **Never default to deletion** without understanding WHY

### 2. Batch vs Online Inference
**What you said:** "Online uses more RAM over time"
**The reality:** Both load the model once. Key differences:
| Aspect | Batch Inference | Online Inference |
|--------|----------------|------------------|
| **Latency** | Minutes/hours acceptable | Milliseconds required |
| **Throughput** | High (millions per batch) | Per-request |
| **Cost model** | Utilization-focused | SLA-focused |
| **Memory** | Model fits in RAM once | Model fits in RAM once |
| **Use case** | Overnight reports, recommendations | Real-time fraud, search ranking |

### 3. SageMaker Endpoints
**What you said:** "Endpoints for testing"
**Reality:** Production HTTPS hosting infrastructure
- **Lifecycle:** Model artifacts → Endpoint config → Endpoint
- **Variants:** Real-time, asynchronous, serverless
- **Deployment strategies:** Blue/green, canary, A/B testing
- **Features:** Autoscaling, data capture, monitoring integration

### 4. Model Monitoring
**What you mixed:** General logging/testing with ML monitoring
**The 4 dimensions you MUST cover:**
1. **Input data quality:** Schema validation, range checks, missing values
2. **Data drift:** PSI, KS-test, population stability
3. **Performance metrics:** Accuracy, precision/recall with ground truth
4. **System health:** Latency p50/p99, error rates, resource utilization
**Actions:** Alert → Triage → Rollback / Retrain

### 5. LSTM Fundamentals
**What you missed:** Cell state vs hidden state mechanics
**Correct explanation:**
- LSTM is an RNN variant (not the first recurrent model)
- **Cell state:** Long-term memory (persistent across time steps)
- **Hidden state:** Short-term memory (output at each step)
- **Three gates:** Forget gate, input gate, output gate
- **Solves:** Vanishing gradient problem in long sequences
- **Modern context:** Largely replaced by Transformers for most tasks

---

## Study Resources (Prioritized by Your Gaps)

### Priority 1: Fix Your Weaknesses
1. **AWS SageMaker Developer Guide** - Read hosting/deployment chapters
2. **"Designing Machine Learning Systems" by Chip Huyen** - Chapters on monitoring, data quality
3. **Hands-On Machine Learning (Géron)** - Outlier detection, preprocessing chapters

### Priority 2: System Design Framework
4. **"Machine Learning System Design Interview" book** - 10 practice problems with solutions
5. **Backprop blog** - Framework for structuring answers
6. **Airbnb Tech Blog** - Real production ML systems

### Priority 3: Communication & Behavioral
7. **"Crucial Conversations"** - Structured conflict handling
8. **"Storytelling with Data"** - Metrics presentation frameworks

---

## Practice Question Bank

### Category 1: Weak Area Deep Dives (Your Priority)

**Q1: Outlier Handling in Production**
"You detect outliers in your fraud detection model's input features. Walk me through your decision process. Do you remove them?"

*Key points to hit:*
- Don't automatically remove—investigate first
- Could be genuine fraud (rare but valid)
- Options: Robust scalers, winsorizing, separate anomaly detection model
- Monitoring: Track outlier rate over time

**Q2: Batch vs Online for E-commerce Recommendations**
"Design a product recommendation system. Do you use batch or online inference?"

*Key points to hit:*
- Latency requirements: <100ms for homepage
- Most recommendations: Batch precomputed, cached
- Real-time signals: Online layer for recent behavior
- Hybrid: Batch for candidates, online for ranking

**Q3: SageMaker Endpoint Architecture**
"You need to deploy a model that handles 10k requests/second with <50ms latency. Design the SageMaker setup."

*Key points to hit:*
- Multi-model endpoints or separate endpoints per model variant
- Autoscaling policies: Target tracking on InvocationsPerInstance
- Endpoint configuration with production variants
- Data capture for monitoring
- A/B testing setup with traffic shifting

**Q4: ML Monitoring Dashboard**
"What metrics do you monitor for a production classification model?"

*Key points to hit:*
- Data quality: Missing rate, feature distributions
- Drift: Input drift, concept drift detection
- Performance: Accuracy, precision/recall (when ground truth available)
- System: Latency percentiles, error rates, resource usage
- Actions: Automated rollback triggers, retrain pipelines

**Q5: Explain LSTM to a Junior Engineer**
"How does an LSTM work, and when would you use it vs a Transformer?"

*Key points to hit:*
- Cell state (long-term) vs hidden state (short-term)
- Gate mechanics: forget, input, output
- Solves vanishing gradients in RNNs
- Use case: Sequential data where order matters, before 2017
- Today: Transformers dominate (self-attention, parallelizable)

### Category 2: Full System Design Questions

**Q6: Design YouTube Video Recommendations**
- Requirements: Scale (2B users), freshness, diversity
- Data: Watch history, likes, demographics
- Model: Two-tower neural network, candidate generation + ranking
- Serving: Batch + online hybrid
- Evaluation: Online A/B test metrics

**Q7: Design Fraud Detection for Stripe**
- Real-time requirements (<50ms)
- Feature engineering: Transaction patterns, velocity
- Model: Gradient boosting + neural network ensemble
- Monitoring: Precision/recall trade-offs, false positive rate

**Q8: Design Instagram Explore Ranking**
- Multi-objective: Engagement + diversity + freshness
- Two-stage: Retrieval (embedding-based) + Ranking (lightGBM/NN)
- Training data: Implicit feedback (clicks, dwell time)
- Cold start: Content-based signals for new items

**Q9: Design Ad Click Prediction**
- Scale: Billions of impressions
- Feature freshness: Real-time user context
- Model: Logistic regression baseline, deep learning for improvement
- Calibration: Predicted probability must match actual CTR

**Q10: Design Visual Search for Pinterest**
- Multi-modal: Image + text
- Embeddings: CNN for images, BERT for text
- Approximate nearest neighbors: FAISS, ScaNN
- Latency: Precomputed embeddings, cached

---

## Framework for Answering (40-minute interview)

### Minute 0-5: Problem Clarification
- WHO is the user?
- WHAT is the business goal?
- SCALE: QPS, data volume, latency requirements
- CONSTRAINTS: Privacy, budget, timeline

### Minute 5-10: ML Task Formulation
- Define the task: Classification? Regression? Ranking?
- Success metrics: Offline + online
- Baseline: What's the simple thing that works?

### Minute 10-20: Data & Features
- Sources: Existing vs new collection
- Labeling: Explicit vs implicit feedback
- Features: User, item, interaction
- Quality: Missing values, outliers, bias

### Minute 20-30: Model & Training
- Architecture: Justify your choice
- Training: Batch size, optimizer, regularization
- Evaluation: Offline metrics, train/validation split

### Minute 30-38: Deployment & Monitoring
- Serving: Batch vs online, caching strategy
- Testing: A/B test design
- Monitoring: The 4 dimensions
- Rollback: When and how

### Minute 38-40: Summary & Trade-offs
- Recap key decisions
- Future improvements
- Scale considerations

---

## Quick Reference Cards

### Card 1: When to Use What Model
| Problem | Start With | Scale Up To |
|---------|-----------|-------------|
| Tabular data | XGBoost/LightGBM | Neural network if massive data |
| Text classification | Logistic regression + TF-IDF | BERT fine-tuning |
| Image classification | ResNet/EfficientNet | Vision Transformer |
| Recommendations | Matrix factorization | Two-tower neural network |
| Sequence modeling | LSTM/GRU | Transformer |

### Card 2: Monitoring Checklist
- [ ] Data quality alerts (schema, range, missing)
- [ ] Distribution drift detection
- [ ] Performance degradation (accuracy, precision, recall)
- [ ] Latency percentiles (p50, p95, p99)
- [ ] Error rate tracking
- [ ] Business metric correlation
- [ ] Automated rollback triggers

### Card 3: SageMaker Components
| Component | Purpose |
|-----------|---------|
| Processing Jobs | Data preprocessing at scale |
| Training Jobs | Distributed model training |
| Endpoints | Real-time inference hosting |
| Batch Transform | Offline batch inference |
| Model Monitor | Data quality & drift detection |
| Pipelines | Orchestrate ML workflows |

---

## Next Steps

1. **This week:** Review the 5 weak area questions above. Write out detailed answers.
2. **Next week:** Pick 2 full system design questions. Practice out loud with a timer.
3. **Ongoing:** Read one Airbnb/Netflix tech blog post per day.

## Mock Interview Checklist

Before your next interview, ensure you can fluently explain:
- [ ] Outlier detection options beyond deletion
- [ ] Batch vs online: latency vs throughput, not memory
- [ ] SageMaker endpoint lifecycle and deployment strategies
- [ ] The 4 dimensions of ML monitoring
- [ ] LSTM: cell state, hidden state, gates, vanishing gradients
- [ ] Structure: Problem → Data → Model → Eval → Deploy → Monitor

---

*Generated based on your Andersen feedback + FAANG interview guides*
