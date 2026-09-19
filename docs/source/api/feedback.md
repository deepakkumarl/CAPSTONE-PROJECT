# `POST /feedback` — User Feedback Endpoint

Records technician user feedback (thumbs up/down ratings and optional comments) for RAG generated responses.

## HTTP Request
`POST /feedback`

## Request Model (`FeedbackRequest`)

| Field | Type | Required | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| `query` | String | Yes | Original technician question | `"What should be checked when an EV reports repeated battery overheating?"` |
| `answer` | String | Yes | Grounded answer text | `"Check coolant pump V54..."` |
| `helpful` | Boolean | Yes | `true` for 👍, `false` for 👎 | `true` |
| `reason` | String | No | Category/reason string | `"Accurate diagnostic steps"` |
| `comments` | String | No | Additional comments | `"Clear instructions."` |

## Response Model (`FeedbackResponse`)
```json
{
  "status": "success",
  "message": "Feedback recorded successfully."
}
```

## Storage Location
Feedback records are saved locally in `data/feedback.json`.

## Example `curl` Command
```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What should be checked when an EV reports repeated battery overheating?",
    "answer": "Check coolant pump V54...",
    "helpful": true,
    "reason": "Accurate diagnostic steps"
  }'
```
