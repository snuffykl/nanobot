## ADDED Requirements

### Requirement: Telegram model selection UI
The system SHALL provide an interactive inline keyboard for model selection when the `/model` command is invoked in Telegram, showing clickable buttons for each model.

#### Scenario: List models with inline keyboard
- **WHEN** a user sends `/model` in Telegram
- **THEN** the bot SHALL reply with a message containing an inline keyboard where each available model is a button
- **AND** the currently selected model button SHALL be prefixed with "✅ "
- **AND** other model buttons SHALL be prefixed with "📋 "

#### Scenario: Switch model via button click
- **WHEN** a user clicks a model button in the inline keyboard
- **THEN** the bot SHALL update the session's model to the selected model
- **AND** the bot SHALL send a confirmation message mentioning the new model name

#### Scenario: Same model button clicked (no-op)
- **WHEN** a user clicks the currently selected model's button
- **THEN** the bot SHALL acknowledge but not change the model
- **AND** the bot SHALL send a message indicating the model is already selected

#### Scenario: Text fallback for non-Telegram channels
- **WHEN** a user sends `/model` in a non-Telegram channel
- **THEN** the bot SHALL respond with plain text listing available models

### Requirement: Unlimited model display
The system SHALL display all available models without artificial limits.

#### Scenario: Provider returns many models
- **WHEN** the provider returns more than 20 models
- **THEN** the system SHALL display all models in the inline keyboard

### Requirement: Model name truncation in display
The system SHALL truncate model names longer than 40 characters for button display.

#### Scenario: Long model name displayed
- **WHEN** a model name exceeds 40 characters
- **THEN** the button text SHALL show the first 37 characters followed by "..."
- **AND** the callback data SHALL contain the correct model index for switching
