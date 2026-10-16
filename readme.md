# AI Security Assurance Lab

I wanted to learn how AI systems actually get attacked, and how to defend them, so I built a small fake company's AI tools and then tried to break them.

The "company" has three AI systems: a customer support chatbot, a document-search assistant, and a team of AI agents that handle support requests. I attacked each one, fixed what broke, and re-tested to prove the fixes worked. Everything runs locally with free, open-source tools (Ollama, Garak, PyRIT, ChromaDB, sentence-transformers).

> All company data in `docs/` is made up for testing, including the "CONFIDENTIAL" files.

## What I did

- Attacked a chatbot with prompt injection and jailbreaks to see if it would leak a secret (using Garak and PyRIT)
- Secured a document-search (RAG) system so users can't see documents they're not allowed to, even with tricky prompts
- Built a multi-agent system and tested whether one agent could trick or impersonate another
- Mapped every issue to the OWASP LLM Top 10 and MITRE ATLAS
- Wrote detection rules and an incident response playbook
- Followed one issue all the way through: attack → logged the risk → added a fix → re-tested → closed

## The three systems

**1. Support chatbot** (`chatbot.py`)
A bank support assistant with a fake secret (`INTERNAL_API_KEY`) hidden in it. The test: can someone trick it into revealing the secret?

**2. Document-search assistant** (`ingest.py`, `query.py`)
Searches a mix of normal and confidential documents. Access is checked when documents are retrieved (`employee` vs `hr`), not just by telling the AI "don't share this", because instructions alone can be bypassed.

**3. Multi-agent system** (`agents.py`, `tools.py`)
A Router agent reads each request and passes it to a Ticketing, Inventory or Escalation agent. Each agent has its own permissions, and agents must prove who they are with a session token before another agent will trust them.

Every security event is written to `security_events.jsonl` by `logger.py`, and `analyze.py` reads that log to spot attacks.

## What I found

| # | Issue | System | Severity | Status |
|---|---|---|---|---|
| R1 | A prompt disguised as a "policy" made the document assistant make up fake citations | 2 | Medium | Fixed & re-tested |
| R2 | One agent tried to inject instructions into the Inventory agent | 3 | High (attempted) | Blocked by existing checks |
| R3 | Faking the `sender` field let anyone pose as another agent and get real inventory data | 3 | Critical | **Fixed & re-tested** |
| R4 | A malicious instruction hidden inside ticket text could be followed later | 3 | Low (not exploited yet) | Documented |

**R3 was the most serious.** Agents trusted each other based only on a name in the message, so I added session-token checks between agents, then re-ran the attack to confirm it was blocked.

## How to run it

1. Install [Ollama](https://ollama.com) and download the model:
   ```bash
   ollama pull llama3.1:8b
   ```
2. Install the Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run each system:
   ```bash
   python chatbot.py                       # 1. support chatbot
   python ingest.py && python query.py     # 2. document search
   python agents.py                        # 3. multi-agent system
   python analyze.py                       # read the security log
   ```

## What I built vs. what the tools did

- **I built:** the chatbot, the document-search pipeline, the multi-agent system and its permission and token checks, all the attack scripts, the logging, the risk register and the traceability mapping.
- **Existing tools:** Garak and PyRIT for automated vulnerability scanning; ChromaDB and sentence-transformers for document search.
