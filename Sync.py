import asyncio
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()

API_ID_1 = os.getenv('API_ID_1')
API_HASH_1 = os.getenv('API_HASH_1')
API_ID_2 = os.getenv('API_ID_2')
API_HASH_2 = os.getenv('API_HASH_2')

if not (API_ID_1 and API_HASH_1 and API_ID_2 and API_HASH_2):
    print("Missing API credentials in .env")
    exit(1)

async def main():
    client1 = TelegramClient('session1', int(API_ID_1), API_HASH_1)
    client2 = TelegramClient('session2', int(API_ID_2), API_HASH_2)

    print("\nAccount 1")
    await client1.start(phone=lambda: input('Enter phone: '))
    me1 = await client1.get_me()
    print(f"Account 1: @{me1.username or me1.first_name}")

    print("\nAccount 2")
    await client2.start(phone=lambda: input('Enter phone: '))
    me2 = await client2.get_me()
    print(f"Account 2: @{me2.username or me2.first_name}")

    @client1.on(events.NewMessage(chats='me'))
    async def handler(event):
        try:
            if event.message.text:
                await client2.send_message('me', event.message.text)
                print("Synced")
            elif event.message.media:
                path = await client1.download_media(event.message.media)
                if path:
                    await client2.send_file('me', path)
                    os.remove(path)
                    print("Synced")
        except Exception as e:
            print(f"Error: {e}")

    await asyncio.gather(
        client1.run_until_disconnected(),
        client2.run_until_disconnected()
    )

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
