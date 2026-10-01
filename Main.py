import os
from telethon import TelegramClient, events, types
from telethon.sessions import StringSession

# Telegram API credentials
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

# Telegram login session
SESSION = os.environ["SESSION"]

# Your Telegram channel username or channel ID
CHANNEL = os.environ["CHANNEL"]

# Fixed 12 reactions
REACTIONS = [
    "❤️",
    "🔥",
    "💯",
    "❤️‍🔥",
    "🏆",
    "💼",
    "🍷",
    "🐬",
    "🙏",
    "🕊️",
    "🥰",
    "🆒",
]

client = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)


@client.on(events.NewMessage(chats=CHANNEL))
async def auto_react(event):
    try:
        reactions = [
            types.ReactionEmoji(emoticon=emoji)
            for emoji in REACTIONS
        ]

        await client(
            __import__(
                "telethon.tl.functions.messages",
                fromlist=["SendReactionRequest"]
            ).SendReactionRequest(
                peer=event.input_chat,
                msg_id=event.id,
                reaction=reactions
            )
        )

        print(
            f"Reacted to message {event.id} "
            f"with all {len(REACTIONS)} reactions."
        )

    except Exception as error:
        print(f"Reaction error on message {event.id}: {error}")


async def main():
    me = await client.get_me()
    print(f"Logged in as: {me.first_name or me.username or me.id}")
    print("Telegram auto-reaction system is running...")
    print(f"Target channel: {CHANNEL}")
    print(f"Reactions configured: {len(REACTIONS)}")


with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()
