## Why

Priority commands in the agent loop (such as `/status`) are currently "session-blind," meaning they are dispatched with a null session context. This causes them to ignore session-specific model overrides, leading to incorrect reporting of the active LLM model.

## What Changes

- Modify `AgentLoop.run()` to resolve the session using `self.sessions.get(msg.session_key)` before creating the `CommandContext` for priority commands.
- Ensure `CommandContext` for priority commands is populated with the resolved session instead of `None`.
- Update priority command handlers to rely on the context session for metadata resolution.

## Capabilities

### New Capabilities
- `unified-session-resolution`: Ensure that all command types (priority and standard) have consistent access to session-specific metadata and overrides.

### Modified Capabilities
- None

## Impact

- `nanobot/agent/loop.py`: Changes to the `run()` method for priority command dispatch.
- `nanobot/command/builtin.py`: Simplification of session retrieval in handlers like `cmd_status`.
