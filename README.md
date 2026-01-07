## Reinforced AI Audit Lib

A small helper library for working with Reinforced AI network. It includes:

- **Subtensor client**: a lightweight wrapper around Subtensor (chain) calls
- **Relayer client**: a JSON-RPC client for the Relayer
- **Vulnerability types**: data models describing detected vulnerabilities

## Subtensor Client

```python
get_metagraph(net_uid: int, block_hash=None)
```
Fetch subnet metagraph data (optionally at a given block).

```python
get_axons(net_uid: int, block_hash=None)
```
Build a list of axon entries registered with metagraph fields.

```python
get_served_axon(net_uid: int, axon_hotkey: str) -> dict | None
```
Fetch the currently served axon info for a hotkey.

```python
get_uid(net_uid: int, axon_hotkey: str, block_hash: str | None = None) -> int | None
```
Resolve UID for a hotkey.

```python
get_last_update(net_uid: int, block_hash: str | None = None) -> list[int] | None
```
Read the `LastUpdate` storage for a subnet.

```python
serve_axon(...) -> tuple[bool, dict | None]
```
Serve axon on the subnet (includes rate-limit checks).

```python
get_tempo_and_commit_reveal_period(net_uid: int) -> tuple[int, int]
```
Read tempo and commit-reveal period.

```python
set_weights(...) -> tuple[bool, dict | None]
```
Normalize and submit weights (includes rate-limit checks).

```python
commit_weights(...)
```
Commit timelocked weights for commit-reveal (v4 by default).

```python
set_identity(...)
```
Set on-chain identity if it differs from the current state.

## Relayer Client

```python
get_miners(signer) -> list[AxonInfo]
```
Fetch miners for the given subnet via the relayer.

```python
get_validators(signer) -> list[AxonInfo]
```
Fetch validators for the given subnet via the relayer.

```python
register_axon(signer, params: RegisterParams) -> ResultModel
```
Register an axon in the relayer.

```python
get_storage(signer) -> ResultModel
```
Get hotkey storage from the relayer.

```python
set_storage(signer, storage: MinerStorage | ValidatorStorage) -> ResultModel
```
Set hotkey storage in the relayer.

```python
perform_scan(signer, uid: int, code: str, validator_version: str | None = None) -> MinerResponseMessage
```
Request a solidity contract scan from a miner.

```python
set_top_miners(signer, miners: list[MedalRequestsMessage]) -> ResultModel
```
Store the list of top miners.

```python
get_activation_code(signer) -> str
```
Request a validator activation code.
