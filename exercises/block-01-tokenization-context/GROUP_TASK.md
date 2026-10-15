# Exercise: learn and test BPE merges

**Exercise + breakout · LLM Day 1 Block 1 · 15 minutes in pairs**

Learning goal: explain how corpus frequencies produce BPE merge rules, and distinguish learning those rules from applying them to new text.

## Before rooms open

Complete the [shared setup](../../README.md) and open the notebook from the repository root:

```sh
uv run --locked python start.py --block 1
```

Inspect the corpus table and the two function interfaces together. You need basic Python loops, dictionaries, lists and tuple keys. All other code is supplied. Show where to edit/run a cell and record predictions; leave the BPE implementation for the room. Downloading the real-tokenizer asset happens during setup.

**Start with the notebook's `cat cat car` example.** Read the whole training text
first, then the table: `cat` appears twice and `car` once. `frequencies` stores
these quantities; `splits` shows the pieces of each word. Follow how the table
adds each word's contribution to one neighbouring-pair count. No code is needed
for this walkthrough. The main exercise uses the separate corpus displayed at
the start of the notebook. All its training words are already supplied.

## Your task

1. **Predict a merge.** Each corpus entry gives a word and how often it occurs. Tokens initially are characters. Predict the most frequent adjacent pair and justify it using contributions from at least two words. Record your prediction before completing TODO 1.
2. **Build the two BPE steps.** In TODO 1, return weighted pair frequencies from the current token lists. In TODO 2, return a new list after applying one selected merge left to right without overlaps. Read the notebook's input/output contracts and boundary rules. The supplied trainer selects the winning pair, recounts and runs three rounds. Use the feedback, then explain one change between successive rounds.
3. **Change one training frequency.** Keep the baseline. Predict what will happen when only `can` changes from frequency 10 to 20; then run that change. Compare the merge order and the final pieces for `maps`. Give a frequency-based explanation for one changed choice. Predict how each trained tokenizer splits the unseen word `rap`, then reveal the results. Explain why encoding this new word does not retrain the tokenizer.
4. **Connect to context.** Open the prepared real-tokenizer/context section. Choose one change that makes the supplied request fit, state its tradeoff, and explain why this toy does not establish a real model's speed or answer quality. No extra coding is needed.

## Bring back

Download one findings file containing your prediction, both three-round traces, the probe-word comparison, and your shared explanation. State one limitation of the character-based toy. Include the context decision in the conclusion field. Both partners should be able to explain the result; swap editor/checker halfway.

Save Python code as well: saving the notebook does not preserve browser text fields. If blocked, open a folded concept check or ask for a room visit. Honest unchanged results count as evidence when explained.

## Timebox

2 minutes to predict, 7 to implement, 4 to compare/explain, 2 to record/export. Return at the trainer's announced time. If you finish early, predict one further merge and justify it before testing.
