# Job ID Generation - CORRECTED

## The Critical Fix

**OLD (BUGGY):** Used search/report date
**NEW (CORRECT):** Use job's POSTED date from the listing

---

## ID Generation Formula

```
job_id = {company}-{title}-{location}-{posted_date}
```

Where `{posted_date}` = The date the job was ORIGINALLY POSTED (not today's date)

---

## Posted Date Extraction

### LinkedIn Examples

| Raw Text | Today's Date | Posted Date | Days Ago |
|----------|--------------|-------------|----------|
| "Posted 1 day ago" | 2026-04-05 | **2026-04-04** | 1 |
| "Posted 3 days ago" | 2026-04-05 | **2026-04-02** | 3 |
| "Posted 1 week ago" | 2026-04-05 | **2026-03-29** | 7 |
| "Posted 2 weeks ago" | 2026-04-05 | **2026-03-22** | 14 |
| "Posted 30+ days ago" | 2026-04-05 | **2026-03-01** | 35+ |

### Indeed Examples

| Raw Text | Posted Date |
|----------|-------------|
| "vor 2 Tagen" (German) | Today - 2 days |
| "vor 1 Woche" | Today - 7 days |
| "Posted Today" | Today |

### RWTH Jobs Portal

Usually shows exact date:
- "Publication date: 01.04.2026" → 2026-04-01
- "Posted: 2026-03-28" → 2026-03-28

### Company Career Pages

Look for:
- "Date posted:"
- "Published:"
- "Posted on:"
- Sometimes in metadata/JSON-LD

---

## Example Walkthrough

### Scenario: Job Found on Multiple Days

**Job:** DeepL - ML Engineer - Cologne
**Actually Posted:** April 1, 2026

**Day 1: April 1 Search**
```
Search finds: "Posted today"
Posted date: 2026-04-01
ID: deepl-ml-engineer-cologne-2026-04-01
Lookup check: NOT FOUND → NEW! ✅
Add to memory
Report: "NEW: DeepL ML Engineer"
```

**Day 2: April 2 Search**
```
Search finds: "Posted 1 day ago"  ← Same job!
Posted date: 2026-04-01  ← Still April 1!
ID: deepl-ml-engineer-cologne-2026-04-01  ← SAME ID!
Lookup check: FOUND! → DUPLICATE! ✅
Update timestamp only
Report: "No new jobs" (or "Still active: DeepL")
```

**Day 7: April 7 Search**
```
Search finds: "Posted 1 week ago"
Posted date: 2026-04-01
ID: deepl-ml-engineer-cologne-2026-04-01
Lookup check: FOUND! → DUPLICATE!
Update timestamp
Report: "Still active: DeepL (7 days old)"
```

**Result:** Job only appears as "NEW" once, then tracked as "still active"!

---

## Updated Agent Instructions

### CRITICAL RULE:

```markdown
## ID Generation Steps

1. **Extract posted date from job listing**
   - Look for: "Posted X days ago", "Date posted:", "Published:"
   - Calculate actual posted date: Today - days_ago
   - If exact date shown, use that directly

2. **Generate ID using POSTED date**
   ```
   job_id = {company}-{title}-{location}-{posted_date}
   ```
   NOT: {company}-{title}-{location}-{today}

3. **Check lookup**
   - If ID exists → DUPLICATE (same job seen before)
   - If ID new → NEW JOB

4. **For reposted jobs**
   - If same job appears with NEW posted date → Treat as NEW
   - This is correct: you want to see reposts!
```

---

## Handling Edge Cases

### Case 1: "Posted 30+ days ago"

```
Raw: "Posted 30+ days ago"
Calculate: Today - 30 = Posted date (approximate)
ID: company-title-location-2026-03-06

Issue: Could be 31, 32, 60 days old - same ID generated
Solution: Acceptable - job is old anyway, likely expired
Alternative: Use special ID suffix: "-old-2026-03"
```

### Case 2: No date shown

```
Some listings don't show date
Fallback: Use today's date, but flag for manual review
Add note: "Date uncertain - verify posting is current"
```

### Case 3: Job reposted by company

```
Original: Posted 2026-04-01, ID: ...-2026-04-01
Repost:   Posted 2026-04-15, ID: ...-2026-04-15  ← DIFFERENT!

Result: Shows as NEW
This is CORRECT: Company reposted = actively hiring = worth applying!
```

### Case 4: Different platforms, same posted date

```
LinkedIn: "Posted 2 days ago" (posted 2026-04-03)
Indeed:   "Posted 2 days ago" (posted 2026-04-03)

Same posted date → Same ID → Exact duplicate caught! ✅
```

---

## Token-Efficient Posted Date Storage

Instead of storing full dates in every ID, could use:
- Julian day: `deepl-ml-engineer-cologne-095` (day 95 of year)
- But full date is clearer and same token cost

Keep: `deepl-ml-engineer-cologne-2026-04-01`

---

## Validation Checklist

Before generating ID, verify:
- [ ] Posted date extracted from job listing (not today's date)
- [ ] Date format: YYYY-MM-DD
- [ ] If relative date ("2 days ago"), calculated correctly
- [ ] ID uses posted date in final segment

---

## Testing the Fix

### Test Case 1: Same job, different search days

```
Job: Amazon - ML Engineer - Aachen
Posted: April 1

Search April 1: ID = amazon-ml-engineer-aachen-2026-04-01 → NEW
Search April 2: ID = amazon-ml-engineer-aachen-2026-04-01 → DUPLICATE ✓
Search April 5: ID = amazon-ml-engineer-aachen-2026-04-01 → DUPLICATE ✓
```

### Test Case 2: Job reposted

```
Job: Google - Data Scientist - Munich
First posted: March 15
Reposted: April 1

Search March 15: ID = ...-2026-03-15 → NEW
Search April 1:  ID = ...-2026-04-01 → NEW (different date!)
Result: Shows twice - CORRECT! (actively hiring)
```

---

## Implementation Note

The agent must:
1. Parse "Posted X days ago" text
2. Calculate: Posted Date = Today - X days
3. Use calculated date in ID

Example calculation:
```python
today = "2026-04-05"
posted_text = "Posted 3 days ago"
days_ago = 3
posted_date = today - 3 days = "2026-04-02"

job_id = f"{company}-{title}-{location}-{posted_date}"
```

---

**This fix ensures jobs are only reported as NEW once, regardless of how many times you search!** ✅
