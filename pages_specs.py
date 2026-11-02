"""DAC, DPC and slice 1. Numbers and rows are read from data-platform-catalog, so the lessons cannot drift."""
from pathlib import Path

import yaml

from kit import box, arrow, text, num, fig, table, note
from reg import page, link, src

CAT = Path.home() / "data-platform-catalog"


def _load(folder):
    return [r for f in sorted((CAT / folder).glob("*.yaml")) for r in yaml.safe_load(f.read_text()) or []]


OBL = {r["id"]: r for r in _load("dac/obligations")}
CAPS = {c["id"]: c for c in _load("dpc/capabilities")}
PORTS = yaml.safe_load((CAT / "dpc" / "ports.yaml").read_text())
TRIAGE = yaml.safe_load((CAT / "dac" / "triage.yaml").read_text())
CONCERNS = yaml.safe_load((CAT / "core" / "concerns.yaml").read_text())
WORLD = yaml.safe_load((CAT / "slices" / "01-orders" / "world.yaml").read_text())
BIND = yaml.safe_load((CAT / "slices" / "01-orders" / "binding-databricks.yaml").read_text())


@page("dac", "What must be true? The Data Assurance Catalog", short="DAC: must be true",
      blurb="Rules a platform must keep, each with a failure story and a test.")
def dac():
    o = OBL["DUP-01"]
    new = [r for r in OBL.values() if not r.get("review_check")]
    core = sum(r["core"] for r in OBL.values())
    out = "<p class='lead'>Start with a story. After an outage, the shop's system resends yesterday's file. The " \
          "pipeline loads it again as if it were new, and the dashboard shows sales doubled. Nobody notices for a day.</p>"
    out += "<p>The rule that stops this is one sentence: <b>a file delivered a second time must not change any total.</b> " \
           "DAC is a list of sentences like that one. Each comes with the story of what goes wrong without it, and " \
           "the test that proves a platform keeps it. We call each one an <b>obligation</b>.</p>"
    d = ""
    parts = [("Statement", "the rule, with MUST"), ("Failure story", "what goes wrong"), ("Test", "how to prove it"),
             ("Evidence", "what a pass leaves behind"), ("Cites", "the standard it points to")]
    for i, (t, s) in enumerate(parts):
        d += box(10 + i * 196, 30, 176, 90, t, s, "solid" if i == 0 else "bx")
        if i:
            d += arrow(10 + i * 196 - 18, 75, 10 + i * 196 - 2, 75)
    out += fig(990, 140, d, "The parts of one obligation", "One obligation, five parts. Read left to right.")
    out += table(["Part", f"For {o['id']}"], [
        ["Statement", o["statement"]], ["Failure story", o["failure_mode"]], ["Test", o["test"]],
        ["Evidence", o["evidence"]], ["Cites", ", ".join(f"{c['standard']}: {c['ref']}" for c in o["cites"])]])
    out += "<h2>Where the rules came from</h2>"
    out += f"<p>We did not start from a blank page. Our public review tool, data-project-review, already had 91 " \
           f"technical checks, tested blind on a sample project, where they found 27 of 27 planted gaps. Those checks " \
           f"are questions a reviewer asks about a project's documents. We kept the ones a running platform can be " \
           f"tested for, with the same ids, so a review finding and a failing test point at the same rule.</p>"
    out += table(["What happened to the 91 checks", "How many", "Example"], [
        ["Became an obligation", len(TRIAGE["obligation"]), "DUP-01: a file sent twice changes no total"],
        ["Stayed a review question only", len(TRIAGE["review_only"]), "EST-02: an estimate given as one number instead of a range. A platform cannot be tested for that."],
        ["New rules nobody else writes down", len(new), "GATE-01: a check that looked at zero rows must report an error, not a pass"],
    ])
    out += f"<p>That makes <b>{len(OBL)} obligations</b>, {core} of them <b>core</b>, meaning every platform owes " \
           f"them whatever its shape.</p>"
    out += "<h2>The rules nobody else writes down</h2>"
    out += "<p>Open standards such as ODCS already say how to write a quality rule for one table. What they do " \
           "not say is what the platform as a whole must promise. These are the rules we add:</p>"
    out += table(["Id", "Rule", "Why it matters"], [[r["id"], r["statement"], r["failure_mode"]] for r in new])
    out += note("Cite, never copy", "<p>When a rule overlaps an open standard, the obligation points to it by " \
                "name and field (for example the ODCS field <code>quality[].metric = duplicateValues</code>) instead " \
                "of repeating it. When the standard changes, our rule stays put.</p>")
    out += f"<p class='deeper'>Every obligation: {src('dac/INDEX.md', 'the DAC index')}. The record format and the " \
           f"counts: {src('dac/README.md', 'dac/README.md')}.</p>"
    return out


@page("dpc", "What must exist? Parts, plugs and products", short="DPC: must exist",
      blurb="Capabilities are the parts; ports are the plugs; a binding says which product sits behind each plug.")
def dpc():
    c = CAPS["DPC-0024"]
    core_ports = [p for p in PORTS if p["tier"] == "core"]
    out = "<p class='lead'>A rule such as \"a file sent twice changes no total\" says what must be true. It does not " \
          "say what you have to build. DPC answers that: the <b>parts</b> a platform must have, and the <b>plug</b> " \
          "each part is reached through.</p>"
    d = box(10, 40, 190, 100, "Obligation (DAC)", ["DUP-01", "a file sent twice", "changes no total"])
    d += arrow(202, 90, 268, 90, "kept by", ly=72)
    d += box(270, 40, 200, 100, "Capability (DPC)", ["DPC-0024", "every write carries", "a batch key"], "solid")
    d += arrow(472, 90, 538, 90, "through", ly=72)
    d += box(540, 40, 190, 100, "Port", ["table_writer", "the plug"])
    d += arrow(732, 90, 798, 90, "served by", ly=72)
    d += box(800, 40, 180, 100, "Product", ["named only in", "the binding"], "bxm")
    out += fig(990, 170, d, "From rule to product", "Follow one rule all the way to a product. Only the last box names a vendor.")
    out += "<h2>Why plugs?</h2>"
    out += "<p>Think of a wall socket. The kettle does not care which power station made the electricity. A " \
           "<b>port</b> is that socket for data: our code always talks to <code>table_writer</code>, and on each cloud a " \
           "small adapter connects it to whatever product does the writing. Moving to another cloud means new " \
           "adapters, not a rewrite.</p>"
    out += f"<h2>One capability, in full</h2>"
    rows = [["Requirement", c["requirement"]], ["Failure story", c["failure_mode"]], ["Port", c["port"]],
            ["Keeps these rules", ", ".join(c["discharges"])]]
    out += table(["Part", f"{c['id']}: {c['title']}"], rows)
    for dd in c.get("design_decisions") or []:
        out += note(f"Decide: {dd['question']}", f"<p><b>The pull both ways.</b> {dd['tension']}</p>"
                                                f"<p><b>Our answer.</b> {dd['resolution']}</p>")
    out += f"<h2>The plugs</h2><p>{len(PORTS)} ports so far, {len(core_ports)} of them needed by every platform " \
           f"(core). Each port lists what our own code decides and what the product brings.</p>"
    svc = {"A": "Acquire", "B": "Model", "C": "Serve", "platform": "Platform"}
    out += table(["Port", "Service", "What it does", "Our code decides"],
                 [[f"<code>{p['port']}</code>", svc[p["service"]], p["summary"].strip(), p["kernel_owns"].strip()]
                  for p in core_ports])
    out += f"<p>{len(CAPS)} capabilities exist so far, all written for {link('slice1', 'slice 1')}. They keep " \
           f"{len({d for c in CAPS.values() for d in c['discharges']})} of the {len(OBL)} rules. The rest " \
           f"(gold, metrics, dashboards, cost, access) arrive with later slices.</p>"
    out += f"<p class='deeper'>The ports file: {src('dpc/ports.yaml', 'dpc/ports.yaml')}. The capabilities: " \
           f"{src('dpc/capabilities/', 'dpc/capabilities/')}.</p>"
    return out


@page("slice1", "Slice 1: orders, from the shop's database to silver", short="Slice 1: orders",
      blurb="Seven pretend days, four planted problems, and all five specs on one small path.")
def slice1():
    out = "<p class='lead'>Writing every rule for every stage before building anything is how specs go stale. So we " \
          "take one thin path, orders from the shop's database to silver, write all five specs for just that path, " \
          "build it, and let the build tell us where the specs are wrong.</p>"
    d = ""
    days = WORLD["clock"]["days"]
    by_day = {e["day"]: e for e in WORLD["calendar"]}
    labels = {"duplicate_delivery": ["same file", "sent twice"], "source_delete": ["3 orders", "deleted"],
              "late_change": ["old change", "arrives late"], "renamed_column": ["amount", "renamed"]}
    d += arrow(10, 70, 980, 70)
    for i in range(1, days + 1):
        x = 20 + (i - 1) * 138
        d += text(x + 55, 50, f"Day {i}", "lbl", "middle")
        e = by_day.get(i)
        if e:
            d += box(x, 95, 112, 80, labels[e["kind"]][0], labels[e["kind"]][1], "solid")
            d += text(x + 56, 200, f"must notice: {e['expect']['detector']}", "sm", "middle")
        else:
            d += box(x, 95, 112, 80, "normal", "day", "bxm")
    out += fig(990, 220, d, "The seven-day world for slice 1",
               "The pretend shop runs for seven days. On four of them, it breaks something on purpose.")
    out += "<p>The <b>world</b> (the DWD file) is a pretend shop. It sends orders every night and, on set days, " \
           "plants a problem. For each problem it names which rule must notice it and which part must handle it. " \
           "At the end, the world compares silver with what it knows is true. It never trusts the platform's own logs.</p>"
    out += table(["Day", "What the world does", "Must notice", "Must handle it", "Judged by"],
                 [[e["day"], e["does"], e["expect"]["detector"],
                   ", ".join(f"{h} {CAPS[h]['title'].lower()}" for h in e["expect"]["handled_by"]), e["expect"]["oracle"]]
                  for e in WORLD["calendar"]])
    out += "<h2>The five files</h2>"
    out += table(["File", "Spec", "What it holds"], [
        ["orders contract", "ODCS (open standard)", "Columns, key, quality rules, freshness. It passes the official ODCS schema check."],
        ["orders manifest", "DPM", "How orders are loaded: history by change sequence, deletes from the change feed, a batch key, tolerances."],
        ["shop world", "DWD", "Clock, change feed, population and the four planted problems."],
        ["Databricks binding", "DBS", "Which product sits behind each plug, and what no product does."],
        ["capabilities", "DPC", f"The {len(CAPS)} parts slice 1 needs."],
    ])
    binds = BIND["bindings"]
    word = {"full": "Databricks covers it", "partial": "Databricks covers part", "none": "Databricks has nothing"}
    full = sum(b["coverage"] == "full" for b in binds.values())
    out += f"<h2>What Databricks does, and what we add</h2><p>The rule for every binding: use what the platform " \
           f"offers as much as possible, fill only the gap, drive it all from the metadata, and connect the dots. " \
           f"For slice 1, Databricks covers {full} of the {len(binds)} plugs completely. For the rest, the binding " \
           f"says what is missing and who fills it:</p>"
    out += table(["Plug", "Coverage", "What is missing", "Filled by"],
                 [[f"<code>{p}</code>", word[b["coverage"]], b.get("gap", ""),
                   (b.get("gap_filled_by") or {}).get("approach", "")]
                  for p, b in binds.items() if b["coverage"] != "full"])
    out += note("Next", "<p>Build slice 1 on Databricks Free Edition, run the seven days, and change the specs " \
                "wherever the build shows a rule is wrong or missing.</p>")
    out += f"<p class='deeper'>All five files: {src('slices/01-orders/', 'slices/01-orders/')}.</p>"
    return out
