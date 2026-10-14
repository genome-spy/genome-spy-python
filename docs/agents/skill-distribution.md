# Agent skill installation and distribution

Available in builds from this checkout. Live deployment follows the existing
documentation release/manual-dispatch policy; a local build is not proof of a
published endpoint.

## Install explicitly

After installing the Python package, install the visualization skill for both
agents in the current project:

```bash
genome-spy-install-skills
```

Choose an agent or a different scope:

```bash
genome-spy-install-skills --agent codex --project /path/to/project
genome-spy-install-skills --agent claude --user
genome-spy-install-skills --user --agent both
```

| Agent | Project root | Personal root |
| --- | --- | --- |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

The installer creates a `create-genomespy-visualization/` folder under each
selected root, including `SKILL.md`, `agents/openai.yaml`, and every reference.
These locations follow the current official
[Codex](https://learn.chatgpt.com/docs/build-skills) and
[Claude Code](https://code.claude.com/docs/en/skills) documentation.
Use a new agent session if the installed skill is not yet visible.

Installation is opt-in. Importing the library and installing the Python package
do not write into agent configuration. Tests use temporary projects and simulated
personal roots; no personal skill directories were changed during verification.

## Existing installations and upgrades

An identical installed folder is reported as unchanged without rewriting it.
A modified folder, including extra files, is refused unless `--force` is supplied.
All selected destinations are checked for conflicts before copying any skill.
Symlink destinations and destinations that are files are refused even with force.

To replace an installed skill after upgrading the package:

```bash
genome-spy-install-skills --agent both --project /path/to/project --force
```

**Force replaces the complete skill folder**, including removing obsolete or
locally added files. Save any edits you want to retain before using it. A replacement
is staged first, and the old folder is restored if the final rename fails.

To inspect the bundled source without installing:

```bash
genome-spy-install-skills --print-path
```

## One canonical source

Maintain only `skills/create-genomespy-visualization/` in the repository. The wheel
build maps that folder into the package resource
`genome_spy/skills/create-genomespy-visualization/`. The source distribution includes
the same canonical source and build mapping. Installed agent folders are generated
copies, not additional editable sources.

Editable development installs read the canonical checkout folder when a bundled
resource is absent. Regular installed wheels use the packaged resource and do not
require a repository checkout. From a checkout, the installer can also be invoked
with `uv run genome-spy-install-skills` or
`uv run python -m genome_spy._skill_install`.

## Comparison with other libraries

[Flexviz's installer](https://github.com/flex-analytics/flexviz/blob/main/flexviz/cli.py)
reads its skill from `flexviz/skills/flexviz-explore/SKILL.md` using package
resources and copies it into project `.agents/skills/` and `.claude/skills/`.
It also supports user scope and refuses changed destination content unless forced.
Its single skill contains a concrete end-to-end workflow tied to its CLI and live
state API. That live exploration scope is broader than this authoring skill.

[Tangermeme's skill router](https://github.com/jmschrei/tangermeme/blob/main/tangermeme/_skills/data/SKILL.md)
links topic-specific reference files loaded on demand. Its
[installer](https://github.com/jmschrei/tangermeme/blob/main/tangermeme/_skills/install.py)
copies the complete bundled directory, defaults to a personal Claude directory,
supports a custom destination and source-path inspection, and requires an explicit
force option for replacement. Installation is opt-in rather than an import side
effect.

Our router plus bundled references already follows progressive disclosure.
Grouped-chart detail has now been split into `references/grouped-charts.md` so a
simple table-chart request does not need the full distribution/clustering material.
The installer now closes the packaging and discovery gap for explicit local
installation. Successful HTML builds also publish separate agent Markdown and
the `llms.txt` index.

## Verification and remaining work

The wheel built from the source distribution contains all four skill files
byte-for-byte. Verification installed that wheel into an isolated environment,
ran outside the repository, and checked both agent destinations, complete relative
references, identical reinstall, conflict refusal, and forced update. Installer
tests also cover simulated personal scope, symlink refusal and replacement rollback.

Curated agent Markdown is routed by `docs/agents/manifest.json` and copied to
`agents/` after successful HTML builds; user guides and gallery examples publish
beside their HTML pages. `llms.txt` links to these explicit Markdown endpoints. The
focused API page is generated from current Python signatures; canonical skill references are reused without maintained copies.
The index also lists user guides and gallery examples grouped by their existing
categories. Markdown exports expand tutorial code includes and preserve explanations
from the maintained sources, so improvements reach agents on the next build.
The existing Pages workflow uploads these outputs with HTML and deploys only on
release or manual dispatch. Verify live URLs after deployment; failed access uses
bundled/local fallback guidance. Human Sphinx parsing excludes `docs/agents/`
because publication is plain Markdown. This installer does not install plugins
or configure cloud agents.
