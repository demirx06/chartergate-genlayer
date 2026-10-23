# CharterGate — GenLayer DAO Charter Compliance & Challenge Registry

CharterGate is an experimental, reusable GenLayer Intelligent Contract for accountable DAO governance decisions. A curator freezes a **natural-language DAO charter** once; users submit proposals and self-attested evidence; validators independently decide whether the supplied evidence supports charter compliance, conflicts with it, or remains insufficient. A rejected user gets exactly **one evidence revision**, while both verdict receipts remain immutable.

## What makes it useful

- Transparent charter freeze and SHA-256 commitment: proposal reviews reference the *same* rulebook.
- Distinct **submitter** and **curator** roles; every case has an immutable submitter identity.
- GenLayer nondeterministic model classification with validators independently recomputing a *decisive* verdict, not tolerating class disagreements.
- `COMPLIANT`, `NON_COMPLIANT`, and fail-closed `INSUFFICIENT_EVIDENCE` instead of an unsafe binary answer.
- Fixed 80/100 confidence threshold; malformed AI responses cannot become approval.
- First result is an immutable receipt. One challenger-supplied changed evidence digest may trigger round 2; old result remains readable.
- Bounded storage (100 cases); control/invisible text filtering; no native token transfer or governance vote execution.

The semantic task — applying language policy to narrative proposals — cannot be performed by ordinary deterministic Solidity alone. Authorization, state transitions, hash binding, challenge limits and outputs remain deterministic; GenLayer consensus is used only where judgment is necessary.

## Contract methods

1. `initialize_charter(charter)` — deploying curator freezes charter exactly once.
2. `submit_proposal(title, proposal, evidence)` — new pending case ID; any participant.
3. `assess(case_id)` — curator requests validator consensus and records immutable round receipt.
4. `challenge(case_id, corrected_evidence)` — original submitter; one revision after a non-approved result.
5. `get_case`, `get_receipt`, `get_charter_hash`, `total_cases` — read-only audit trail.

**Example:** Charter requires transparent budget, vote period, milestones, accountable team, risk controls and appeal process. A proposal is reviewed; if its evidence omits milestones it should produce `INSUFFICIENT_EVIDENCE`. A corrected submission may earn `COMPLIANT` on round 2. Actual LLM decisions are not guaranteed or asserted in advance.

## Quick start / validation

Python 3.12 is recommended for the linked GenLayer toolchain.

```bash
python -m pip install -r requirements.txt
python -m pytest tests/offline -q
python -m pytest tests/direct -q
genvm-lint check contracts/charter_gate.py
```

Offline tests use a *fake* SDK to check local logic; **they do not test GenLayer**. The `tests/direct` suite uses `direct_vm`, `direct_deploy`, mock LLM and validator-reexecution fixtures from the real GenLayer testing SDK, and must pass in GitHub Actions before submission. See `.github/workflows/ci.yml`.

## Technical evidence status (23 Oct 2026)

- Python syntax: PASS.
- Offline mock tests: **16 PASS** on preparation machine.
- Direct Mode/GenVM lint/CI: **NOT EXECUTED** on preparation machine (SDK not installed); require GitHub Actions confirmation.
- Public Studionet/Bradbury deployment and receipt: **NOT DONE**.
- Static `site/` folder: UI simulation ONLY, not deployed GenLayer contract.

Do not fabricate passing CI, public validator votes, tx hashes, token rewards or Portal acceptance. Before Portal submission, owner must review the project, provide a real GitHub link, ensure required tests pass, and accurately disclose authorship. A specific CP amount cannot be guaranteed.

## Folder map

- `contracts/charter_gate.py`: real GenLayer contract candidate.
- `tests/offline`: pure Python sanity checks, NOT chain proof.
- `tests/direct`: actual GenLayer Direct Mode regressions (to be run via CI).
- `docs/THREAT_MODEL.md`: security scope and open limitations.
- `docs/PROOF_STATUS.md`: what has and has not been proven.
- `docs/REVIEWER_GUIDE.md`: reproducibility walkthrough.
- `PORTAL_DRAFT.md`: text for review *after* evidence exists.
- `site/`: clearly labeled browser-only demonstration.

No GitHub account connected and nothing was submitted to GenLayer Portal during preparation.
