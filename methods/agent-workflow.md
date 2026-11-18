# Working with agents on hardware projects

How a larger hardware build was run with AI agents writing most of its CAD, firmware and host software,
and what carried over. A project made from `templates/project/` starts with all of this in place.

## Files that keep a project's memory

Anything said only in chat is lost. If it matters for the build, it goes in a file.

| File | Holds | Rule |
|---|---|---|
| `log/decisions.md` | Choices we have **made** | Dated, with a short rationale and what would make us revisit it. Append; supersede with a new entry. An "In force" table at the top |
| `log/open-questions.md` | Things **still being discussed** | Options and trade-offs. An entry moves to decisions when settled |
| `log/status.md` | Where the build **is now** | A snapshot of about 60 lines. Overwrite freely |
| `log/todo.md` | What's next | Short and ordered. No completed items |
| `log/journal.md` | What happened, by date | Append-only: measurements, builds, results, reasons |

**Archive by day.** `journal.md` and `decisions.md` hold only the latest day. Running `ws-archive-logs` moves older
entries into `log/archive/{journal,decisions}/YYYY-MM-DD.md`. Find an entry with
`grep -rn '^## .*<words>' log/` and read up to the next `## `. Agents append to the journal with a heredoc and
do not read it. If you need old history to understand the current design, the reference doc is missing
something: fix the doc.

## Rules that kept the agents honest

- **No unmeasured numbers** (`cad-in-code.md`). This forced a caliper or a STEP file before every part.
- **Passing a simulator is not hardware acceptance.** Keep a list of unverified assumptions in the
  software doc, each with the physical check that clears it.
- **Look at the pictures.** Photos of the real hardware in `images/` settle fit questions faster than
  reasoning does. Use JPEG, because agents cannot open `.jxl` (`tools/images.sh` converts them).
- **Keep files small.** CI runs `ws-check-file-sizes`, which fails past 800 lines or when an allowlisted file
  grows. Give a new feature for a large file a new module.
- **Keep docs about the current design.** History goes in the journal and decisions.
- **Explain the engineering.** Spell a term out the first time it appears, and say why a choice matters. Don't
  dumb it down.
- **Say who may do what with each machine** (`equipment/README.md`). An agent may slice and check
  freely. A person's word starts anything that moves or heats.

## Parallel agents

Several agents can work in one repo at once:

- Specialist agents change their own code, docs and tests, append to the journal, commit only their
  own paths, and finish with a short hand-off.
- One integrating session reconciles the shared files: `status.md`, `todo.md`, and the "In force" table.
- If you must touch a shared file, re-read it immediately before editing and change only your lines.

## A north star

Once the question is clear, write it at the top of `AGENTS.md`, with the one metric that says whether the work moved.
Before starting any new instrument, study or figure, an agent should be able to say in one sentence which step of the
critical path it unblocks. Without that sentence, agents drift into polishing parked work.
