from .constants import PUNISHMENT_ROLE, GUILD_ID, PUNISHMENT_CHANNEL, MEMBER_ROLE, R18_ROLE
from .views import BotExtensionTetPunishmentView
from .subcog import BotExtensionTetSubCog
from discord import Member


class BotExtensionTetLogic(BotExtensionTetSubCog):
    def member_update_validator(self, before: Member, after: Member) -> bool:
        if after.guild.id != GUILD_ID:
            return False

        if before.roles == after.roles:
            return False

        for name, id in [
            ('punishment', PUNISHMENT_ROLE),
            ('member', MEMBER_ROLE),
            ('R18', R18_ROLE)
        ]:
            if name not in self.roles:
                role = after.guild.get_role(id)
                if role is None:
                    return False

                self.roles[name] = role

        if self.punishment_channel is None:
            self.punishment_channel = [  # ? i have to do it this way so mypy doesn't complain
                channel for channel
                in after.guild.text_channels
                if channel.id == PUNISHMENT_CHANNEL
            ][0]
            if self.punishment_channel is None:
                return False

        if self.punishment_channel is None:
            return False

        return True

    async def auto_purge(self, before: Member, after: Member) -> None:
        if self.punishment_channel is None:
            return

        if not (
            self.roles['punishment'] in before.roles and
            self.roles['punishment'] not in after.roles
        ):
            return

        if self.roles['punishment'].members:
            return

        if not await self.punishment_channel.history(limit=1).flatten():
            return

        view = BotExtensionTetPunishmentView()

        await self.punishment_channel.send(
            embed=view.embed(
                before,
                await self.client.helpers.embed_color(before.guild.id)),
            view=view
        )

    async def store_roles(self, before: Member, after: Member) -> None:
        if not (
            self.roles['punishment'] not in before.roles and
            self.roles['punishment'] in after.roles
        ):
            return

        self.stored_roles[after] = []

        if self.roles['member'] in after.roles:
            self.stored_roles[after].append(self.roles['member'])

        if self.roles['R18'] in after.roles:
            self.stored_roles[after].append(self.roles['R18'])

        await after.remove_roles(
            *self.stored_roles[after],
            reason='punishment role add'
        )

    async def restore_roles(self, before: Member, after: Member) -> None:
        if after not in self.stored_roles:
            return

        if not (
            self.roles['punishment'] in before.roles and
            self.roles['punishment'] not in after.roles
        ):
            return

        await after.add_roles(
            *self.stored_roles[after],
            reason='punishment role remove'
        )

        del self.stored_roles[after]
