#!/bin/sh
set -eu
cp /keys/id_ed25519 /tmp/inventory-key
chmod 600 /tmp/inventory-key
exec ansible-playbook "$@"
