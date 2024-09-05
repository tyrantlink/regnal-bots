from discord import slash_command, ApplicationContext
from .subcog import BotExtensionTetSubCog
from .constants import MEMBER_ROLE, GUILD_ID
from discord.embeds import Embed


class BotExtensionTetCommands(BotExtensionTetSubCog):
    @slash_command(
        name='aschente',
        description='you\'ve read the rules',
        guild_ids=[GUILD_ID])
    async def slash_aschente(self, ctx: ApplicationContext) -> None:
        embed = Embed(color=0xf9b5fa)
        role = ctx.guild.get_role(MEMBER_ROLE)
        if ctx.author.get_role(role.id):
            embed.set_author(name='you already had the role, so i didn\'t do anything',
                             icon_url=self.client.user.display_avatar.url)
            await ctx.response.send_message(embed=embed, ephemeral=True)
            return
        await ctx.author.add_roles(role, reason='used /aschente')
        embed.set_author(name='welcome to disboard~!',
                         icon_url=self.client.user.display_avatar.url)
        await ctx.response.send_message(embed=embed, ephemeral=True)
