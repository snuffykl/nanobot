# Project Overview: nanobot

## Vision
nanobot is an ultra-lightweight personal AI agent designed for stability, long-running autonomy, and ease of research. It is inspired by the concept of delivering professional-grade agent functionality with a radically minimized codebase.

## Core Philosophy
- **Ultra-Lightweight**: Minimize lines of code and resource footprint to ensure fast startup and low overhead.
- **Research-Ready**: Maintain a clean, readable, and modular architecture that is easy for developers to modify, extend, and understand.
- **Stability First**: Optimized for long-running tasks with a robust runtime that handles retries, session recovery, and proactive context management.
- **Provider & Channel Agnostic**: Decouples the "brain" (LLM providers) from the "body" (chat channels), allowing seamless integration across diverse ecosystems.

## Primary Capabilities
- **Autonomous Tool Use**: Executes a wide array of built-in and custom skills (shell, filesystem, web search, MCP).
- **Layered Memory**: Implements a sophisticated memory system (Short-term $\rightarrow$ Intermediate $\rightarrow$ Long-term) to avoid context rot.
- **Multi-Channel Gateway**: Supports various chat platforms (Telegram, Discord, WeChat, Slack, etc.) via a unified gateway.
- **Proactive Execution**: Uses a "Heartbeat" system to perform periodic tasks without user intervention.

## High-Level Constraints
- **YAGNI (You Ain't Gonna Need It)**: Avoid adding complex abstractions unless they provide immediate, tangible value.
- **Transparency**: System state (memory, logs, task status) should be inspectable and manageable by the user.
- **Isolation**: Use workspaces and sandboxing (e.g., bubblewrap) to ensure security and a clean development environment.
