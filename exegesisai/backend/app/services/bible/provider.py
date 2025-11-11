from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class VerseText:
    reference: str
    translation: str
    text: str


class BibleProvider:
    """
    Lightweight abstraction over whichever Bible API the deployment uses.

    For the starter project we keep everything in-memory to avoid third-party keys.
    Swap the implementations with real HTTP calls (ESV API, YouVersion, etc.) as needed.
    """

    def __init__(self, api_key: str | None = None, provider: str = "esv"):
        self.api_key = api_key
        self.provider = provider

    async def lookup(self, ref: str, translation: str = "ESV") -> VerseText:
        stub = {
            "Romans 12:2": (
                "Do not be conformed to this world, but be transformed by the renewal of your mind, "
                "that by testing you may discern what is the will of God, what is good and acceptable and perfect."
            ),
            "Psalm 23:1": "The LORD is my shepherd; I shall not want.",
        }
        text = stub.get(
            ref,
            "Sample verse text. Connect a real Bible API to retrieve canonical content.",
        )
        return VerseText(reference=ref, translation=translation, text=text)

    async def context(self, ref: str, translation: str = "ESV", window: int = 1) -> list[VerseText]:
        base = await self.lookup(ref, translation)
        before = VerseText(
            reference=f"{ref} (prev)",
            translation=translation,
            text="Previous verse context stub.",
        )
        after = VerseText(
            reference=f"{ref} (next)",
            translation=translation,
            text="Following verse context stub.",
        )
        return [before, base, after]

    async def cross_references(self, ref: str) -> list[str]:
        mapping = {
            "Romans 12:2": ["2 Corinthians 3:18", "Ephesians 4:23"],
            "Psalm 23:1": ["John 10:11", "Philippians 4:19"],
        }
        return mapping.get(ref, ["John 3:16"])

    async def search(self, query: str, mode: str = "keyword") -> list[dict[str, str]]:
        verses = [
            {"reference": "Romans 12:2", "snippet": "Be transformed by the renewal of your mind."},
            {"reference": "Psalm 23:1", "snippet": "The LORD is my shepherd; I shall not want."},
            {"reference": "John 3:16", "snippet": "For God so loved the world..."},
        ]
        if mode == "keyword":
            return [v for v in verses if query.lower() in v["snippet"].lower()]
        return verses[:2]
