# CharterGate threat model

1. **Evidence forgery:** Proposal text and excerpts are self-attested; no HTTP or publisher-authenticity check. Never label the verdict a proof of a DAO's actual compliance.
2. **Prompt injection:** User-provided proposal/evidence are quoted as JSON in an untrusted section, control chars rejected and validator checks the exact decisive outcome. These mitigations reduce but do not eliminate semantic manipulation.
3. **Model confidence/consensus:** Threshold <80 and malformed results degrade to INSUFFICIENT_EVIDENCE; leader-validator class mismatch rejects comparison. Real world adversarial LLM evaluation and cross-validator independence are not proven.
4. **Curator censorship:** Curator has exclusive right to request evaluations; cannot replace frozen charter or rewrite receipts, but can decline to review. This is a major governance/trust limitation.
5. **Revisions:** One changed evidence digest by the original submitter is allowed after non-approval; immutable first receipt remains readable. No deadlines or formal dispute panel.
6. **Resource limits:** At most 100 cases and two reviews each; user pays transaction execution fees where applicable. No per-address case limit.
7. **Privacy:** Proposal and evidence are stored on-chain and therefore public; do not include private or sensitive material.
8. **Scope:** Never executes DAO votes, disburses funds, authenticates supporting documents, or provides legal advice.
