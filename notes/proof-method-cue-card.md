# Proof-method cue card

This is not a rule engine.
It is a way to pick a strong first move.

## Use these cues

### Direct proof
Reach for this first when the hypotheses unpack into definitions you can push forward step by step.

Good signs:
- the statement is an implication,
- the main objects come with usable definitions,
- the conclusion looks like something you can build from the assumptions.

### Contrapositive
Use this when the conclusion is negative or awkward, but its negation is concrete.

Good signs:
- the claim has the form `if P, then Q`,
- `not Q` is easier to work with than `Q`,
- the forward route feels indirect, but reversing the pressure makes the structure cleaner.

Classic shape:
- if `n^2` is even, then `n` is even.

### Contradiction
Use this when assuming the opposite creates an impossible combination.

Good signs:
- the statement claims something cannot happen,
- the opposite assumption forces incompatible parity, divisibility, order, or minimality conditions,
- every direct route feels artificial.

Classic shape:
- irrationality proofs,
- nonexistence claims,
- uniqueness arguments with a hidden clash.

### Counterexample
Use this first when the statement is universal and might simply be false.

Good signs:
- the claim says "for all" or makes a broad pattern claim,
- a small test case is cheap to try,
- the statement feels plausible but not structurally supported.

One honest counterexample beats a page of hopeful algebra.

### Proof by cases
Use this when the domain splits naturally into a short exhaustive list.

Good signs:
- positive / zero / negative,
- even / odd,
- overlapping definitions that can be partitioned cleanly.

If the case split feels arbitrary or explodes into bookkeeping, back up.

### Induction
Use this when the claim is indexed by an integer and really reduces from a larger case to a smaller one.

Good signs:
- the statement is about all `n` beyond a starting point,
- the expression or structure at `n + 1` contains the structure at `n`,
- the problem feels recursive, cumulative, or buildable.

Do not use induction just because `n` appears in the statement.

## One anti-fake rule

Before writing the full proof, force one sentence:

- Why does this method fit better than the next most obvious one?

If that sentence sounds fake, switch methods early.

## Best use

Carry this card into mixed practice.
Then log two things after each problem:
- which method you chose first,
- which method would have been cleaner in retrospect.
