# Obsidian Headless Sync

On machines without a display, use `obsidian-headless` to sync vaults via Obsidian Sync — useful when an agent writes to the wiki on a server while you browse on desktop/mobile.

## Setup

```bash
# Requires Node.js 22+
npm install -g obsidian-headless

# Login (requires Obsidian account with Sync subscription)
ob login --email <email> --password '<password>'

# Create a remote vault for the wiki
ob sync-create-remote --name "LLM Wiki"

# Connect the wiki directory to the vault
cd ~/wiki
ob sync-setup --vault "<vault-id>"

# Initial sync
ob sync

# Continuous sync (foreground — use systemd for background)
ob sync --continuous
```

## Systemd Background Sync

```ini
# ~/.config/systemd/user/obsidian-wiki-sync.service
[Unit]
Description=Obsidian LLM Wiki Sync
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/path/to/ob sync --continuous
WorkingDirectory=/home/user/wiki
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now obsidian-wiki-sync
sudo loginctl enable-linger $USER
```

## Obsidian Desktop Settings

- Set attachment folder to `raw/assets/`
- Enable Wikilinks (default on)
- Install Dataview for queries like: `TABLE tags FROM "entities" WHERE contains(tags, "company")`

If using an Obsidian skill alongside Create Wiki Skill, set `OBSIDIAN_VAULT_PATH` to the same directory as `WIKI_PATH`.
