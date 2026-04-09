# Chapter 2: Introduction to Machine Learning Systems Design
## From "Designing Machine Learning Systems" by Chip Huyen

---

## Chapter Overview

This chapter covers:
1. **Objectives** - Why the system is needed and how to align business and ML goals
2. **Requirements** - Four key requirements: reliability, scalability, maintainability, adaptability
3. **Iterative Process** - The cyclical nature of ML system development
4. **Mind vs Data** - The debate between model-centric and data-centric approaches

---

## 1. Business and ML Objectives

### Key Insight
> "Most companies don't care about the fancy ML metrics."

**The Core Problem:**
- Companies assess ML model impact through experimentation (A/B testing)
- They choose the model that leads to **better business metrics**, regardless of ML metrics
- Business metrics impact profit either:
  - **Directly:** Conversion rate, cost reduction
  - **Indirectly:** Customer satisfaction, time spent on site

**Example - Netflix's Take Rate:**
Many companies create custom metrics to map business to ML metrics. Netflix uses "take rate" to measure how often users actually watch recommended content.

### Decoupling Objectives

**Traditional Approach (Single Model):**
```
loss = α × objective₁ + β × objective₂
```

**Better Practice (Separate Models):**
```
score = α × score₁ + β × score₂
```

Train different models for each objective, then weight outputs:
- Allows changing system behavior without retraining
- Different monitoring policies per model
- Improves maintainability

### Interview Questions on Objectives

1. **"How do you translate business metrics into ML metrics?"**
   - Identify business goal (e.g., increase revenue)
   - Find proxy ML metric (e.g., click-through rate)
   - Establish correlation through A/B testing

2. **"Your model has 95% accuracy but business metrics didn't improve. Why?"**
   - Accuracy might not correlate with business value
   - Could be optimizing wrong metric
   - Need to verify with A/B testing

3. **"How do you handle multiple objectives?"**
   - Train separate models per objective
   - Weight outputs during inference
   - Allows flexible tuning without retraining

---

## 2. Four Requirements for ML Systems

### 1. Reliability
**Definition:** System continues to perform correctly even in face of adversity (hardware, software, human errors).

**ML-Specific Challenges:**
- ML systems can **fail silently** (no 500 errors, just wrong predictions)
- Need monitoring for prediction quality, not just uptime
- Methods discussed in Chapter 8 (Monitoring)

**Interview Questions:**
- "How do you detect when an ML model fails in production?"
- "What's the difference between a traditional system failure and an ML failure?"

### 2. Scalability
**Definition:** System can scale up/down according to demand and manage all artifacts, models, and data.

**Key Aspects:**
- Handle increasing traffic (more predictions)
- Handle growing data volume
- Manage model versions and artifacts
- Distributed training when needed

**Interview Questions:**
- "How would you design a system for 10x traffic increase?"
- "How do you handle models that don't fit in memory?"

### 3. Maintainability
**Definition:** Different people can contribute and use the same tools; code is documented and versioned.

**Best Practices:**
- Structured workloads for multi-disciplinary teams
- Code, data, and artifacts versioned
- Models must be reproducible
- Documentation for handoffs

**Interview Questions:**
- "How do you ensure reproducibility in ML experiments?"
- "How do you version control both code and data?"

### 4. Adaptability
**Definition:** System can evolve in response to data shifts, target changes, or business objectives without service interruption.

**Key Challenges:**
- Data distribution shifts over time
- Business objectives change
- Must update models without downtime
- Continual learning (Chapter 9)

**Interview Questions:**
- "How do you detect data drift?"
- "How do you update a production model without downtime?"

---

## 3. The Iterative Process

ML system development is **NOT linear**—it's iterative and cyclical:

```
        ┌─────────────────┐
        │  1. Project     │
        │    Scoping      │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  2. Data        │
        │  Engineering    │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  3. ML Model    │
        │   Development   │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  4. Deployment  │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  5. Monitoring  │
        │  & Continual    │
        │    Learning     │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  6. Business    │
        │    Analysis     │
        └────────┬────────┘
                 │
                 └──────────────► (Back to 1, 2, or 3)
```

### Step 1: Project Scoping
- Define objectives and goals
- Identify constraints
- Determine resources needed
- Identify stakeholders

### Step 2: Data Engineering
- Data curation (sampling, labeling)
- Define data pipelines
- Handle storage and processing

### Step 3: ML Model Development
- Feature engineering
- Model training (the "fun" part)
- Initial experimentation

### Step 4: Deployment
- Make models available to users
- Online or batch prediction
- Handle inference infrastructure

### Step 5: Monitoring & Continual Learning
- Monitor performance in production
- Ensure system remains reliable, scalable, maintainable, adaptable
- Retrain and update models

### Step 6: Business Analysis
- Evaluate model performance against business goals
- Generate new business insights
- Inform next iteration

### Iteration Examples

**Example 1:** After examining data, you realize it's impossible to get the data needed → Frame the problem differently.

**Example 2:** After training, you realize you need more data or re-labeling → Go back to data engineering.

**Example 3:** After serving, user behavior differs from assumptions → Update the model.

---

## 4. Mind vs Data: The Great Debate

### Model-Centric Approach ("Mind")
**Focus:** Spending time researching inductive bias and architectural designs
- Better algorithms
- Clever architectures
- Domain knowledge in model design

**Advocates:** Traditional ML researchers, those who believe in "intelligent design"

### Data-Centric Approach ("Data")
**Focus:** Getting more data and computation
- Larger datasets
- More compute
- Let the model learn patterns from data

**Advocates:** Modern deep learning practitioners, Sutton's "Bitter Lesson"

### The Evidence
**Success stories supporting data-centric:**
- **AlexNet (2012):** Showed power of large data + GPUs
- **BERT (2018):** Pre-trained on massive text corpora
- **GPT series:** Scaling laws show performance improves with data

### Key Insight
> "The progress of ML in the last decade relies on having access to a large amount of data."

### Practical Implications
1. **Start simple:** Use simple models with good data
2. **Data quality > model complexity:** Clean data beats fancy algorithms
3. **Invest in data infrastructure:** Data collection, labeling, pipelines
4. **Don't neglect either:** Both matter, but data is often the bottleneck

### Interview Questions
- "What's more important: better algorithms or more data?"
- "When would you prioritize model architecture over data collection?"
- "How do you decide between a complex model with less data vs simple model with more data?"

---

## Interview Questions Summary

### Conceptual Questions

1. **Why do companies care about business metrics more than ML metrics?**
   - Business metrics tie directly to revenue/impact
   - ML metrics are proxies, not guarantees of business value
   - A/B testing with business metrics validates real impact

2. **Explain the four requirements for ML systems.**
   - **Reliability:** Works correctly despite failures
   - **Scalability:** Handles growing demand
   - **Maintainability:** Multiple people can work on it
   - **Adaptability:** Evolves with changing data/objectives

3. **Why is ML system development iterative?**
   - Discoveries in later stages inform earlier stages
   - Data availability affects problem framing
   - User behavior differs from training assumptions
   - Business objectives change over time

4. **Compare model-centric vs data-centric approaches.**
   - Model-centric: Focus on algorithms, architectures
   - Data-centric: Focus on data quantity and quality
   - Modern ML success often comes from data + compute
   - Both matter, but data is often the bottleneck

### Design Questions

5. **"Design a recommendation system for Netflix. How do you align ML and business objectives?"**
   - Business: Maximize watch time, subscriber retention
   - ML proxy: Click-through rate, completion rate
   - Decouple: Separate models for engagement vs diversity
   - Measure: A/B test with actual revenue/retention metrics

6. **"How would you make an ML system reliable?"**
   - Monitor predictions, not just uptime
   - Detect silent failures (prediction drift)
   - Have rollback mechanisms
   - Use shadow deployment for testing

7. **"Your model performance degrades over time. What do you do?"**
   - Check for data drift (Chapter 8)
   - Monitor feature distributions
   - Set up automated retraining
   - Ensure adaptability in system design

---

## Key Takeaways

1. **Business drives ML:** ML metrics are proxies; business metrics matter
2. **Decouple objectives:** Separate models for different objectives
3. **Four requirements:** Reliability, scalability, maintainability, adaptability
4. **Iterative process:** ML development is cyclical, not linear
5. **Data > Algorithms:** Modern ML success comes from data + compute
6. **Start holistic:** Consider deployment and maintenance from day one

---

## Related Chapters
- **Chapter 1:** Overview of ML Systems (real-world use cases)
- **Chapter 3:** Data Engineering Fundamentals
- **Chapter 8:** Data Distribution Shifts and Monitoring (reliability)
- **Chapter 9:** Continual Learning and Test in Production (adaptability)
- **Chapter 10:** Infrastructure and Tooling (scalability, maintainability)

---

**Source:** Chip Huyen, "Designing Machine Learning Systems" (O'Reilly, 2022)  
**Chapter 2 Summary compiled from:**
- GitHub: chiphuyen/dmls-book
- Lucas Cruz blog summary
- O'Reilly book preview
