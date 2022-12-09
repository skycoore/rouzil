from discord.ext import commands
import json
import os
import sys
sys.path.insert(0, f"{os.getcwd()}")
from bot import get_prefix, translation_of, prefix
import discord

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, newPrefix):
        prefixes = json.load(open("datas/prefixes.json", "r"))

        prefixes[str(ctx.guild.id)] = newPrefix
        if newPrefix == prefix:
            prefixes.pop(str(ctx.guild.id))

        json.dump(prefixes, open("datas/prefixes.json", "w"))

        await ctx.channel.send(translation_of("prefix", ctx).format(newPrefix))

    @commands.command(name="language", aliases=["lang"])
    @commands.has_permissions(administrator=True)
    async def language(self, ctx, language):
        translations = json.load(open("datas/translations.json", "r"))
        translations = [key for key, value in translations.items()]

        if language not in translations:
            await ctx.channel.send(translation_of("language_error", ctx).format(get_prefix(self.bot, ctx), [translation for translation in translations]))
        else:
            languages = json.load(open("datas/languages.json", "r"))
            languages[str(ctx.guild.id)] = language
            json.dump(languages, open("datas/languages.json", "w"))

            await ctx.channel.send(translation_of("language", ctx).format(language))

def setup(bot):
    bot.add_cog(Utility(bot))