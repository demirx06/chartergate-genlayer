"""Pure Python SDK stub. Never call this GenLayer Direct Mode or chain proof."""
import importlib.util
import json
import sys
import types
from pathlib import Path

class UserError(Exception):
    pass
class Result:
    def __init__(self, calldata): self.calldata = calldata
class VM:
    UserError = UserError
    Return = Result
    def run_nondet_unsafe(self, leader, validator):
        value = leader()
        if not validator(Result(value)):
            raise UserError('Validator disagreement')
        return value
class GL:
    Contract = type('Contract', (), {})
    vm = VM()
    message = types.SimpleNamespace(sender_address='0x'+'a'*40)
    public = types.SimpleNamespace(write=lambda f:f, view=lambda f:f)
    nondet = types.SimpleNamespace(model={"decision":"COMPLIANT","confidence":92})
    nondet.exec_prompt = lambda prompt, response_format='json': GL.nondet.model

sdk=types.ModuleType('genlayer')
sdk.gl=GL;sdk.TreeMap=dict;sdk.u32=int
sys.modules['genlayer']=sdk

spec=importlib.util.spec_from_file_location('charter_gate', Path(__file__).resolve().parents[2]/'contracts/charter_gate.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
contract_type=module.CharterGate
