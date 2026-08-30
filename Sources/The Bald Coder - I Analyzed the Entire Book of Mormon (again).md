---
aliases:
  - "The Bald Coder - Book of Mormon Embedding Analysis"
  - "I'm a Data Scientist. I Analyzed the ENTIRE Book of Mormon (again)."
  - "The Bald Coder - I Analyzed the Entire Book of Mormon Again"
tags:
  - source/video
  - by/the-bald-coder
  - tradition/lds
  - topic/book-of-mormon
  - topic/data-analysis
  - topic/embeddings
date: ""
author: "The Bald Coder"
url: "https://youtu.be/tKE2HFiXkw8"
authority: C
authority_reason: "A follow-up to the creator's first Book of Mormon data-analysis video, rebuilt to answer its critics. He replaces the black-box LLM scoring (Gemini) with a small, non-generative embedding model and cosine similarity — a genuinely more transparent and reproducible method, since the vector math is inspectable rather than a hidden LLM judgment. But he explicitly disclaims the work as 'by no means academic,' not peer-reviewed, and something you should 'under no circumstances consider scientific in any way'; the 27 thematic probes are hand-written, the embedding model is still trained on human text, and the final 'good fruit' verdict is his own interpretation. Informed, honest, popular-level commentary — tier C, not a scholarly study."
---

# The Bald Coder - I Analyzed the Entire Book of Mormon (again)

A follow-up video in which an LDS data-science creator **re-runs** his earlier thematic analysis of scripture after critics objected that the first version just asked a large language model to "make up a score." This time he uses a **non-generative embedding model**: every verse of four texts — the Old Testament, New Testament, Book of Mormon and Quran (60,000+ verses) — is converted to a vector, and 27 hand-written natural-language "probes" (e.g. *Jesus Christ*, *atonement*, *equality*) are ranked against each verse by **cosine similarity**. He tests the same three claims as before: the Book of Mormon is Christ-centered, it teaches good ethical principles, and it therefore passes Jesus's "by their fruits" test in [[Matthew 7.15-20|Matthew 7]]. He opens by disclaiming the analysis as non-academic, non-peer-reviewed, and not scientific.

## Summary

- **Method upgrade (answering the black-box critique).** The switch from Gemini (an LLM that "already has context on the Bible and Book of Mormon" and behaves as a black box) to a small embedding model that "runs directly on my laptop" is the whole point of the re-do — cosine similarity between verse-vectors and a probe is inspectable vector math, not a hidden generative judgment. It only partly escapes the guardrail in [[A Data Analysis of Scripture Is Only as Objective as Its Model]]: the embedding model is still trained on human text, and the probe wording and final interpretation remain the creator's.
- **Christ-centered result replicates.** The new method reproduces the first video's ranking — New Testament and Book of Mormon in a near-tie for most Christ-centered (the NT edges first, so the Book of Mormon lands second), Old Testament third, Quran last. The single most Christ-centered verse across all four texts is [[3 Nephi 9|3 Nephi 9:21]]. See [[The Book of Mormon Scores Higher Than the Bible on Christ-Centeredness]].
- **Shared universal morality.** Probes built on named human-rights/ethics frameworks (the UN Universal Declaration of Human Rights, an academic standard, and Pew Research) find the Book of Mormon teaches principles like care, equality and justice at rates comparable to the Bible; taking the cosine similarity of every text's moral profile, all four align at ≥95%. See [[The Book of Mormon Teaches Universal Moral Principles Shared Across Scripture]].
- **"Good fruit" — but for everyone.** He concludes the Book of Mormon passes the [[Matthew 7.15-20|Matthew 7]] test as good fruit, while applying the *identical* verdict to the Old Testament, New Testament and Quran — "we have so much more in common than we do differences." See [[The Book of Mormon Passes the Matthew 7 By Their Fruits Test]].

## Concepts Discussed

- [[The Book of Mormon Scores Higher Than the Bible on Christ-Centeredness]] — updated with this video's embedding-model replication
- [[The Book of Mormon Teaches Universal Moral Principles Shared Across Scripture]]
- [[The Book of Mormon Passes the Matthew 7 By Their Fruits Test]]
- [[A Data Analysis of Scripture Is Only as Objective as Its Model]]
- [[Spiritual Confirmation Not Data Is Why People Keep Reading Scripture]]

## References

[^1]: [[The Bald Coder - I Analyzed the Entire Book of Mormon (again)|Bald Coder — BoM Embedding Analysis]], [04:00], https://youtu.be/tKE2HFiXkw8

---
See also: [[Sources]] · [[The Bald Coder]] · [[The Book of Mormon Scores Higher Than the Bible on Christ-Centeredness]] · [[The Book of Mormon Teaches Universal Moral Principles Shared Across Scripture]] · [[The Book of Mormon Passes the Matthew 7 By Their Fruits Test]] · [[Matthew 7.15-20|Matthew 7:15-20]]
