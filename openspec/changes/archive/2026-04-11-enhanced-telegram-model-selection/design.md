## Context

The `/model` command lists models and requires typing to switch. Inline buttons in Telegram provide one-click model selection.

## Goals / Non-Goals

**Goals:**
- Provide clickable inline buttons for model selection in Telegram
- Show currently selected model with ✅ prefix
- Show available models with 📋 prefix
- No limit on number of models (show all)

**Non-Goals:**
- No persistence of model preference (session-only)
- No changes to other channels (text-based fallback)

## Decisions

### 1. Inline keyboard markup via OutboundMessage

**Decision**: Add optional `reply_markup` field to `OutboundMessage`.

**Rationale**: Minimal change, keeps architecture clean. Channels interpret as needed.

### 2. Callback data carries model index

**Decision**: Button `callback_data` is `model:<index>` (1-based index).

**Rationale**: Simple, no complex state. Index resolves to model name from stored list.

### 3. Models stored in session metadata

**Decision**: When sending keyboard, store models list in `session.metadata["_model_list"]`.

**Rationale**: Callback handler can look up model by index without re-fetching from provider.

### 4. Channel handles its own callbacks

**Decision**: `TelegramChannel._on_callback` handles all model selection logic.

**Rationale**: Consistent with existing architecture. Channel has access to session_manager.

## Implementation Sketch

```python
# cmd_model returns:
OutboundMessage(
    content="Select a model:",
    metadata={
        "render_as": "model_list",
        "models": [...],
        "current_model": "..."
    }
)

# TelegramChannel.send() checks render_as and sends keyboard
keyboard = build_model_keyboard(models, current)
sent = await bot.send_message(reply_markup=keyboard)

# Store for callback:
session.metadata["_model_list"] = models

# Callback handler:
index = int(callback_data.split(":")[1]) - 1
model = session.metadata["_model_list"][index]
```

## Risks / Trade-offs

- **[Risk]** Session restart clears models list
  - **Mitigation**: User just sends `/model` again

- **[Risk]** Race condition if provider changes model list between /model and callback
  - **Mitigation**: Use stored list, not re-fetched
