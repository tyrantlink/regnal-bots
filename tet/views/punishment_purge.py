from utils.pycord_classes import View
from discord import Embed,Member,Interaction,ButtonStyle
from ..constants import PUNISHMENT_ROLE
from discord.ui import button,Button


class BotExtensionTetPunishmentView(View):
	def __init__(self) -> None:
		super().__init__(timeout=None)
		self.add_items(self.button_purge,self.button_dismiss)
	
	def embed(self,user:Member,color:int) -> Embed:
		return Embed(
			title = 'auto purge',
			description = f'{user.mention} has lost the <@&{PUNISHMENT_ROLE}> role\n\nwould you like to purge this channel?',
			color = color)

	@button(
		label = 'purge all messages',
		style = ButtonStyle.red,
		custom_id = 'button_purge')
	async def button_purge(self,button:Button,interaction:Interaction) -> None:
		if not interaction.channel.permissions_for(interaction.user).manage_messages:
			await interaction.response.send_message('you do not have permission to delete messages in this channel, please contact an admin',ephemeral=True)
			return
		await interaction.channel.purge(
			limit=10000,
			reason=f'{interaction.user.name} purged all messages')

		await interaction.response.send_message('all messages have been purged',ephemeral=True)

	@button(
		label = 'dismiss',
		style = ButtonStyle.gray,
		custom_id = 'button_dismiss')
	async def button_dismiss(self,button:Button,interaction:Interaction) -> None:
		await interaction.message.delete()
		await interaction.response.send_message('purge prompt dismissed',ephemeral=True)