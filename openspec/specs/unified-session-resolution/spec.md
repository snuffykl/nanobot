## ADDED Requirements
## Purpose
After switching models feature was introduced, there is a need to unified session context to make sure consistency of the model value being notified or to be aware of.

### Requirement: Unified Session Context for All Commands
The system SHALL ensure that all command handlers, including priority commands, receive a `CommandContext` that contains the correctly resolved `Session` object if one exists for the current session key.

#### Scenario: Priority command with existing session
- **WHEN** a priority command (e.g., `/status`) is executed for a session that has an existing session file on disk
- **THEN** the `CommandContext.session` SHALL be populated with the corresponding `Session` object

#### Scenario: Priority command with no existing session
- **WHEN** a priority command is executed for a session key that does not have a corresponding session file
- **THEN** the `CommandContext.session` SHALL be `None`, and the system SHALL NOT create a new empty session file on disk

#### Scenario: Model override resolution in priority commands
- **WHEN** a priority command is executed for a session that has a model override set in its metadata
- **THEN** the command handler SHALL be able to retrieve the correct model via `loop.get_effective_model(ctx.session)`
