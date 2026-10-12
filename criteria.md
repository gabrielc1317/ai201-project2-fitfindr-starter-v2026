# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
     Since search_listings uses deterministic keyword overlap rather then sheer language model, a query can describe a valid item utilising wording that doesnt overlap enought with the listing text. 4 out of 5 is a good target as the vast majority of matching listings per query return a fitcard.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
     Since the search_listing uses deterministic keyword overlap, there should be no reason an impossible query triggers the second tool to begin with. 5 out of 5 is reasonable as an impossible query should stop at the first tool instead of sending missing/random data to other tools and wasting resources and time.

---

## 3. Something about state

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->
The listing ID stored in session["Selected_Item"]["ID"] is the same listing ID that is provided to suggest_outfit in 5 out 5 succesful runs.


**Why this target:**
The target of 5 out 5 runs is chosen strictly because the search is deterministic, to ensure the correct listings are stored and passed between calls/functions, 5 out 5 of the succesful runs should contain that exact same listing id. There should never be a different or incorrect listing ID provided due to the architecture of the agent.


---

## 4. Something about the fit card

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->
     Each fit card should mention the selected items' prices and platform it was found on. Aswell as being 2 to four sentences long.



**Why this target:**
When a fit card is generated, the deterministic variables should always be provided, the price and platform so the user can be given directly the correct information for the selected item(s). Aswell as a description between 2 to 4 sentences long ensuring that no inadequate description is provided in the context of length, meaning not too short that the user is left guessing and not too long that it becomes complicated.



---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->
The search should always respect the maximum price set by the user in 5 out of 5 searches when 'max_price' is provided. Every listing returned by 'search_listings' should be less than or equal to that maximum price.


**Why this target:**
Since this is deterministic and the idea behind thrifting is to get clothes for a good price/bargain, the maximum price when provided by the user should always be respected in each search. Because of this 5 out of 5 runs is chosen for this criteria as its a core principle of the tool, even though the maximum price is an optional input, returning a listing above the user's provided 'max_price' would be a complete failure by the tool.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
