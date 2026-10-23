# CharterGate — reviewer instructions

1. Read contract and security limitations. Nothing here transfers native GEN.
2. Compare published source hash from the CI job to the checked-in contract.
3. Inspect `.github/workflows/ci.yml`. The `tests/offline` suite runs using a fake SDK; the `tests/direct` suite uses the actual `genlayer-test` Direct Mode SDK and validator re-execution. **Both must actually pass in GitHub Actions.** The GenVM linter must pass, too.
4. Check a successful judgment, unauthorized caller rejection, malformed model result, decision-threshold crossing, and validator class disagreement test.
5. To claim public network validation, separately authorize a test wallet and fees, run an authentic GenLayer Studio/Studionet lifecycle, verify state read-back and save actual explorer receipts and finality. Do not claim this has happened yet.
6. Only present personal work with accurate attribution. Another project's acceptance is not a guaranteed points schedule.
