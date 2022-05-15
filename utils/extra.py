from typing import TYPE_CHECKING, Any, Optional
from random import randint

from discord import Message, Embed

from utils.simple_paginator import SimplePaginator

if TYPE_CHECKING:
    from discord import MessageReference
else:
    MessageReference = Any

__all__: tuple[str, ...] = ("reference", "RTFMEmbedPaginator")


def reference(message) -> Optional[MessageReference]:
    reference: Optional[MessageReference] = message.reference
    if reference and isinstance(reference.resolved, Message):
        return reference.resolved.to_reference()

    return None


class RTFMEmbedPaginator(SimplePaginator):
    def format_page(self, page: str) -> Embed:
        return Embed(title="Packages:", description=page, color=randint(0, 16777215))
