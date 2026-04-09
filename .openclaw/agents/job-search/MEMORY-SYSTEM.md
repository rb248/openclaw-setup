# Job Search Agent - Memory & Deduplication System

## The Problem
Without memory, the agent shows the same jobs repeatedly, wasting time and creating noise.

## The Solution
Track seen jobs in a memory file and filter duplicates before reporting.

## Memory File Structure

File: `~/agents/job-search/workspace/job-memory.json`

```json
{
  "schema": "job-memory-v1",
  "lastUpdated": "2026-04-04T23:00:00Z",
  "jobs": {
    "amazon-aachen-ml-engineer-2026-04-01": {
      "company": "Amazon",
      "title": "Machine Learning Engineer",
      "location": "Aachen",
      "firstSeen": "2026-04-01T09:00:00Z",
      "source": "LinkedIn",
      "url": "https://...",
      "status": "new",
      "lastChecked": "2026-04-04T09:00:00Z"
    },
    "rwth-ika-phd-autonomous-driving-2026-03-28": {
      "company": "RWTH IKA",
      "title": "PhD Position - Autonomous Driving",
      "location": "Aachen",
      "firstSeen": "2026-03-28T09:00:00Z",
      "source": "RWTH Jobs Portal",
      "url": "https://...",
      "status": "applied",
      "appliedDate": "2026-03-30T14:00:00Z",
      "lastChecked": "2026-04-04T09:00:00Z"
    }
  },
  "stats": {
    "totalSeen": 45,
    "newThisWeek": 12,
    "applied": 8,
    "rejected": 2,
    "interview": 1
  }
}
```

## Job ID Generation
Create unique IDs from: `{company}-{title}-{location}-{date-posted}`
Sanitized: lowercase, alphanumeric only, truncated to 50 chars each field.

## Status Tracking
- `new` - First time seen
- `viewed` - Reviewed but not applied
- `applied` - Application submitted
- `interview` - In interview process
- `rejected` - Application rejected
- `offer` - Job offer received
- `declined` - Declined by RB
- `expired` - Job posting closed/old

## Deduplication Workflow

### Daily Search Routine:
1. **Load Memory** - Read `job-memory.json`
2. **Search** - Query job platforms for new postings
3. **Filter** - For each job found:
   - Generate job ID
   - Check if ID exists in memory
   - If exists: Update `lastChecked` timestamp, skip reporting
   - If new: Add to memory with `status: new`, report it
4. **Report** - Only output NEW jobs not seen before
5. **Save** - Write updated memory back to file

### Weekly Cleanup:
- Mark jobs older than 60 days as `expired`
- Archive expired jobs to `job-archive.json`
- Keep last 90 days in active memory

## Smart Duplicate Detection

Even with different URLs, same job might appear on multiple platforms:

**Fuzzy matching criteria:**
- Same company + similar title (80% match) + same location = duplicate
- Example: "ML Engineer" on LinkedIn = "Machine Learning Engineer" on Indeed

**Implementation:**
```
For each new job:
  1. Check exact ID match (fast)
  2. If no exact match, check fuzzy match:
     - Same company (case-insensitive)
     - Location matches
     - Title similarity > 80% (using Levenshtein or simple word overlap)
  3. If fuzzy match found, merge sources, keep earliest firstSeen
```

## Application Tracking Integration

When RB applies to a job:
1. Update job status in memory: `applied`
2. Add `appliedDate` and `applicationMethod`
3. Optional: Track follow-up dates

Manual update command:
```bash
# RB or agent can update status
# This updates job-memory.json
```

## Reporting Enhancements

### Daily Report Shows:
- **NEW JOBS** (today): Jobs never seen before
- **STILL OPEN** (this week): Jobs seen before but still active
- **APPLIED**: Your application status tracking

### Weekly Report Shows:
- New opportunities this week
- Jobs you should follow up on (applied 7+ days ago)
- Trending companies (posting multiple roles)
- Market insights (salary ranges, hot skills)

## Memory Maintenance

### Auto-Cleanup (Weekly):
- Jobs with `status: expired` → Archive
- Jobs older than 90 days → Archive
- Jobs with `status: rejected` and 30+ days old → Archive

### Manual Cleanup:
```bash
# View memory stats
openclaw ask --agent job-search "Show me my job search memory stats"

# Mark job as applied
openclaw ask --agent job-search "I applied to the Amazon ML Engineer job, update status"

# Archive old jobs
openclaw ask --agent job-search "Archive all jobs older than 60 days"
```

## Implementation in Agent Prompt

The agent should:
1. ALWAYS read `job-memory.json` before searching
2. Generate job IDs for every found job
3. Compare against memory before adding to report
4. Update memory with new jobs + timestamps
5. Save memory after every search
6. Include "previously seen" count in report

## Example Output With Memory

```
## Daily Job Search Report - April 4, 2026

**NEW OPPORTUNITIES (3)** 🎉
1. Google - ML Engineer - Munich (Posted today)
   [First time seen]
   
2. SAP - Data Scientist - Walldorf (Posted yesterday)
   [First time seen]
   
3. BMW - PhD Autonomous Driving - Munich (Posted 2 days ago)
   [First time seen]

**STILL ACTIVE (12)** ⏰
(Seen in previous searches, still accepting applications)
- Amazon - ML Engineer - Aachen (First seen: Apr 1)
- RWTH IKA - Research Assistant - Aachen (First seen: Mar 28)
...

**YOUR PIPELINE** 📊
- Applied: 8
- Interview: 1 (SAP - scheduled Apr 10)
- Rejected: 2
- New to review: 3

**MEMORY STATS**
- Total jobs tracked: 45
- Seen this week: 12
- Filtered as duplicates today: 7
```

## Benefits

✅ **No duplicates** - Same job won't appear multiple times
✅ **Progress tracking** - Know where you stand with each opportunity
✅ **Pipeline visibility** - See full application funnel
✅ **Time savings** - Focus only on new opportunities
✅ **Insights** - Track which companies post frequently
✅ **Follow-up reminders** - Don't miss follow-ups

## Files

- `~/agents/job-search/workspace/job-memory.json` - Active job tracking
- `~/agents/job-search/workspace/job-archive.json` - Archived/old jobs
- `~/agents/job-search/workspace/daily-results.md` - Today's new jobs only
- `~/agents/job-search/workspace/pipeline-status.md` - Your application pipeline

## Agent Update Required

Modify the job-search agent's AGENTS.md to include:
- "Always check job-memory.json before reporting"
- "Generate job IDs and deduplicate"
- "Update memory after each search"
- "Track application status when provided"
