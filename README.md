# Data Engineering Tutorial

Hand-drawn, question-first lessons on how data platforms work, from the till to the dashboard. Source for
[cleandataengineering.ai/learn/](https://cleandataengineering.ai/learn/), where the simulators (DataTwin Studio,
Delta and Spark internals, the Problem Lab) are already live.

Lessons so far (each is added as a piece of the platform is settled):

| Page | What it teaches |
|---|---|
| Start here | The spine, the four problems every team meets, the five specifications, where the work is |
| Words | Every term in plain language |
| DAC: must be true | What an obligation is, where the 66 came from, the rules nobody else writes down |
| DPC: must exist | Parts, plugs (ports) and products; one capability in full with its design decision |
| Slice 1: orders | The seven-day world, four planted problems, the five files, what no product does |

The spec pages read their numbers from [data-platform-catalog](https://github.com/dataagentsai/data-platform-catalog)
(expected beside this folder), so a lesson cannot drift from the spec.

```bash
uv run --with pyyaml python build.py   # writes site/
```

The drawing kit (`kit.py`) is copied from agent-harness-tutorial.
