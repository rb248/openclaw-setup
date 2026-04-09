# CV Writer Agent - Heartbeat Reminders

Daily reminder at 5:30 PM for CV review and tailoring.

## Reminder Schedule

**5:30 PM Daily** - CV Review & Tailoring Time

## State Tracking

Read/Write: `~/agents/cv-writer/workspace/heartbeat-state.json`

```json
{
  "lastReminders": {
    "cv": "2026-04-05T17:30:00Z"
  },
  "lastCVUpdate": "2026-04-05T10:00:00Z"
}
```

## Heartbeat Logic

### 5:30 PM CV Reminder

```
IF current time >= 17:30
   AND lastReminders.cv date < today:
   
   Check recent activity:
   - Files modified in ~/awesome-cv/ today?
   - Any pending applications from job-search?
   
   Send reminder:
   "✍️ CV Writer Check-in (5:30 PM)
   
   📝 Evening CV Tasks:
   • Review today's applications
   • Tailor CVs for tomorrow's targets
   • Update base resume if needed
   
   📁 Active Files:
   - Base CV: ~/awesome-cv/rb-resume.tex
   - Cover Letter: ~/awesome-cv/rb-cover-letter.tex
   
   💡 Need Help?
   Send me a job description and I'll create a tailored CV!
   
   What would you like to work on?"
   
   Update: lastReminders.cv = now
   Save: heartbeat-state.json
```

## Output

Send reminder message to user.
If already reminded today: Reply `HEARTBEAT_OK`
