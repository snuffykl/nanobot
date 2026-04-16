# Context Map: nanobot

This document maps logical system components to their physical locations in the codebase. Use this map to quickly locate the relevant files for implementation or debugging.

## 🧠 Core Agent Engine
*Where the "thinking" and execution happen.*

| Component | File Path | Description |
| :--- | :--- | :--- |
| **Main Execution Loop** | `nanobot/agent/loop.py` | Coordinates the cycle of message $\rightarrow$ context $\rightarrow$ LLM $\rightarrow$ tools. |
| **LLM Runner** | `nanobot/agent/runner.py` | Handles the actual API calls and iterative tool-call loops. |
| **Context Assembly** | `nanobot/agent/context.py` | Assembles the final prompt (Identity, Memory, Skills). |
| **Subagent Management** | `nanobot/agent/subagent.py` | Logic for spawning and managing background agents. |
| **Agent Hooks** | `nanobot/agent/hook.py` | The interceptor system for observing/modifying the agent loop. |

## 💾 Memory & Session State
*Where the agent remembers and persists data.*

| Component | File Path | Description |
| :--- | :--- | :--- |
| **Layered Memory** | `nanobot/agent/memory.py` | Implementation of `Consolidator` and `Dream` (Long-term memory). |
| **Session Manager** | `nanobot/session/manager.py` | Handles session retrieval, persistence, and metadata. |
| **Session Model** | `nanobot/session/models.py` | The data structure for a conversation session. |
| **Memory Store** | `nanobot/agent/memory.py` | Low-level file I/O for `SOUL.md`, `USER.md`, and `MEMORY.md`. |

## 🔌 Extensibility & Plugins
*Where new capabilities are added.*

| Component | File Path | Description |
| :--- | :--- | :--- |
| **Provider Registry** | `nanobot/providers/registry.py` | The single source of truth for all supported LLM providers. |
| **Tool Registry** | `nanobot/agent/tools/registry.py` | Manages the discovery and registration of agent tools. |
| **Built-in Tools** | `nanobot/agent/tools/` | Implementations of shell, filesystem, web, and messaging tools. |
| **Channel Plugins** | `nanobot/channels/` | Individual implementations for Telegram, Discord, WeChat, etc. |
| **Skills Loader** | `nanobot/agent/skills.py` | Logic for loading custom skill directories into the agent. |

## ⚙️ Infrastructure & Configuration
*The plumbing that keeps the system running.*

| Component | File Path | Description |
| :--- | :--- | :--- |
| **Config Schema** | `nanobot/config/schema.py` | Pydantic models defining the `config.json` structure. |
| **Message Bus** | `nanobot/bus/` | Event-driven routing of `Inbound` and `Outbound` messages. |
| **Gateway** | `nanobot/gateway/` | Proxies channel events to the `MessageBus`. |
| **Cron/Heartbeat** | `nanobot/cron/` & `nanobot/heartbeat/` | Logic for scheduled tasks and proactive wake-ups. |
| **CLI Interface** | `nanobot/cli/` | Command-line entry points for `onboard`, `agent`, `status`, etc. |

## 🛠️ Key Files for SDD (Spec Driven Development)
When starting a new feature, check these files first:
- **Adding a Tool**: `nanobot/agent/tools/registry.py` $\rightarrow$ `nanobot/agent/loop.py`
- **Adding a Provider**: `nanobot/providers/registry.py` $\rightarrow$ `nanobot/config/schema.py`
- **Changing Context/Prompt**: `nanobot/agent/context.py`
- **Modifying Memory Flow**: `nanobot/agent/memory.py`
