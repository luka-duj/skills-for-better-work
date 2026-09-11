# Install and try the skills

## Before you start

Use a compatible local Codex or Claude Code installation with access to your files and a writable project. Client subscriptions and permissions are separate from this repository. Installing the instruction package requires no Python, Node.js, API key, GitHub account, or new service. A workflow that later builds a prototype may need tools appropriate to that accepted slice.

## Release availability

This guide covers the public `0.4.0-alpha` pack. After extracting the repository, confirm that `pack.json` lists all six skills before running the install commands.

## Get the files

1. [Download ZIP](https://github.com/luka-duj/skills-for-better-work/archive/refs/heads/main.zip).
2. Extract it. Open the extracted folder containing `README.md`, `skills`, and `LICENSE`.
3. Open a terminal in that folder. In PowerShell use `Set-Location -LiteralPath 'C:/path with spaces/skills-for-better-work-main'`; on macOS/Linux use `cd '/path with spaces/skills-for-better-work-main'`. Replace the example path with your extracted folder.

Alternatively, with Git installed:

```sh
git clone https://github.com/luka-duj/skills-for-better-work.git
cd skills-for-better-work
```

Keep the checkout if you want the repository validator and evaluation fixtures. Copying skill folders alone does not install the repository's checker.

## Codex

Use the user-level `.agents/skills` location documented by OpenAI. Existing `.codex/skills` installations may still be visible in your client; do not install a second copy with the same name. First follow [Update an existing installation](#update-an-existing-installation).

Run the block for your operating system from the extracted repository root. It checks every destination before copying and stops if an existing installation is found.

### PowerShell

```powershell
$ErrorActionPreference = 'Stop'
$skillNames = @('better-work-loop','process-before-platform','shape-the-slice','build-the-slice','prove-before-pilot','prepare-review-handoff')
$skillRoot = Join-Path $env:USERPROFILE '.agents/skills'
foreach ($skillName in $skillNames) {
    $source = Join-Path (Get-Location) "skills/$skillName"
    if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) {
        throw "Missing $source/SKILL.md. Open the extracted repository root first."
    }
    $target = Join-Path $skillRoot $skillName
    $legacy = Join-Path $env:USERPROFILE ".codex/skills/$skillName"
    if ((Test-Path -LiteralPath $target) -or (Test-Path -LiteralPath $legacy)) {
        throw "Existing installation: $skillName. Follow the update instructions first."
    }
}
New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
foreach ($skillName in $skillNames) {
    $source = Join-Path (Get-Location) "skills/$skillName"
    Copy-Item -LiteralPath $source -Destination (Join-Path $skillRoot $skillName) -Recurse -ErrorAction Stop
}
$skillNames | ForEach-Object { Get-Item -LiteralPath (Join-Path $skillRoot "$_/SKILL.md") }
```

### macOS or Linux

```sh
(
set -eu
skill_root="$HOME/.agents/skills"
for skill in better-work-loop process-before-platform shape-the-slice build-the-slice prove-before-pilot prepare-review-handoff; do
  test -f "./skills/$skill/SKILL.md" || { echo "Open the extracted repository root first: missing $skill"; exit 1; }
  if [ -e "$skill_root/$skill" ] || [ -L "$skill_root/$skill" ] || [ -e "$HOME/.codex/skills/$skill" ] || [ -L "$HOME/.codex/skills/$skill" ]; then
    echo "Existing installation: $skill. Follow the update instructions first."
    exit 1
  fi
done
mkdir -p "$skill_root"
for skill in better-work-loop process-before-platform shape-the-slice build-the-slice prove-before-pilot prepare-review-handoff; do
  cp -R "./skills/$skill" "$skill_root/$skill"
  test -f "$skill_root/$skill/SKILL.md"
done
printf '%s\n' 'Skill folders copied. Check discovery in your client.'
)
```

### Check discovery and try it

Open your writable project in Codex. In CLI or IDE, use `/skills` or type `$` to select the skill; desktop interfaces may expose a Skills selector instead. If the copied skill is absent, restart the client and check the folder layout below. Select the skill explicitly and use the [first-use prompt in the README](../README.md#use-it).

Discovery succeeds when the intended skill name is listed and invocation loads its instructions. Expect a focused question before a completed brief. Do not count a generic answer from an unselected assistant as a successful installation.

## Claude Code

Use the same complete folders. In the PowerShell block, change only the `$skillRoot` assignment to `Join-Path $env:USERPROFILE '.claude/skills'`. In the shell block, change only `skill_root` to `"$HOME/.claude/skills"`. The conservative legacy check can remain; it alerts you to an existing copy before you duplicate it across clients.

Invoke `/better-work-loop` for the complete loop or `/process-before-platform` for the decision-only path. Claude Code reads the shared `SKILL.md` packages, but it does not use Codex's `agents/openai.yaml` metadata. Adjust recorded paths and tool permissions when your environment differs. This repository does not claim equivalent behavior in Claude Code.

## Update an existing installation

Do not copy a new release over an old folder: files removed by a newer release could otherwise remain active.

1. Close sessions using the affected skills. Keep any generated work in its project output folder.
2. Identify each existing skill folder in `.agents/skills`, legacy `.codex/skills`, or `.claude/skills`. Use the path shown by the client if uncertain.
3. Move each complete affected folder into a new dated backup directory **outside every skills discovery directory**. Check the exact source and backup paths first. Keep all local customizations in the backup; do not delete it.
4. For a multi-skill pack, back up all affected folders before installing the new set. Do not mix package versions.
5. Run the fresh-install block from the new extracted source. Compare your customizations with the new files before reapplying any of them.
6. Check discovery and repeat a sanitized prompt. If copying stops partway, move the partially installed folders to a separate backup directory before retrying; the block deliberately refuses to merge them.

For rollback, move the new folders out of discovery and restore the complete backed-up set to its original location. Keep one active copy of each skill name.

## Troubleshooting

| Symptom | Check |
|---|---|
| Skill is missing | The installed path must end in `<skill-name>/SKILL.md`, not `<skill-name>/<skill-name>/SKILL.md`. Restart the client and inspect its discovery location. |
| Referenced file is missing | Copy the complete folder, including `references`, `schemas`, `assets`, and `agents` when present. A raw `SKILL.md` download is insufficient. |
| Existing installation error | Follow the backup-and-replace procedure above; do not add `Force` to overwrite it. |
| The agent cannot write the brief | Open a writable project, name the intended output location, and use the client's normal permission mechanism. Do not disable its sandbox. |
| Questions appear instead of a finished brief | This is expected. Answer what you know; unavailable evidence can remain unknown when discovery closes. |
| A command fails midway | Preserve the error, check directory permissions and available space, and move partial copies out of discovery before retrying. |

## Repository tests

Python 3.11+ is needed only for the [repository validation commands](technical-guide.md#validate), not for copying the skill folders. Behavioral use still requires a compatible AI client.

[Back to the README](../README.md)
