## Why

Currently, switching the LLM model requires typing the full model name. Adding inline buttons with clickable model selection makes switching faster and more intuitive. Buttons show model numbers with checkmark for the currently selected one.

## What Changes

- `/model` now shows inline keyboard buttons for Telegram (text fallback for other channels)
- Each button shows: `✅ 1. model-name` (selected) or `📋 2. model-name` (available)
- Clicking a button switches the model immediately
- No limit on number of models shown (unlike previous keyboard approach)

## Capabilities

### New Capabilities
- `telegram-model-selector`: Inline keyboard UI for model selection in Telegram with toggle buttons

### Modified Capabilities
- `builtin-commands`: The `/model` command enhanced with interactive Telegram UI

## Impact

- **Code changes**: 
  - `nanobot/bus/events.py` - add optional `reply_markup` field to OutboundMessage
  - `nanobot/channels/telegram.py` - inline keyboard handling, callback handler
  - `nanobot/channels/base.py` - add session_manager property
  - `nanobot/channels/manager.py` - pass session_manager to channels
  - `nanobot/command/builtin.py` - include models in metadata for Telegram
