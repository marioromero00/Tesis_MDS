"""Copia verificable de documentos y notas externas al repositorio, sin borrar versiones."""
from pathlib import Path
import hashlib
import json
import shutil

def main():
    repo = Path(__file__).resolve().parents[1]
    base = repo.parent.parent
    destination = repo / "respaldo_local"
    candidates = [base / "README.md", base / "AGENTS.md"]
    candidates += sorted((base / "notas").glob("*.md"))
    candidates += sorted((base / "notas").glob("*.json"))
    candidates += sorted(p for p in (base / "documentos").rglob("*") if p.is_file() and not p.is_symlink() and not p.name.startswith("."))
    assert (base / "documentos/01 Tesis MDS/CLAUDE.md").exists(), "No se encontró el espacio local de tesis"
    records = []
    for source in candidates:
        target = destination / source.relative_to(base)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
        records.append(dict(path=str(target.relative_to(repo)), sha256=digest, bytes=target.stat().st_size))
    (destination / "manifiesto.json").write_text(json.dumps(dict(files=records, excluded=["datos crudos externos", "logs de ejecución externos", "entornos y cachés", "credenciales"]), ensure_ascii=False, indent=2) + "\n")
    print(f"{len(records)} archivos copiados y verificados")

if __name__ == "__main__":
    main()
