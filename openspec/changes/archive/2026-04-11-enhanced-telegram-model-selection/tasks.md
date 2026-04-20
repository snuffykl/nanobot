## 1. Core data model change

- [x] 1.1 Add `reply_markup` field to `OutboundMessage` in `bus/events.py`

## 2. Add inline keyboard support to TelegramChannel

- [x] 2.1 Import `InlineKeyboardButton`, `InlineKeyboardMarkup`, `CallbackQueryHandler`
- [x] 2.2 Add `_model_keyboards: dict[str, int]` to `__init__`
- [x] 2.3 Register `CallbackQueryHandler` in `start()` with pattern `r"^model:"`
- [x] 2.4 Add `build_model_keyboard()` helper function
- [x] 2.5 Add `_on_callback()` method to handle button clicks
- [x] 2.6 Handle `model_list` render mode in `send()` method
- [x] 2.7 Add `"callback_query"` to `allowed_updates` in polling

## 3. Add session_manager to channels

- [x] 3.1 Add `session_manager` property to `BaseChannel`
- [x] 3.2 Update `ChannelManager` to accept and pass `session_manager`
- [x] 3.3 Update CLI to pass `session_manager` when creating `ChannelManager`

## 4. Enhance cmd_model for Telegram

- [x] 4.1 Include models list in `metadata` when returning model list
- [x] 4.2 Add `render_as: model_list` indicator

## 5. Test and validation

- [x] 5.1 Test `/model` shows inline keyboard in Telegram
- [x] 5.2 Test clicking a model button switches the model
- [x] 5.3 Test clicking already-selected model shows appropriate message
- [x] 5.4 Test text fallback works for non-Telegram channels
