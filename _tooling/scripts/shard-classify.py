#!/usr/bin/env python
"""DRY-RUN domain classifier for Concepts/. Classifies each root-level note by its
TAGS (YAML + inline #apologetics//#topic//#tradition/ hashtags) and TITLE only --
NOT the prose body (body words like "culture"/"protestant" cause false matches).
Writes a manifest (domain<TAB>filename) and prints the distribution. MOVES NOTHING."""
import os, re, glob
from collections import Counter

CONC = r"C:\Users\Josep\hermes-advocate\Concepts"
MANIFEST = r"C:\Users\Josep\AppData\Local\hermes\scripts\_shard-manifest.tsv"

# (substring-in-tag, domain), priority order: specific topical tags first,
# broad LDS tags (joseph-smith, restoration) last so they don't swallow specifics.
TAG2DOM = [
 ("debate-map","debate-maps"),
 ("book-of-mormon-witness","book-of-mormon"), ("book-of-mormon","book-of-mormon"),
 ("temple","temple-priesthood"), ("priesthood","temple-priesthood"), ("masonry","temple-priesthood"),
 ("trinity","god-trinity"), ("nature-of-god","god-trinity"), ("divine-council","god-trinity"),
 ("creation-ex-nihilo","god-trinity"), ("theosis","god-trinity"), ("deification","god-trinity"),
 ("godhead","god-trinity"), ("divine-investiture","god-trinity"),
 ("problem-of-evil","problem-of-evil"), ("hell","problem-of-evil"), ("free-will","problem-of-evil"),
 ("theodicy","problem-of-evil"),
 ("grace","salvation-grace"), ("atonement","salvation-grace"), ("salvation","salvation-grace"),
 ("soteriolog","salvation-grace"), ("justification","salvation-grace"),
 ("atheism","natural-theology"), ("fine-tuning","natural-theology"), ("evolution","natural-theology"),
 ("cosmolog","natural-theology"), ("science","natural-theology"), ("fine_tuning","natural-theology"),
 ("canon","bible-canon"), ("sola-scriptura","bible-canon"), ("biblical-origins","bible-canon"),
 ("old-testament","bible-canon"), ("new-testament","bible-canon"), ("textual","bible-canon"),
 ("biblical-studies","bible-canon"),
 ("catholic","other-religions"), ("protestant","other-religions"), ("islam","other-religions"),
 ("creed","other-religions"), ("papacy","other-religions"), ("orthodox","other-religions"),
 ("evangelical","other-religions"), ("reformation","other-religions"),
 ("abortion","ethics-culture"), ("marriage","ethics-culture"), ("ethics","ethics-culture"),
 ("gender","ethics-culture"), ("sexual","ethics-culture"), ("morality","ethics-culture"),
 ("method","method-epistemology"), ("epistemolog","method-epistemology"),
 ("faith-crisis","method-epistemology"), ("critical-response","method-epistemology"),
 ("historiograph","method-epistemology"), ("historical-method","method-epistemology"),
 ("polygam","joseph-smith"), ("first-vision","joseph-smith"), ("prophecy","joseph-smith"),
 ("joseph-smith","joseph-smith"), ("book-of-abraham","joseph-smith"),
 ("restoration","restoration-history"), ("apostasy","restoration-history"),
 ("church-history","restoration-history"), ("mormonism","restoration-history"),
 ("adam-god","restoration-history"), ("word-of-wisdom","restoration-history"), ("lds","restoration-history"),
]
# TITLE fallback (regex on filename), used only when no tag matched. Broad LDS last.
TITLE = [
 ("book-of-mormon", r"\bnephi|\blehi\b|jaredite|\balma\b|chiasm|nahom|cumorah|\bmulek|zarahemla|mosiah|king benjamin|brass plates"),
 ("temple-priesthood", r"temple|endowment|priesthood|masonry|freemason|\bgarment|\bordinance|\bsealing"),
 ("god-trinity", r"trinit|godhead|\bgod\b|divine|theosis|deifi|exaltation|ex nihilo|embodi|impassib|omni|monotheism"),
 ("problem-of-evil", r"problem of evil|\bhell\b|theodicy|free will|determinism|suffering|universalis"),
 ("salvation-grace", r"\bgrace\b|atonement|salvation|justification|faith alone|\bworks\b|repentance"),
 ("natural-theology", r"atheis|fine.tuning|cosmolog|\bkalam|design|evolution|darwin|big bang|naturalis|\bgod exists"),
 ("bible-canon", r"\bcanon|sola scriptura|\bbible\b|scripture|manuscript|translation|testament|gospel|\bpaul|isaiah|deuteronom|septuagint|allein"),
 ("other-religions", r"\bluther|calvin|catholic|\bpope\b|papac|protestant|\bcreed|nicaea|nicene|\bislam|\bquran|reformation|trent|orthodox"),
 ("ethics-culture", r"abortion|marriage|\bgender|sexual|\bfamily\b|feminis|slavery|\brace\b|\bwoke"),
 ("joseph-smith", r"joseph smith|first vision|polygam|plural marriage|kinderhook|seer stone|nauvoo|kirtland|book of abraham|witness"),
 ("method-epistemology", r"\bmethod|epistem|faith crisis|presentism|rhetoric|fallac|steelman|burden of proof|historian"),
]
TITLE = [(d, re.compile(p, re.I)) for d, p in TITLE]

def classify(name, txt):
    m = re.match(r'^---\n(.*?)\n---', txt, re.S)
    tagblob = ""
    if m:
        tm = re.search(r'^tags:\s*(.*)$((?:\n[ \t]+-.*)*)', m.group(1), re.M)
        if tm: tagblob = (tm.group(1) or "") + " " + (tm.group(2) or "")
    tagblob += " " + " ".join(re.findall(r'#[A-Za-z0-9/_-]+', txt))
    tl = tagblob.lower()
    for key, dom in TAG2DOM:
        if key in tl:
            return dom, "tag"
    for dom, rx in TITLE:
        if rx.search(name):
            return dom, "title"
    return "restoration-history", "default"  # generic LDS apologetics catch-all

dist = Counter(); src = Counter(); manifest = []
for f in sorted(glob.glob(os.path.join(CONC, "*.md"))):
    base = os.path.basename(f); name = base[:-3]
    if name == "Concepts": continue
    try: txt = open(f, encoding="utf-8", errors="replace").read()
    except Exception: txt = ""
    dom, how = classify(name, txt)
    dist[dom]+=1; src[how]+=1; manifest.append((dom, base))

with open(MANIFEST,"w",encoding="utf-8") as out:
    for dom, base in manifest: out.write(f"{dom}\t{base}\n")

print(f"Total: {len(manifest)}   (by tag: {src['tag']}, by title: {src['title']}, default->restoration: {src['default']})\n")
for d,c in sorted(dist.items(), key=lambda kv:-kv[1]):
    flag = "   <== OVER 1000!" if c>1000 else ""
    print(f"  {c:5d}  {d}{flag}")
