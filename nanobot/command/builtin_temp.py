from __future__ import annotations

from typing import Any
from nanobot.bus.events import OutboundMessage

async def cmd_temp(ctx: Any) -> OutboundMessage:
    """Manage the LLM temperature for the current session.
    Usage:
        /temp <value>   — Set temperature (e.g., /temp 0.2)
        /temp           — Show current temperature
    """
    loop = ctx.loop
    session = ctx.session or loop.sessions.get_or_create(ctx.key)
    args = ctx.args.strip()

    # Get current temperature from session or fallback to provider default
    current_temp = session.metadata.get("temperature", loop.provider.generation.temperature)

    if not args:
        return OutboundMessage(
            channel=ctx.msg.channel, chat_id=ctx.msg.chat_id,
            content=f"Current temperature for this session: `{current_temp}`\n\n"
                    f"Use `/temp <value>` to change it (0.0 - 2.0).",
            metadata=dict(ctx.msg.metadata or {})
        )

    try:
        target_temp = float(args.split()[0])
        if not (0.0 <= target_temp <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        
        session.metadata["temperature"] = target_temp
        loop.sessions.save(session)
        
        return OutboundMessage(
            channel=ctx.msg.channel, chat_id=ctx.msg.chat_id,
            content=f"Temperature set to `{target_temp}` for this session.",
            metadata=dict(ctx.msg.metadata or {})
        )
    except (ValueError, IndexError) as e:
        return OutboundMessage(
            channel=ctx.msg.channel, chat_id=ctx.msg.chat_id,
            content=f"Error: {str(e) if isinstance(e, ValueError) else 'Invalid temperature value'}. "
                    f"Please provide a number between 0.0 and 2.0.",
            metadata=dict(ctx.msg.metadata or {})
        )
