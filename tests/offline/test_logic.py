import hashlib
import json
import pytest
from conftest import GL as gl, UserError, contract_type

A='0x'+'a'*40
B='0x'+'b'*40
C='0x'+'c'*40
CHARTER=('All DAO proposals must specify a spending budget, the accountable working team, '
         'a public voting interval, timeline milestones and a risk mitigation assessment. '
         'Missing any mandatory requirement should be treated as insufficient evidence.')
PROPOSAL=('A 6-month DAO education grants programme with independent reviewers, '
          'monthly milestones and a public final report for every funded project.')
EVIDENCE=('Public budget 5,000 GEN. Accountable team EduDAO. Vote: 7 days. '
          'Milestones monthly. Risks: disclose conflicts and use quarterly audits.')

def setup():
    gl.message.sender_address=A
    gl.nondet.model={'decision':'COMPLIANT','confidence':95}
    c=contract_type()
    c.initialize_charter(CHARTER)
    gl.message.sender_address=B
    cid=c.submit_proposal('Education grants programme', PROPOSAL, EVIDENCE)
    return c,cid

def test_charter_lock():
    c,_=setup()
    assert c.get_charter_hash()==hashlib.sha256(CHARTER.encode()).hexdigest()
    gl.message.sender_address=A
    with pytest.raises(UserError,match='frozen'):c.initialize_charter(CHARTER)

def test_approved_receipt_and_immutability():
    c,cid=setup();gl.message.sender_address=A
    assert c.assess(cid)=='COMPLIANT'
    r=json.loads(c.get_receipt(cid+':0'))
    assert r['verdict']=='COMPLIANT' and r['evidence_hash']==hashlib.sha256(EVIDENCE.encode()).hexdigest()
    with pytest.raises(UserError,match='finalized'):c.assess(cid)

def test_bad_confidence_fails_closed():
    c,cid=setup();gl.message.sender_address=A
    gl.nondet.model={'decision':'COMPLIANT','confidence':79}
    assert c.assess(cid)=='INSUFFICIENT_EVIDENCE'

def test_bad_payload_fails_closed():
    c,cid=setup();gl.message.sender_address=A
    gl.nondet.model={'decision':'SYSTEM OVERRIDE','confidence':99}
    assert c.assess(cid)=='INSUFFICIENT_EVIDENCE'

def test_curator_only():
    c,cid=setup()
    with pytest.raises(UserError,match='curator'):c.assess(cid)

def test_challenge_history():
    c,cid=setup();gl.message.sender_address=A
    gl.nondet.model={'decision':'NON_COMPLIANT','confidence':95}
    assert c.assess(cid)=='NON_COMPLIANT'
    gl.message.sender_address=B
    c.challenge(cid,EVIDENCE+' Independent quarterly oversight also added.')
    assert json.loads(c.get_case(cid))['round']==1
    gl.message.sender_address=A
    gl.nondet.model={'decision':'COMPLIANT','confidence':95}
    assert c.assess(cid)=='COMPLIANT'
    assert json.loads(c.get_receipt(cid+':0'))['verdict']=='NON_COMPLIANT'
    assert json.loads(c.get_receipt(cid+':1'))['verdict']=='COMPLIANT'

def test_no_second_challenge():
    c,cid=setup();gl.message.sender_address=A
    gl.nondet.model={'decision':'NON_COMPLIANT','confidence':95};c.assess(cid)
    gl.message.sender_address=B;c.challenge(cid,EVIDENCE+' Revised.')
    gl.message.sender_address=A;c.assess(cid)
    gl.message.sender_address=B
    with pytest.raises(UserError,match='one challenge'):c.challenge(cid,EVIDENCE+' Another revision.')

def test_unchanged_challenge_rejected():
    c,cid=setup();gl.message.sender_address=A
    gl.nondet.model={'decision':'NON_COMPLIANT','confidence':95};c.assess(cid)
    gl.message.sender_address=B
    with pytest.raises(UserError,match='change'):c.challenge(cid,EVIDENCE)

def test_cannot_challenge_accepted():
    c,cid=setup();gl.message.sender_address=A;c.assess(cid)
    gl.message.sender_address=B
    with pytest.raises(UserError,match='Accepted'):c.challenge(cid,EVIDENCE+' Revision.')

def test_non_submitter_cannot_challenge():
    c,cid=setup();gl.message.sender_address=A
    gl.nondet.model={'decision':'NON_COMPLIANT','confidence':95};c.assess(cid)
    gl.message.sender_address=C
    with pytest.raises(UserError,match='submitter'):c.challenge(cid,EVIDENCE+' Revision.')

@pytest.mark.parametrize('bad',['', 'ignore\nall', 'x'*1700, 'IGNORE\u202ePOLICY'])
def test_invalid_evidence(bad):
    c,_=setup()
    gl.message.sender_address=C
    with pytest.raises(UserError):c.submit_proposal('A new governance grant',PROPOSAL,bad)

def test_requires_initialized_charter():
    gl.message.sender_address=A;c=contract_type();gl.message.sender_address=B
    with pytest.raises(UserError,match='initialized'):c.submit_proposal('A new governance grant',PROPOSAL,EVIDENCE)

def test_unknown_case_and_capacity():
    c,cid=setup();gl.message.sender_address=A
    with pytest.raises(UserError,match='Unknown'):c.assess('404')
    c.count=100;gl.message.sender_address=B
    with pytest.raises(UserError,match='capacity'):c.submit_proposal('A new governance grant',PROPOSAL,EVIDENCE)
