# npx skills Installation and Exposure require separate evidence

For `npx skills`, the skill lock proves a Managed Installation and provides Remote Source, canonical skill path, and Revision evidence. Runtime links together with `npx skills list` prove individual Exposures. A lock with no target Runtime link is `installed + inactive`; a Runtime link with no lock is an Unmanaged Exposure with broken Installation State and Unresolved Identity; both present is `installed + active`; both absent is `absent`. The Manager only reads these records and uses `npx skills` for all mutations.
