"""Start here and the glossary."""
from kit import box, arrow, text, num, fig, table, note
from reg import page, link


def spine(y=40):
    """The spine: data moves one way, left to right."""
    names = [("Shop's", "database"), ("Landing", "as received"), ("Bronze", "everything"), ("Silver", "cleaned"),
             ("Gold", "shaped"), ("Semantic", "metrics"), ("Dashboard", "people")]
    d, w, gap = "", 112, 28
    for i, (t, s) in enumerate(names):
        x = 10 + i * (w + gap)
        d += box(x, y, w, 80, t, s, "solid" if t == "Silver" else ("bxm" if i in (0, 6) else "bx"))
        if i:
            d += arrow(x - gap + 2, y + 40, x - 4, y + 40)
    return d


@page("index", "Start here: what are we building, and why?", short="Start here",
      blurb="A shop's till, a dashboard, and the five questions every data platform has to answer.")
def index():
    d = spine()
    d += text(500, 160, "Data moves one way. Every arrow is a place where something can go wrong.", "tx", "middle")
    out = "<p class='lead'>A clothing shop sells a shirt. A few hours later, the owner opens a dashboard and sees " \
          "the day's sales. Between the till and the dashboard sits a <b>data platform</b>: the machinery that copies, " \
          "cleans and shapes the numbers. This tutorial is about building that machinery so the number on the " \
          "dashboard is right, and so you can prove it.</p>"
    out += fig(990, 180, d, "The data spine from the shop's database to the dashboard",
               "The spine. Each box is a stage; the dark one, silver, is where slice 1 ends.")
    out += "<h2>Four things that go wrong in the first week</h2>"
    out += table(["What happens", "What the dashboard shows if nobody planned for it"], [
        ["The shop's system sends yesterday's file again after an outage", "Sales doubled for a day"],
        ["A cancelled order is deleted at the source", "The order still counted, so sales are too high"],
        ["An old change arrives after a newer one", "An order shows the wrong status"],
        ["Someone renames the <code>amount</code> column", "Sales quietly drop to zero, and it looks like a bad week"],
    ])
    out += "<p>None of these is rare. Every data team meets all four. The work is to make the platform notice each " \
           "one and handle it the same way every time, on any cloud.</p>"
    out += "<h2>Five questions, five specifications</h2>"
    out += "<p>We write the answers down as five specifications. A <b>specification</b> is a list of rules written " \
           "plainly enough that someone else could build from it and test against it. Four of them never name a " \
           "product, so the same rules hold on Databricks, Microsoft, AWS or Google. Only the last one names products.</p>"
    d = ""
    cards = [("DAC", "What must be TRUE?", "dac.html"), ("DPC", "What must EXIST?", "dpc.html"),
             ("DWD", "What must it FACE?", "slice1.html"), ("DPM", "What does THIS one DO?", "slice1.html"),
             ("DBS", "Which PRODUCT?", "slice1.html")]
    for i, (t, s, h) in enumerate(cards):
        d += box(10 + i * 196, 30, 176, 96, t, s, "bx", href=h)
    out += fig(990, 140, d, "The five specifications", "Click a box to open its lesson.")
    out += table(["Short name", "Full name", "In one sentence"], [
        ["DAC", "Data Assurance Catalog", "Rules that must hold, each with a test: \"a file sent twice changes no total\"."],
        ["DPC", "Data Platform Catalog", "The parts a platform must have, and the plug (port) each part is reached through."],
        ["DWD", "Data World Description", "A pretend shop that sends data and breaks things on purpose, on a calendar."],
        ["DPM", "Data Platform Manifest", "One file per dataset saying how it is loaded; everything is switched on by default."],
        ["DBS", "Data Binding Spec", "For one cloud, which product sits behind each plug. The only place product names appear."],
    ])
    out += "<h2>Where we are</h2>"
    out += table(["Step", "What", "Status"], [
        ["1", "Decide names, repositories and how ingestion works", "Done"],
        ["2", "Check what already exists, so we only build what is missing", "Done"],
        ["3", f"{link('dac', 'DAC')}: what must be true (66 rules)", "Draft done"],
        ["4", f"{link('dpc', 'DPC')}: plugs (22) and parts (32 so far)", "Started"],
        ["5", f"{link('slice1', 'Slice 1')}: orders, from the shop's database to silver, with all five specs", "Spec done"],
        ["6", "Build slice 1 on Databricks, then fix the specs where the build proves them wrong", "Next"],
    ])
    out += note("Words you will meet", f"<p>Bronze, silver, port, obligation, watermark: every word is explained in "
                                       f"plain language on the {link('glossary', 'words page')}.</p>")
    return out


WORDS = [
    ("Spine", "The stages data passes through, always in the same order: source, landing, bronze, silver, gold, semantic, experiences."),
    ("Landing", "A folder where files are kept exactly as they arrived, so a mistake in reading them can be redone."),
    ("Bronze", "Every record as delivered, with a note of when and from which file it came. Nothing is cleaned or removed."),
    ("Silver", "Cleaned data: right types, no duplicates, history kept, bad rows set aside with a reason."),
    ("Gold", "Data shaped for a business question, such as sales per store per day."),
    ("Semantic layer", "The one place where each business number (a metric, such as revenue) is defined."),
    ("Specification (spec)", "A list of rules written plainly enough that someone else could build from it and test against it."),
    ("Obligation", "A rule in DAC that must be true and can be tested, for example \"rerunning a job changes nothing\"."),
    ("Capability", "A part in DPC that must exist, for example \"every write carries a batch key\"."),
    ("Port", "A plug: the fixed shape through which the platform talks to a product. Swap the product, keep the plug."),
    ("Adapter", "The small piece of code that connects one product to one port."),
    ("Binding", "For one cloud, the list of which product sits behind each port."),
    ("Contract", "A file saying what a table promises: its columns, key, quality rules and freshness. We use the open ODCS format."),
    ("Manifest", "One file per dataset saying how it is loaded. Pipelines are generated from it; nobody hand-writes them."),
    ("Mover and lander", "The mover copies bytes from the source into landing; it can be any tool. The lander is our own code that reads landing and writes bronze."),
    ("Watermark", "A bookmark: how far we have read in a source, so the next run starts from there."),
    ("Batch key", "A label on every write saying which delivery it came from, so loading the same delivery twice changes nothing."),
    ("Idempotent", "Safe to repeat: running it twice gives the same result as running it once."),
    ("Quarantine", "A table where rows that failed a rule are kept, with the reason, until someone fixes them."),
    ("Reconciliation", "Comparing counts and totals between stages to prove nothing was lost or doubled."),
    ("Lineage", "A record of which table was made from which, so you can follow a number back to its source."),
    ("Change capture (CDC)", "Reading only what changed in a source database (inserts, updates, deletes) instead of copying it all."),
    ("History (type 2)", "Keeping every version of a row with the dates it was valid, instead of overwriting it."),
    ("Waiver", "Permission to switch a rule off for one dataset, with a reason, an approver and an end date."),
    ("Archetype", "A pipeline's shape, such as a file drop, a database copy or a stream. Each shape owes slightly different rules."),
    ("Thin slice", "One small path built end to end (here: orders, source to silver) before widening, so mistakes show early."),
]


@page("glossary", "The words, in plain language", short="Words",
      blurb="Every term used in these lessons, in one or two sentences.")
def glossary():
    out = "<p class='lead'>Each word is explained the way you would explain it to a friend who has never worked with " \
          "data. If a lesson uses a word that is not here, that is a bug in the lesson.</p>"
    out += table(["Word", "What it means"], [[f"<b>{w}</b>", m] for w, m in WORDS])
    return out
