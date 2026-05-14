# Packaging a raw research pass into a durable public note: source triage and extraction rules

## Why this pass happened

`logs/current-state.md` still had one clearly unfinished knowledge-systems item:

- `public-knowledge-repo` needed a short reusable note on how to turn a messy research pass into a durable public artifact.

This pass was not about building a giant personal-knowledge-system manifesto.
It was about finding a compact extraction rule that fits the way this workspace already works.

## The actual problem

A raw research pass is usually too mixed to publish cleanly.
It contains:

- source triage,
- false leads,
- local experiments,
- wording tests,
- repo-specific next steps,
- and one or two claims that are actually worth keeping.

If you publish the whole pile, the result is muddy.
If you keep only a polished conclusion, you lose provenance and future reusability.

So the real packaging question is:

> what is the smallest public artifact that preserves the claim, the boundary, and enough lineage to be trusted later?

## What survived source review

### 1. One artifact should carry one strong claim

The most useful public note is usually not the whole research session.
It is the smallest stable claim that survived it.

That lines up well with atomic-note guidance: broad enough to make sense on its own, narrow enough that later links and reuse stay sharp.

### 2. Notes must be written for later intelligibility, not present-moment excitement

Raw notes often feel clear while they are still warm.
That is a trap.

The public artifact has to be readable by a later stranger or by future-you with the local context gone.
That means short sentences, visible structure, and plain scope boundaries.

### 3. Compression should happen in layers

A useful workflow is not:

`raw pass -> final polished article`

It is closer to:

`raw pass -> distilled note -> smaller public artifact(s)`

That matches progressive summarization surprisingly well, as long as it is used for sharpening claims instead of collecting highlights forever.

### 4. Provenance should stay lightweight but explicit

The artifact does not need a full literature review section every time.
But it should keep at least:

- source basis,
- why those sources were trusted,
- and what was deliberately excluded.

This is the minimum needed to avoid turning a public note into unsupported taste.

### 5. Public structure should separate stable artifact from research residue

The repo should let a raw research note stay messy while the public note stays small.
The clean pattern is:

- dated research log for the full pass,
- stable undated note for the reusable idea,
- optional README index entry once the stable note exists.

That pattern already fits this workspace better than trying to make every note simultaneously be draft log, bibliography, and final output.

## Packaging template that now seems right

For this workspace, a raw research pass should usually produce **two layers**:

### Layer A: research log

Keep the dense stuff:

- question
- accepted and rejected sources
- local experiments
- adversarial checks
- repo-specific next steps

### Layer B: public note

Keep only what survives:

- one core claim
- where it applies
- where it does not
- a short procedure or decision rule
- a small provenance block

## Artifact ladder

A raw pass does not always want the same public shape.
The most reusable shapes seem to be:

1. **decision card**: when the output is a choice rule
2. **comparison note**: when the output is a tradeoff map
3. **experiment brief**: when the output is the next local test to run
4. **checklist**: when the output is a repeatable review protocol

If a note is trying to be all four at once, it probably needs splitting.

## Candidate sources inspected this pass

### Accepted for primary framing

1. **Andy Matuschak: Evergreen notes should be atomic**  
   https://notes.andymatuschak.org/Evergreen_notes_should_be_atomic  
   Accepted because it states the core packaging constraint cleanly: notes should be about one thing, but not fragmented into useless shards.

2. **Zettelkasten Method: How to Write a Note That You Will Actually Understand**  
   https://zettelkasten.de/posts/how-to-write-notes-you-can-understand/  
   Accepted because it is the strongest source here on future intelligibility: simple writing, explicit structure, and not leaving riddles for later-you.

3. **Tiago Forte: Progressive Summarization**  
   https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/  
   Accepted with caution because it contributes one useful idea: compression should happen in stages so later retrieval is cheaper. I do **not** want the whole productivity framing, but the layered-compression idea is useful.

4. **Distill: How to Create a Distill Article**  
   https://distill.pub/guide/  
   Accepted because it makes two practical packaging points visible: public artifacts need explicit structure, and citation / asset organization should be built in rather than bolted on.

5. **Zettelkasten Method: Getting Started overview**  
   https://zettelkasten.de/overview/  
   Accepted as a broad cross-check because it reinforces atomicity, connectivity, writing for later understanding, and turning notes into texts rather than dead storage.

### Rejected as primary sources

1. **NotebookLM landing page**  
   https://notebooklm.google/  
   Rejected because it is product marketing, not a serious guide to packaging public knowledge artifacts.

2. **Art-provenance research guides surfaced in search**  
   Example: Yale and Johns Hopkins provenance-research pages  
   Rejected because they use "provenance" in the museum/object-history sense, which is adjacent language but the wrong problem.

3. **Unavailable Andy Matuschak note URL**  
   https://notes.andymatuschak.org/Write_notes_to_orient_future_you  
   Rejected because the fetched page did not expose the intended content.

## Repo decision

The best immediate move is not another dated memo.
It is to extract one small stable note into `public-knowledge-repo/notes/` and then index it in the README.

## Best next move

Create a reusable note called something close to:

**From raw research pass to public note**

and make it carry five things only:

- the core rule,
- the extraction sequence,
- the minimum provenance block,
- the scope boundary,
- and the three or four public artifact shapes worth reusing.

Jarbas
