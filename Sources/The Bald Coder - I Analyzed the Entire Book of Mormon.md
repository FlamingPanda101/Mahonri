---
aliases:
  - "The Bald Coder - Book of Mormon Data Analysis"
  - "I'm a Data Scientist. I Analyzed the ENTIRE Book of Mormon."
tags:
  - source/video
  - by/the-bald-coder
  - tradition/lds
  - topic/book-of-mormon
  - topic/data-analysis
date: ""
author: "The Bald Coder"
url: "https://youtu.be/iHc1YDraCWs"
authority: C
authority_reason: "An LDS data-science hobbyist with a master's in data science who ran an LLM-scored sentiment/thematic analysis of the Book of Mormon and Bible. Honest about method limits (the author himself disclaims it as proof), but the scoring is fully LLM-generated (Gemini), unvalidated, and not peer-reviewed — informed-but-uncited C-tier commentary, not a scholarly study."
---

# The Bald Coder - I Analyzed the Entire Book of Mormon

A short video in which an LDS creator with a master's degree in data science applies **natural-language processing** to score every chapter of the Book of Mormon and the Bible on two axes — how **Christ-centered** the text is (1–10) and how **moral/ethical** it is (1–10) — then compares the distributions. He frames the Christ-centered test as an application of Jesus's "by their fruits ye shall know them" ([[Matthew 7.15-20|Matthew 7:15–20]]) and explicitly hedges the conclusion, warning that the scores were produced by a large language model trained on biased human data and are not proof of anything.

## Summary

- **Method.** Each chapter's text was fed to the Gemini API with two scoring prompts (Christ-centeredness and morality, each 1–10 with a rationale), then summary statistics were visualized. This is [[A Data Analysis of Scripture Is Only as Objective as Its Model]] — the technique borrows the objectivity of sentiment analysis but inherits the model's biases. See [[The Book of Mormon Scores Higher Than the Bible on Christ-Centeredness]].
- **Results.** The Book of Mormon's mean Christ-centeredness (7.89) exceeds the whole Bible's (5.11) and is comparable to the New Testament's (9.12) while spanning a far broader period (≈600 BC–AD 400); its mean morality score (9.03) is near the New Testament's (9.06). The creator concludes the book would register as "good fruit" on the Matthew 7 test — testifying of Christ and inviting moral living.
- **Self-undercutting caveat.** The video's own thesis is that no data analysis (of the Book of Mormon *or* the Bible) can settle a book's truth, because "you cannot definitively say whether or not this is true regardless of what technology you're using"; people keep reading scripture because of spiritual experience, not statistics — see [[Spiritual Confirmation Not Data Is Why People Keep Reading Scripture]].

## References

[^1]: [[The Bald Coder - I Analyzed the Entire Book of Mormon|The Bald Coder - Book of Mormon Data Analysis]], [02:30], https://youtu.be/iHc1YDraCWs

---
See also: [[Sources]] · [[The Book of Mormon Scores Higher Than the Bible on Christ-Centeredness]] · [[A Data Analysis of Scripture Is Only as Objective as Its Model]] · [[Matthew 7.15-20|Matthew 7:15-20]]
