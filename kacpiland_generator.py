
import re
import textwrap
from html import escape
from typing import Dict, Iterable, Sequence, Tuple

import streamlit as st


def _slugify(text: str) -> str:
    """Generate a URL-friendly slug."""
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug[:96]


def _ensure_min_length_name(base_name: str, descriptors: Sequence[str], minimum: int = 100) -> str:
    """Extend the product name with descriptors until the required length is reached."""
    extended_name = base_name.strip()
    iterator = list(descriptors) if descriptors else []

    if not iterator:
        iterator = ["premium", "wysokiej jakości", "dla wymagających klientów"]

    index = 0
    while len(extended_name) < minimum:
        descriptor = iterator[index % len(iterator)]
        separator = " | " if extended_name else ""
        extended_name = f"{extended_name}{separator}{descriptor}".strip()
        index += 1

    return extended_name


def _normalize_sequence(values: Sequence[str]) -> Sequence[str]:
    return [value.strip() for value in values if value and value.strip()]


def _format_list_items(items: Iterable[str]) -> str:
    return "".join(f"<li>{escape(item)}</li>" for item in items if item.strip())


def _format_parameters_table(parameters: Dict[str, str]) -> str:
    rows = []
    for key, value in parameters.items():
        if key.strip() and value.strip():
            rows.append(
                f"<tr><th scope='row'>{escape(key.strip())}</th><td>{escape(value.strip())}</td></tr>"
            )
    return "".join(rows)


def _format_faq(faq_entries: Sequence[Tuple[str, str]]) -> str:
    blocks = []
    for question, answer in faq_entries:
        if question.strip() and answer.strip():
            blocks.append(
                textwrap.dedent(
                    f"""
                    <div class='faq-item'>
                        <h3>{escape(question.strip())}</h3>
                        <p>{escape(answer.strip())}</p>
                    </div>
                    """
                ).strip()
            )
    return "".join(blocks)


def _count_words(text: str) -> int:
    """Return the number of words ignoring HTML tags."""

    without_tags = re.sub(r"<[^>]+>", " ", text)
    words = re.findall(r"\w+", without_tags, flags=re.UNICODE)
    return len(words)


def _generate_alt_texts(
    rodzaj: str,
    marka: str,
    model: str,
    styl: str,
    keywords: Sequence[str],
    desired_count: int = 4,
) -> Sequence[str]:
    unique_keywords = []
    for keyword in keywords:
        normalized = keyword.lower()
        if normalized and normalized not in unique_keywords:
            unique_keywords.append(normalized)

    alt_texts = []
    base_phrase = f"{rodzaj.strip()} {marka.strip()} {model.strip()}".strip() or rodzaj.strip() or marka.strip()
    style_phrase = styl.strip().lower() or rodzaj.strip().lower()
    for index in range(desired_count):
        keyword = unique_keywords[index % len(unique_keywords)] if unique_keywords else style_phrase
        keyword = keyword.strip()
        if keyword:
            alt_texts.append(f"{base_phrase} w stylu {style_phrase} – {keyword}")
        else:
            alt_texts.append(f"{base_phrase} w stylu {style_phrase}")

    return alt_texts


def generuj_opis_produktu(
    marka: str,
    model: str,
    rodzaj: str,
    cechy_kluczowe: Sequence[str],
    materialy: Sequence[str],
    zastosowania: Sequence[str],
    korzysci: Sequence[str],
    slowa_kluczowe: Sequence[str],
    slowa_long_tail: Sequence[str],
    parametry: Dict[str, str],
    elementy_zestawu: Sequence[str],
    faq_entries: Sequence[Tuple[str, str]],
    styl: str,
    inspiracja: str,
    docelowy_ton: str,
    docelowe_slowo_kluczowe: str,
    cta: str,
    target_words: int = 1500,
) -> Dict[str, str]:
    cechy_kluczowe = list(_normalize_sequence(cechy_kluczowe))
    materialy = list(_normalize_sequence(materialy))
    zastosowania = list(_normalize_sequence(zastosowania))
    korzysci = list(_normalize_sequence(korzysci))
    slowa_kluczowe = list(_normalize_sequence(slowa_kluczowe))
    slowa_long_tail = list(_normalize_sequence(slowa_long_tail))
    elementy_zestawu = list(_normalize_sequence(elementy_zestawu))
    faq_entries = [
        (pytanie.strip(), odpowiedz.strip())
        for pytanie, odpowiedz in faq_entries
        if pytanie.strip() and odpowiedz.strip()
    ]

    podstawowa_nazwa = (
        f"{marka.strip()} {model.strip()} {rodzaj.strip()} – {', '.join(cechy_kluczowe[:3])}"
    ).strip()
    rozszerzona_nazwa = _ensure_min_length_name(podstawowa_nazwa, cechy_kluczowe)
    url = _slugify(rozszerzona_nazwa)

    materialy_calosc = ", ".join(materialy) if materialy else "szlachetne materiały premium"
    materialy_glowne = ", ".join(materialy[:2] or materialy) or materialy_calosc

    cechy_list = []
    for index, cecha in enumerate(cechy_kluczowe):
        powiazana_korzysc = (
            korzysci[index % len(korzysci)]
            if korzysci
            else "harmonię między estetyką a funkcjonalnością"
        )
        cechy_list.append(
            f"{cecha.capitalize()} – dzięki niej {rodzaj.strip().lower()} zapewnia {powiazana_korzysc}."
        )

    if materialy:
        cechy_list.append(
            f"Materiały premium: {materialy_calosc} gwarantują trwałość i perfekcyjne wykończenie."
        )

    seo_fraza = docelowe_slowo_kluczowe.strip() or styl.strip() or rodzaj.strip()
    cechy_list.append(
        f"Projekt podporządkowany SEO – bogata narracja wykorzystująca frazy jak {seo_fraza}."
    )

    paragrafy_zastosowania = []
    for idx, zastosowanie in enumerate(zastosowania, start=1):
        paragrafy_zastosowania.append(
            textwrap.fill(
                (
                    f"Dzięki przemyślanej konstrukcji {rodzaj.strip()} sprawdza się jako {zastosowanie.strip().lower()}, "
                    f"łącząc styl {styl.lower()} z funkcjonalnością, której oczekują miłośnicy designu. "
                    f"{docelowy_ton.strip().capitalize()} narracja podkreśla, że każdy element został zaprojektowany, aby zapewnić "
                    f"komfort użytkowania zarówno na co dzień, jak i podczas wyjątkowych okazji."
                ),
                120,
            )
        )

    korzysci_paragrafy = []
    for benefit in korzysci:
        korzysci_paragrafy.append(
            textwrap.fill(
                (
                    f"Korzystając z {rodzaj.strip()}, zyskujesz {benefit.strip().lower()}, co bezpośrednio przekłada się na pozytywne "
                    f"doświadczenie użytkownika. Produkt łączy {materialy_calosc} z dopracowanym rzemiosłem, dzięki czemu "
                    f"spełnia oczekiwania nawet najbardziej wymagających klientów."),
                120,
            )
        )

    slowa_wprowadzenia = [
        marka.strip(),
        model.strip(),
        rodzaj.strip(),
        styl.strip(),
    ] + slowa_kluczowe + slowa_long_tail
    slowa_wprowadzenia = [s for s in slowa_wprowadzenia if s]

    wprowadzenie = textwrap.fill(
        (
            f"{rodzaj.strip()} {marka.strip()} {model.strip()} przenosi Twoje wnętrze w świat {styl.lower()} i świadomego designu. "
            f"Zaprojektowany, aby zachwycać każdym detalem, produkt doskonale wpisuje się w potrzeby osób, które szukają "
            f"połączenia estetyki i funkcjonalności. Wprowadzając do przestrzeni subtelne akcenty, {rodzaj.strip()} tworzy "
            f"przyjazny klimat i wzmacnia charakter aranżacji, niezależnie od tego, czy mówimy o domowym salonie, czy eleganckiej przestrzeni komercyjnej."
        ),
        120,
    )

    short_description = textwrap.fill(
        (
            f"{rodzaj.strip()} {marka.strip()} {model.strip()} łączy {materialy_glowne} oraz {styl.lower()} "
            f"charakter, tworząc rozwiązanie, które harmonijnie wpisuje się w wymagające aranżacje. Wykorzystaj go, aby podkreślić "
            f"unikalny styl wnętrza i zapewnić użytkownikom wyjątkowe doświadczenia premium."
        ),
        120,
    )

    zestaw_opis = ", ".join(elementy_zestawu)
    parametry_opis = ", ".join(
        f"{klucz.lower()} {wartosc}" for klucz, wartosc in list(parametry.items())[:3] if klucz.strip() and wartosc.strip()
    )
    dzialanie_segmenty = [
        f"Przygotuj przestrzeń montażową i rozpakuj zestaw obejmujący {zestaw_opis or 'wszystkie niezbędne elementy'}.",
        f"Zgodnie z instrukcją zamontuj {rodzaj.strip().lower()}, zwracając uwagę na detale jak {parametry_opis or 'ergonomiczne wymiary i wygodne mocowania'}.",
        f"Po uruchomieniu produkt oferuje {', '.join(korzysci[:2]) if korzysci else 'komfort i styl'}, budując atmosferę w duchu {styl.lower()} i wzmacniając SEO dzięki konsekwentnym frazom kluczowym.",
    ]
    tekst_dzialania = "\n".join(dzialanie_segmenty)
    tekst_dzialania_html = "<ol>" + "".join(
        f"<li>{escape(segment)}</li>" for segment in dzialanie_segmenty
    ) + "</ol>"

    cechy_bullet = _format_list_items(cechy_list)
    materialy_bullet = _format_list_items(
        [
            f"Naturalne i wyselekcjonowane materiały: {', '.join(materialy)}" if materialy else "",
            f"Ręczne dopracowanie detali zgodnie ze standardami {marka.strip()}",
            f"Design inspirowany stylem {styl.strip()}"
        ]
    )
    zastosowania_text = "".join(f"<p>{escape(paragraf)}</p>" for paragraf in paragrafy_zastosowania)
    korzysci_text = "".join(f"<p>{escape(paragraf)}</p>" for paragraf in korzysci_paragrafy)
    parametry_rows = _format_parameters_table(parametry)
    zestaw_items = _format_list_items(elementy_zestawu)
    faq_html = _format_faq(faq_entries)

    sekcja_dlaczego = textwrap.fill(
        (
            f"Wybierając {rodzaj.strip()}, inwestujesz w produkt, który łączy w sobie autentyczność materiałów, dopracowaną formę "
            f"oraz technologię wspierającą komfort użytkowania. {marka.strip()} gwarantuje niezawodność i wysokie standardy produkcji, "
            f"a przy tym umożliwia personalizację przestrzeni zgodnie z Twoimi preferencjami. {rodzaj.strip()} to także odpowiedź na aktualne "
            f"trendy rynkowe, w których dominują rozwiązania {styl.lower()} i świadomy dobór detali."
        ),
        120,
    )

    inspiracja_text = textwrap.fill(
        (
            f"{inspiracja.strip()} Wyobraź sobie, jak {rodzaj.strip()} oświetla przestrzeń, tworząc scenę idealną do chwil relaksu, "
            f"rodzinnych spotkań lub pracy w skupieniu. Produkt staje się centralnym punktem aranżacji, wprowadzając atmosferę "
            f"pełną ciepła i dopracowanego stylu."
        ),
        120,
    )

    keywords_block = ", ".join(slowa_wprowadzenia)

    alt_texts = _generate_alt_texts(
        rodzaj,
        marka,
        model,
        styl,
        slowa_kluczowe + slowa_long_tail + [docelowe_slowo_kluczowe],
    )
    alt_text_html = _format_list_items(alt_texts)

    link_slug = _slugify(docelowe_slowo_kluczowe or rodzaj or styl or "kolekcja")
    docelowy_link = f"https://kacpiland.com.pl/kategoria/{link_slug}"
    link_anchor = f"Zobacz też inne {rodzaj.strip().lower() or 'produkty'} w stylu {styl.lower() or 'kacpiland'}"

    opis_dlugi = textwrap.dedent(
        f"""
        <h1>{escape(rozszerzona_nazwa)}</h1>
        <p class='intro'>{escape(wprowadzenie)}</p>
        <h2>Najważniejsze cechy produktu</h2>
        <ul>
            {cechy_bullet}
            {materialy_bullet}
        </ul>
        <h2>Opis i zastosowanie</h2>
        {zastosowania_text}
        {korzysci_text}
        <h2>Jak działa i jak z niego korzystać?</h2>
        {tekst_dzialania_html}
        <h2>Wymiary i parametry techniczne</h2>
        <table class='parametry'>
            <tbody>
                {parametry_rows}
            </tbody>
        </table>
        <h2>Co otrzymujesz w zestawie?</h2>
        <ul>
            {zestaw_items}
        </ul>
        <h2>Dlaczego warto wybrać właśnie ten produkt?</h2>
        <p>{escape(sekcja_dlaczego)}</p>
        <h2>FAQ – najczęściej zadawane pytania</h2>
        {faq_html}
        <h2>Inspiracja i lifestyle</h2>
        <p>{escape(inspiracja_text)}</p>
        <h2>Alt tagi dla zdjęć</h2>
        <ul>{alt_text_html}</ul>
        <h2>Linkowanie wewnętrzne</h2>
        <p><a href="{docelowy_link}">{escape(link_anchor)}</a></p>
        <p class='keywords'><strong>Słowa kluczowe:</strong> {escape(keywords_block)}</p>
        <p class='cta'><strong>{escape(cta.strip())}</strong></p>
        """
    ).strip()

    # Zapewnij minimalną liczbę słów dla SEO
    slowa = _count_words(opis_dlugi)
    padding_index = 0
    while slowa < target_words:
        dodat_kor = korzysci[padding_index % len(korzysci)] if korzysci else "wyjątkową jakość wykonania"
        dodat_cecha = cechy_kluczowe[padding_index % len(cechy_kluczowe)] if cechy_kluczowe else "wszechstronne zastosowanie"
        dodatkowy_akapit = textwrap.fill(
            (
                f"Dodatkowo {rodzaj.strip()} wyróżnia się takimi detalami jak {dodat_cecha.lower()}, co wzmacnia "
                f"jego pozycję w swojej kategorii. Z perspektywy użytkownika oznacza to {dodat_kor.lower()}, a także gwarancję, "
                f"że produkt pozostanie niezawodny na wiele sezonów intensywnego użytkowania."
            ),
            120,
        )
        opis_dlugi += f"\n<p>{escape(dodatkowy_akapit)}</p>"
        slowa = _count_words(opis_dlugi)
        padding_index += 1

    return {
        "nazwa": rozszerzona_nazwa,
        "url": f"https://kacpiland.com.pl/produkty/{url}",
        "krotki_opis": short_description,
        "dlugi_opis": opis_dlugi,
        "tekst_dzialania": tekst_dzialania,
        "alt_teksty": alt_texts,
        "link_wewnetrzny": docelowy_link,
    }


def generuj_opis_kategorii(nazwa_kategorii, typy_produktow, cechy_wspolne, korzysci, grupa_docelowa, frazy_glowne, frazy_poboczne):
    h1 = f"{nazwa_kategorii} – stwórz idealną przestrzeń"
    krotki_opis = f"Odkryj {nazwa_kategorii.lower()} – wygodne, trwałe i dopasowane do Twojego wnętrza."
    opis = f"""
<h1>{h1}</h1>
<p><strong>Krótki opis:</strong><br>{krotki_opis}</p>
<h2>Opis kategorii: {nazwa_kategorii}</h2>
<p>Twoje wnętrze zasługuje na meble, które łączą funkcjonalność z estetyką. {nazwa_kategorii} dostępne w sklepie kacpiland.com.pl to propozycje, które pozwalają stworzyć harmonijną i wygodną przestrzeń.</p>
<h3>Typy produktów:</h3>
<ul>{''.join(f'<li>{t}</li>' for t in typy_produktow)}</ul>
<h3>Wspólne cechy produktów:</h3>
<ul>
<li><strong>Materiały:</strong> {', '.join(cechy_wspolne.get('materiał', []))}</li>
<li><strong>Kolorystyka:</strong> {', '.join(cechy_wspolne.get('kolor', []))}</li>
<li><strong>Style:</strong> {', '.join(cechy_wspolne.get('styl', []))}</li>
<li><strong>Przeznaczenie:</strong> {', '.join(cechy_wspolne.get('przeznaczenie', []))}</li>
</ul>
<h3>Korzyści:</h3>
<ul>{''.join(f'<li>✔️ {k}</li>' for k in korzysci)}</ul>
<h3>Grupa docelowa:</h3>
<ul>{''.join(f'<li>{g}</li>' for g in grupa_docelowa)}</ul>
<h3>Frazy SEO:</h3>
<ul>
<li><strong>Główne:</strong> {', '.join(frazy_glowne)}</li>
<li><strong>Poboczne:</strong> {', '.join(frazy_poboczne)}</li>
</ul>
<h3>Podsumowanie:</h3>
<p>{nazwa_kategorii} to połączenie designu, funkcjonalności i jakości. Postaw na komfort i styl – wybierz rozwiązania idealnie dopasowane do Twoich potrzeb.</p>
    """
    return opis.strip()

st.title("🛋️ Generator treści – kacpiland.com.pl")

zakladka_produkt, zakladka_kategoria = st.tabs(["Opis produktu", "Opis kategorii"])

with zakladka_produkt:
    st.header("Generator opisu produktu zgodnie z wytycznymi SEO")
    marka = st.text_input("Marka", "Kacpiland Studio")
    model = st.text_input("Model", "Aurora LX")
    rodzaj = st.text_input("Rodzaj produktu", "Designerska lampa wisząca")
    cechy = st.text_area("Cechy kluczowe (enter oddziela)", "ręcznie pleciony klosz\nregulowana wysokość\nenergooszczędne źródło światła LED").splitlines()
    materialy = st.text_input("Materiały (oddzielone przecinkami)", "rattan, stal malowana proszkowo, szkło").split(",")
    zastosowania = st.text_area("Zastosowania (enter oddziela)", "oświetlenie salonu\naranżacje w stylu boho\nprzytulne kawiarnie").splitlines()
    korzysci = st.text_area("Korzyści dla klienta (enter oddziela)", "wprowadza ciepłe, rozproszone światło\npodkreśla naturalny charakter wnętrza\nłatwa w montażu i czyszczeniu").splitlines()
    slowa_kluczowe = st.text_input("Frazy kluczowe (oddzielone przecinkami)", "lampa boho, kinkiet rattanowy, designerskie oświetlenie").split(",")
    slowa_long_tail = st.text_input("Frazy long tail (oddzielone przecinkami)", "lampa boho do salonu, rattanowa lampa wisząca, naturalne oświetlenie do domu").split(",")
    parametry_input = st.text_area(
        "Parametry techniczne (format: nazwa=wartość, enter oddziela)",
        "Wysokość=35 cm\nŚrednica=22 cm\nŹródło światła=E27 LED\nDługość przewodu=120 cm"
    ).splitlines()
    elementy_zestawu = st.text_area(
        "Elementy zestawu (enter oddziela)",
        "lampa z kloszem\nkomplet montażowy\ninstrukcja w języku polskim"
    ).splitlines()
    faq_input = st.text_area(
        "FAQ (format: pytanie|odpowiedź, enter oddziela)",
        "Czy lampa wymaga specjalistycznego montażu?|Nie, wystarczy standardowa instalacja sufitowa.\nCzy można używać żarówek LED?|Tak, oprawa jest w pełni kompatybilna z energooszczędnymi żarówkami LED.\nJak czyścić klosz?|Wystarczy delikatnie przetrzeć miękką, suchą ściereczką."
    ).splitlines()
    styl = st.text_input("Dominujący styl", "boho chic")
    inspiracja = st.text_area(
        "Akapit inspiracyjny",
        "Zanurz się w przytulnej atmosferze naturalnych materiałów i miękkiego światła."
    )
    docelowy_ton = st.text_input("Ton wypowiedzi", "emocjonalny i inspirujący")
    docelowe_slowo_kluczowe = st.text_input("Główne słowo kluczowe", "lampa boho")
    cta = st.text_input("Call To Action", "Dodaj do koszyka i poznaj magię naturalnego światła!")
    target_words = st.slider("Docelowa liczba słów w opisie", min_value=900, max_value=2000, value=1500, step=50)

    parametry = {}
    for linia in parametry_input:
        if "=" in linia:
            k, v = linia.split("=", 1)
            parametry[k.strip()] = v.strip()

    faq_entries = []
    for wpis in faq_input:
        if "|" in wpis:
            pytanie, odpowiedz = wpis.split("|", 1)
            faq_entries.append((pytanie.strip(), odpowiedz.strip()))

    if st.button("✨ Wygeneruj opis produktu"):
        wynik = generuj_opis_produktu(
            marka,
            model,
            rodzaj,
            cechy,
            [m.strip() for m in materialy if m.strip()],
            zastosowania,
            korzysci,
            slowa_kluczowe,
            slowa_long_tail,
            parametry,
            elementy_zestawu,
            faq_entries,
            styl,
            inspiracja,
            docelowy_ton,
            docelowe_slowo_kluczowe,
            cta,
            target_words,
        )

        st.subheader("Nazwa produktu")
        st.code(wynik["nazwa"])
        st.subheader("Adres URL")
        st.code(wynik["url"])
        st.subheader("Krótki opis")
        st.write(wynik["krotki_opis"])
        st.subheader("Tekst działania")
        st.markdown("\n".join(f"- {krok}" for krok in wynik["tekst_dzialania"].splitlines()))
        st.subheader("Alt tagi dla zdjęć")
        st.markdown("\n".join(f"- {alt}" for alt in wynik["alt_teksty"]))
        st.subheader("Link wewnętrzny")
        st.code(wynik["link_wewnetrzny"])
        st.subheader("Długi opis (HTML)")
        st.code(wynik["dlugi_opis"], language="html")

with zakladka_kategoria:
    st.header("Generator opisu kategorii")
    nazwa = st.text_input("Nazwa kategorii", "Krzesła do kuchni i jadalni")
    typy = st.text_area("Typy produktów (enter oddziela)", "krzesła drewniane\nkrzesła tapicerowane\nkrzesła z podłokietnikami").splitlines()
    cechy_input = st.text_area("Cechy wspólne (format: materiał=..., kolor=..., styl=..., przeznaczenie=...)",
                               "materiał=lite drewno, metal, welur\nkolor=biel, szarość, dąb\nstyl=skandynawski, klasyczny\nprzeznaczenie=kuchnia, jadalnia").splitlines()
    korzysci = st.text_area("Korzyści (enter oddziela)", "Wysoki komfort siedzenia\nStylowe wykończenie\nŁatwość czyszczenia").splitlines()
    grupa = st.text_area("Grupa docelowa (enter oddziela)", "Rodziny z dziećmi\nMłode pary\nSeniorzy").splitlines()
    frazy_glowne = st.text_input("Frazy główne SEO (oddzielone przecinkami)", "krzesła do kuchni, krzesła do jadalni").split(",")
    frazy_poboczne = st.text_input("Frazy poboczne SEO (oddzielone przecinkami)", "krzesła drewniane, krzesła tapicerowane").split(",")

    cechy = {"materiał": [], "kolor": [], "styl": [], "przeznaczenie": []}
    for linia in cechy_input:
        if "=" in linia:
            k, v = linia.split("=", 1)
            cechy[k.strip()] = [s.strip() for s in v.split(",")]

    if st.button("🎉 Wygeneruj opis kategorii"):
        wynik = generuj_opis_kategorii(nazwa, typy, cechy, korzysci, grupa, frazy_glowne, frazy_poboczne)
        st.markdown("### ✨ Wygenerowany opis HTML:")
        st.code(wynik, language='html')
