# CharterGate — Consensus DAO Charter Compliance and Challengeable Decision Receipts

**Contribution category:** Developer / Intelligent Contracts

CharterGate is a reusable GenLayer Intelligent Contract for reviewing DAO governance proposals against a frozen, human-readable charter. Each proposal is bound to an evidence digest, then assessed through GenLayer validator consensus as COMPLIANT, NON_COMPLIANT, or INSUFFICIENT_EVIDENCE. The system keeps immutable decision receipts, applies curator-only controls, rejects low-confidence or malformed decisions, and permits one evidence revision after an adverse or inconclusive decision.

Unlike a generic AI prompt wrapper, CharterGate relies on GenLayer's consensus execution for a real semantic policy judgment while enforcing deterministic authorization, hashes and revision limits on-chain. It does not transfer funds or claim that a model determines legal validity.

**Evidence:** A real GenLayer Studionet test successfully deployed the contract, froze a DAO charter, submitted a proposal, completed consensus assessment and read the stored result. The observed verdict was COMPLIANT; the integration test passed (1/1, 58.33s).

**Source repository:** https://github.com/demirx06/chartergate-genlayer

**Live test run:** https://github.com/demirx06/chartergate-genlayer/actions/runs/40023509447

**Studionet contract:** https://explorer-studio.genlayer.com/address/0xa87a9D861909410160Eee4540dA1Af3cE8a5B425

**Transaction and source-hash proof:** https://github.com/demirx06/chartergate-genlayer/blob/main/docs/PROOF_MANIFEST.json

**Limitations:** Studionet research prototype; no external security audit or mainnet deployment is claimed. Submission and authorship should be reviewed for accuracy by the submitting account owner before posting.
