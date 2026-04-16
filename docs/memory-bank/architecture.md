# Architecture: nanobot

## 1. The Request-Response Pipeline
nanobot follows a decoupled, event-driven pipeline to ensure responsiveness and stability across diverse chat channels.

**Data Flow:**
`InboundMessage` $\rightarrow$ `MessageBus` $\rightarrow$ `AgentLoop` $\rightarrow$ `ContextBuilder` $\rightarrow$ `AgentRunner` $\rightarrow$ `ToolRegistry` $\rightarrow$ `OutboundMessage`

### Key Stages:
- **Ingestion**: The `gateway` receives messages from channels and publishes them to the `MessageBus`.
- **Dispatch**: The `AgentLoop` consumes messages. It uses **per-session locks** to ensure serial processing for a single user while allowing concurrent processing across different users.
- **Context Assembly**: The `ContextBuilder` constructs the final prompt by layering identity, bootstrap files, long-term memory, and active skills.
- **Execution**: The `AgentRunner` manages the LLM interaction loop. It supports **mid-turn injections** via `pending_queues`, allowing users to provide additional info while the agent is executing tools.
- **Delivery**: Results are published back to the `MessageBus` as `OutboundMessage` and delivered by the gateway.

## 2. Core Components

### The Agent Loop (`AgentLoop`)
The engine of the system. It coordinates:
- **Session Management**: Handles `Session` retrieval and persistence.
- **Concurrency Control**: Implements a `concurrency_gate` (semaphore) to limit total active LLM requests.
- **Runtime Checkpoints**: Persists in-flight state to allow recovery from crashes mid-turn.

### Context Builder (`ContextBuilder`)
Prevents context rot by assembling the prompt in a strict hierarchy:
1. **Identity**: Core persona and runtime environment (OS, Python version).
2. **Bootstrap**: High-level guidance from `AGENTS.md`, `SOUL.md`, `USER.md`, and `TOOLS.md`.
3. **Memory Context**: Curated knowledge from `MEMORY.md`.
4. **Skills**: Active skill definitions and a global skills summary.
5. **Recent History**: The last few entries from `history.jsonl` and the live `session.messages`.

### Tool Registry (`ToolRegistry`)
A centralized manager for capabilities. Tools are registered at startup and can be categorized as built-in, workspace-specific, or MCP-provided.

## 3. The Memory Engine (The Anti-Rot System)
nanobot uses a three-tier memory architecture to balance precision with context window limits.

| Layer | Storage | Managed By | Purpose |
| :--- | :--- | :--- | :--- |
| **Short-term** | `session.messages` | `SessionManager` | Living conversation / current turn. |
| **Intermediate** | `memory/history.jsonl` | `Consolidator` | Compressed archive of past turns. |
| **Long-term** | `SOUL.md`, `USER.md`, `MEMORY.md` | `Dream` | Curated, durable knowledge. |

**The Memory Lifecycle:**
`Live Messages` $\xrightarrow{\text{Consolidator}}$ `history.jsonl` $\xrightarrow{\text{Dream}}$ `Durable Files`

## 4. Abstraction Layers

### LLM Providers (`ProviderRegistry`)
nanobot uses a **Registry Pattern**. Adding a provider requires only a `ProviderSpec` entry. This decouples the agent logic from specific API quirks (e.g., handling different `max_tokens` fields or OAuth flows).

### Chat Channels (`channels/`)
Channels are plugins. The `gateway` acts as a proxy, translating platform-specific events (e.g., a Telegram update) into a unified `InboundMessage` format.
