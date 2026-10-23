# CharterGate — GenLayer DAO Charter Compliance & Challenge Registry

CharterGate is a reusable GenLayer Intelligent Contract for evidence-aware DAO governance review. An authorized curator freezes a human-readable charter once; participants submit proposals and supporting text; validator consensus classifies each proposal as `COMPLIANT`, `NON_COMPLIANT`, or `INSUFFICIENT_EVIDENCE`. Each review produces an immutable decision receipt, and the original submitter has one opportunity to challenge a non-compliant or insufficient result with revised evidence.

## Why GenLayer?

Deciding whether a narrative proposal complies with governance policy requires semantic judgment that ordinary deterministic contracts cannot perform alone. CharterGate confines model evaluation to GenLayer nondeterministic execution with validators independently checking the decisive outcome; ownership rules, evidence hashes, state transitions, and challenge limits remain deterministic.

## Main features

- One-time charter freeze with SHA-256 commitment.
- Separate curator and proposal-submitter permissions.
- SHA-256 evidence commitments and immutable review receipts.
- Validator-backed `COMPLIANT` / `NON_COMPLIANT` / `INSUFFICIENT_EVIDENCE` outcomes.
- Fail-closed malformed or low-confidence model responses.
- At most one revised-evidence challenge after an adverse or inconclusive decision.
- Bounded input lengths, storage limits, and no native token transfers.

## Contract interface

- `initialize_charter(charter)` — freeze the policy once.
- `submit_proposal(title, proposal, evidence)` — register a proposal.
- `assess(case_id)` — run validator-backed review and record a receipt.
- `challenge(case_id, corrected_evidence)` — one permitted evidence revision.
- `get_case`, `get_receipt`, `get_charter_hash`, `total_cases` — audit-oriented read-only calls.

Source: [`contracts/charter_gate.py`](contracts/charter_gate.py).

## Reproducible tests

```bash
python -m pip install -r requirements.txt
python -m pytest tests/offline -q
python -m pytest tests/direct -q
genvm-lint check contracts/charter_gate.py
```

GitHub verification workflow: [CI Actions](https://github.com/demirx06/chartergate-genlayer/actions/workflows/ci.yml). It covers Python compilation, offline tests, GenLayer Direct Mode tests, GenVM lint, and source hashing. Offline tests are not chain evidence.

## Public GenLayer Studionet verification — 24 October 2026

A manually authorized test run deployed CharterGate and exercised on-chain initialization, proposal submission, GenLayer consensus review, and state readback.

- [Successful GitHub Actions network run](https://github.com/demirx06/chartergate-genlayer/actions/runs/40023509447): `1 passed in 58.33s`.
- [Deployed contract on GenLayer Studionet](https://explorer-studio.genlayer.com/address/0xa87a9D861909410160Eee4540dA1Af3cE8a5B425): `0xa87a9D861909410160Eee4540dA1Af3cE8a5B425`.
- Observed consensus verdict: `COMPLIANT`.
- Full source hash, commit, transaction hashes, test summary: [`docs/PROOF_MANIFEST.json`](docs/PROOF_MANIFEST.json).
- Updated evidence ledger: [`docs/PROOF_STATUS.md`](docs/PROOF_STATUS.md).

This demonstrates the tested Studionet scenario, not an independent security audit or guaranteed behavior for every proposal. The example site in `site/` is a static demonstration, not a blockchain-connected production frontend. No GEN token transfer or financial escrow is claimed.

## Documentation

- [`docs/REVIEWER_GUIDE.md`](docs/REVIEWER_GUIDE.md) — reviewer instructions.
- [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md) — risks and limitations.
- [`docs/PROOF_STATUS.md`](docs/PROOF_STATUS.md) — test and deployment status.
- [`PORTAL_DRAFT.md`](PORTAL_DRAFT.md) — draft submission text for human review.
