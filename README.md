# Еммі Нетер — Математичні праці українською

Український переклад зібрання математичних праць Еммі Нетер (Emmy Noether, 1882–1935): статті 1–43, лекції «Алгебра
гіперкомплексних величин» (зимовий семестр 1929/30 року) в опрацюванні М. Дойрінга (M. Deuring), стаття Г. Капферера
(H. Kapferer) з доповненням, написаним спільно з Е. Нетер, а також бібліографія та списки коротких повідомлень,
рецензій і книжок, у підготовці яких брала участь Еммі Нетер. Видання виходить у PDF і в редагованому LaTeX.

[**Читати основний текст — PDF, 502 сторінка**](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/01-noether-uk-base.pdf) ·
[Текст із редакційними виправленнями — PDF, 508 сторінок](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/04-noether-uk-emendations.pdf) ·
[Усі файли видання від 27 жовтня 2026 року](https://github.com/KokunoYumeto/emmy-noether-uk/releases/tag/noether-uk-2026-11-15-r2)

## How this was made: AI's failure modes, and what we do about them

Everything here was produced by AI. The translation was made in a first pass mostly by GPT-5.6 Sol (OpenAI Codex,
reasoning effort ultra), by the user's account (July and August 2026). Its formulas were then brought into line with the German text, which Claude Opus 5.5 at
effort max compared page by page with Noether's printed originals (785 page checks, 26 October 2026), in automatic and
hand rounds by Claude Opus 5.5 at effort max (26-27 October; 2,570 lines in the last hand round), against the known
failures of AI translation of mathematics: renamed letters, formulas changed or dropped, statements narrowed, passages
reworked or garbled, sentences and displays dropped, broken layout. Every change passes a release filter, and every PDF
is checked for lines running into the margin (Claude Opus 5.5 at effort high, 15 November). No person has reviewed the
translation. What was done in each round, the measured figures and what is still open:
[How this was made](https://github.com/KokunoYumeto/emmy-noether#how-this-was-made-ais-failure-modes-and-what-we-do-about-them).

## Як створено видання

Український текст перекладено ШІ — моделями OpenAI Codex (за словами користувача, переважно GPT-5.6 Sol з рівнем міркування ultra). Виправлення
й набір виконали OpenAI Codex — GPT-6 Astra, рівень міркування Ultra, 23–24 жовтня 2026 року, і Claude Opus 5.5
(Anthropic, рівень міркування max) 26–27 жовтня 2026 року; Claude Opus 5.5 звірив формули з німецьким текстом, прочитаним за друкованими
сторінками Нетер. Програму складання створив OpenAI Codex — GPT-6 Astra, Ultra, 24 жовтня 2026 року.

## Стан

Видання містить усі перелічені праці, але статтю 43 подано скорочено (близько третини повного тексту), а статті 41
і 42 — приблизно в чотирьох п’ятих обсягу. Статті 23, 24, 30, 31, 32, 34, 37 і 41–43, а також частини статей 35 і 40
ґрунтуються на ранішому англійському перекладі, формули якого місцями розходяться з німецьким текстом. У статті 2
три виноски німецького тексту (примітку про Σ₃ і посилання на Gordan — Kerschensteiner, с. 92 і 134) позначено лише
зірочкою або приєднано до сусіднього речення. PDF не мають закладок. Переклад не перевіряла людина, тож у ньому
можуть залишатися помилки; подекуди формули ще можуть іти за попередньою німецькою транскрипцією. Виправлення
приймаються через [сторінку issues](https://github.com/KokunoYumeto/emmy-noether-uk/issues).

## Зміст і з чого почати

Видання має два варіанти тексту; кожен має PDF, один файл LaTeX і архів джерел:

| Варіант | PDF | LaTeX | Джерела |
|---|---|---|---|
| Основний текст: зберігає читання перших публікацій; редакційні примітки обговорюють ці читання | [PDF, 502 с.](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/01-noether-uk-base.pdf) | [LaTeX](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/02-noether-uk-base.tex) | [ZIP](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/03-noether-uk-base-sources.zip) |
| Текст із редакційними виправленнями: виправлення внесено в текст, кожне пояснено в редакційній примітці | [PDF, 508 с.](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/04-noether-uk-emendations.pdf) | [LaTeX](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/05-noether-uk-emendations.tex) | [ZIP](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/06-noether-uk-emendations-sources.zip) |

[Контрольні суми SHA-256](https://github.com/KokunoYumeto/emmy-noether-uk/releases/download/noether-uk-2026-11-15-r2/07-noether-uk-SHA256SUMS.txt).
Ті самі файли лежать у [`editions/2026-10-24-r2/uk/`](editions/2026-10-24-r2/uk/).

Складання: файл LaTeX містить усі початкові файли з їхніми преамбулами. Програма Python
[`build.py`](editions/2026-10-24-r2/uk/build.py) розпаковує їх, компілює за допомогою XeLaTeX і об’єднує PDF частин у
порядку читання; потрібні Python 3, pypdf, а також пакети TeX і шрифти, зазначені в преамбулах. Архів ZIP містить ті
самі джерела в початковій структурі разом із програмою складання.

Видання серпня 2026 року (v2026.08.22-r2) зберігається в [`reader/`](reader/) (PDF) і [`source/`](source/) (LaTeX);
методику його редакції описано в [METHODOLOGY.md](METHODOLOGY.md), складання — у [BUILD.md](BUILD.md), записи
перевірок лежать в [`evidence/`](evidence/). Німецький текст, видання іншими мовами та відомі відмінності між
виданнями наведено на [центральній сторінці](https://kokunoyumeto.github.io/emmy-noether/).

## Автори та джерела

- Математичні праці належать Еммі Нетер і співавторам, названим у них: Вернер Шмайдлер (Werner Schmeidler,
  стаття 17), Р. Брауер (R. Brauer, стаття 32), Р. Брауер і Г. Гассе (H. Hasse, стаття 38). Лекції 1929/30 року
  опрацював М. Дойрінг. Праця 45 належить Г. Капфереру, доповнення до неї написано спільно з Е. Нетер. Відомості про
  перші публікації, підписи й посилання наведено в текстах.
- Редакція серпня 2026 року спиралася на німецький проєктний корпус NOETH-DE-ED-0015. Формули нинішнього видання
  звірено з німецьким текстом, порівняним посторінково з першими публікаціями
  ([випуск noether-de-2026-10-26](https://github.com/KokunoYumeto/modern-latex-manuscripts/releases/tag/noether-de-2026-10-26)).

## Права

Еммі Нетер померла 1935 року, тому її праці перебувають у суспільному надбанні в Європейському Союзі та всюди, де строк охорони спливає через 70 років після смерті автора. У США її праці, вперше опубліковані 1931 року або пізніше, охороняються до спливу 95 років після публікації (праці 1931 року стають вільними 1 січня 2027 року). Тією мірою, якою видавець має права на переклад, виправлення та верстку, виконані ШІ, він передає їх у суспільне надбання за [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.uk). Лекції в записі M. Deuring, праця H. Kapferer і внесок названих співавторів цією заявою не охоплюються; права на них залишаються за їхніми авторами або спадкоємцями.