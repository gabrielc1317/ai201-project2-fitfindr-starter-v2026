"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings
import re


# ── Helper Functions ──────────────────────────────────────────────────
def _size_matches(requested: str, listing_size: str) -> bool:
    """Match size tokens without accidental substring matches. eg: L -> XL"""
    requested = requested.strip().casefold()
    listing_size = listing_size.strip().casefold()

    alpha_sizes = {"xxs", "xs", "s", "m", "l", "xl", "xxl", "xxxl"}

    listing_tokens = re.findall(
        r"\b(?:xxxl|xxl|xl|xxs|xs|s|m|l)\b|[a-z]+\d+\d+", listing_size,)

    if requested in alpha_sizes:
        return requested in listing_tokens
    return requested in listing_tokens

# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    # TODO: 
    listings = load_listings()
    query_tokens = set(re.findall(r"[a-z0-9]+", description.casefold()))
    scored: list[tuple[int, dict]] =[]

    for listing in listings:
        if max_price is not None and listing["price"] > max_price:
            continue

        if size is not None and not _size_matches(size, listing["size"]):
            continue
        searchable_parts = [
            listing["title"],
            listing["description"],
            listing["category"],
            " ".join(listing["style_tags"]),
            listing["size"],
            " ".join(listing["colors"]),
            listing["brand"] or "",
            listing["platform"],
        ]

        searchable_text = " ".join(searchable_parts).casefold()
        searchable_tokens = set(re.findall(r"[a-z0-9]+", searchable_text))

        score = len(query_tokens & searchable_tokens)

        if score > 0:
            scored.append((score, listing))

    scored.sort(key=lambda pair: pair[0], reverse=True)

    return [
        listing
        for _, listing in scored[: config.SEARCH_RESULT_LIMIT]
    ]



# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    # TODO: 
    items = wardrobe.get("items", [])

    item_details = (
        f"Item: {new_item['title']}\n"
        f"Category: {new_item['category']}\n"
        f"Colors: {', '.join(new_item['colors'])}\n"
        f"Style tags: {', '.join(new_item['style_tags'])}\n"
        f"Size: {new_item['size']}\n"
    )
    system = (
        "You are a clothing styling assistant. "
        "Give practical, specific outfit suggestions using the information provided. "
        "Keep the response concise."
    )
    if not items:
        prompt = ( 
            f"{item_details}\n"
            "The user has no items available.\n"
            "Suggest one or two general ways to style this item. "
            "Mention the types of clothing, shoes, or accessories that would pair well with it."
        )
        return generate(prompt, system=system)
    
    wardrobe_lines = []

    for item in items:
        wardrobe_lines.append(
            f"- {item['name']} "
            f"(category: {item['category']}); "
            f"colors: {', '.join(item['colors'])}; "
            f"style: {', '.join(item['style_tags'])}"
        )
    
    wardrobe_text = "\n".join(wardrobe_lines)

    prompt = (
        f"{item_details}\n"
        "The user already owns these wardrobe pieces:\n"
        f"{wardrobe_text}\n\n"
        "Suggest one or two outfits that combine the new item with existing pieces "
        "from the user's wardrobe. Refer to the existing wardrobe pieces by name."
    )

    return generate(prompt, system=system)



# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # TODO: replace this with your implementation
    if not outfit or not outfit.strip():
        return "A fit card cannot be created because no outfit suggestion was provided."

    system = (
        "You write short social-media-style fashion captions. "
        "Keep the caption between two and four sentences long."
        "Make it sound like a real post rather than a product description."
    )
    prompt = ( 
        f"New item: {new_item['title']}\n"
        f"Price: ${new_item['price']:.2f}\n"
        f"Platform: {new_item['platform']}\n"
        f"Style tags: {', '.join(new_item['style_tags'])}\n"
        f"Outfit suggestion:\n{outfit}\n\n"
        "Write a 2-to-4 sentence fit-card caption. "
        "Mention the item, its price, and its platform exactly one each. "
        "Describe the overall vibe of the outfit."
    )
    return generate(prompt, system=system)
