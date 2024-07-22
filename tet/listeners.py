from .constants import REACTION_MESSAGES, ROLES, LIMITED_TO_ONE, PUNISHMENT_CHANNEL, PUNISHMENT_ROLE
from discord import RawReactionActionEvent, Member, Forbidden
from .views import BotExtensionTetPunishmentView
from .subcog import BotExtensionTetSubCog
from discord.ext.commands import Cog


class BotExtensionTetListeners(BotExtensionTetSubCog):
    @Cog.listener('on_raw_reaction_add')
    @Cog.listener('on_raw_reaction_remove')
    async def on_raw_reaction_update(self, payload: RawReactionActionEvent) -> None:
        if payload.message_id not in REACTION_MESSAGES:
            return

        reaction = payload.emoji.name if payload.emoji.id is None else payload.emoji.id
        role_id = ROLES.get(reaction, None)

        if role_id is None:
            return

        try:
            guild = self.client.get_guild(payload.guild_id) or await self.client.fetch_guild(payload.guild_id)
        except Forbidden:
            return

        if guild is None:
            return

        try:
            member = payload.member or guild.get_member(payload.user_id)

            if not isinstance(member, Member):
                member = await guild.fetch_member(payload.user_id)

        except Forbidden:
            return

        if member is None:
            return

        match payload.event_type:
            case 'REACTION_ADD':
                if reaction in LIMITED_TO_ONE:
                    await member.remove_roles(
                        *[
                            guild.get_role(ROLES.get(r))
                            for r in LIMITED_TO_ONE
                            if member.get_role(ROLES.get(r)) is not None
                        ],
                        atomic=False,
                        reason='reaction role add'
                    )

                await member.add_roles(
                    guild.get_role(role_id), reason='reaction role add')

            case 'REACTION_REMOVE':
                await member.remove_roles(
                    guild.get_role(role_id), reason='reaction role remove')

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member) -> None:
        if before.roles == after.roles:
            return

        if PUNISHMENT_ROLE not in [role.id for role in before.roles]:
            return

        if PUNISHMENT_ROLE in [role.id for role in after.roles]:
            return

        channel = before.guild.get_channel(PUNISHMENT_CHANNEL)

        if channel is None:
            return

        view = BotExtensionTetPunishmentView()

        await channel.send(
            embed=view.embed(
                before,
                await self.client.helpers.embed_color(before.guild.id)),
            view=view)
