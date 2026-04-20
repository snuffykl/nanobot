# LLM Temperature Control

## Why
Users need to control the "creativity" or "randomness" of the LLM's responses. A low temperature is better for factual/coding tasks, while a high temperature is better for creative writing.

## What
Add a `/temp <value>` slash command that allows users to modify the sampling temperature for the current session. The temperature should persist for the duration of the session.

## Context

**Relevant files:**
- `nanobot/providers/base.py` — Defines `GenerationSettings` and `LLMProvider.chat/chat_with_retry`, which already accept `temperature`.
- `nanobot/command/builtin.py` — Where slash commands are registered.
- `nanobot/command/builtin_temp.py` — Implementation of the `/temp` command logic.
- `nanobot/channels/telegram.py` — Telegram command menu and regex handlers.
- `nanobot/session/manager.py` — Manages session state and metadata.

**Patterns to follow:**
- Follow the pattern of `cmd_model` in `nanobot/command/builtin.py` for updating session-specific settings in `session.metadata`.

**Key decisions already made:**
- Use `session.metadata["temperature"]` to store the session-specific temperature.
- The `LLMProvider` already supports temperature; the change is primarily in the command layer and how that value is passed to the provider during agent loop execution.

## Constraints

**Must:**
- Validate that the input is a valid float.
- Constrain temperature to a reasonable range (e.g., 0.0 to 2.0).
- Ensure the session metadata is saved.

**Must not:**
- Modify the global default temperature for other sessions.
- Add new dependencies.

**Out of scope:**
- Adding a UI slider for temperature (this is a CLI/Chat command feature).
- Modifying provider-specific temperature implementations.

## Tasks

### T1: Implement `/temp` slash command

**Do:** 
1. Create `cmd_temp` in `nanobot/command/builtin_temp.py` to avoid circular imports with `CommandContext`.
2. Implement logic to:
    - Parse the argument as a float.
    - Validate the range (0.0 <= temp <= 2.0).
    - Store it in `session.metadata["temperature"]`.
    - Save the session.
3. Register the command in `nanobot/command/builtin.py`'s `register_builtin_commands` using both `.exact("/temp")` and `.prefix("/temp ")`.
4. Update `build_help_text()` to include `/temp`.
5. Update `nanobot/channels/telegram.py` to include `/temp` in `BOT_COMMANDS` and the regex filter.

**Files:** `nanobot/command/builtin_temp.py`, `nanobot/command/builtin.py`, `nanobot/channels/telegram.py`

**Verify:** 
- Manual: Send `/temp 0.2` and verify the response "Temperature set to 0.2 for this session."
- Manual: Send `/temp invalid` and verify error message.
- Manual: Send `/temp 5.0` and verify range validation error.
- Manual: In Telegram, verify `/temp` appears in the command menu (requires bot restart).

### T2: Integrate session temperature into Agent Loop

**Do:**
1. Locate where the agent calls the LLM provider (likely in `nanobot/agent/loop.py` or `nanobot/agent/runner.py`).
2. Modify the call to `chat_with_retry` or `chat_stream_with_retry` to use the temperature from `session.metadata` if present, falling back to the provider's default.

**Files:** `nanobot/agent/loop.py` (or `nanobot/agent/runner.py`)

**Verify:** 
- Manual: Set temperature to 0.0 (deterministic) and verify consistent responses for the same prompt.
- Manual: Set temperature to 1.5 (creative) and verify more varied responses.

## Done

- [ ] `/temp <value>` correctly updates session metadata.
- [ ] Input validation prevents crashes or invalid LLM requests.
- [ ] The LLM provider actually receives and uses the session-specific temperature.
- [ ] `/help` lists the new command.
- [ ] No regressions in `/model` or session management.
