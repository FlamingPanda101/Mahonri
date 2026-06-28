# Launches the apologist (Mahonri) gateway with the correct vault path forced into the
# process environment, so it overrides the user-level OBSIDIAN_VAULT_PATH (which points
# at hermes-brain for the main Jarvis bot). Keeps the two bots' vaults separate.
$env:OBSIDIAN_VAULT_PATH = "C:\Users\Josep\hermes-advocate"
$env:HERMES_ACCEPT_HOOKS = "1"
& "C:\Users\Josep\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe" -p apologist gateway run
