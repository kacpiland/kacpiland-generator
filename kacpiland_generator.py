
import streamlit as st

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

st.title("🛋️ Generator opisów kategorii – kacpiland.com.pl")

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

if st.button("🎉 Wygeneruj opis"):
    wynik = generuj_opis_kategorii(nazwa, typy, cechy, korzysci, grupa, frazy_glowne, frazy_poboczne)
    st.markdown("### ✨ Wygenerowany opis HTML:")
    st.code(wynik, language='html')
