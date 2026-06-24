# Skills Manager

A "skills manager" — a single tool to inventory, install, sync, and diagnose the skills/plugins scattered across multiple coding-agent runtimes (codex, claude code, zcode) on one machine.

## Language

**Runtime**:
A specific coding agent that consumes skills. Stage 1 managed Runtimes are Codex and Claude Code; other detected runtimes such as ZCode are reported as unmanaged until they have a supported Native Installer and verification evidence.
_Avoid_: agent, tool (too generic)

**Runtime Identity**:
The stable identity of a Runtime product, independent of its installed version, such as `codex`, `claude-code`, or `zcode`.
_Avoid_: runtime version, executable path

**Runtime Adapter**:
The Manager module that collects Runtime Facts and collection findings for one Runtime behind the common inventory orchestration seam. A Runtime Adapter owns native acquisition and parsing but does not normalize Observed Evidence or decide Capability Identity.
_Avoid_: Native Installer, Observed Evidence module

**Fact Collection Finding**:
A failure or limitation encountered while collecting Runtime Facts that cannot be attributed to one native record, such as an unavailable command or unreadable registry. It remains visible in Unified Inventory diagnostics without manufacturing an Observed Evidence record.
_Avoid_: Evidence Finding, Installation State

**Installation Channel**:
The mechanism that placed a capability into a Runtime: Codex Plugin, Claude Code Plugin, `npx skills`, or a Runtime built-in. Installation Channel describes delivery and is not part of Capability Identity.
_Avoid_: capability type, source

**Installation Package**:
A remotely published package that groups one or more Capabilities and may support multiple Package Formats. It is identified by normalized Remote Source plus package path and is the scope used for package-level install, update, and uninstall effects.
_Avoid_: capability, runtime install

**Installation**:
One managed presence of an Installation Package in a Runtime and scope through a specific Package Format. The same Capability may have several independent Installations whose update and removal lifecycles must remain separate.
_Avoid_: capability, package format

**Exposure**:
One path by which a Runtime discovers and can invoke a Capability. Multiple Installations can create duplicate Exposures of the same Capability in one Runtime.
_Avoid_: installation, capability identity

**Exposure Migration**:
The coordinated replacement of one Exposure with another for the same Capability and Runtime. The replacement Exposure is installed and verified before the previous Exposure is removed.
_Avoid_: reinstall, automatic upgrade

**Package Format**:
The runtime-specific representation of an Installation Package: `codex-plugin`, `claude-code-plugin`, `npx-skills`, or `built-in`. Package Formats have different manifests, registries, scopes, and native operations even when they belong to the same Installation Package.
_Avoid_: installation channel, capability type

**Capability Set**:
The Capabilities exposed by one Package Format of an Installation Package. Different Package Formats under the same package root may have different Capability Sets.
_Avoid_: selection set, package contents

**Capability Name**:
The canonical display name from the Capability's `SKILL.md` frontmatter. Manifest and registry labels are retained as aliases in Observed Evidence; name differences do not affect Capability Identity.
_Avoid_: plugin name, registry label

**Metadata Drift**:
A difference in non-identity metadata such as Capability Name, description, or labels across Package Formats or Installations.
_Avoid_: revision drift, format capability drift

**Format Capability Drift**:
A difference between the Capability Sets declared by two Package Formats of the same Installation Package. The Manager reports it and uses the target Runtime's actual format when planning effects.
_Avoid_: revision drift, duplicate exposure

**Source of Truth (SoT)**:
The source location from which a capability is installed: a Remote Source plus canonical `SKILL.md` path, or Runtime Identity plus built-in path. Revision is tracked separately and does not change Capability Identity.
_Avoid_: origin (ambiguous with git origin)

**Capability Identity**:
The stable identity of one capability across runtimes and Installation Channels. For a remotely installed skill it is normalized Remote Source plus canonical `SKILL.md` path; for a Built-in Skill it is Runtime Identity plus built-in path. Name, Revision, Runtime, and Installation Channel are not part of this identity.
_Avoid_: skill name, plugin name

**Remote Source**:
The normalized GitHub or Git remote from which an installable capability originates. Equivalent remote forms such as SSH and HTTPS identify the same source after normalization.
_Avoid_: local checkout, marketplace label

**Development-local Installation**:
An existing Installation sourced from a local marketplace or checkout rather than a Remote Source. Stage 1 reports it read-only, does not create new development-local Installations, excludes it from cross-machine sync, and does not automatically merge it with a Remote Capability.
_Avoid_: remote installation, unresolved identity

**Remote Inspection**:
A read-only fetch of a known Remote Source to resolve manifests, canonical paths, or Revision evidence. Local listing is offline by default; Remote Inspection is allowed for installation, update checks, and incomplete Identity Resolution, but never searches unknown repositories to guess a source.
_Avoid_: source discovery by name, installation

**Source Claim**:
An Operator-provided candidate Remote Source for an Unresolved Identity. The Manager verifies content and canonical path through Remote Inspection, then uses a Native Installer to replace or reinstall the local entry so authoritative source evidence is created; it never edits a lock file or registry to manufacture provenance.
_Avoid_: manual registry edit, name-based match

**Resolved Identity**:
A Capability Identity backed by enough evidence to apply equality, deduplication, version-drift, and sync decisions.
_Avoid_: probable match, inferred match

**Unresolved Identity**:
An installed entry whose evidence is insufficient to establish a Capability Identity. It remains independently visible and actionable but cannot be merged, deduplicated, or synced by identity.
_Avoid_: unknown capability, same-name match

**Runtime Facts**:
The runtime-specific facts a Runtime adapter can directly verify from native commands, registries, manifests, and files. Each Runtime may use its own fact shape; facts are incomplete by design and become Observed Evidence only after the Manager applies required fields, Unknown Value rules, validation, and stable evidence identity.
_Avoid_: Observed Evidence, Capability Identity

**Observed Evidence**:
The Manager-normalized evidence record produced from Runtime Facts. It has the versioned required shape needed by Unified Inventory, but may still be insufficient to resolve Capability Identity.
_Avoid_: Runtime Facts, identity

**Evidence Subject**:
What one Observed Evidence record describes: an `installation` native record or a `runtime-detection`. Only valid installation evidence may produce an Installation, Capability, or Exposure; runtime detection contributes Runtime presence and managed/unmanaged diagnostics without inventing a package.
_Avoid_: Package Format, Installation State

**Evidence Validity**:
Whether one native record satisfied the Observed Evidence contract: `valid` or `invalid`. Missing identity evidence normally produces an Unresolved Identity rather than invalid evidence; invalid means the native record itself cannot be interpreted reliably. Invalid evidence remains visible with Unknown Values and Evidence Findings, but cannot participate in Identity Resolution, deduplication, drift analysis, or mutation planning.
_Avoid_: Identity Resolution, Installation State

**Evidence Identity**:
The stable identity of one Observed Evidence record, derived from Runtime Identity, provenance source, native record identity, and Installation Scope. It does not depend on mutable state, Revision, discovered Capability Set, or display names.
_Avoid_: Capability Identity, Installation Identity

**Evidence Provenance**:
The share-safe summary of where Observed Evidence came from, including source kind, source identifier, and collection result. Unified Inventory retains Evidence Provenance but not complete native registry, command, manifest, or filesystem payloads.
_Avoid_: Runtime Facts payload, Registry

**Evidence Finding**:
A machine-readable explanation of why Observed Evidence is invalid, incomplete, or lower-confidence. Evidence Findings belong to one evidence record and do not by themselves describe Installation or Exposure conflicts across records.
_Avoid_: Inventory Finding, warning string

**Identity Resolution**:
The Manager's explicit result of evaluating Observed Evidence. It contains either a Resolved Identity or an Unresolved Identity and is the only basis for equality, deduplication, version-drift, and sync decisions.
_Avoid_: source ID, inferred match

**Revision**:
The installed version of a capability at one Runtime Install Path, expressed as a commit SHA or version when available. A Built-in Skill inherits its Runtime version as Revision. Two installs can share a Capability Identity while using different Revisions.
_Avoid_: identity, Source of Truth

**Floating Revision Request**:
An install request that follows a Remote Source default branch or Native Installer default rather than naming a fixed Revision. It is allowed for initial installation, but Unified Inventory records the resolved Revision and Revision Sync never uses a floating value.
_Avoid_: resolved revision, latest version identity

**Revision Relation**:
The comparison result between two installs of the same Capability: `same`, `different`, or `unknown`. Missing or incomparable Revisions produce `unknown`, never an assumed match.
_Avoid_: capability relation

**Revision Order**:
A verified `older` or `newer` relationship between two Revisions. It requires source-specific ordering evidence such as Git ancestry or validated semantic versions and is outside the Manager MVP.
_Avoid_: install time order, lexical version order

**Sync Status**:
Whether the Manager has enough identity and Revision evidence to evaluate or perform synchronization. It is `indeterminate` when Identity is unresolved or Revision Relation is unknown.
_Avoid_: install status, enabled status

**Coverage Sync**:
Ensuring a Capability has an effective Exposure in every Operator-selected Runtime. Coverage Sync has no default target set; the Manager must obtain explicit Runtime targets before execution.
_Avoid_: revision sync, install everywhere implicitly

**Revision Sync**:
Aligning resolved Revisions across existing Installations of one Capability. It requires explicit Operator intent or confirmation and never assumes Revision Order.
_Avoid_: coverage sync, update all

**Format Alignment**:
Migrating an Exposure toward the preferred Runtime-native Package Format. It is a recommendation requiring confirmation and follows verify-before-remove Exposure Migration.
_Avoid_: revision sync, reinstall

**Marketplace**:
A git repo that publishes one or more plugins, registered with a runtime under a name (e.g. `claude-plugins-official`, `gm-skills`). Each marketplace has its own registry file per runtime.
_Avoid_: repo (too generic)

**Registry**:
A runtime's own bookkeeping file that records which plugins are installed, where, at what version/scope. Codex/claude/zcode each maintain their own — there is no cross-runtime registry today.
_Avoid_: manifest (a plugin has a manifest; the registry lists many plugins)

**Dead Link**:
A symlink or registry entry pointing at a path that no longer exists (e.g. a gstack symlink after the repo moved). The primary failure mode loose skills silently suffer.

**Manager** (the thing we are building):
An **agent skill** that coordinates and records skill management across Runtimes. It reads native installation evidence, selects and invokes Codex, Claude Code, or `npx skills` operations, records a unified inventory, and verifies outcomes; it does not implement another installer or own a cross-runtime registry.
_Avoid_: CLI, tool, command (these imply a human types structured commands)

**Native Installer**:
The authoritative mechanism that performs and records an Installation: Codex Plugin commands, Claude Code Plugin commands, or `npx skills`. The Manager invokes Native Installers but does not reproduce their mutation logic.
_Avoid_: Manager, registry editor

**Installer Availability**:
Whether a Native Installer executable and required runtime are callable for mutations. Registry-backed list and doctor Actions may continue when unavailable, but install, uninstall, enable, and disable are blocked.
_Avoid_: installation state, runtime detected

**Installer Compatibility**:
Whether the detected Native Installer version supports the operations and evidence required by the Manager. The Manager diagnoses incompatibility but does not automatically upgrade Codex, Claude Code, Node/npm, or `skills`.
_Avoid_: capability revision, installer availability

**Unified Inventory**:
The Manager's current, derived, read-only view of native installation evidence, Identity Resolution, packages, Capabilities, Revisions, and Exposures. It is regenerated on demand, is never an authoritative registry, and is not retained as Manager-owned history.
_Avoid_: registry, lock file

**Inventory Schema Version**:
The explicit version of the machine-readable Unified Inventory contract. The Stage 1 redesign may replace the current flat `entries` and `source.id` shape while preserving the `inventory.py --json` command entrypoint.
_Avoid_: package version, capability revision

**Unknown Value**:
An explicit inventory value used when required evidence is unavailable. Required schema fields remain present and use `unknown` rather than disappearing or implying a default.
_Avoid_: omitted field, assumed value

**Redacted Inventory**:
A shareable Unified Inventory rendering that replaces home paths, reduces project path detail, removes credentials and URL secrets, and preserves identity relationships without exposing local sensitive data.
_Avoid_: authoritative inventory, credential export

**Inventory Fixture**:
A synthetic collection of Runtime Facts, native outputs, and temporary files that drives the public inventory entrypoint deterministically. Inventory Fixtures primarily assert the versioned Unified Inventory result; direct Runtime Adapter tests are reserved for acquisition and parsing edge cases.
_Avoid_: production snapshot, helper-unit test

**Capability View**:
The default Unified Inventory view, grouping every Runtime Exposure and Installation Package under Capability Identity.
_Avoid_: package list

**Package View**:
A Unified Inventory view grouping Package Formats and affected Capabilities under Installation Package, used to evaluate package-level update and removal effects.
_Avoid_: capability view

**Runtime View**:
A Unified Inventory view grouping effective Exposures by Runtime and scope, used to verify what each Runtime can currently invoke.
_Avoid_: registry dump

**Global Exposure**:
An Exposure available across projects for one Runtime, such as a user-scoped Plugin or global `npx skills` install.
_Avoid_: project exposure

**Scoped Exposure**:
An Exposure limited to a project or local scope. Capability View summarizes Scoped Exposures by default and expands project paths when Revision drift, duplicate Exposure, or Operator inspection requires it.
_Avoid_: global exposure

**Installation Scope**:
The Native Installer's placement scope for one Installation, such as Claude Code `user`, `project`, or `local`, and `npx skills` `global` or `project`. When more than one scope is valid, the Operator must choose; the Manager does not infer project scope from the current directory.
_Avoid_: runtime target, exposure state

**Selection Set**:
The Operator-approved Capabilities or Installation Packages selected from a Remote Source before installation. A multi-package or multi-skill Remote Source has no default Selection Set, and “all” must be explicit.
_Avoid_: discovered catalog, implicit all

**Package Impact**:
The pre-install inventory of everything an Installation Package can add to a target Runtime: Capabilities, hooks, MCP servers, commands, scripts, apps, authentication requirements, Package Formats, Remote Source, Revision, package root, and scope.
_Avoid_: capability list, security approval

**Package Removal**:
Removal of an Installation Package or one Runtime Installation through its Native Installer while preserving user data by default.
_Avoid_: data removal, capability deletion

**Data Removal**:
Deletion of package-owned user data or state after separate explicit Operator authorization. Ambiguous directories are never removed.
_Avoid_: package removal, cache cleanup

**Unsupported Format**:
A target Runtime for which the selected Remote Source offers neither a Runtime-native Plugin format nor support through `npx skills`. The corresponding Action is blocked; the Manager does not copy files or create links outside a Native Installer.
_Avoid_: unavailable capability, best-effort install

**Partial Success**:
A multi-Runtime Action in which one or more Native Installer operations succeed before another fails. The Manager stops, regenerates Unified Inventory, and asks the Operator whether to retain successful Installations or explicitly restore the previous state.
_Avoid_: rolled back, complete success

**Execution Plan**:
The ordered set of Native Installer operations for one approved Action. The Manager preflights every target, orders operations dynamically by risk and verifiability, verifies after each operation, and stops on the first failure.
_Avoid_: fixed runtime order, transaction

**Action Authorization**:
The Operator's approval for an Execution Plan. A request that already names the Action, Capability or Package, target Runtime, and required scope counts as authorization; the Manager asks again only when preflight discovers broader, destructive, scoped, or multi-Capability effects.
_Avoid_: blanket permission, implicit sync target

**Registry Verification**:
Confirmation that the Native Installer's authoritative record reflects the intended Installation State and configuration.
_Avoid_: discovery verification

**Managed Installation**:
An Installation present in its Native Installer's authoritative record. For `npx skills`, the global or project skill lock establishes the managed Installation.
_Avoid_: active exposure

**Unmanaged Exposure**:
A Runtime Exposure whose native Installation record is missing. It is reported as broken with Unresolved Identity until reclaimed through a Native Installer.
_Avoid_: installed skill, local-only capability

**Discovery Verification**:
Confirmation that the target Runtime can enumerate or otherwise reliably discover the intended Capability Exposure. File presence alone is insufficient.
_Avoid_: registry verification, invocation verification

**Invocation Verification**:
Confirmation that the Runtime can actually invoke the Capability. It is required for Exposure Migration and conflict repair, or when explicitly requested, but is not the default for routine Actions.
_Avoid_: discovery verification

**Operator**:
The human who gives natural-language instructions to the agent. Distinguished from the agent that executes them.
_Avoid_: user (too generic)

**Action**:
Something the Manager coordinates on the Operator's behalf against one or more Runtimes. Canonical actions: list, doctor, repair, install, uninstall, enable, disable, and sync.
_Avoid_: command (implies a typed CLI invocation)

**Doctor Action**:
A read-only diagnosis of Installer Availability, Installer Compatibility, native record consistency, Identity Resolution, Installation State, Exposure State, scope overlap, and manifest resolution. It never performs repairs.
_Avoid_: repair, mutation

**Recommendation**:
A non-executing proposal derived from Unified Inventory findings. Facts, Findings, and Recommendations remain distinct, and a Recommendation becomes an Execution Plan only after Operator selection.
_Avoid_: action authorization, automatic repair

**Repair Action**:
An explicitly authorized mutation plan derived from doctor findings and executed only through Native Installers.
_Avoid_: automatic doctor fix

**Installation State**:
Whether one Installation is `installed`, `absent`, or `broken`, derived while normalizing Runtime Facts from its Native Installer's authoritative record and required files.
_Avoid_: exposure state, enabled state

**Native Record Inconsistency**:
A conflict between a Native Installer record and required on-disk or discovery evidence, such as a registry entry whose installed path is missing. Installation State is `broken`; both evidence sets remain visible until a Repair Action uses the Native Installer.
_Avoid_: absent installation, stale inventory

**Exposure State**:
Whether one installed Capability is `active`, `inactive`, `ambiguous`, or `unknown` in a Runtime. Observed Evidence may establish `active`, `inactive`, or `unknown`; only Unified Inventory may derive `ambiguous` by comparing multiple Exposures. Exposure State is evaluated separately from Installation State.
_Avoid_: installation state

**Disable Action**:
A coordinated transition from an active Exposure to an inactive or absent Exposure in one Runtime. Native Plugin formats use their enable/disable operation; `npx skills` removes only the target Runtime link while preserving other Exposures and source records.
_Avoid_: uninstall capability

**Enable Action**:
A coordinated transition that makes an installed Capability active in one Runtime. Native Plugin formats use their enable operation; `npx skills` restores the target Runtime link through its Native Installer.
_Avoid_: reinstall package

**Duplicate Exposure**:
Two or more Installations exposing the same Capability to the same Runtime. The Manager does not infer load precedence; it marks the Exposure State `ambiguous` and recommends retaining the Runtime-native Plugin Exposure.
_Avoid_: duplicate capability

## Resolved decisions

- **Identity = Source of Truth without Revision** (ADR-0001). Same capability ⟺ same source location; Revision differences are version drift.
- **Runtime Facts, Observed Evidence, and Identity stay separate** (ADR-0003). Runtime adapters report Runtime Facts; the Manager normalizes them into Observed Evidence; identity decisions consume Identity Resolution.
- **Runtime adapters share orchestration, not fact schemas** (ADR-0019). Every Runtime Adapter returns Runtime Facts plus collection findings through one seam while retaining its Runtime-specific fact shape.
- **Observed Evidence schema 2.0 replaces 1.0** (ADR-0015). Evidence Subject, Validity, Provenance, and Findings become explicit; invalid and runtime-detection evidence cannot manufacture installation entities.
- **Installation Channel is not identity** (ADR-0004). Codex Plugin, Claude Code Plugin, and `npx skills` installs converge when their Remote Source and canonical `SKILL.md` path match.
- **Package and Capability are separate** (ADR-0005). One Installation Package can expose several Capabilities through different Package Formats.
- **One preferred Exposure per Runtime** (ADR-0006). Prefer native Plugin format; use `npx skills` when no native Plugin exists.
- **Manager coordinates native installers** (ADR-0002). Installation behavior and authoritative records remain owned by Codex, Claude Code, and `npx skills`.
- **Manager is executable** (ADR-0007). It may invoke Native Installers, then regenerates Unified Inventory to verify the result.
- **Exposure migration is verify-before-remove** (ADR-0008). Native Plugin availability is recommended, not applied automatically.
- **Manager is stateless** (ADR-0009). It stores neither Unified Inventory snapshots nor an Action Log.
- **Stage 1 has an evidence gate** (ADR-0018). All identity, native-operation, verification, fixture, redaction, and unmanaged-ZCode criteria must pass.

## Delivery stages

- **Stage 1**: Unified Inventory views; Codex Plugin, Claude Code Plugin, and `npx skills` adapters; Identity Resolution; list, doctor, install, uninstall, enable, disable; Registry Verification and Discovery Verification. ZCode is reported as unmanaged.
- **Stage 2**: Coverage Sync, Revision Sync, Format Alignment, Source Claim, Invocation Verification, and additional Runtime adapters when stable Native Installer and verification evidence exist.
- **Form = a plugin in gm-skills** (Q4). The Manager ships as one plugin in the gm-skills marketplace, distributed the same way as its siblings.
- **Stage 1 scope** is defined in ADR-0012 and ADR-0018.
- **Interaction model = agent-driven, not CLI-driven** (Q6 reversal). The Manager is a skill an agent reads; it is not a binary an Operator types at.
