# CharterGate — Current Verification Status

**Last updated:** 24 October 2026. This file supersedes the pre-deployment status dated 23 October 2026.

| Evidence | Verified result | Source |
|---|---|---|
| Python syntax, offline tests, GenLayer Direct Mode, GenVM lint | PASS (GitHub CI) | https://github.com/demirx06/chartergate-genlayer/actions/workflows/ci.yml |
| Real GenLayer Studionet integration | PASS: 1 test in 58.33 seconds | https://github.com/demirx06/chartergate-genlayer/actions/runs/40023509447 |
| Contract deployment | Contract address recorded | https://explorer-studio.genlayer.com/address/0xa87a9D861909410160Eee4540dA1Af3cE8a5B425 |
| Charter initialization | Transaction hash recorded | Manifest below |
| Proposal submission | Transaction hash recorded | Manifest below |
| Consensus assessment | `COMPLIANT` observed; transaction recorded | Manifest below |
| Independent external security audit | NOT PERFORMED | — |
| Portal approval or points | NOT CLAIMED | — |

**Evidence manifest:** [`PROOF_MANIFEST.json`](PROOF_MANIFEST.json). It specifies the exact tested commit `e914a8f9b785de580f1a529a3da27c909eb6cd9d`, source SHA-256 `64608fb2f9e2fda66be4b38ce129856518d26a51213a435b64585afcf0fb4bf6`, contract address, three transaction hashes and observed outcome. The later documentation-only updates do not change the tested contract source.

**Scope and limitations:** This establishes one genuine GenLayer Studionet lifecycle, not a third-party audit, proof of legal compliance, token transfers or an evaluation of every possible input. The `site/` files are an illustrative local static demo, not a live blockchain-connected application. Future contract edits require new testing and revalidation of source hashes.
