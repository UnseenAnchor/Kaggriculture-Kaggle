"""Submit through the official Kaggle CLI (requires Kaggle CLI >= 1.8.0)."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
file_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "submission" / "main.py"
message = sys.argv[2] if len(sys.argv) > 2 else "Kaggriculture agent"

candidates = [
    shutil.which("kaggle"),
    r"D:\ke\Scripts\kaggle.exe",
]
cli = next((p for p in candidates if p and Path(p).exists()), None)
if not cli:
    raise SystemExit("Official Kaggle CLI >=1.8.0 not found")

subprocess.run(
    [cli, "competitions", "submit", "kaggriculture", "-f", str(file_path), "-m", message],
    cwd=ROOT,
    check=True,
)
