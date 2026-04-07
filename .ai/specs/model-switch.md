# Spec: Lightweight Model Switching for LLM Gateway

## Why
Allow users to switch the LLM model for their current provider via a Telegram command without restarting the bot or modifying configuration files. This implementation focuses on a "lightweight" approach, restricting switching to models available within the active provider.

## What
Add a `/model` command that allows users to:
1. **List** all available models for the currently active provider.
2. **Switch** the active model for the current chat session.
3. **Persist** this choice across restarts per-session via session metadata.

## Context
- **Active Provider**: The bot uses the provider configured in `config.json`. This feature allows switching models *within* that provider (e.g., switching from `gpt-4o` to `gpt-4o-mini` while staying on the OpenAI/OpenRouter provider).
- **Session Scope**: Model overrides are stored in `Session.metadata`, meaning different chats can use different models simultaneously.
- **Provider API**: Uses the OpenAI-compatible `/models` endpoint to fetch the available model list.

## Constraints
- **Provider Lock**: Must not allow switching to a different provider (e.g., cannot switch from OpenAI to Anthropic).
- **Persistence**: Selection must persist in the session's JSONL metadata.
- **Validation**: Only models returned by the provider's API should be settable.
- **No Dependencies**: Must not introduce new external libraries.
- **UI**: Acknowledge that Telegram UI commands must be registered manually via BotFather.

## Implementation Plan

### T1: Effective Model Resolution
- **AgentLoop**: Add `get_effective_model(session)` method.
  - Logic: If `session.metadata.get("model")` exists, return it; otherwise, return the global `self.model`.
- **AgentLoop**: Update `_run_agent_loop` to pass the result of `get_effective_model(session)` into the `AgentRunSpec`.

### T2: Provider Model Listing
- **LLMProvider (Base)**: Define `async def list_models() -> list[str] | None`.
- **OpenAICompatProvider**: Implement `list_models` by calling `self._client.models.list()` and returning a list of model IDs.

### T3: The `/model` Command
- **Handler**: Implement `cmd_model(ctx)`.
  - **Case A (No Args)**: Call `loop.provider.list_models()`. Format a list of models, highlighting the current effective model.
  - **Case B (With Args)**: Take the first argument as the model name. Validate it against the list from `list_models()`. If valid, save it to `session.metadata["model"]` and call `loop.sessions.save(session)`.
- **Registration**: Register as both `exact("/model")` and `prefix("/model ")` in `register_builtin_commands`.
- **Help**: Update `build_help_text()` to include the command.

### T4: Telegram Channel Integration
- **nanobot/channels/telegram.py**:
    - Add `BotCommand("model", "List or switch LLM model")` to the `BOT_COMMANDS` list so it appears in Telegram's command menu on startup (via `set_my_commands()`).
    - Add `model` to the regex filter for `_forward_command`: `r"^/(new|stop|restart|status|dream|model)(?:@\w+)?(?:\s+.*)?$"` so `/model` messages are forwarded to the `AgentLoop` command router.

### T5: Telegram UI Registration (Deployment — optional)
- The BotFather registration step is **no longer required** because the bot now auto-registers commands via `set_my_commands()` on startup.
- As a fallback, users can still register commands manually if the auto-registration fails (e.g. network errors) by visiting **@BotFather → /mybots → [Bot] → Edit Bot → Edit Commands**.

## Verification
- [x] `/model` (no args) → Returns a list of models from the current provider.
- [x] `/model <valid-model>` → Confirms switch; subsequent messages use the new model.
- [x] `/model <invalid-model>` → Returns an error message and does not switch.
- [x] Restart bot → Session still uses the overridden model.
- [x] Other sessions → Use the global default model.
