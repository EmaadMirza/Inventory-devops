"""Generate this localhost lab's credentials; never add .secrets to version control."""
from pathlib import Path
import secrets
import subprocess

root = Path(__file__).resolve().parent.parent
folder = root / ".secrets"
folder.mkdir(exist_ok=True)
password = folder / "jenkins-admin-password"
if not password.exists():
    password.write_text(secrets.token_urlsafe(24), encoding="utf-8")
key = folder / "id_ed25519"
if not key.exists():
    subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-f", str(key), "-N", ""], check=True)
print("Lab credentials ready in ignored .secrets; existing credentials preserved.")
