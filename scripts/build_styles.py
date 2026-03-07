from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
entry = root / "scss" / "styles.scss"
out = root / "styles.css"

text = entry.read_text()
pattern = re.compile(r'@import\s+"([^"]+)";')

chunks = []
for m in pattern.finditer(text):
    rel = m.group(1)
    file_path = entry.parent / f"{rel}.scss"
    if not file_path.exists():
        # support partial naming with underscore
        rp = Path(rel)
        file_path = (entry.parent / rp.parent / f"_{rp.name}.scss")
    chunks.append(file_path.read_text().rstrip())

out.write_text("\n\n".join(chunks) + "\n")
print(f"Generated {out}")
