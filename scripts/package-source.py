"""Package committed source/evidence, two reports, runnable JAR and both Git branches."""
import hashlib
from pathlib import Path
import subprocess
import zipfile

root = Path(__file__).resolve().parent.parent
subprocess.run(["git", "bundle", "create", str(root / ".lab/source-history.bundle"), "--all"], cwd=root, check=True)
files = subprocess.check_output(["git", "ls-files", "-z"], cwd=root).decode().split("\0")
archive = root / "source-package.zip"
with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
    for name in sorted(filter(None, files)):
        assert not any(part in (".secrets", ".lab", ".git") for part in Path(name).parts), name
        z.write(root / name, "mini-inventory-devops/" + name)
    z.write(root / "target/mini-inventory.jar", "mini-inventory-devops/artifacts/mini-inventory.jar")
    z.write(root / ".lab/source-history.bundle", "mini-inventory-devops/git-history.bundle")
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert sum(n.endswith(".pdf") for n in z.namelist()) == 2
    assert any(n.endswith("repo_link.txt") for n in z.namelist())
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
print(f"Validated {archive.name}: {archive.stat().st_size:,} bytes; SHA256 {digest}")
