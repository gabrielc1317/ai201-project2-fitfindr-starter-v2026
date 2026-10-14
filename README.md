# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
The user is able to search listing data from thrift stores. They user can filter and categorize by description, size, and price. The tool will rank matching items based of user's selected filters/categories. Essentialy finding a "fit" (outfit) for the user, utilising thrift store listings.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does: Searches thrift store listing data for items that match users description and other optional paramaters such as price and size, and ranks them by keyword overlap.**
- **Inputs:'description' (str), 'size' (str | None), 'max_price' (float | None)** <!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:A list[dict] of matching listing dictionaries, ordered from best match to worst match, limited to config.SEARCH_RESULT_LIMIT. Each listing contains the following fields: (id, title, description, category, style_tags, size, condition, price, colors, brand, platform)**
- **When it has nothing: Returns an empty list**

### `suggest_outfit`

- **What it does: Uses the selected thrift listing and the user's wadrobe to generate one or two outfit suggestions. **
- **Inputs: 'new item' (dict), 'wardrobe' (dict)**
- **Returns: A non empty string (str) containing outfit suggestions. If wardrobe items are available it should also name pieces the user already owns**
- **When it has nothing: Returns general styling advice rather then failing and returning an empty string**

### `create_fit_card`

- **What it does:Turns the selected listing and outfit suggestion into a short caption someone could post about the find.**
- **Inputs: 'outfit' (str), 'new_item' (dict)**
- **Returns: A non empty string (str) containing a 2 to 4 sentence caption that mentions the item, price, platform, and overall outfit vibe.**
- **When it has nothing:**

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule: If search_listings returns an empty list, the agent stores a message in session["error"] explaining that no listings were matched and that user should change the description, size, or maximum price. The agent then stops without calling suggest_outfit or create_fit_card. If atleast one listing is returned, the agent stores them in session["search_results"] and selects the highest ranked result, stores it in the session["selected_item"], uses it with session["wardrobe"] to call suggest_outfit and stores it in session["outfit_suggestion"]. Then uses that session to call create_fit_card and stores the final caption in session["fit_card"] .**

**Where it lives:'agent.py::run_agent'** `agent.py::run_agent`

**How the query is parsed: The query is parsed determinstically using string/regex parsing.** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:The parsed search values are stored in session["parsed"] and used to call search_listings. The search results are stored in session["search_listings"] and the highest ranked result as session["selected_item"]. That selected item is then read back from the session alongside session["wardrobe"]and passed to suggest_outfit, whose result is stored as session["outfit_suggestion"]. Then session["outfit_suggestion"] and session["selected_item"] are read from the session and passed to create_fit_card, and the resulting caption is stored as session["fit_card"]** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
Output:
Found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit: Here are two outfit ideas using your new Y2K baby tee and items from your wardrobe:

Outfit 1: Casual Streetwear Y2K
- Baggy straight-leg jeans
- Black cropped zip hoodie
- Chunky white sneakers
- Black crossbody bag

Outfit 2: Edge Meets Vintage
- Wide-leg khaki trousers
- Vintage black denim jacket
- Black combat boots

Fit card: Channeling major early 2000s energy with this dreamy butterfly print Y2K baby tee. Grab it now on Depop for just $18.00 to instantly upgrade your rotation. Pair it with baggy denim and chunky sneakers for the ultimate off-duty streetwear look, or toughen it up with combat boots for a sweet-meets-edgy vibe.

```
```
extra: testing branch where search returns nothing:
$ python app.py ask 'designer ballgown size XXS under $5'2000s
Output:
No listings matched your search. Try broadening the description, changing the size, or raising the maximum price.

0 model calls this session
```
**The three tools, tested one at a time**


```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
Output:
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Output: 
**Outfit 1: Classic Streetwear Casual**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* Tucking the fitted white tank into the mid-rise vintage Levi's creates a clean silhouette, while the black denim jacket and chunky white sneakers lean into the streetwear aesthetic.

**Outfit 2: Cozy Layered Look**
*   **Top:** Oversized grey crewneck sweatshirt 
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Shoes:** Black combat boots
*   *Why it works:* Cinch the Levi's with the brown leather belt, do a half-tuck with the oversized grey crewneck for balanced proportions, and finish with black combat boots to add a subtle edge.


```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Output:
Nothing beats the effortless streetwear vibe of a truly broken-in pair of denim. These Vintage Levi's 501 Jeans in a medium wash are up on my depop for just $38.00. Throw them on with your favorite crisp white sneakers for the ultimate classic casual look.

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for: How to avoid simple substring match, since a request for L should not automatically XL*
- *What came back: AI suggested tokenizing the listing size with a regular expression so sizes such as L, XL, S/M, and numeric sizes could be compared as separate tokens instead of raw substrings.*
- *What I changed: I added a _size_matches() helper that normalizes the requested size and listing size, extracts size tokens with regex, and checks membership against those tokens.*

**Moment 2**

- *What I asked for:Help debugging why suggest_outfit() was returning an empty string for both a normal wardrobe and an empty wardrobe.*
- *What came back: AI first helped isolate the model adapter by testing generate() directly. After that worked, I inspected the actual suggest_outfit() function being executed and found that the file still contained the starter stub returning "".*
- *What I changed:I saved the actual suggest_outfit() implementation into tools.py, then reran both the normal-wardrobe and empty-wardrobe tests and confirmed that both returned useful outfit suggestions.*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->
     Unit 4 Stretch Feature

For the stretch feature, I am moving a second tool onto MCP. In addition to search_listings, I will expose suggest_outfit through the MCP server and have the agent call both tools through the MCP client. create_fit_card will remain a local tool.

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
