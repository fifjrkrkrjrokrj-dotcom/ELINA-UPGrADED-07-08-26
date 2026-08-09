from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app
from ShrutiMusic.utils.permissions import adminsOnly
from config import BANNED_USERS

@app.on_message(
    filters.command(["approveall", "acceptall"]) & filters.group & ~BANNED_USERS
)
@adminsOnly("can_invite_users")
async def approve_all(client, message: Message):
    chat_id = message.chat.id
    
    msg = await message.reply_text("Approving all pending join requests. Please wait...")
    
    try:
        if hasattr(app, "approve_all_chat_join_requests"):
            await app.approve_all_chat_join_requests(chat_id)
        else:
            # Fallback to iterating
            async for request in app.get_chat_join_requests(chat_id):
                try:
                    await app.approve_chat_join_request(chat_id, request.user.id)
                except Exception:
                    pass
        await msg.edit_text("Successfully approved all pending join requests!")
    except Exception as e:
        await msg.edit_text(f"An error occurred while approving requests:\n`{str(e)}`")
