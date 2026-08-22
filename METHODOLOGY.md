# Методика українського видання / Ukrainian-edition methodology

## Українська версія

### 1. Опора і межі

Редакційна опора цієї лінії — німецький проєктний корпус `NOETH-DE-ED-0015` (51A25101C04877AE740989E72B2AD65A7A7E65B081077C4A518BF1737AD5B907). Він контролює структуру, формули й передбачуваний зміст, але не оголошується критичним німецьким виданням. Українські тексти є перекладними свідками цієї редакції; вони не утворюють загального нормативного «канону української математичної мови».

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
