# Optimized Job Search Memory Architecture

## Problem
Current workflow loads entire `job-memory.json` (~15 jobs × ~500 tokens = ~7500 tokens per search). At 100 jobs = ~50,000 tokens just for memory lookup!

## Solution: Multi-Tier Memory System

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  ACTIVE MEMORY (30 days) - Quick Access                      │
│  ├─ job-index.json (just IDs + timestamps)    ~200 tokens   │
│  └─ job-memory-active.json (full details)     ~2000 tokens  │
├─────────────────────────────────────────────────────────────┤
│  ARCHIVE (>30 days) - Load on demand                         │
│  └─ job-archive-YYYY-MM.json (monthly files)                │
├─────────────────────────────────────────────────────────────┤
│  LOOKUP INDEX - Tiny, always loaded                          │
│  └─ job-lookup.json (ID → file location map)  ~100 tokens   │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

### 1. **job-lookup.json** (Always Loaded - Tiny)
```json
{
  "schema": "lookup-v1",
  "totalJobs": 150,
  "lastUpdated": "2026-04-05T08:00:00Z",
  "index": {
    "amazon-ml-engineer-aachen-2026-04-01": {
      "file": "job-memory-active.json",
      "firstSeen": "2026-04-01T09:00:00Z",
      "status": "new"
    },
    "deepl-ml-engineer-cologne-2026-03-15": {
      "file": "job-archive-2026-03.json",
      "firstSeen": "2026-03-15T10:00:00Z",
      "status": "applied"
    }
  }
}
```
**Size**: ~100 tokens for 150 jobs (vs 50,000 for full memory)

### 2. **job-memory-active.json** (Last 30 Days)
Full details for recent jobs only.
```json
{
  "jobs": {
    "amazon-ml-engineer-aachen-2026-04-01": { ...full details... },
    "deepl-nlp-engineer-cologne-2026-04-02": { ...full details... }
  }
}
```
**Max size**: ~30 jobs × 500 tokens = ~15,000 tokens (constant!)

### 3. **job-archive-YYYY-MM.json** (Monthly Archives)
Old jobs, only loaded when needed.
- `job-archive-2026-03.json`
- `job-archive-2026-02.json`
- etc.

### 4. **job-stats.json** (Pipeline Stats - Separate)
```json
{
  "stats": {
    "totalSeen": 150,
    "newThisWeek": 3,
    "applied": 12,
    "interview": 2,
    "rejected": 3
  }
}
```

---

## Optimized Workflow

### Daily Search (Token-Efficient)

**Step 1: Load Lookup Index** (~100 tokens)
```
Read: job-lookup.json
```

**Step 2: Check Duplicates** (No additional tokens!)
```
For each new job found:
  - Generate job ID
  - Check if ID exists in lookup.index
  - If YES: It's a duplicate, skip
  - If NO: It's new, proceed
```

**Step 3: Load Active Memory** (only if new jobs found)
```
Read: job-memory-active.json (~2000 tokens max)
```

**Step 4: Update Files**
```
Write: job-lookup.json (append new entries)
Write: job-memory-active.json (append new jobs)
Write: job-stats.json (update counters)
```

**Total Token Usage**: ~2,100 tokens (vs 50,000+)

---

## Weekly Cleanup

**Archive Old Jobs (>30 days):**
1. Find jobs in active memory older than 30 days
2. Move to `job-archive-2026-03.json`
3. Update lookup index to point to archive file
4. Truncate active memory

**Result**: Active memory stays small (~30 jobs max)

---

## Smart Duplicate Detection (Enhanced)

### Two-Stage Check

**Stage 1: Exact Match (O(1) via lookup)**
```
job-id in lookup.index ? 
  YES → Duplicate
  NO  → Stage 2
```

**Stage 2: Fuzzy Match (Load only if needed)**
```
If many jobs from same company:
  Load only those company's jobs from active memory
  Check title similarity
```

---

## Implementation for Agent

### New AGENTS.md Instructions

```markdown
## 🔴 CRITICAL: Token-Efficient Memory System

### Step 1: Load Lookup Index (ALWAYS)
Read: ~/agents/job-search/workspace/job-lookup.json
- This is TINY (~100 tokens for 150 jobs)
- Contains all job IDs and their locations

### Step 2: Check for Duplicates (ZERO additional tokens)
For each job found during search:
  1. Generate job ID: {company}-{title}-{location}-{posted-date}
  2. Check: Does ID exist in lookup.index?
     - YES → Duplicate! Update timestamp in lookup, SKIP
     - NO  → New job! Proceed to Step 3

### Step 3: Load Active Memory (ONLY if new jobs found)
IF new jobs were found:
  Read: ~/agents/job-search/workspace/job-memory-active.json
  - Contains only last 30 days (~2000 tokens max)
  
### Step 4: Update All Files
Write updated files:
  1. job-lookup.json (append new entries)
  2. job-memory-active.json (append new jobs)
  3. job-stats.json (update counters)
  
### Step 5: Weekly Archive (Automatic)
Every Sunday:
  - Move jobs >30 days old to job-archive-YYYY-MM.json
  - Update lookup index
  - Keep active memory small

## Token Budget
- Lookup check: ~100 tokens (constant)
- Active memory: ~2000 tokens max (constant)
- Total per search: ~2100 tokens (vs 50,000+ in old system)
```

---

## Migration from Old System

### One-Time Conversion Script
```bash
#!/bin/bash
# migrate-memory.sh

# Read old job-memory.json
# Split into:
#   - job-lookup.json (extract just IDs + metadata)
#   - job-memory-active.json (last 30 days)
#   - job-archive-2026-03.json (older jobs)
#   - job-stats.json (extracted stats)
```

---

## Benefits

| Metric | Old System | New System | Improvement |
|--------|-----------|------------|-------------|
| **Token usage** | 50,000+ | ~2,100 | **24x reduction** |
| **Duplicate check speed** | O(n) scan | O(1) lookup | **Instant** |
| **Max memory loaded** | All jobs | Last 30 days | **Constant size** |
| **Scalability** | Degrades | Stable | **Handles 1000+ jobs** |

---

## File Sizes (Estimated)

| File | 50 Jobs | 200 Jobs | 1000 Jobs |
|------|---------|----------|-----------|
| job-lookup.json | ~50 tokens | ~200 tokens | ~800 tokens |
| job-memory-active.json | ~2000 tokens | ~2000 tokens | ~2000 tokens |
| **Total per search** | **~2100** | **~2200** | **~2800** |
| (Old system) | ~10,000 | ~40,000 | ~200,000 |

---

## Agent Tools Required

- `read` - For lookup, active memory, archives
- `write` - For updating files
- `edit` - For appending to JSON (or read→modify→write)

## Files to Create

1. `job-lookup.json` - Master index
2. `job-memory-active.json` - Recent jobs only
3. `job-archive-2026-04.json` - Monthly archives
4. `job-stats.json` - Pipeline statistics
5. `MEMORY-ARCHITECTURE.md` - This documentation
