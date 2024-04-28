from __future__ import annotations

import json
import zlib
from random import randint
from typing import TYPE_CHECKING, Any, NamedTuple, Optional

from discord import Embed, Message

from utils.simple_paginator import SimplePaginator

if TYPE_CHECKING:
    from discord import MessageReference

    from ..main import RTFMBot
else:
    MessageReference = Any

__all__: tuple[str, ...] = ("reference", "RTFMEmbedPaginator", "rtfm")


def reference(message) -> Optional[MessageReference]:
    reference: Optional[MessageReference] = message.reference
    if reference and isinstance(reference.resolved, Message):
        return reference.resolved.to_reference()

    return None


class RTFMEmbedPaginator(SimplePaginator):
    def format_page(self, page: str) -> Embed:
        return Embed(title="Packages:", description=page, color=randint(0, 16777215))


class RtfmObject(NamedTuple):
    name: str
    url: str

    def __str__(self) -> str:
        return self.name


async def rtfm(bot: RTFMBot, url: str) -> list[RtfmObject]:

    async with await bot.session.get(f"{url}objects.inv") as response:
        lines = (await response.read()).split(b"\n")

    first_10_lines = lines[:10]
    first_10_lines = [n for n in first_10_lines if not n.startswith(b"#")]

    lines = first_10_lines + lines[10:]
    joined_lines = b"\n".join(lines)
    full_data = zlib.decompress(joined_lines)
    normal_data = full_data.decode()
    new_list = normal_data.split("\n")

    results = []
    for x in new_list:
        try:
            name, type, _, fragment, *label = x.split(" ")

            text = " ".join(label)

            if text != "-":
                label = text

            else:
                label = name

        except:
            continue

        fragment = fragment.replace("$", name)
        results.append(RtfmObject(label, url + fragment))

    return results


async def algolia_lookup(bot: RTFMBot, app_id: str, app_key: str, index: str, query: str):

    results = []

    headers = {
        "Content-Type": "application/json",
        "X-Algolia-API-Key": app_key,
        "X-Algolia-Application-Id": app_id,
    }

    # Construct complete JSON string
    data_string = json.dumps({"query": query})

    async with await bot.session.post(
        f"https://{app_id}.algolia.net/1/indexes/{index}/query",
        data=data_string,
        headers=headers,
    ) as response:
        if not response.ok:

            results[RtfmObject("Getting Started", "https://discord.com/developers/docs/")]
            # quick fix.

            return results

        resp = await response.json()
        values = resp["hits"]

        for value in values:
            results.append(RtfmObject(value["anchor"], value["url"]))

        return results
