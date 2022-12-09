from discord.ext import commands
import discord
import json
import os

os.chdir(os.getcwd())

config = json.load(open("config.json", "r"))

token = config["token"]
prefix = config["prefix"]

class MyBot(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

        for cog in os.listdir("cogs/"):
            if cog.endswith(".py"):
                cog = f"cogs.{cog[:-3]}"
                self.load_extension(cog)
                print(f"Loaded {cog}")

        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{prefix}help"))

    async def on_message(self, message):
        if message.author.bot:
            return

        try:
            if message.mentions[0] == self.user:
                await message.channel.send(translation_of("if_mentionned", message).format(message.author.mention, get_prefix(self, message)))
        except:
            pass

        return await self.process_commands(message)

def translation_of(command, message):
    languages = json.load(open("datas/languages.json", "r"))
    translations = json.load(open("datas/translations.json", "r", encoding="utf-8"))
    return translations[languages.get(str(message.guild.id)) or "en"][command]

def get_prefix(bot, message):
    prefixes = json.load(open("datas/prefixes.json", "r"))
    return prefixes.get(str(message.guild.id)) or prefix

if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True

    bot = MyBot(command_prefix=get_prefix, intents=intents)

    bot.run(token)