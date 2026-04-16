# Technical Patterns: nanobot

## 1. The Golden Paths (Standard Implementation Workflows)
To maintain the "ultra-lightweight" nature of nanobot, follow these established patterns for adding new capabilities.

### Adding a New Tool
1. **Define the Tool**: Create a class in `nanobot/agent/tools/` (or within a skill directory).
2. **Registration**: 
   - For built-in tools: Register in `AgentLoop._register_default_tools`.
   - For custom skills: Add the tool to the skill's loading logic so `SkillsLoader` can pick it up.
3. **Interface**: Ensure the tool accepts `workspace` and `allowed_dir` for security boundaries.

### Adding a New LLM Provider
1. **Registry Update**: Add a new `ProviderSpec` entry to `nanobot/providers/registry.py`.
2. **Schema Update**: Add the corresponding provider field to `ProvidersConfig` in `nanobot/config/schema.py`.
3. **Backend Mapping**: Map the provider to one of the existing backends (`openai_compat`, `anthropic`, `azure_openai`, etc.) or implement a new backend if a unique API protocol is required.

### Adding a New Chat Channel
1. **Implementation**: Create a new module in `nanobot/channels/`.
2. **Gateway Integration**: Ensure the channel can be enabled via `config.json` and supports the `send()` interface.
3. **Event Mapping**: Map platform-specific events (webhooks, polling) into the unified `InboundMessage` format.

## 2. Coding Standards & Principles

### Asynchronous Architecture
- **Async-First**: The core loop (`AgentLoop`), runner (`AgentRunner`), and bus (`MessageBus`) are all `async`. Never use blocking I/O in these paths; use `asyncio` or wrap blocking calls in `run_in_executor`.
- **Non-Blocking Dispatch**: Use the `MessageBus` to decouple the receipt of a message from its processing.

### Lightweight Design
- **Composition over Inheritance**: Favor small, focused classes (e.g., `AgentHook`) that can be composed rather than deep inheritance hierarchies.
- **YAGNI**: Do not implement "generic" abstractions for future use cases. Build for the current requirement and refactor only when a pattern emerges.
- **Minimal Dependencies**: Keep the core footprint small. Avoid adding heavy libraries if a lightweight native implementation exists.

### Type Safety
- **Strict Hinting**: Use Python 3.11+ type annotations throughout. Use `from __future__ import annotations` and `TYPE_CHECKING` blocks to avoid circular imports.

## 3. Persistence & State Management

### Session State
- Use `SessionManager` for all conversation-specific state.
- Avoid global variables. State should be stored in `Session.metadata` or passed via `AgentHookContext`.

### Durable Memory
- All long-term knowledge must be stored in Markdown files (`SOUL.md`, `USER.md`, `MEMORY.md`) to remain human-readable and agent-editable.
- Changes to durable memory should ideally be managed by the `Dream` process to ensure coherence.

## 4. Error Handling & Logging
- **Structured Logging**: Use `loguru` for all logs. Use `logger.debug` for trace-level info and `logger.warning/error` for failures.
- **Graceful Degradation**: Provider failures should be caught at the `AgentRunner` level with appropriate retry logic, ensuring the user receives a clear error message instead of a traceback.
