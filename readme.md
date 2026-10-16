# AI Security Assurance Lab

I wanted to learn how AI systems actually get attacked, and how to defend them, so I built a small fake company's AI tools and then tried to break them.

The "company" has three AI systems: a customer support chatbot, a document-search assistant, and a team of AI agents that handle support requests. I attacked each one, fixed what broke, and re-tested to prove the fixes worked. Everything runs locally with free, open-source tools (Ollama, Garak, PyRIT, ChromaDB, sentence-transformers).

## What this project demonstrates

- Red-teaming an LLM chatbot for prompt injection, jailbreaks, and data leakage (Garak, PyRIT)
- Securing a RAG (retrieval-augmented generation) system against indirect prompt injection and cross-tenant data leakage
- Designing and attacking a multi-agent system (router + ticketing + inventory + escalation agents), including agent-to-agent trust attacks
- Mapping every finding to OWASP LLM Top 10 and MITRE ATLAS
- Building detection rules and an incident response playbook
- Tracing one finding end-to-end: attack -> risk register -> control -> evidence -> fix -> retest -> closed

## Architecture

**Target 1 - Support chatbot** (`chatbot.py`): a FinTrust Bank customer support assistant with a planted fake secret (`INTERNAL_API_KEY`), used to test whether prompt injection and jailbreak attempts could extract it.

**Target 2 - RAG assistant** (`ingest.py`, `query.py`): a document-search system over a mix of general and confidential company documents, with role-based access control (`employee` vs `hr`) enforced at retrieval time, not just in the prompt.

**Target 3 - Multi-agent system** (`agents.py`, `tools.py`): a Router Agent that classifies incoming requests and hands them to one of three specialist agents (Ticketing, Inventory, Escalation), each with its own role-based permissions and session-token verification between agents.

## Key findings

| # | Finding | Module | Severity | Status |
|---|---|---|---|---|
| R1 | Subtle "policy-framed" prompt injection caused the RAG assistant to fabricate document citations | B | Medium | Fixed & retested |
| R2 | Cross-agent injection attempt against the Inventory Agent | C | High (attempted) | Blocked by existing role + untrusted-data checks |
| R3 | Agent impersonation — a forged `sender` field returned real inventory data with no identity verification | C | Critical | **Fixed & retested** (see traceability diagram) |
| R4 | Confused deputy — a malicious instruction embedded in ticket content, no active exploit yet but a real latent attack surface | C | Low (latent) | Identified, documented |

## What I built vs. what the tools did

- **Built myself:** the chatbot, RAG pipeline, multi-agent system and its permission/token logic, all attack scripts, the logging and analysis layer, the risk register and traceability mapping.
- **Used existing tools:** Garak and PyRIT for automated LLM vulnerability scanning (Module A), ChromaDB and sentence-transformers for the RAG vector store (Module B).

## How to run it

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install requests garak pyrit chromadb sentence-transformers pandas

ollama pull llama3.1:8b
ollama serve  # in a separate terminal

python chatbot.py      
python ingest.py        
python query.py        
python agents.py        
python analyze.py      
```
