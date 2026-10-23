"""Real Studionet proof. Opt-in only; deploys and signs test transactions.

Requires an operator to explicitly authorize GitHub Actions manual dispatch.
This is a test-network check, NOT proof of a production deployment.
"""
import hashlib
import json
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


@pytest.mark.integration
def test_chartergate_public_studionet_lifecycle(default_account):
    factory = get_contract_factory("CharterGate")
    contract = factory.deploy(account=default_account, consensus_max_rotations=4)
    print("CHARTERGATE_STUDIONET_CONTRACT=" + str(contract.address), flush=True)

    charter = (
        "DAO approvals must disclose the funding amount, identify a responsible proposer, "
        "include a public review period, and describe how conflicts of interest are handled."
    )
    tx = contract.initialize_charter(args=[charter]).transact(
        wait_interval=10000, wait_retries=50
    )
    assert tx_execution_succeeded(tx)
    print("CHARTER_INITIALIZED_TX=" + str(tx.get("hash", "")), flush=True)
    assert str(contract.get_charter_hash().call()) == hashlib.sha256(
        charter.encode("utf-8")
    ).hexdigest()

    proposal = (
        "The DAO proposes a small contributor education grant; the proposer is named, "
        "the budget is published, and the request provides a review and conflict policy."
    )
    evidence = (
        "Self-attested proposal record: proposer Alex; budget 250 test units; public "
        "comment window seven days; related-party reviewers must abstain."
    )
    tx = contract.submit_proposal(args=["Education grant example", proposal, evidence]).transact(
        wait_interval=10000, wait_retries=50
    )
    assert tx_execution_succeeded(tx)
    print("PROPOSAL_SUBMITTED_TX=" + str(tx.get("hash", "")), flush=True)
    case = json.loads(str(contract.get_case(args=["0"]).call()))
    assert case["state"] == "PENDING"
    assert case["provenance"] == "SELF_ATTESTED_NOT_VERIFIED"
    assert case["evidence_hash"] == hashlib.sha256(evidence.encode()).hexdigest()

    tx = contract.assess(args=["0"]).transact(
        consensus_max_rotations=4, wait_interval=10000, wait_retries=80
    )
    assert tx_execution_succeeded(tx)
    print("CONSENSUS_REVIEW_TX=" + str(tx.get("hash", "")), flush=True)
    receipt = json.loads(str(contract.get_receipt(args=["0:0"]).call()))
    reviewed = json.loads(str(contract.get_case(args=["0"]).call()))
    assert reviewed["state"] == "REVIEWED"
    assert receipt["verdict"] in {
        "COMPLIANT", "NON_COMPLIANT", "INSUFFICIENT_EVIDENCE"
    }
    assert receipt["evidence_hash"] == case["evidence_hash"]
    assert receipt["charter_hash"] == hashlib.sha256(charter.encode()).hexdigest()
    assert receipt["limitation"] == "SEMANTIC_REVIEW_OF_SELF_ATTESTED_TEXT"
    print("CHARTERGATE_OBSERVED_VERDICT=" + receipt["verdict"], flush=True)
