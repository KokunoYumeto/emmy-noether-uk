# Машинний покажчик українського видання

`LANGUAGE_EDITION_INDEX.json` є стабільною машинною точкою входу до поточного українського видання корпусу Еммі Нетер. Поле `canonical_language_key` має значення `uk-Cyrl`; `canonical_sources` називає чотири редаговані джерела з точними розмірами та SHA-256; `canonical_reader` називає повний 588-сторінковий читач; `authority_chain`, `decision_evidence`, `qa` та `reproduction` фіксують джерельну владу, редакційну послідовність і спосіб відтворення.

«Канонічний» тут означає лише канонічну голову цього українського проєктного видання. Це не нормативний канон української мови, не посвідчення носіями мови й не рецензоване критичне видання. Новий сеанс Codex або інший інструмент має починати з JSON-покажчика, перевіряти всі хеші й додавати нові рішення монотонно, а не переписувати попередню історію.

# Machine index for the Ukrainian edition

`LANGUAGE_EDITION_INDEX.json` is the stable machine entrypoint for the current Ukrainian Emmy Noether edition. Use `canonical_language_key` to identify `uk-Cyrl`, `canonical_sources` for the four editable witnesses, `canonical_reader` for the complete 588-page reader, and the authority, decision, QA, and reproduction sections to verify and extend the edition.

Here, “canonical” means canonical only within this project edition lane. It is not a prescriptive Ukrainian-language canon, native-speaker certification, or a peer-reviewed critical edition. Successors must verify all declared hashes and append evidence rather than rewrite prior decisions.
