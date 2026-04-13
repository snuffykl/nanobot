## Context

Currently, the `AgentLoop` handles priority commands (e.g., `/status`, `/stop`) separately from standard messages. Priority commands are dispatched in `AgentLoop.run()` with a `CommandContext` where `session` is explicitly set to `None`. 

This creates a "session gap" where priority commands must manually attempt to resolve the session using `loop.sessions.get_or_create(ctx.key)`. If there is any discrepancy in key resolution or if the command handler doesn't implement this rescue logic, session-specific metadata (like model overrides) is ignored.

## Goals / Non-Goals

**Goals:**
- Unify session resolution so that all commands, including priority commands, are session-aware by default.
- Ensure that `CommandContext` always contains the correct resolved `Session` object if one exists.
- Prevent the creation of unnecessary "ghost" session files on disk for read-only priority commands.

**Non-Goals:**
- Change the priority dispatching logic itself (the "lock-free" nature of priority commands is preserved).
- Modify the `Session` data model.

## Decisions

**1. Use `.get()` instead of `.get_or_create()` in `run()`**
The loop will resolve the session using `self.sessions.get(msg.session_key)` before creating the `CommandContext`. 
- **Rationale**: Priority commands like `/status` or `/help` are typically read-only. Using `.get()` avoids creating a new session on disk if one doesn't already exist, while still providing the existing session's metadata if it does.

**2. Inject Session into `CommandContext` at the Loop Level**
The `CommandContext` will be instantiated with the resolved session.
- **Rationale**: This moves the responsibility of session resolution from the individual command handler to the `AgentLoop`, ensuring consistency across all commands.

## Risks / Trade-offs

- **[Risk]** Priority commands that *do* need to create a session if one is missing will now start with `session=None`.
- **[Mitigation]** The existing rescue logic in handlers (`session = ctx.session or loop.sessions.get_or_create(ctx.key)`) can remain as a fallback for commands that genuinely need to ensure a session exists, though most priority commands are read-only.
