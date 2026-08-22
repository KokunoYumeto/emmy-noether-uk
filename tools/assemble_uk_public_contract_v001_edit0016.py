#!/usr/bin/env python3
"""Assemble the deterministic public contract for UK001-EDIT-0016.

The contract is intentionally finite and human-facing: a complete reader, an
editable-source archive, an evidence/provenance archive, a checksum manifest,
and a standalone GitHub repository tree.  Internal task state and temporary
build material are not publication artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VERSION = "2026.08.22-r2"
RELEASE_DATE = "2026-08-22"
RELEASED_AT = "2026-08-22T00:00:00Z"
CONCEPT_DOI = "10.5281/zenodo.21926373"
PREDECESSOR_DOI = "10.5281/zenodo.21926374"
GLOBAL_DOI = "10.5281/zenodo.20412587"
GERMAN_DOI = "10.5281/zenodo.21940320"
GERMAN_AUTHORITY = {
    "authority_id": "NOETH-DE-ED-0015",
    "bytes": 2154017,
    "sha256": "51A25101C04877AE740989E72B2AD65A7A7E65B081077C4A518BF1737AD5B907",
}
REPOSITORY = "https://github.com/KokunoYumeto/emmy-noether-uk"
RELEASE_FILENAMES = (
    "00_NOETHER_UKRAINIAN_COMPLETE_LINKED_READER.pdf",
    "01_NOETHER_UKRAINIAN_EDITABLE_SOURCES.zip",
    "02_NOETHER_UKRAINIAN_EVIDENCE_AND_PROVENANCE.zip",
    "03_NOETHER_UKRAINIAN_SHA256_MANIFEST.txt",
)

PINNED_INPUTS = {
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
    "release_v001_edit0016/source/emmy-noether-ukrainian-v001-edit0016.tex": (
        397,
        "55AED0126C521A18008FA7D4622BB52F638C1DC4CF9560D89EAE9D6F851FADD1",
    ),
    "release_v001_edit0016/pdf/emmy-noether-ukrainian-v001-edit0016.pdf": (
        3292434,
        "846634F9E9F8940D918A1411330D1B801CD7EC27DBC8C1D3603DBBF9CCBFA02B",
    ),
    "release_v001_edit0016/evidence/build-manifest.json": (
        12727,
        "2D05539EBCAFE85241C6D520098BA9BBB321F54A1BE27EF643A725BA2C1925F2",
    ),
    "release_v001_edit0016/evidence/RELEASE_AUDIT_VISUAL_QA_UK001_EDIT0016.json": (
        5712,
        "1B11CDF1EB8FC93E45E4D77A73DF2BBEE713E17D898561F525B7EF1777210D21",
    ),
    "UKRAINIAN_DECISIONS_v001.jsonl": (
        27508,
        "D19E6FAA87237363B036F643A127E8A4D21EBCDD8B05341962603C81AD61B17C",
    ),
    "machine_index/LANGUAGE_EDITION_INDEX.json": (
        5994,
        "6865DB8D81E07824F46371DB49C4771DC3266C81B21ADC86620A54CC0FE6E0E9",
    ),
    "machine_index/README.md": (
        2108,
        "2C8CF91143298F0ED5D761091FF57292036F8BBBE5EB6D9D16CEC5A68516E402",
    ),
}

TOOL_PINS = {
    "apply_uk_portable_provenance_locators_v001.py": (
        7468,
        "8D4BC0C1D7F5A95D3EAD870B372A8A7E617DE84BB0D99E52C2517E199C3636C5",
    ),
    "audit_uk_release_v001_edit0016.py": (
        18273,
        "01163EDBA6FFAC737D95290C4C3C627AAB675901604187F717C8E873B40909FF",
    ),
    "build_uk_edit0015_crosshead_reference.py": (
        7595,
        "41A96C87D8AB381B888E6EEFAEDFAC8038B6201D41893101D25B97941D5B6B68",
    ),
    "build_uk_release_v001_edit0016.py": (
        10796,
        "034D535B4A1DA703EA19E4726D6DDCA9CE5677B93202A454D78342EFBA98D051",
    ),
}

# The builder is portable.  Other historical/QA tools authenticate controlled
# evidence but embed custody-only paths, so their hashes are published instead.
PUBLIC_TOOL_NAMES = ("build_uk_release_v001_edit0016.py",)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def text_bytes(value: str) -> bytes:
    return value.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def record(path: Path, relative_to: Path) -> dict:
    return {
        "path": path.relative_to(relative_to).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def write_exact(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refusing to replace existing output: {path}")
    path.write_bytes(payload)
    if path.read_bytes() != payload:
        raise RuntimeError(f"write readback mismatch: {path}")


def portable_public_text(relative: str, data: bytes) -> tuple[bytes, dict | None]:
    """Remove private Windows custody roots from a public evidence derivative."""

    text = data.decode("utf-8")
    original = data
    replacements = 0
    patterns = (
        (re.compile(r"C:/Users/[^/\\\s\"']+/Documents/interlanguage/", re.I), "interlanguage-workspace://"),
        (re.compile(r"C:\\\\Users\\\\[^\\]+\\\\Documents\\\\interlanguage\\\\", re.I), "interlanguage-workspace://"),
        (re.compile(r"C:\\Users\\[^\\]+\\Documents\\interlanguage\\", re.I), "interlanguage-workspace://"),
        (re.compile(r"C:/Users/[^/\\\s\"']+/", re.I), "user-filesystem://"),
        (re.compile(r"C:\\\\Users\\\\[^\\]+\\\\", re.I), "user-filesystem://"),
        (re.compile(r"C:\\Users\\[^\\]+\\", re.I), "user-filesystem://"),
        (re.compile(r"C:/Users/[^/\\\s\"']+", re.I), "user-filesystem://"),
        (re.compile(r"C:\\\\Users\\\\[^\\\s\"']+", re.I), "user-filesystem://"),
        (re.compile(r"C:\\Users\\[^\\\s\"']+", re.I), "user-filesystem://"),
    )
    for pattern, replacement in patterns:
        text, count = pattern.subn(replacement, text)
        replacements += count
    public = text_bytes(text)
    if public == original:
        return public, None
    return public, {
        "path": relative,
        "policy": "private Windows custody root replaced by a logical public locator; canonical bytes remain in controlled custody",
        "replacements": replacements,
        "canonical": {"bytes": len(original), "sha256": sha256_bytes(original)},
        "public_copy": {"bytes": len(public), "sha256": sha256_bytes(public)},
    }


def authenticate_inputs() -> None:
    failures: list[str] = []
    for relative, expected in {**PINNED_INPUTS, **TOOL_PINS}.items():
        path = ROOT / relative
        if not path.is_file():
            failures.append(f"missing {relative}")
            continue
        actual = (path.stat().st_size, sha256(path))
        if actual != expected:
            failures.append(f"pin mismatch {relative}: expected {expected}, got {actual}")
    if failures:
        raise RuntimeError("\n".join(failures))

    rows = [json.loads(line) for line in (ROOT / "UKRAINIAN_DECISIONS_v001.jsonl").read_text(encoding="utf-8").splitlines()]
    if len(rows) != 16 or len({row["decision_id"] for row in rows}) != 16:
        raise RuntimeError("decision ledger is not the sealed 16-row monotonic sequence")
    if rows[-1]["decision_id"] != "UK001-EDIT-0016":
        raise RuntimeError("decision ledger head mismatch")
    for number in range(1, 17):
        path = ROOT / "decision_records" / f"UK001-EDIT-{number:04d}.json"
        if not path.is_file():
            raise FileNotFoundError(path)
        json.loads(path.read_text(encoding="utf-8"))


def portable_machine_index(version_doi: str) -> dict:
    index = json.loads((ROOT / "machine_index/LANGUAGE_EDITION_INDEX.json").read_text(encoding="utf-8"))
    index["schema"] = "noether-language-edition-index/1.1-public"
    index["edition_status"] = "published_release"
    index["updated_at"] = RELEASED_AT
    for item in index["canonical_sources"]:
        item["path"] = "source/" + Path(item["path"]).name
    index["canonical_reader"]["path"] = "reader/" + RELEASE_FILENAMES[0]
    index["decision_evidence"]["ledger"]["path"] = "evidence/UKRAINIAN_DECISIONS_v001.jsonl"
    index["decision_evidence"]["head_sidecar"]["path"] = "evidence/decisions/UK001-EDIT-0016.json"
    index["qa"]["build_manifest"]["path"] = "evidence/build-manifest.json"
    index["qa"]["release_audit"]["path"] = "evidence/RELEASE_AUDIT_VISUAL_QA_UK001_EDIT0016.json"
    index["publication"].update({
        "version": VERSION,
        "publication_date": RELEASE_DATE,
        "ukrainian_concept_doi": CONCEPT_DOI,
        "current_version_doi": version_doi,
        "repository": REPOSITORY,
        "public_record": f"https://zenodo.org/records/{version_doi.rsplit('.', 1)[-1]}",
        "state_at_index_creation": "sealed public release contract",
        "artifact_contract": list(RELEASE_FILENAMES),
    })
    return index


def readme(version_doi: str) -> str:
    record_id = version_doi.rsplit(".", 1)[-1]
    reader_url = f"https://zenodo.org/records/{record_id}/files/{RELEASE_FILENAMES[0]}"
    return f"""# Еммі Нетер: повне українське видання корпусу

[Читати повний 588-сторінковий PDF]({reader_url}) · [сталий DOI українського видання](https://doi.org/{CONCEPT_DOI}) · [DOI цієї версії](https://doi.org/{version_doi})

Це повне підтримуване українське видання корпусу праць Еммі Нетер: статті 1–43, лекції 1929/30 року про гіперкомплексні величини (праця 44), стаття 45 та українська бібліографія. Разом із книгою оприлюднено редаговані джерела, послідовний журнал редакційних рішень, засоби відтворення, результати складання й перевірки та машинний покажчик.

## Що містить версія {VERSION}

- 588 сторінок формату A4; чотири окремо складані компоненти: 530 + 46 + 7 + 5 сторінок.
- 16 послідовних і відтворюваних редакційних рішень із точними локаторами, доказами, відхиленими варіантами та зворотними перетвореннями; відкритих редакційних блокувань і невирішених диспозицій — 0.
- Два незалежні чисті складання дали побайтово однакові PDF. Перевірено структуру TeX, формули, посилання, шрифти, видобутий текст, відповідність попередній голові після суто прованансної зміни та 25 візуальних контрольних сторінок.
- Приватні шляхи вилучено з публічних копій доказів і замінено переносними логічними локаторами. Машинна точка входу: [`machine/LANGUAGE_EDITION_INDEX.json`](machine/LANGUAGE_EDITION_INDEX.json).

Це машинно-асистоване наукове робоче видання, а не рецензоване критичне видання і не твердження про перевірку носіями української мови. Відсутність зовнішнього, громадського та носійського рецензування розкрито прямо. Наступні виправлення можуть бути випущені як нові версії в тому самому DOI-родоводі.

## Публічні файли

1. `00_...pdf` — повний читальний PDF.
2. `01_...zip` — редаговані TeX-джерела, зображення, інструкції складання та машинний покажчик.
3. `02_...zip` — журнал рішень, докази походження, методика, відтворювальні інструменти та QA.
4. `03_...txt` — SHA-256 і розміри перших трьох файлів.

Німецька проєктна опора: `NOETH-DE-ED-0015`, [DOI {GERMAN_DOI}](https://doi.org/{GERMAN_DOI}). Глобальний багатомовний каталог: [DOI {GLOBAL_DOI}](https://doi.org/{GLOBAL_DOI}). Межі прав описано в [`LICENSE`](LICENSE).

---

# Emmy Noether: Complete Ukrainian Corpus Edition

[Read the complete 588-page PDF]({reader_url}) · [stable Ukrainian concept DOI](https://doi.org/{CONCEPT_DOI}) · [DOI for this version](https://doi.org/{version_doi})

This is the complete maintained Ukrainian edition of the Emmy Noether corpus: Papers 1–43, the 1929/30 lectures on hypercomplex quantities (Work 44), Paper 45, and the Ukrainian bibliography. Editable sources, the monotonic editorial-decision record, reproduction tools, build and review evidence, and a machine-readable entrypoint accompany the book.

Version {VERSION} seals 16 reversible editorial decisions with zero open holds or unresolved dispositions. Two independent clean builds produced byte-identical PDFs. TeX structure, mathematics, references, fonts, extracted text, cross-head identity after the provenance-only final edit, and 25 visual control pages passed review. Public evidence copies use portable logical locators rather than private workstation paths.

This is a machine-assisted scholarly working edition, not a peer-reviewed critical edition and not a claim of native-speaker certification. The lack of external, community, and native-speaker review is disclosed explicitly. Later corrections may be released as successor versions in the same DOI lineage. See [`METHODOLOGY.md`](METHODOLOGY.md), [`BUILD.md`](BUILD.md), and the machine index for the complete scope and method.
"""


def methodology() -> str:
    return f"""# Методика українського видання / Ukrainian-edition methodology

## Українська версія

### 1. Опора і межі

Редакційна опора цієї лінії — німецький проєктний корпус `NOETH-DE-ED-0015` ({GERMAN_AUTHORITY['sha256']}). Він контролює структуру, формули й передбачуваний зміст, але не оголошується критичним німецьким виданням. Українські тексти є перекладними свідками цієї редакції; вони не утворюють загального нормативного «канону української математичної мови».

### 2. Як ухвалювалися рішення

Кожна змістова правка отримала послідовний номер `UK001-EDIT-....`, точний локатор, стан до й після, ролі джерел, відхилені варіанти, оцінку невизначеності та зворотне перетворення. Галузеву термінологічну літературу застосовано лише в межах її доказової компетенції. Інші перекладні лінії використовувалися як порівняльні свідки, а не як авторитет української мови.

### 3. Роль ШІ

OpenAI Codex допомагав виявляти розбіжності, формулювати кандидатні читання, збирати докази, виконувати детерміновані перетворення та технічні перевірки. ШІ не підмінено ярликом «перевірено людиною»: зовнішнього, громадського або носійського рецензування не проводилося. Тому публікація чесно називає себе машинно-асистованим науковим робочим виданням.

### 4. Відтворюваність і походження

Попередні свідки не переписувалися заднім числом. Шістнадцятирядковий журнал задає монотонний порядок рішень, а кожне перетворення має побайтовий попередник і зворотний хід. Чотири TeX-джерела та один графічний ресурс закріплено довжиною й SHA-256. Завершальна правка змінила лише 198 приватних префіксів у коментарях `Source:` на схему `noether-corpus://`; видимий текст і формули не змінилися.

Публічні копії ранніх записів рішень додатково замінюють локальні корені зберігання логічними URI. `PUBLIC_COPY_TRANSFORMATIONS.json` фіксує довжини й SHA-256 канонічних і публічних копій. Історичні інструменти з локальними шляхами представлені точними хешами вихідних текстів; переносимими виконуваними інструментами випуску є поточний збирач і пакувальник.

### 5. Складання та перевірка

Кожний компонент двічі послідовно складався XeLaTeX без shell escape і потім об'єднувався в A4-читач. Два чисті складання побайтово збіглися. Випуск блокується за відсутнього знака, невизначеного посилання чи цитати, повторної мітки або хибної кількості сторінок. Для всіх 530 сторінок компонента статей 1–43 потоки вмісту й видобутий текст збіглися з попередником після суто прованансної правки. Окремо переглянуто 25 сторінок, що охоплюють виправлені місця, межі всіх компонентів, повну статтю 45 і останню сторінку. Всі 83 шрифтові записи вбудовані й підмножинні; обмеження ToUnicode дев'яти традиційних математичних шрифтів розкрито.

### 6. Публікаційна й правова межа

PDF є похідним результатом, а не незалежним перекладним свідком. CC0 застосовується лише до тих створених проєктом перекладів, набору, метаданих, інструментів і доказів, щодо яких проєкт має відповідні права. Оригінальні праці, німецький редакційний матеріал, факсиміле, шрифти, програми й інші сторонні об'єкти зберігають власний правовий статус.

## English counterpart

The project German authority is `NOETH-DE-ED-0015`; it controls structure, formulas, and intended meaning but is not claimed as a critical German edition. Every substantive Ukrainian change has a monotonic `UK001-EDIT-....` record with exact locators, before/after payloads, evidence roles, rejected alternatives, uncertainty, and reverse replay. Domain terminology sources are used only within their evidentiary scope; other translation lanes are comparators, not native-Ukrainian authority.

OpenAI Codex assisted with discrepancy detection, candidate formulation, evidence assembly, deterministic transformation, and technical QA. No external, community, or native-speaker review is claimed. Four pinned TeX sources and one pinned image build serially with two XeLaTeX passes and no shell escape. Two clean builds are byte-identical; structural, math, reference, citation, label, font, text-extraction, cross-head, and targeted visual gates pass. The public machine index makes the edition discoverable and replayable without private filesystem paths.

The final edit changed only 198 provenance prefixes in TeX comments to portable `noether-corpus://` locators. A 530-page cross-head comparison found no content-stream or extracted-text difference. Public derivatives of older decision records replace private custody roots with logical URIs and pin both canonical and public-copy hashes. Historical tools that embed local custody paths are represented by exact source hashes; the current builder and package assembler are portable. The PDF is a derived artifact, not an independent translation witness, and the rights boundary above remains controlling.
"""


def build_instructions() -> str:
    return """# Складання / Build

Вимоги: Python 3, XeLaTeX і пакет Python `pypdf`. Розпакуйте архів зі збереженням структури та виконайте з його кореня:

```text
python build_uk_release_v001_edit0016.py --build
```

Збирач перевіряє розміри й SHA-256 чотирьох TeX-файлів і зображення, виконує по два послідовні проходи XeLaTeX без shell escape та створює чотири компонентні PDF і повний A4-читач. Зафіксований результат скінченного аудиту та точні хеші його контрольованих інструментів містяться в архіві доказів.

Requirements: Python 3, XeLaTeX, and the Python package `pypdf`. Run the command above from the extracted archive root. The builder authenticates the four TeX files and image by byte count and SHA-256, performs two serial XeLaTeX passes without shell escape, and creates four component PDFs plus the complete A4 reader. The sealed finite-audit result and exact hashes of its controlled tools are in the evidence archive.
"""


def license_text() -> str:
    return """Посвята CC0 1.0 Universal застосовується лише тією мірою, якою проєкт має права на створені ним переклад, набір, метадані, маніфести, інструменти та докази. Оригінальні праці Еммі Нетер, німецький редакційний матеріал, факсиміле, шрифти, програми та інші сторонні матеріали не переліцензовуються і зберігають власний правовий статус та ліцензії.

CC0 1.0 Universal dedication applies only to the extent rights exist in project-created translation, typesetting, metadata, manifests, tools, and evidence. Emmy Noether's original works, German editorial material, facsimiles, fonts, software, and other third-party material are not relicensed and retain their own legal status and licenses.
"""


def citation_cff(version_doi: str) -> str:
    return f'''cff-version: 1.2.0
message: "Якщо ви використовуєте це видання, цитуйте наведену бібліографічну форму. / If you use this edition, cite the preferred citation."
title: "Еммі Нетер: повне українське видання корпусу"
type: dataset
authors:
  - family-names: Noether
    given-names: Emmy
version: "{VERSION}"
date-released: "{RELEASE_DATE}"
url: "https://doi.org/{version_doi}"
preferred-citation:
  type: book
  title: "Еммі Нетер: повне українське видання корпусу / Emmy Noether: Complete Ukrainian Corpus Edition"
  authors:
    - family-names: Noether
      given-names: Emmy
  doi: "{version_doi}"
  version: "{VERSION}"
  date-released: "{RELEASE_DATE}"
  languages:
    - "uk"
'''


def coverage_tsv() -> str:
    return """component\tcoverage\tpages\tartifact\tproject_authority
Статті 1–43 / Papers 1–43\tcomplete\t530\tbase-papers1-43-uk.tex\tNOETH-DE-ED-0015
Лекції 1929/30 / Work 44\tcomplete\t46\t44-book-uk.tex\tNOETH-DE-ED-0015
Стаття 45 / Paper 45\tcomplete\t7\t45-uk.tex\tNOETH-DE-ED-0015
Бібліографія / Bibliography\tcomplete\t5\tbib-uk.tex\tNOETH-DE-ED-0015
"""


def limitations_tsv() -> str:
    return """item_id\tstatus\tdescription
GENERAL-001\tdisclosed\tМашинно-асистоване наукове робоче видання; наступні виправлення виходять новими версіями. / Machine-assisted scholarly working edition; later corrections are released as successor versions.
REVIEW-001\tnot_completed_not_a_gate\tНе заявлено зовнішньої, громадської чи носійської сертифікації українського тексту. / No external, community, or native-speaker certification is claimed.
CRITICAL-001\tnot_claimed\tНі німецька опора проєкту, ні український переклад не оголошуються критичним виданням. / Neither the project German authority nor this Ukrainian translation is claimed as a critical edition.
OPEN-HOLDS\tzero\tНа голові UK001-EDIT-0016 немає відкритих редакційних блокувань чи диспозицій. / No open editorial holds or dispositions at UK001-EDIT-0016.
MATH-FONT-001\tdisclosed\tДев'ять традиційних математичних символьних шрифтів не мають ToUnicode; текстові та кириличні шрифти його мають. / Nine traditional math-symbol fonts lack ToUnicode; text and Cyrillic fonts carry it.
"""


def datacite_relations(version_doi: str) -> dict:
    return {
        "schema": "noether-language-datacite-relations/1.1",
        "language": {"bcp47": "uk", "script": "Cyrl", "name": "Ukrainian / українська"},
        "language_concept_doi": CONCEPT_DOI,
        "exact_release_doi": version_doi,
        "relations": [
            {"subject": CONCEPT_DOI, "relationType": "IsPartOf", "object": GLOBAL_DOI},
            {"subject": version_doi, "relationType": "IsVersionOf", "object": CONCEPT_DOI},
            {"subject": version_doi, "relationType": "IsDerivedFrom", "object": GERMAN_DOI},
            {"subject": version_doi, "relationType": "IsSupplementedBy", "object": REPOSITORY},
        ],
        "translation_semantics": {
            "intended_relation": "IsTranslationOf",
            "object": {"doi": GERMAN_DOI, **GERMAN_AUTHORITY},
            "note": "The precise translation relation is preserved here and in prose; the public Zenodo relation uses IsDerivedFrom where its form vocabulary requires a supported relation.",
        },
    }


def zenodo_metadata(version_doi: str) -> dict:
    record_id = version_doi.rsplit(".", 1)[-1]
    reader_url = f"https://zenodo.org/records/{record_id}/files/{RELEASE_FILENAMES[0]}"
    description = (
        f'<p><strong><a href="{reader_url}">Читати повне 588-сторінкове українське видання</a></strong> / '
        f'<a href="{reader_url}?download=1">завантажити PDF</a>.</p>'
        f'<p>Повне підтримуване українське видання корпусу Еммі Нетер: статті 1–43, лекції 1929/30 року про гіперкомплексні величини (праця 44), стаття 45 та українська бібліографія. Версія {VERSION} закріплює 16 послідовних відтворюваних редакційних рішень, переносні локатори походження та два побайтово однакові чисті складання. Перевірено структуру TeX, математичний запис, посилання, шрифти, видобутий текст, міжголовну тотожність після суто прованансної правки та контрольні сторінки; відкритих редакційних блокувань немає.</p>'
        '<p>Це машинно-асистоване наукове робоче видання, а не рецензоване критичне видання і не твердження про перевірку носіями української мови. Редаговані джерела, рішення, засоби відтворення, QA та машинний покажчик оприлюднено разом із книгою.</p>'
        f'<p>Сталий DOI українського видання: <a href="https://doi.org/{CONCEPT_DOI}">{CONCEPT_DOI}</a>; DOI цієї версії: <a href="https://doi.org/{version_doi}">{version_doi}</a>. Німецька проєктна опора: <a href="https://doi.org/{GERMAN_DOI}">NOETH-DE-ED-0015</a>; глобальний багатомовний каталог: <a href="https://doi.org/{GLOBAL_DOI}">{GLOBAL_DOI}</a>; джерела: <a href="{REPOSITORY}">{REPOSITORY}</a>.</p>'
        f'<hr><p><strong>English.</strong> This complete maintained Ukrainian edition covers Papers 1–43, the 1929/30 hypercomplex-quantities lectures, Paper 45, and the Ukrainian bibliography. Version {VERSION} seals 16 reversible editorial decisions, portable provenance locators, two byte-identical clean builds, and passing TeX/math/link/font/text/cross-head/visual QA, with zero open editorial holds. It is a machine-assisted scholarly working edition, not a peer-reviewed critical edition and not a claim of native-speaker certification. Editable sources, replay evidence, reproduction tools, and the public machine index accompany the reader.</p>'
        '<p>CC0 applies only to the extent rights exist in project-created translation, typesetting, metadata, manifests, tools, and evidence. Original works, German editorial material, facsimiles, fonts, software, and other third-party material retain their own legal status and licenses.</p>'
    )
    return {
        "upload_type": "publication",
        "publication_type": "book",
        "title": "Еммі Нетер: повне українське видання корпусу / Emmy Noether: Complete Ukrainian Corpus Edition",
        "creators": [{"name": "Noether, Emmy"}],
        "contributors": [{"name": "AI typesetting & translation", "type": "Other"}],
        "description": description,
        "access_right": "open",
        "license": "cc-zero",
        "publication_date": RELEASE_DATE,
        "version": VERSION,
        "language": "ukr",
        "keywords": [
            "Еммі Нетер", "Emmy Noether", "українська мова", "Ukrainian",
            "переклад", "translation", "математика", "алгебра", "machine-assisted edition",
        ],
        "related_identifiers": [
            {"identifier": GLOBAL_DOI, "relation": "isPartOf", "resource_type": "publication-other"},
            {"identifier": GERMAN_DOI, "relation": "isDerivedFrom", "resource_type": "publication-book"},
            {"identifier": REPOSITORY, "relation": "isSupplementedBy", "resource_type": "software"},
        ],
    }


def zip_exact(path: Path, entries: dict[str, bytes]) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(path)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(2026, 8, 22, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, entries[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(path, "r") as archive:
        if archive.testzip() is not None:
            raise RuntimeError(f"ZIP CRC failure: {path}")
        if archive.namelist() != sorted(entries):
            raise RuntimeError(f"ZIP inventory/order mismatch: {path}")
        for name, payload in entries.items():
            if archive.read(name) != payload:
                raise RuntimeError(f"ZIP payload mismatch: {path}!{name}")
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "entries": len(entries),
        "uncompressed_bytes": sum(len(payload) for payload in entries.values()),
    }


def collect_decisions() -> tuple[dict[str, bytes], list[dict]]:
    entries: dict[str, bytes] = {}
    transformations: list[dict] = []
    for number in range(1, 17):
        stem = f"UK001-EDIT-{number:04d}"
        for suffix in (".json", ".md"):
            source = ROOT / "decision_records" / f"{stem}{suffix}"
            if not source.is_file():
                continue
            relative = f"evidence/decisions/{source.name}"
            public, transformation = portable_public_text(relative, source.read_bytes())
            entries[relative] = public
            if transformation:
                transformations.append(transformation)
    return entries, transformations


def collect_tools() -> dict[str, bytes]:
    entries = {f"tools/{name}": (ROOT / name).read_bytes() for name in PUBLIC_TOOL_NAMES}
    entries[f"tools/{Path(__file__).name}"] = Path(__file__).read_bytes()
    return entries


def historical_tool_hashes_tsv() -> bytes:
    lines = ["path\tbytes\tsha256\tpublic_disposition"]
    for name, (size, digest) in sorted(TOOL_PINS.items()):
        disposition = "portable_executable_in_archive" if name in PUBLIC_TOOL_NAMES else "canonical_source_hash_only_private_custody_paths_not_published"
        lines.append(f"{name}\t{size}\t{digest}\t{disposition}")
    return text_bytes("\n".join(lines) + "\n")


def assemble(output: Path, version_doi: str) -> dict:
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    output.mkdir(parents=True)
    release = output / "release"
    repository = output / "repository_tree"
    release.mkdir()
    repository.mkdir()

    index_bytes = json_bytes(portable_machine_index(version_doi))
    readme_bytes = text_bytes(readme(version_doi))
    methodology_bytes = text_bytes(methodology())
    build_bytes = text_bytes(build_instructions())
    license_bytes = text_bytes(license_text())
    coverage_bytes = text_bytes(coverage_tsv())
    limitations_bytes = text_bytes(limitations_tsv())
    relations_bytes = json_bytes(datacite_relations(version_doi))
    zenodo_bytes = json_bytes(zenodo_metadata(version_doi))
    decision_entries, transformations = collect_decisions()
    transformations_bytes = json_bytes({
        "schema": "noether-public-copy-transformations/1.0",
        "policy": "Only public derivatives are path-sanitized; canonical controlled-workspace bytes and hashes remain unchanged.",
        "logical_roots": {
            "interlanguage-workspace://": "repository/project-relative custody root",
            "user-filesystem://": "non-workspace user-file root; resolve from evidence rather than a private path",
        },
        "files": sorted(transformations, key=lambda item: item["path"]),
    })
    tool_hashes_bytes = historical_tool_hashes_tsv()

    reader_source = ROOT / "release_v001_edit0016/pdf/emmy-noether-ukrainian-v001-edit0016.pdf"
    reader_public = release / RELEASE_FILENAMES[0]
    shutil.copyfile(reader_source, reader_public)
    if reader_public.read_bytes() != reader_source.read_bytes():
        raise RuntimeError("reader copy mismatch")

    source_entries: dict[str, bytes] = {
        "README.md": readme_bytes,
        "BUILD.md": build_bytes,
        "LICENSE": license_bytes,
        "machine/LANGUAGE_EDITION_INDEX.json": index_bytes,
        "machine/README.md": (ROOT / "machine_index/README.md").read_bytes(),
        "release_metadata/COMPONENT_COVERAGE.tsv": coverage_bytes,
        "release_metadata/DATACITE_RELATIONS.json": relations_bytes,
        "release_metadata/LIMITATIONS_AND_REVIEW.tsv": limitations_bytes,
        "release_metadata/RELEASE_IDENTITY.json": json_bytes({
            "schema": "noether-ukrainian-release-identity/1.0",
            "version": VERSION,
            "publication_date": RELEASE_DATE,
            "concept_doi": CONCEPT_DOI,
            "version_doi": version_doi,
            "decision_head": "UK001-EDIT-0016",
            "repository": REPOSITORY,
        }),
        "source/base-papers1-43-uk.tex": (ROOT / "source/base-papers1-43-uk.tex").read_bytes(),
        "source/44-book-uk.tex": (ROOT / "source/44-book-uk.tex").read_bytes(),
        "source/45-uk.tex": (ROOT / "source/45-uk.tex").read_bytes(),
        "source/bib-uk.tex": (ROOT / "source/bib-uk.tex").read_bytes(),
        "source/emmy-noether-ukrainian-v001-edit0016.tex": (ROOT / "release_v001_edit0016/source/emmy-noether-ukrainian-v001-edit0016.tex").read_bytes(),
        "assets/authority_rosette_native_supported_mask.png": (ROOT / "assets/authority_rosette_native_supported_mask.png").read_bytes(),
        "build_uk_release_v001_edit0016.py": (ROOT / "build_uk_release_v001_edit0016.py").read_bytes(),
    }
    source_zip_record = zip_exact(release / RELEASE_FILENAMES[1], source_entries)

    evidence_entries: dict[str, bytes] = {
        "README.md": readme_bytes,
        "METHODOLOGY.md": methodology_bytes,
        "LICENSE": license_bytes,
        "COMPONENT_COVERAGE.tsv": coverage_bytes,
        "DATACITE_RELATIONS.json": relations_bytes,
        "LIMITATIONS_AND_REVIEW.tsv": limitations_bytes,
        "machine/LANGUAGE_EDITION_INDEX.json": index_bytes,
        "machine/LANGUAGE_EDITION_INDEX.workspace.json": (ROOT / "machine_index/LANGUAGE_EDITION_INDEX.json").read_bytes(),
        "machine/README.md": (ROOT / "machine_index/README.md").read_bytes(),
        "evidence/UKRAINIAN_DECISIONS_v001.jsonl": (ROOT / "UKRAINIAN_DECISIONS_v001.jsonl").read_bytes(),
        "evidence/build-manifest.json": (ROOT / "release_v001_edit0016/evidence/build-manifest.json").read_bytes(),
        "evidence/RELEASE_AUDIT_VISUAL_QA_UK001_EDIT0016.json": (ROOT / "release_v001_edit0016/evidence/RELEASE_AUDIT_VISUAL_QA_UK001_EDIT0016.json").read_bytes(),
        "evidence/PUBLIC_COPY_TRANSFORMATIONS.json": transformations_bytes,
        "evidence/HISTORICAL_TOOL_SOURCE_HASHES.tsv": tool_hashes_bytes,
        "evidence/PREDECESSOR_RELEASE.json": json_bytes({
            "schema": "noether-ukrainian-predecessor-release/1.0",
            "version": "2026.08.14-r1",
            "version_doi": PREDECESSOR_DOI,
            "concept_doi": CONCEPT_DOI,
            "preservation_note": "The predecessor remains immutable and public; this successor records the complete UK001 decision lineage and does not silently rewrite it.",
        }),
    }
    evidence_entries.update(decision_entries)
    evidence_entries.update(collect_tools())
    evidence_zip_record = zip_exact(release / RELEASE_FILENAMES[2], evidence_entries)

    manifest_lines = []
    for name in RELEASE_FILENAMES[:3]:
        path = release / name
        manifest_lines.append(f"{sha256(path)}  {path.stat().st_size}  {name}")
    write_exact(release / RELEASE_FILENAMES[3], text_bytes("\n".join(manifest_lines) + "\n"))

    repo_files: dict[str, bytes] = {
        "README.md": readme_bytes,
        "METHODOLOGY.md": methodology_bytes,
        "BUILD.md": build_bytes,
        "LICENSE": license_bytes,
        "CITATION.cff": text_bytes(citation_cff(version_doi)),
        ".zenodo.json": zenodo_bytes,
        ".publication_identity.json": json_bytes({
            "schema": "emmy-noether-language-repository-identity/1.1",
            "language": "uk-Cyrl",
            "release_tag": f"v{VERSION}",
            "concept_doi": CONCEPT_DOI,
            "version_doi": version_doi,
            "repository": REPOSITORY,
            "decision_head": "UK001-EDIT-0016",
        }),
        f"reader/{RELEASE_FILENAMES[0]}": reader_public.read_bytes(),
        "source/base-papers1-43-uk.tex": source_entries["source/base-papers1-43-uk.tex"],
        "source/44-book-uk.tex": source_entries["source/44-book-uk.tex"],
        "source/45-uk.tex": source_entries["source/45-uk.tex"],
        "source/bib-uk.tex": source_entries["source/bib-uk.tex"],
        "source/emmy-noether-ukrainian-v001-edit0016.tex": source_entries["source/emmy-noether-ukrainian-v001-edit0016.tex"],
        "assets/authority_rosette_native_supported_mask.png": source_entries["assets/authority_rosette_native_supported_mask.png"],
        "machine/LANGUAGE_EDITION_INDEX.json": index_bytes,
        "machine/README.md": source_entries["machine/README.md"],
        "evidence/UKRAINIAN_DECISIONS_v001.jsonl": evidence_entries["evidence/UKRAINIAN_DECISIONS_v001.jsonl"],
        "evidence/build-manifest.json": evidence_entries["evidence/build-manifest.json"],
        "evidence/RELEASE_AUDIT_VISUAL_QA_UK001_EDIT0016.json": evidence_entries["evidence/RELEASE_AUDIT_VISUAL_QA_UK001_EDIT0016.json"],
        "evidence/COMPONENT_COVERAGE.tsv": coverage_bytes,
        "evidence/DATACITE_RELATIONS.json": relations_bytes,
        "evidence/LIMITATIONS_AND_REVIEW.tsv": limitations_bytes,
        "evidence/PUBLIC_COPY_TRANSFORMATIONS.json": transformations_bytes,
        "evidence/HISTORICAL_TOOL_SOURCE_HASHES.tsv": tool_hashes_bytes,
        "evidence/PUBLIC_ARTIFACT_SHA256.tsv": text_bytes(
            "filename\tbytes\tsha256\n" + "".join(
                f"{name}\t{(release / name).stat().st_size}\t{sha256(release / name)}\n"
                for name in RELEASE_FILENAMES
            )
        ),
    }
    repo_files.update(decision_entries)
    repo_files.update(collect_tools())
    for relative, payload in sorted(repo_files.items()):
        write_exact(repository / relative, payload)
    tree_tsv = "path\tbytes\tsha256\n" + "".join(
        f"{relative}\t{len(payload)}\t{sha256_bytes(payload)}\n"
        for relative, payload in sorted(repo_files.items())
    )
    write_exact(repository / "evidence/REPOSITORY_TREE_SHA256.tsv", text_bytes(tree_tsv))

    package = {
        "schema": "noether-ukrainian-public-contract/1.0",
        "release_id": "NOETHER-UK-v001-UK001-EDIT-0016",
        "version": VERSION,
        "publication_date": RELEASE_DATE,
        "concept_doi": CONCEPT_DOI,
        "version_doi": version_doi,
        "decision_head": "UK001-EDIT-0016",
        "authenticated_inputs": {
            relative: {"bytes": size, "sha256": digest}
            for relative, (size, digest) in sorted(PINNED_INPUTS.items())
        },
        "release_files": [record(release / name, output) for name in RELEASE_FILENAMES],
        "source_archive_verification": source_zip_record,
        "evidence_archive_verification": evidence_zip_record,
        "repository_files": [
            record(path, output)
            for path in sorted(repository.rglob("*"))
            if path.is_file()
        ],
        "public_status": {
            "editorial_holds": 0,
            "unresolved_editorial_dispositions": 0,
            "reader_pages": 588,
            "deterministic_build": "PASS",
            "finite_audit": "PASS",
            "visual_qa": "PASS",
            "native_review": "not completed; not claimed",
            "critical_edition": "not claimed",
        },
    }
    package_path = output / "PACKAGE_MANIFEST.json"
    write_exact(package_path, json_bytes(package))
    json.loads(package_path.read_text(encoding="utf-8"))
    return package


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--version-doi", required=True)
    args = parser.parse_args()
    if not args.version_doi.startswith("10.5281/zenodo."):
        parser.error("--version-doi must be a Zenodo DOI")
    authenticate_inputs()
    package = assemble(args.output.resolve(), args.version_doi)
    print(json.dumps({
        "status": "PASS",
        "version_doi": package["version_doi"],
        "release_files": package["release_files"],
        "repository_file_count": len(package["repository_files"]),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
