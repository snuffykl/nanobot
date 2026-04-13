## 1. Core Implementation

- [x] 1.1 Update `AgentLoop.run()` in `nanobot/agent/loop.py` to resolve the session using `self.sessions.get(msg.session_key)` before creating the `CommandContext` for priority commands.
- [x] 1.2 Update the `CommandContext` instantiation in `AgentLoop.run()` to pass the resolved session instead of `None`.

## 2. Command Handler Cleanup

- [x] 2.1 Update `cmd_status` in `nanobot/command/builtin.py` to rely on `ctx.session` directly instead of using the `ctx.session or loop.sessions.get_or_create(ctx.key)` rescue logic.
- [x] 2.2 Audit other priority command handlers for similar rescue logic and simplify them to use `ctx.session`.

## 3. Verification

- [x] 3.1 Verify that `/status` correctly reports the session-specific model override when a session exists.
- [x] 3.2 Verify that `/status` correctly reports the global default model when no session exists.
- [x] 3.3 Verify that no new empty session files are created on disk when executing read-only priority commands (like `/status` or `/help`) for a new session key.
