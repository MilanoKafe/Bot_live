from aiogram import BaseMiddleware
from aiogram.types import Message, Update, CallbackQuery
from typing import Callable, Any, Awaitable
import logging

from utils import get_user
from utils import append_chat_entry

logger = logging.getLogger(__name__)


def _extract_message(event: Any) -> Message | None:
    """Return a Message from various event types (Update/Message/CallbackQuery)."""
    if isinstance(event, Update):
        if event.message:
            return event.message
        if event.callback_query and event.callback_query.message:
            return event.callback_query.message
        return None
    if isinstance(event, Message):
        return event
    if isinstance(event, CallbackQuery):
        return event.message
    return None


class AntiCheatingMiddleware(BaseMiddleware):
    """
    Prevent forwarding/copying and similar actions that may reveal questions.
    Also blocks interactions from banned users.
    Handles both Message and CallbackQuery events.
    """

    async def __call__(
        self,
        handler: Callable[[Any], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        message = _extract_message(event)
        if message:
            # Block banned users early
            try:
                user = get_user(message.from_user.id)
                if user and user.get('is_banned'):
                    try:
                        await message.answer("❌ Siz botdan bloklangansiz. Agar bu xato bo'lsa, admin bilan bog'laning.")
                    except Exception:
                        pass
                    return
            except Exception:
                # If get_user fails for any reason, continue gracefully
                pass

            # Log user's incoming messages and callback data
            try:
                from aiogram.types import Message, Update, CallbackQuery
                # If this is a callback query event, log the callback.data as a special entry
                if isinstance(event, CallbackQuery) or (isinstance(event, Update) and getattr(event, 'callback_query', None)):
                    cq = event.callback_query if isinstance(event, Update) else event
                    data_txt = f"<callback:{cq.data}>"
                    append_chat_entry(message.from_user.id, data_txt, direction='in')

                # For regular Message events, log text or placeholder
                if isinstance(event, Message) or (isinstance(event, Update) and getattr(event, 'message', None)):
                    txt = message.text if getattr(message, 'text', None) else '<non-text-message>'
                    append_chat_entry(message.from_user.id, txt, direction='in')
            except Exception:
                pass

            # If message is forwarded, block it
            if getattr(message, "forward_from", None) or getattr(message, "forward_from_chat", None):
                await message.answer("❌ Forward qilish taqiqlanadi!")
                return

            # Optionally block copy/paste by checking entities or media (best-effort)
            # Allow bot commands to pass
            if message.text and message.text.startswith("/"):
                pass

        return await handler(event, data)


class TestStateMiddleware(BaseMiddleware):
    """
    During a test, block other user commands/messages that could interfere.
    Also respects banned-user block from AntiCheatingMiddleware.
    """

    async def __call__(
        self,
        handler: Callable[[Any], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        message = _extract_message(event)
        state = data.get("state")

        # If banned, block here as well (defensive)
        if message:
            try:
                user = get_user(message.from_user.id)
                if user and user.get('is_banned'):
                    try:
                        await message.answer("❌ Siz botdan bloklangansiz. Agar bu xato bo'lsa, admin bilan bog'laning.")
                    except Exception:
                        pass
                    return
            except Exception:
                pass

        if message and state:
            current_state = await state.get_state()
            if current_state and "test" in current_state.lower():
                # If the user sends commands other than allowed ones, block them
                if message.text and not message.text.startswith(('/start', '/admin')):
                    await message.answer(
                        "❌ Test davomida boshqa buyruqlar foydalanib bo'lmaydi!\nIltimos, test tugagigunga kutib turing."
                    )
                    return

        return await handler(event, data)
