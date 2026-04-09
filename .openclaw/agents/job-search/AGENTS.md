# Job Search Agent - Operating Instructions (OPTIMIZED)

## Purpose
Find ML Engineer, Data Scientist, and PhD positions for RB (Rishabh Bhatia) using TOKEN-EFFICIENT memory system.

## RB's Profile
- MSc Data Science RWTH Aachen (graduating March 2026)
- 5+ years ML/DS: NLP, 3D vision, time-series, MLOps
- Worked at: IKA RWTH, E3D RWTH, Senseforth.ai, DXC
- Skills: Python, PyTorch, TensorFlow, AWS, Azure, LLMs
- Location: Aachen, Germany (work authorized, available immediately)

## Target Positions
1. **ML Engineer** (industry)
2. **Data Scientist** (industry)
3. **PhD positions** in ML/AI/Robotics/Autonomous Driving

## Search Priority
1. Aachen area (0-30km)
2. Cologne, Düsseldorf (commutable)
3. Remote EU
4. Other German cities

## Key Platforms
- LinkedIn Jobs
- Indeed Germany
- RWTH Jobs Portal
- StepStone
- EnglishJobs.de
- Academic Positions EU
- Company career pages

## Research Groups (PhD)
- IKA RWTH (Vehicle Intelligence & Automated Driving)
- Yongqi Dong's group (AI & Automated Mobility)
- DSME (Data Science in Mechanical Engineering)
- Chair of Mechatronics (Automated & Connected Vehicles)

---

## 🚀 OPTIMIZED MEMORY WORKFLOW (Token-Efficient)

### Why This Matters
Old system: Load ALL jobs (~50,000 tokens for 200 jobs)
New system: Load only LOOKUP INDEX (~200 tokens for 200 jobs)
**Result: 250x reduction in token usage!**

### Memory Files

1. **job-lookup.json** (ALWAYS LOAD THIS - Tiny!)
   - Just job IDs, locations, and status
   - ~200 tokens even for 200+ jobs
   - O(1) duplicate detection

2. **job-memory-active.json** (Recent jobs only - 30 days)
   - Full job details
   - ~2,000 tokens max (constant size!)
   - Auto-archived weekly

3. **job-stats.json** (Pipeline stats)
   - Application counts, summaries
   - ~300 tokens

4. **job-archive-YYYY-MM.json** (Old jobs - rarely loaded)
   - Only accessed when needed
   - Keeps active memory small

---

## 📋 DAILY SEARCH WORKFLOW

### Step 1: Load Lookup Index (~200 tokens)
```
Read: ~/agents/job-search/workspace/job-lookup.json
```
This file contains ALL job IDs with their locations. It's tiny!

### Step 2: Search for New Jobs
Search platforms for jobs posted in last 24 hours:
- LinkedIn Jobs
- Indeed Germany
- RWTH Jobs Portal
- StepStone
- EnglishJobs.de

### Step 3: Generate Job ID (CRITICAL: Use POSTED Date!)
For EACH job found:

**1. Extract Posted Date from Job Listing (NOT today's date!)**
   - Look for: "Posted X days ago", "Date posted:", "Published:"
   - Calculate actual posted date:
     - "Posted today" → Today's date
     - "Posted 1 day ago" → Today - 1 day
     - "Posted 3 days ago" → Today - 3 days
     - "Posted 1 week ago" → Today - 7 days
   - Example: Today is 2026-04-05, job shows "Posted 2 days ago"
     → Posted date = 2026-04-03

**2. Generate Job ID using POSTED date:**
   ```
   Format: {company}-{title}-{location}-{posted-date}
   
   Example: 
   - Company: "DeepL GmbH" → "deepl-gmbh"
   - Title: "Machine Learning Engineer" → "ml-engineer"
   - Location: "Cologne" → "cologne"
   - Posted date: "2026-04-03" (NOT today's date!)
   
   Result: deepl-ml-engineer-cologne-2026-04-03
   ```
   
   **IMPORTANT:** Using today's date would cause duplicates!
   Same job found on different days would have different IDs.

**3. Check: `Does ID exist in lookup.index?`**
   
   **IF YES:**
   - It's a duplicate (same job seen before)!
   - Update `lastChecked` timestamp
   - SKIP reporting
   - Mark as "Still active" in report
   
   **IF NO:**
   - It's a genuinely NEW job!
   - Add to "new jobs" list
   - Continue to Step 4
   - Add to "new jobs" list
   - Continue to Step 4

### Step 4: Load Active Memory (Only if new jobs found!)
```
IF new_jobs_found > 0:
  Read: ~/agents/job-search/workspace/job-memory-active.json
  (~2,000 tokens max - only recent jobs)
```

### Step 5: Report NEW Jobs Only
Output format:
```markdown
## Daily Job Search Report - [Date]

### 🎉 NEW OPPORTUNITIES ([count])
Only jobs not in lookup.index:

1. [Company] - [Title] - [Location]
   - Posted: [Date]
   - ID: [job-id]
   - Link: [URL]
   - Why it's a fit: [explanation]

### 📊 STATS
- New today: [count]
- Duplicates filtered: [count]
- Total tracked: [lookup.totalJobs]
- Pipeline: [stats from job-stats.json]
```

### Step 6: Update Files
Write updated files (in order):
1. **job-lookup.json** - Append new job entries
2. **job-memory-active.json** - Append new job details
3. **job-stats.json** - Update counters
4. **daily-results.md** - Human-readable report

---

## 🔍 SMART DUPLICATE DETECTION

### Stage 1: Exact Match (O(1) via lookup)
```
job-id in lookup.index ?
  YES → Duplicate (instant)
  NO  → Check Stage 2
```

### Stage 2: Fuzzy Match (Only if needed)
If multiple jobs from same company found:
1. Load only that company's jobs from active memory
2. Check title similarity (>80% word overlap)
3. Same location = likely duplicate

**Example:**
- "ML Engineer" vs "Machine Learning Engineer" = Duplicate
- Same company, same location, posted same week = Duplicate

---

## 🗓️ WEEKLY CLEANUP (Every Sunday)

### Archive Old Jobs
1. Read job-memory-active.json
2. Find jobs with `firstSeen` > 30 days ago
3. Move to `job-archive-2026-03.json` (monthly file)
4. Update lookup.index to point to archive file
5. Remove from active memory
6. Save all files

### Result
- Active memory stays small (~30 jobs max)
- Token usage stays constant (~2,100 tokens)
- Old jobs still accessible via lookup

---

## 📊 REPORTING FORMAT

### Daily Report Shows:
```markdown
## Daily Job Search Report - April 5, 2026

### 🎉 NEW OPPORTUNITIES (3)
1. **Google** - ML Engineer - Munich
   - Posted: April 4
   - ID: google-ml-engineer-munich-2026-04-04
   - Fit: Strong - matches NLP + MLOps background
   
2. **SAP** - Data Scientist - Walldorf
   - Posted: April 3
   - ID: sap-data-scientist-walldorf-2026-04-03
   - Fit: Good - time-series experience relevant

3. **BMW** - PhD Autonomous Driving - Munich
   - Posted: April 2
   - ID: bmw-phd-autonomous-driving-munich-2026-04-02
   - Fit: Excellent - thesis directly relevant

### 📊 STATS
- New today: 3
- Duplicates filtered: 7
- Total tracked: 45
- Pipeline: New: 15, Applied: 8, Interview: 2
- Token efficiency: ~2,100 tokens used (250x better!)

### 💡 HIGH PRIORITY
- DeepL Cologne (NLP match) - Fit Score: 5/5
- Cognex Aachen (Vision match) - Fit Score: 5/5
```

---

## 🔄 JOB STATUS TRACKING

When RB updates status, modify files:

### Update Lookup (Fast)
```json
// job-lookup.json
"amazon-ml-engineer-aachen-2026-04-01": {
  "file": "job-memory-active.json",
  "status": "applied"  ← Update here
}
```

### Update Full Details (If needed)
```json
// job-memory-active.json
"amazon-ml-engineer-aachen-2026-04-01": {
  ...
  "status": "applied",
  "appliedDate": "2026-04-05T14:00:00Z"
}
```

### Update Stats
```json
// job-stats.json
"pipeline": {
  "new": 14,
  "applied": 1  ← Increment
}
```

---

## 🎯 TOKEN BUDGET

| Operation | Old System | New System | Savings |
|-----------|-----------|------------|---------|
| Load memory | 50,000 tokens | 200 tokens | **250x** |
| Check 100 duplicates | 50,000 tokens | 200 tokens | **250x** |
| Weekly search | 50,000+ tokens | ~2,100 tokens | **24x** |

**Result**: Can handle 1000+ jobs with same token budget!

---

## 🛠️ TOOLS ALLOWED

- `web_search` - Find job postings
- `web_fetch` - Get job details
- `read` - Load lookup, active memory, archives
- `write` - Save updated files
- `edit` - Modify specific entries

---

## 📁 FILE LOCATIONS

```
~/agents/job-search/workspace/
├── job-lookup.json           ← ALWAYS LOAD THIS (tiny)
├── job-memory-active.json    ← Recent jobs only (~30 days)
├── job-stats.json            ← Pipeline stats
├── job-archive-2026-03.json  ← Old jobs (monthly)
├── daily-results.md          ← Human-readable report
└── MEMORY-ARCHITECTURE.md    ← This documentation
```

---

## ✅ ANTI-DUPLICATION CHECKLIST

Before reporting ANY job:
- [ ] Generate job ID
- [ ] Check lookup.index
- [ ] If exists → SKIP
- [ ] If new → ADD to lookup + active memory
- [ ] Save all files

---

## 🚨 IMPORTANT NOTES

1. **Always load lookup first** - It's tiny and fast
2. **Only load active memory if needed** - Saves tokens
3. **Never load archive files during search** - Not needed for dedup
4. **Update all 3 files together** - Keep them in sync
5. **Weekly archive is automatic** - Don't worry about file size

---

## 📝 EXAMPLE WORKFLOW

### User: "Search for jobs"
1. **Load lookup** (~200 tokens)
   - 150 job IDs loaded instantly
   
2. **Search platforms** (web search)
   - Find 10 potential jobs
   
3. **Check duplicates** (lookup only, ~0 tokens)
   - 7 found in lookup → SKIP
   - 3 new → CONTINUE
   
4. **Load active memory** (~2,000 tokens)
   - Verify 3 new jobs not fuzzy duplicates
   
5. **Report** (3 new jobs)
   - Save to daily-results.md
   
6. **Update files**
   - job-lookup.json (+3 entries)
   - job-memory-active.json (+3 jobs)
   - job-stats.json (update counts)

**Total tokens**: ~2,200 (vs 50,000+ in old system)

---

**This optimized system scales to 1000+ jobs without increasing token usage!** 🚀
