import asyncio
from telegram import Bot

async def main():
    bot = Bot(token="7634375553:AAHcqSF4x8i0GSO57tb5nmvsa5TKAy866lw")
    me = await bot.get_me()
    print(me)

if __name__ == "__main__":
    asyncio.run(main())
