# Job Search Agent - Heartbeat Reminders

Run these checks every ~30 minutes via heartbeat.

## Reminder Schedule

| Time | Task | Description |
|------|------|-------------|
| **3:00 PM** | LinkedIn Research | Reminder to research/create LinkedIn post content |
| **5:00 PM** | Job Search | Reminder to review jobs and apply |
| **5:30 PM** | CV Review | Reminder to update/tailor CV for applications |

## State Tracking

Read/Write: `~/agents/job-search/workspace/heartbeat-state.json`

```json
{
  "lastReminders": {
    "linkedin": "2026-04-05T15:00:00Z",
    "jobsearch": "2026-04-05T17:00:00Z",
    "cv": "2026-04-05T17:30:00Z"
  },
  "lastJobSearch": "2026-04-05T09:00:00Z"
}
```

## Heartbeat Logic

### Step 1: Check Time & State
```
Current time: Check now
Current date: Today (YYYY-MM-DD)

Check if reminders already sent today:
- Read heartbeat-state.json
- Compare lastReminders.{task} date with today
```

### Step 2: Trigger Reminders

**LinkedIn Research (3:00 PM)**
```
IF current time >= 15:00 
   AND lastReminders.linkedin date < today:
   
   Send reminder:
   "📱 LinkedIn Time! (3:00 PM)
   
   Research ideas for today's post:
   - Technical lesson learned?
   - Project milestone to share?
   - Industry trend to comment on?
   
   Check content calendar: ~/linkedin-content-calendar.md"
   
   Update: lastReminders.linkedin = now
   Save: heartbeat-state.json
```

**Job Search (5:00 PM)**
```
IF current time >= 17:00
   AND lastReminders.jobsearch date < today:
   
   Load job-stats.json
   Load job-lookup.json
   
   Count:
   - New jobs today
   - Jobs in pipeline
   - High priority jobs
   
   Send reminder:
   "🔍 Job Search Time! (5:00 PM)
   
   📊 Your Pipeline:
   - New jobs to review: X
   - Applied (waiting): Y
   - Interviews: Z
   
   🎯 Today's Actions:
   - Review new jobs in ~/daily-results.md
   - Apply to high-priority positions
   - Follow up on pending applications
   
   💡 High Priority:
   [List top 2-3 jobs from highPriorityJobs]"
   
   Update: lastReminders.jobsearch = now
   Save: heartbeat-state.json
```

**CV Review (5:30 PM)**
```
IF current time >= 17:30
   AND lastReminders.cv date < today:
   
   Check job-stats.json for:
   - Jobs applied today
   - Jobs needing tailored CVs
   
   Send reminder:
   "✍️ CV Review Time! (5:30 PM)
   
   📝 Today's Tasks:
   - Review CVs sent today
   - Tailor CV for tomorrow's applications
   - Update ~/awesome-cv/rb-resume.tex if needed
   
   🎯 Focus:
   - ATS keywords for German market
   - Quantified achievements
   - Skills alignment
   
   Need a custom CV? Ask me!"
   
   Update: lastReminders.cv = now
   Save: heartbeat-state.json
```

### Step 3: Save State
Always save updated timestamps to prevent duplicate reminders.

## Reminder Content Examples

### LinkedIn (3 PM)
```
💼 LinkedIn Content Time!

Ideas for today:
• Share a technical win from this week
• Comment on an industry trend
• Post a resource that helped you
• Ask your network a question

Templates ready in: ~/linkedin-content-calendar.md

What would you like to post about?
```

### Job Search (5 PM)
```
🔍 Evening Job Search Check!

Today's Stats:
├─ New jobs found: 0
├─ Still active: 15
├─ Your pipeline: 0 applied, 0 interview
└─ High priority: 2

🎯 Recommended Actions:
1. Review DeepL ML Engineer (Cologne) - Fit: 5/5
2. Review Cognex Principal Engineer (Aachen) - Fit: 5/5
3. Apply to 1-2 positions before end of day

Need help with applications?
```

### CV Review (5:30 PM)
```
✍️ CV Tailoring Time!

Perfect time to:
✓ Review today's applications
✓ Prepare CVs for tomorrow
✓ Update your base resume

Active CVs: ~/awesome-cv/
Latest version: rb-resume.tex

Want me to create a tailored CV for a specific job?
```

## Workflow

1. **Read state file** (if exists)
2. **Check current time**
3. **Compare with reminder schedule**
4. **Send reminder if due and not sent today**
5. **Update state file**
6. **End heartbeat**

## Files to Access

- `~/agents/job-search/workspace/heartbeat-state.json` - Reminder tracking
- `~/agents/job-search/workspace/job-stats.json` - Pipeline stats
- `~/agents/job-search/workspace/job-lookup.json` - Job list
- `~/agents/job-search/workspace/high-priority-jobs.md` - Priority list
- `~/linkedin-content-calendar.md` - Content templates
- `~/awesome-cv/rb-resume.tex` - Base CV

## Output

Send reminder as message to user.
If nothing to remind: Reply `HEARTBEAT_OK`

## Example Heartbeat Flow

**2:45 PM heartbeat:**
```
Time: 14:45
Check: 14:45 < 15:00 → No LinkedIn reminder
Check: 14:45 < 17:00 → No job search reminder
Check: 14:45 < 17:30 → No CV reminder
Result: HEARTBEAT_OK
```

**3:15 PM heartbeat:**
```
Time: 15:15
Check: 15:15 >= 15:00 ✓
Check: lastReminders.linkedin < today ✓
Action: Send LinkedIn reminder
Update: lastReminders.linkedin = 15:15
Result: Reminder sent!
```

**3:45 PM heartbeat:**
```
Time: 15:45
Check: 15:45 >= 15:00 ✓
Check: lastReminders.linkedin = today ✗ (already sent)
Result: HEARTBEAT_OK
```

**5:15 PM heartbeat:**
```
Time: 17:15
Check: 17:15 >= 17:00 ✓
Check: lastReminders.jobsearch < today ✓
Action: Send job search reminder
Update: lastReminders.jobsearch = 17:15
Result: Reminder sent!
```

This ensures reminders are sent ONCE per day at the scheduled time.
