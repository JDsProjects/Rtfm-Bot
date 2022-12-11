from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

from discord import ButtonStyle, Embed
from discord.ui import View
from discord.ui import button as button_decorator
from discord.utils import maybe_coroutine

if TYPE_CHECKING:
    from discord import Interaction, InteractionMessage, Message, WebhookMessage
    from discord.ext.commands.context import Context
    from discord.ui.button import Button
    from discord.ui.item import Item
    from typing_extensions import Self

    ValidPage = Union[str, Embed]
    PossibleMessage = Union[InteractionMessage, Message, WebhookMessage]
else:
    Interaction = Any
    Button = Any
    Context = Any

__all__: tuple[str, ...] = ("SimplePaginator",)


class SimplePaginator(View):
    def __init__(
        self,
        pages: list[ValidPage],
        *,
        delete_message_after: bool = False,
    ):
        self.pages = pages
        super().__init__()

        self.delete_message_after = delete_message_after

        self.message: Optional[PossibleMessage] = None
        self.current_page: int = 0

    def _init_children(self) -> list[Item[Self]]:
        org_children = super()._init_children()

        # only show stop button if there is only 1 page.
        if len(self.pages) <= 1:
            return [item for item in org_children if item.callback.callback.__name__ == "stop_button"]
        return org_children

    def format_page(self, page: ValidPage) -> ValidPage:
        return page

    async def get_page_kwargs(self, page_number: int) -> dict[str, Any]:
        page = await maybe_coroutine(self.format_page, self.pages[page_number])

        base_kwargs: dict[str, Any] = {"content": None, "embeds": [], "view": self}
        if isinstance(page, Embed):
            base_kwargs["embeds"].append(page)
        elif isinstance(page, str):
            base_kwargs["content"] = page
        elif isinstance(page, dict):
            return page

        return base_kwargs

    async def update(self, interaction: Interaction) -> None:
        if hasattr(self, "right_button") and hasattr(self, "left_button"):
            if self.current_page >= len(self.pages) - 1:
                self.right_button.disabled = True
                self.left_button.disabled = False
            elif self.current_page == 0:
                self.right_button.disabled = False
                self.left_button.disabled = True

        if self.current_page > len(self.pages):
            self.current_page = 0

        kwargs = await self.get_page_kwargs(self.current_page)
        if not interaction.response.is_done():
            await interaction.response.edit_message(**kwargs)
            if not self.message:
                self.message = await interaction.original_message()
        else:
            if self.message:
                await self.message.edit(**kwargs)
            else:
                await interaction.message.edit(**kwargs)  # type: ignore
                self.message = interaction.message

    async def start(
        self, ctx: Optional[Context] = None, interaction: Optional[Interaction] = None, **kwargs
    ) -> Optional[PossibleMessage]:
        kwargs = await self.get_page_kwargs(self.current_page)
        if self.message:
            await self.message.edit(**kwargs)
            return self.message

        if ctx:
            self.message = await ctx.send(**kwargs)
        elif interaction:
            if not interaction.response.is_done():
                await interaction.response.send_message(**kwargs)
                self.message = await interaction.original_message()
            else:
                self.message = await interaction.followup.send(wait=True, **kwargs)

        return self.message

    @button_decorator(emoji="⬅️", style=ButtonStyle.secondary, custom_id="left")
    async def left_button(self, interaction: Interaction, button: Button) -> None:
        self.current_page -= 1
        await self.update(interaction)

    @button_decorator(label="Stop", style=ButtonStyle.red, custom_id="stop")
    async def stop_button(self, interaction: Interaction, button: Button) -> None:
        self.stop()
        if self.delete_message_after:
            await self.message.delete()  # type: ignore

    @button_decorator(emoji="➡️", style=ButtonStyle.secondary, custom_id="right")
    async def right_button(self, interaction: Interaction, button: Button) -> None:
        self.current_page += 1
        await self.update(interaction)
