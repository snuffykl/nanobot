# Subagent Respects Session Model Override

## Why

When a user switches models via `/model`, the main agent loop correctly uses the session-overridden model — but spawned subagents always use the global default model. This means subagent research runs on the wrong model, producing unexpected results or errors, and the user never gets a response from the model they selected.

## What

Subagents spawned via the `spawn` tool use the same effective model as the session that spawned them (i.e., the session-overridden model when one is set, otherwise the global default). A test confirms the model override propagates end-to-end from session metadata through SpawnTool into SubagentManager.

## Context

**Relevant files:**
- `nanobot/agent/loop.py` — `_set_tool_context()` sets channel/chat_id on tools; `get_effective_model()` resolves session model override; `SubagentManager` is constructed with the global `self.model`
- `nanobot/agent/subagent.py` — `SubagentManager.__init__` captures `model` at construction time; `_run_subagent` uses `self.model` in the `AgentRunSpec`
- `nanobot/agent/tools/spawn.py` — `SpawnTool.execute()` calls `self._manager.spawn()` with no model parameter
- `nanobot/session/manager.py` — `Session.metadata["model"]` stores the per-session model override
- `nanobot/command/builtin.py` — `cmd_model` sets `session.metadata["model"]`

**Patterns to follow:**
- `SpawnTool.set_context(channel, chat_id)` pattern for propagating per-request context from loop to tool — see `nanobot/agent/tools/spawn.py:28-31`
- `AgentLoop.get_effective_model(session)` as the single source of truth for model resolution — see `nanobot/agent/loop.py:319-322`

**Key decisions already made:**
- Model override is session-scoped, stored in `Session.metadata["model"]`
- The effective model is `session.metadata["model"]` if set, otherwise the global default
- SubagentManager already accepts an optional `model` parameter in its constructor

## Constraints

**Must:**
- Pass the session-effective model from AgentLoop → SpawnTool → SubagentManager at spawn time
- Fall back to the global default when no session override exists
- Preserve all existing subagent behavior when no model override is set

**Must not:**
- Change the SubagentManager constructor signature in a breaking way
- Add new dependencies
- Modify unrelated code (channels, CLI, provider logic)

**Out of scope:**
- Provider switching (switching to a model from a different provider)
- Subagent streaming or progress reporting
- Changing how `/model` validation works

## Tasks

### T1: Propagate effective model to SpawnTool and SubagentManager

**Do:**
1. Add a `_model` attribute to `SpawnTool` (default `None`) to hold the current session-effective model.
2. Extend `SpawnTool.set_context()` to also accept and store an optional `model` parameter — e.g., `set_context(self, channel, chat_id, model=None)`. When `model` is provided, store it as `self._model`.
3. In `SpawnTool.execute()`, pass `model=self._model` to `self._manager.spawn()`.
4. Add `model: str | None = None` parameter to `SubagentManager.spawn()`. When provided, use it instead of `self.model` in the call to `_run_subagent()`.
5. In `_run_subagent()`, add a `model` parameter and use it in the `AgentRunSpec` instead of `self.model`.
6. Update `AgentLoop._set_tool_context()` to resolve the effective model via `self.get_effective_model(session)` and pass it to `spawn.set_context()`. Since `_set_tool_context` doesn't currently have access to the session, add an optional `session` parameter and thread it through from the two call sites in `_process_message()`.

**Files:** `nanobot/agent/tools/spawn.py`, `nanobot/agent/subagent.py`, `nanobot/agent/loop.py`

**Verify:** `cd /home/snuffykl/code/nanobot && python -m pytest tests/agent/test_task_cancel.py -x -q`

### T2: Add test for model override propagation

**Do:**
1. Add a test in `tests/agent/test_task_cancel.py` (in `TestSubagentCancellation`) that verifies when `SpawnTool.set_context` receives a model override, the spawned subagent uses that model in its `AgentRunSpec`.
2. Add a test verifying `SubagentManager.spawn()` forwards the model parameter to `_run_subagent`.
3. Add a test verifying that when no model override is set, `SubagentManager.spawn()` falls back to `self.model`.

**Files:** `tests/agent/test_task_cancel.py`

**Verify:** `cd /home/snuffykl/code/nanobot && python -m pytest tests/agent/test_task_cancel.py -x -q`

## Done

- [ ] `python -m pytest tests/agent/test_task_cancel.py -x -q` passes
- [ ] Manual: `/model gpt-4o-mini` → spawn a research subagent → subagent runs on `gpt-4o-mini` (check logs for `model=gpt-4o-mini` in AgentRunSpec)
- [ ] Manual: No `/model` override → spawn subagent → subagent uses global default model
- [ ] No regressions in existing subagent tests