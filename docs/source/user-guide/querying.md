# Querying & Diagnostic Assistance

Technicians interact with the system through **Tab 1: Diagnostic Assistant**.

## Asking Diagnostic Questions

1. **Custom Input**: Type any technical question in the chat input bar (e.g., *"What checks should be performed on the battery cooling circuit?"*).
2. **Suggested Diagnostic Questions**: Click preset buttons for quick diagnostic routines:
   - EV Battery Overheating Checks
   - Charging System Faults
   - CP & PP Signal Verification
   - Battery Cooling Circuit Checks
   - HV Insulation Test Prerequisites

## Answer Display & Grounding Status

Every response includes:
- **Grounded Technical Answer**: Generated strictly from retrieved document context using Ollama `qwen2.5:1.5b`.
- **Grounding Badge**:
  - `Grounding: 🟢 HIGH`: Top retrieved source relevance score $\ge 0.60$.
  - `Grounding: 🟡 MEDIUM`: Top retrieved source relevance score $\in [0.35, 0.60)$.
  - `Grounding: 🔴 INSUFFICIENT`: No documents passed similarity threshold; anti-hallucination fallback returned.
- **Supporting Sources**: Expandable accordions displaying source metadata and relevance scores.
- **Feedback Buttons**: Thumbs up (👍) and thumbs down (👎) buttons allowing technicians to record quality feedback.

## Anti-Hallucination Fallback Behavior

If a query asks for information not present in the ingested BMW service manuals (e.g., *"How do I reset oil change light on a 1995 E36?"*), the system returns:

> *"I could not find sufficient information in the available BMW service documentation."*
