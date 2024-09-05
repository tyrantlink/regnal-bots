from discord import Role, TextChannel, Member
from utils.pycord_classes import SubCog
from client import Client


class BotExtensionTetSubCog(SubCog):
    def __init__(self) -> None:
        self.client: Client
        self.roles: dict[str, Role]
        self.punishment_channel: TextChannel | None
        self.stored_roles: dict[Member, list[Role]]
        super().__init__()

    def member_update_validator(
        self, before: Member, after: Member) -> bool: ...

    async def auto_purge(self, before: Member, after: Member) -> None:
        ...

    async def store_roles(self, before: Member, after: Member) -> None:
        ...

    async def restore_roles(self, before: Member, after: Member) -> None:
        ...
