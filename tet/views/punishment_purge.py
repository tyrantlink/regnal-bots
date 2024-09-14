from ..constants import PUNISHMENT_ROLE, PUNISHMENT_ARCHIVE_CHANNEL
from discord import Embed, Member, Interaction, ButtonStyle, File
from utils.pycord_classes import View
from discord.ui import button, Button
from io import StringIO


class BotExtensionTetPunishmentView(View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_items(
            self.button_purge,
            self.button_dismiss,
            self.button_archive,
            self.button_archive_purge)

    def embed(self, user: Member, color: int) -> Embed:
        return Embed(
            title='auto purge',
            description=(
                f'{user.mention} has lost the <@&{PUNISHMENT_ROLE}> role\n\nwould you like to purge this channel?'),
            color=color)

    @button(
        label='purge all messages',
        style=ButtonStyle.red,
        custom_id='button_purge')
    async def button_purge(self, button: Button, interaction: Interaction) -> None:
        if not interaction.channel.permissions_for(interaction.user).manage_messages:
            await interaction.response.send_message('you do not have permission to delete messages in this channel, please contact an admin', ephemeral=True)
            return
        await interaction.channel.purge(
            limit=10000,
            reason=f'{interaction.user.name} purged all messages')

        await interaction.response.send_message('all messages have been purged', ephemeral=True)

    @button(
        label='dismiss',
        style=ButtonStyle.gray,
        custom_id='button_dismiss')
    async def button_dismiss(self, button: Button, interaction: Interaction) -> None:
        await interaction.message.delete()
        await interaction.response.send_message('purge prompt dismissed', ephemeral=True)

    @button(
        label='archive',
        style=ButtonStyle.green,
        custom_id='button_archive')
    async def button_archive(self, button: Button, interaction: Interaction) -> None:
        channel = interaction.guild.get_channel(PUNISHMENT_ARCHIVE_CHANNEL)

        if channel is None:
            await interaction.response.send_message('archive channel not found', ephemeral=True)
            return

        await interaction.response.defer(invisible=False)

        messages = [
            (
                f'{message.author.display_name}: {message.content}'
                + '\n{'+'}{'.join([attachment.filename for attachment in message.attachments])+'}'
                if message.attachments
                else ''
            )
            async for message in interaction.channel.history(limit=100000, oldest_first=True)
            if message is not None and (message.content or message.attachments)
        ]

        await channel.send(
            file=File(StringIO('\n'.join(messages)), filename='archive.txt')
        )

        await interaction.followup.send('channel has been archived', ephemeral=True)

    @button(
        label='archive, then purge',
        style=ButtonStyle.red,
        row=1,
        custom_id='button_archive_purge')
    async def button_archive_purge(self, button: Button, interaction: Interaction) -> None:
        if not interaction.channel.permissions_for(interaction.user).manage_messages:
            await interaction.response.send_message('you do not have permission to delete messages in this channel, please contact an admin', ephemeral=True)
            return

        channel = interaction.guild.get_channel(PUNISHMENT_ARCHIVE_CHANNEL)

        if channel is None:
            await interaction.response.send_message('archive channel not found', ephemeral=True)
            return

        await interaction.response.defer(invisible=False)

        messages = [
            (
                f'{message.author.display_name}: {message.content}'
                + '\n{'+'}{'.join([attachment.filename for attachment in message.attachments])+'}'
                if message.attachments
                else ''
            )
            async for message in interaction.channel.history(limit=100000, oldest_first=True)
            if message is not None and (message.content or message.attachments)
        ]

        await channel.send(
            file=File(StringIO('\n'.join(messages)), filename='archive.txt')
        )

        await interaction.channel.purge(
            limit=10000,
            reason=f'{interaction.user.name} purged all messages')

        await interaction.followup.send('channel has been archived and purged', ephemeral=True)
