# Observed Evidence Deepening

**Status:** implemented.

## Goal

Turn Observed Evidence into a deep module between Runtime Adapters and Unified Inventory. Runtime-specific acquisition and parsing stay behind adapters; evidence normalization, validation, stable identity, and provenance become local to one module.

## Decision flow

```text
Native command / registry / manifest / filesystem
  → Runtime Adapter
  → Runtime-specific Runtime Facts + Fact Collection Findings
  → Observed Evidence module
  → normalized Observed Evidence + Evidence Findings
  → Identity Resolution
  → Unified Inventory entities, conflicts, views, and diagnostics
```

## Module ownership

### Runtime Adapter

Owns:

- native command and filesystem acquisition;
- native payload parsing;
- Runtime-specific fallback behavior;
- Runtime-specific fact shapes;
- Fact Collection Findings.

Does not own:

- required Observed Evidence fields;
- Unknown Value defaults;
- Evidence Validity or Evidence Identity;
- Capability or Package identity;
- cross-record Exposure conflicts.

Every Runtime Adapter participates in the same inventory orchestration seam. Native and fixture acquisition are private adapters inside the Runtime Adapter implementation.

### Observed Evidence module

Owns:

- interpretation of every supported Runtime Facts shape;
- Inventory Schema Version `2.0` evidence contract;
- Evidence Subject;
- required fields and Unknown Value rules;
- record-level Evidence Validity;
- Evidence Findings;
- stable Evidence Identity;
- share-safe Evidence Provenance;
- Installation State;
- per-record Exposure State: `active`, `inactive`, or `unknown`.

Does not own:

- native acquisition;
- Capability equality;
- cross-record `ambiguous` Exposure State;
- mutation planning.

### Identity Resolution module

Consumes only valid installation Observed Evidence. It owns Remote Source normalization, canonical paths, built-in identity, Package identity, Capability identity, and Revision Relation.

### Unified Inventory module

Consumes normalized evidence and Identity Resolution. It owns Installation Package, Installation, Capability, and Exposure relationships; cross-record `ambiguous` state; Findings and Recommendations; Capability, Package, and Runtime Views.

## Evidence contract invariants

1. One interpretable native record produces one Observed Evidence record.
2. Evidence Subject is `installation` or `runtime-detection`.
3. Evidence Validity is `valid` or `invalid`.
4. Missing Remote Source or Capability path normally produces valid evidence plus Unresolved Identity.
5. Malformed or contradictory native record structure produces invalid evidence.
6. Invalid evidence remains visible with Unknown Values, provenance, and Evidence Findings.
7. Invalid evidence cannot produce Identity Resolution or enter mutation planning.
8. Only valid installation evidence may produce Installation, Capability, or Exposure entities.
9. Runtime detection may contribute Runtime presence and managed/unmanaged diagnostics, but never a synthetic package.
10. Complete native payloads are not retained in Unified Inventory.
11. One `npx skills` lock record remains one Observed Evidence record even when it contains several Runtime Exposure facts.
12. One Claude Code installed-plugin record per scope remains one Observed Evidence record.
13. Evidence Findings and Fact Collection Findings are structured records, not free-form warning strings.

## Stable identity

Evidence Identity is derived from:

- Runtime Identity;
- Evidence Subject;
- provenance source kind and share-safe source identifier;
- native record identity;
- Installation Scope.

The native record identity is the authoritative registry selector or lock key, not the Capability display name. A local provenance locator may contribute to the internal hash, but Unified Inventory exposes only a share-safe identifier.

Evidence Identity excludes:

- mutable Installation or Exposure State;
- Revision;
- Capability Set;
- display names;
- validation findings.

Capability Identity and Installation identity remain separate from Evidence Identity.

When a malformed record has a stable native locator, it retains the same Evidence Identity as it moves from invalid to valid. When the adapter cannot identify or individually locate a native record, it emits a Fact Collection Finding instead of inventing unstable evidence identity from array position.

## Validation model

Evidence Findings are structured records attached to one evidence record. They identify:

- missing required discriminator;
- malformed native record;
- contradictory facts;
- unsupported native record variant;
- provenance that cannot be made share-safe.

A collection failure that cannot be attributed to one native record is a Fact Collection Finding, not invalid evidence.

## Runtime-specific facts

Runtime Facts intentionally do not share one large schema.

- Codex facts may retain marketplace selector, native enabled state, plugin path, source kind, and built-in markers.
- Claude Code facts may retain plugin selector, marketplace identity, install scope, project path, install path, and revision.
- `npx skills` facts may retain lock identity, scope, skill record, Runtime links, and managed/unmanaged status.
- ZCode Stage 1 facts contain only runtime detection sufficient to report unmanaged status.

The Observed Evidence module contains one internal interpreter for each supported fact shape. Those interpreters are implementation details, not separate public seams.

For `npx skills`, the interpreter creates one Installation candidate from the lock record and zero or more Exposure candidates from Runtime links. It does not duplicate the Installation evidence for each Runtime.

## Test surface

The versioned Unified Inventory JSON produced through the public inventory entrypoint is the primary test surface.

Inventory Fixtures must cover:

- valid Codex, Claude Code, and `npx skills` facts;
- malformed native records becoming invalid evidence;
- collection failures becoming Fact Collection Findings;
- missing source/path remaining valid but Unresolved;
- stable Evidence Identity across Revision and state changes;
- stable Evidence Identity when one malformed native record becomes valid;
- invalid evidence producing no package, installation, capability, or exposure;
- one npx lock record producing one evidence record and multiple Exposures;
- ZCode runtime detection producing no synthetic package;
- cross-format Capability convergence;
- global/project scope overlap;
- redacted provenance and paths;
- real-machine read-only smoke behavior.

Direct Runtime Adapter tests remain only for native acquisition and parser variants. Tests should not construct the complete Observed Evidence dictionary or import its required-field implementation constants.

## Migration

1. Add schema `2.0` Inventory Fixtures and expected final JSON.
2. Implement the Observed Evidence module behind those fixtures.
3. Migrate Codex Runtime Facts and adapter tests.
4. Migrate Claude Code Runtime Facts and adapter tests.
5. Migrate `npx skills` Runtime Facts and adapter tests.
6. Move ZCode detection behind a Runtime Adapter.
7. Make Identity Resolution reject invalid or runtime-detection evidence.
8. Make Unified Inventory create entities only from valid installation evidence.
9. Update views, doctor, redaction, SKILL instructions, and validators atomically.
10. Delete the old shared evidence dictionaries, adapter evidence constructors, and implementation-oriented fixture helpers.

Do not add a compatibility module for schema `1.0`; the Manager is stateless and the command entrypoint remains stable.

## Acceptance

- Runtime Adapters no longer emit the full Observed Evidence schema.
- Inventory orchestration does not know Runtime-specific parameters or ZCode special cases.
- Observed Evidence validation and ID rules exist in one module.
- Invalid records are visible but isolated from identity and mutation.
- ZCode detection appears only as unmanaged Runtime presence.
- Capability, Package, and Runtime Views remain consistent.
- Existing Native Installer ownership and read-only inventory guarantees remain unchanged.
- All synthetic fixtures, skill/plugin validators, redaction checks, and real-machine read-only smoke tests pass.
