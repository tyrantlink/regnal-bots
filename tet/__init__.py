from .views import BotExtensionTetPunishmentView
from .listeners import BotExtensionTetListeners
from .commands import BotExtensionTetCommands
from discord import Role, TextChannel, Member
from .logic import BotExtensionTetLogic
from discord.ext.commands import Cog
from client import Client

# ? most of this extension is hardcoded garbage because i don't want to go through the effort of making it a real feature


class BotExtensionTet(
    Cog,
    BotExtensionTetListeners,
    BotExtensionTetCommands,
    BotExtensionTetLogic
):
    def __init__(self, client: Client):
        self.client = client
        self.client.add_view(BotExtensionTetPunishmentView())
        self.roles: dict[str, Role] = {}
        self.punishment_channel: TextChannel | None = None
        self.stored_roles: dict[Member, list[Role]] = {}


def setup(client: Client):
    client.add_cog(BotExtensionTet(client))
