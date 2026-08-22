#!/usr/bin/env python3
"""Build the authenticated Emmy Noether Ukrainian UK001-EDIT-0016 reader."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
RELEASE = ROOT / "release_v001_edit0016"
BUILD = ROOT / "tmp" / "pdfs" / "uk_release_v001_edit0016"
SOURCE_DATE_EPOCH = "1787356800"  # 2026-08-22T00:00:00Z

SOURCE_PINS = {
    "source/base-papers1-43-uk.tex": (
        2683138,
        "508BE633BD8DF81854582BD5FE7229A4B09C3AA1EDEDC7D0909FA6C00204CC4D",
    ),
    "source/44-book-uk.tex": (
        234758,
        "7C52BCFAD8B097DE6D2C94C37290BEA63D0320E1B282763299C16394D69F451F",
    ),
    "source/45-uk.tex": (
        35081,
        "8437DB33C1A2D42AFFCEA56EECBA74300232D81AB79C808754671E5F6299BBD9",
    ),
    "source/bib-uk.tex": (
        12777,
        "8A15AB2116E25CCEA760AD96E26ACDF217333CE6B3679D3D5FA235A1992D0F09",
    ),
    "assets/authority_rosette_native_supported_mask.png": (
        797,
        "B2AF3955A8255B4A6D925E174B7B81311C64C669CE21B07E75002494E55F2FF5",
    ),
}

COMPONENTS = (
    ("base-papers1-43", "source/base-papers1-43-uk.tex"),
    ("44-book", "source/44-book-uk.tex"),
    ("45", "source/45-uk.tex"),
    ("bib", "source/bib-uk.tex"),
)
READER_NAME = "emmy-noether-ukrainian-v001-edit0016"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def record(path: Path, *, relative_to: Path = ROOT) -> dict:
    return {
        "path": path.resolve().relative_to(relative_to.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def authenticate_sources() -> None:
    failures: list[str] = []
    for relative, expected in SOURCE_PINS.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing {relative}")
            continue
        actual = (path.stat().st_size, sha256(path))
        if actual != expected:
            failures.append(f"pin mismatch {relative}: expected {expected}, got {actual}")
    if failures:
        raise RuntimeError("\n".join(failures))


def install_exact(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.is_file() and target.read_bytes() == source.read_bytes():
            return
        raise FileExistsError(f"refusing non-identical release source: {target}")
    shutil.copy2(source, target)
    if target.read_bytes() != source.read_bytes():
        raise RuntimeError(f"copy verification failed: {target}")


def write_exact(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == payload:
            return
        raise FileExistsError(f"refusing non-identical authored file: {path}")
    path.write_bytes(payload)


def prepare_release_sources() -> list[dict]:
    installed: list[dict] = []
    for relative in SOURCE_PINS:
        source = ROOT / relative
        if relative.startswith("source/"):
            target = RELEASE / "source" / source.name
        else:
            target = RELEASE / "source" / "assets" / source.name
        install_exact(source, target)
        installed.append(record(target))
    return installed


def warning_summary(log_path: Path) -> dict:
    text = log_path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    return {
        "missing_character": lowered.count("missing character:"),
        "undefined_reference": lowered.count("reference") if "there were undefined references" in lowered else 0,
        "undefined_citation": lowered.count("citation") if "there were undefined citations" in lowered else 0,
        "multiply_defined_label": lowered.count("multiply defined"),
        "overfull_hbox": lowered.count("overfull \\hbox"),
        "overfull_vbox": lowered.count("overfull \\vbox"),
    }


def clear_outputs(build_dir: Path, jobname: str) -> None:
    for name in (
        f"{jobname}.aux", f"{jobname}.log", f"{jobname}.out", f"{jobname}.pdf",
        f"{jobname}.synctex.gz", f"{jobname}.toc", f"{jobname}.xdv",
        "pass1.stdout.log", "pass2.stdout.log",
    ):
        path = build_dir / name
        if path.is_file():
            path.unlink()


def run_xelatex(source: Path, build_dir: Path, jobname: str) -> tuple[Path, list[dict]]:
    build_dir.mkdir(parents=True, exist_ok=True)
    clear_outputs(build_dir, jobname)
    environment = os.environ.copy()
    environment.update({"SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH, "FORCE_SOURCE_DATE": "1", "TZ": "UTC"})
    logs: list[dict] = []
    for pass_number in (1, 2):
        command = [
            "xelatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
            "-file-line-error", f"-jobname={jobname}", f"-output-directory={build_dir.resolve()}",
            str(source.resolve()),
        ]
        completed = subprocess.run(
            command, cwd=source.parent, env=environment, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace",
        )
        stdout_path = build_dir / f"pass{pass_number}.stdout.log"
        stdout_path.write_text(completed.stdout, encoding="utf-8", newline="\n")
        tex_log = build_dir / f"{jobname}.log"
        entry = {"pass": pass_number, "exit_code": completed.returncode, "stdout": record(stdout_path)}
        if tex_log.exists():
            entry["tex_log"] = record(tex_log)
            entry["warnings"] = warning_summary(tex_log)
        logs.append(entry)
        if completed.returncode:
            raise RuntimeError(f"XeLaTeX failed for {source}; see {stdout_path}")
    produced = build_dir / f"{jobname}.pdf"
    if not produced.is_file():
        raise FileNotFoundError(produced)
    final = logs[-1].get("warnings", {})
    for key in ("missing_character", "undefined_reference", "undefined_citation", "multiply_defined_label"):
        if final.get(key):
            raise RuntimeError(f"release-blocking {key} in {build_dir / (jobname + '.log')}")
    return produced, logs


def install_generated(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".new")
    if temporary.exists():
        temporary.unlink()
    shutil.copy2(source, temporary)
    if temporary.read_bytes() != source.read_bytes():
        raise RuntimeError(f"generated copy mismatch: {target}")
    os.replace(temporary, target)


def pages(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


def cumulative_recipe(component_pdfs: list[Path]) -> Path:
    recipe = RELEASE / "source" / f"{READER_NAME}.tex"
    lines = [
        "% Portable cumulative reader recipe; component hashes are in evidence/build-manifest.json.",
        r"\documentclass[a4paper]{article}", r"\usepackage{pdfpages}", r"\begin{document}",
    ]
    for component in component_pdfs:
        relative = Path("..") / "pdf" / "components" / component.name
        lines.append(r"\includepdf[pages=-]{" + relative.as_posix() + "}")
    lines.append(r"\end{document}")
    write_exact(recipe, ("\n".join(lines) + "\n").encode("utf-8"))
    return recipe


def build_release() -> dict:
    source_records = prepare_release_sources()
    (RELEASE / "pdf" / "components").mkdir(parents=True, exist_ok=True)
    (RELEASE / "evidence").mkdir(parents=True, exist_ok=True)
    components: list[dict] = []
    component_outputs: list[Path] = []
    for stem, relative in COMPONENTS:
        source = RELEASE / "source" / Path(relative).name
        jobname = f"{stem}-uk"
        produced, logs = run_xelatex(source, BUILD / "components" / stem, jobname)
        output = RELEASE / "pdf" / "components" / f"{jobname}.pdf"
        install_generated(produced, output)
        component_outputs.append(output)
        components.append({
            "component": stem, "source": record(source),
            "pdf": {**record(output), "pages": pages(output)}, "build_logs": logs,
        })

    recipe = cumulative_recipe(component_outputs)
    produced, logs = run_xelatex(recipe, BUILD / "reader", READER_NAME)
    reader = RELEASE / "pdf" / f"{READER_NAME}.pdf"
    install_generated(produced, reader)
    expected_pages = sum(item["pdf"]["pages"] for item in components)
    actual_pages = pages(reader)
    if actual_pages != expected_pages:
        raise RuntimeError(f"cumulative page mismatch: {actual_pages} != {expected_pages}")

    manifest = {
        "schema": "noether-ukrainian-build-manifest/1.0",
        "release_id": "NOETHER-UK-v001-UK001-EDIT-0016",
        "generated_at": "2026-08-22T00:00:00Z",
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
        "build_policy": {
            "engine": "XeLaTeX", "passes_per_document": 2, "serial": True, "shell_escape": False,
            "release_blockers": ["nonzero engine exit", "missing glyph", "undefined reference", "undefined citation", "multiply-defined label", "cumulative page mismatch"],
        },
        "authenticated_inputs": {rel: {"bytes": size, "sha256": digest} for rel, (size, digest) in SOURCE_PINS.items()},
        "installed_release_sources": source_records,
        "language": "Ukrainian", "language_tag": "uk-Cyrl", "decision_head": "UK001-EDIT-0016",
        "components": components, "cumulative_recipe": record(recipe),
        "reader_pdf": {**record(reader), "pages": actual_pages}, "build_logs": logs,
    }
    manifest_path = RELEASE / "evidence" / "build-manifest.json"
    manifest_path.write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    if json.loads(manifest_path.read_text(encoding="utf-8")) != manifest:
        raise RuntimeError("manifest readback mismatch")
    return {"manifest": record(manifest_path), "reader": manifest["reader_pdf"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    if args.prepare_only == args.build:
        parser.error("select exactly one of --prepare-only or --build")
    authenticate_sources()
    if args.prepare_only:
        print(json.dumps({"status": "PASS", "installed": prepare_release_sources()}, indent=2))
        return 0
    result = build_release()
    print(json.dumps({"status": "PASS", **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
