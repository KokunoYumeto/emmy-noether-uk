# Складання / Build

Вимоги: Python 3, XeLaTeX і пакет Python `pypdf`. Розпакуйте архів зі збереженням структури та виконайте з його кореня:

```text
python build_uk_release_v001_edit0016.py --build
```

Збирач перевіряє розміри й SHA-256 чотирьох TeX-файлів і зображення, виконує по два послідовні проходи XeLaTeX без shell escape та створює чотири компонентні PDF і повний A4-читач. Зафіксований результат скінченного аудиту та точні хеші його контрольованих інструментів містяться в архіві доказів.

Requirements: Python 3, XeLaTeX, and the Python package `pypdf`. Run the command above from the extracted archive root. The builder authenticates the four TeX files and image by byte count and SHA-256, performs two serial XeLaTeX passes without shell escape, and creates four component PDFs plus the complete A4 reader. The sealed finite-audit result and exact hashes of its controlled tools are in the evidence archive.
