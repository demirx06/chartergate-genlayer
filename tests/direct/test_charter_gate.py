"""GenLayer Direct Mode tests — require official SDK; mocks are NOT public chain proofs."""
import hashlib
import json
import pytest

CHARTER=('DAO grants must disclose an itemized budget, working group ownership, a voting '
         'window, delivery milestones, risk controls, and the appeal procedure. '
         'Failure to specify mandatory requirements prevents compliance approval.')
PROPOSAL=('This proposal requests a six-month education-grant programme with public '
          'progress dashboards, accountability reports and quarterly delivery reviews.')
EVIDENCE=('Budget: 5000 GEN. Working group: Civic Learning Unit. Vote: seven days. '
          'Milestones: every month. Risk: conflicts disclosed. Appeals: seven-day window.')

def setup(direct_vm,direct_deploy,direct_alice,direct_bob):
    direct_vm.sender=direct_alice
    c=direct_deploy('contracts/charter_gate.py')
    c.initialize_charter(CHARTER)
    direct_vm.sender=direct_bob
    cid=c.submit_proposal('Public grants programme',PROPOSAL,EVIDENCE)
    return c,cid

def decision(vm, verdict='COMPLIANT',confidence=92):
    vm.clear_mocks()
    vm.mock_llm(r'(?s).*CharterGate consensus DAO-policy review.*',
                json.dumps({'decision':verdict,'confidence':confidence}))

def test_pass_consensus(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_alice;decision(direct_vm)
    assert c.assess(cid)=='COMPLIANT'
    r=json.loads(c.get_receipt(cid+':0'))
    assert r['verdict']=='COMPLIANT'
    assert r['evidence_hash']==hashlib.sha256(EVIDENCE.encode()).hexdigest()
    assert direct_vm.run_validator() is True

@pytest.mark.parametrize('v',('NON_COMPLIANT','INSUFFICIENT_EVIDENCE'))
def test_negative_states(v,direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_alice;decision(direct_vm,v)
    assert c.assess(cid)==v

@pytest.mark.parametrize('confidence',(0,50,79,101))
def test_confidence_never_grants_pass(confidence,direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_alice;decision(direct_vm,'COMPLIANT',confidence)
    assert c.assess(cid)=='INSUFFICIENT_EVIDENCE'

def test_validator_rejects_decisive_disagreement(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_alice;decision(direct_vm,'COMPLIANT')
    c.assess(cid)
    decision(direct_vm,'NON_COMPLIANT')
    assert direct_vm.run_validator() is False

def test_validator_rejects_threshold_crossing(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_alice;decision(direct_vm,'COMPLIANT',95)
    c.assess(cid)
    decision(direct_vm,'COMPLIANT',79)
    assert direct_vm.run_validator() is False

def test_validator_accepts_nondispositive_confidence_drift(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_alice;decision(direct_vm,'COMPLIANT',95)
    c.assess(cid)
    decision(direct_vm,'COMPLIANT',84)
    assert direct_vm.run_validator() is True

def test_curator_only_and_freeze(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    with direct_vm.expect_revert('curator'): c.assess(cid)
    direct_vm.sender=direct_alice
    with direct_vm.expect_revert('frozen'): c.initialize_charter(CHARTER)

def test_challenge_and_immutable_receipts(direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_alice;decision(direct_vm,'NON_COMPLIANT')
    c.assess(cid)
    direct_vm.sender=direct_bob
    c.challenge(cid,EVIDENCE+' New reviewed attachment is provided.')
    direct_vm.sender=direct_alice;decision(direct_vm,'COMPLIANT')
    c.assess(cid)
    assert json.loads(c.get_receipt(cid+':0'))['verdict']=='NON_COMPLIANT'
    assert json.loads(c.get_receipt(cid+':1'))['verdict']=='COMPLIANT'
    direct_vm.sender=direct_bob
    with direct_vm.expect_revert('one challenge'): c.challenge(cid,EVIDENCE+' Another')

@pytest.mark.parametrize('bad',('','short','injected\nline','x'*1700))
def test_bad_evidence_rejected(bad,direct_vm,direct_deploy,direct_alice,direct_bob):
    c,cid=setup(direct_vm,direct_deploy,direct_alice,direct_bob)
    with direct_vm.expect_revert(): c.submit_proposal('Another grants programme',PROPOSAL,bad)
