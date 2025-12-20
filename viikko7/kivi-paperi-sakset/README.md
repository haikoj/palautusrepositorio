# Kivi-Paperi-Sakset Web-UI

Web-käyttöliittymä kivi-paperi-sakset pelille.

## Asennus

Asenna riippuvuudet Poetryllä:

```bash
poetry install
```

## Käynnistys

Käynnistä web-sovellus:

```bash
poetry run python src/app.py
```

Sovellus käynnistyy osoitteessa: http://127.0.0.1:5000

## Peliohjeet

1. Valitse pelimuoto:
   - **Pelaaja vs Pelaaja**: Kaksinpeli
   - **Pelaaja vs Tekoäly**: Pelaa yksinkertaista tekoälyä vastaan
   - **Pelaaja vs Parannettu Tekoäly**: Pelaa oppivaa tekoälyä vastaan

2. Peli päättyy automaattisesti kun jompikumpi pelaaja saavuttaa **5 voittoa**!

3. Siirrot:
   - 🪨 Kivi (k)
   - 📄 Paperi (p)
   - ✂️ Sakset (s)

## Ominaisuudet

- Moderni, responsiivinen web-käyttöliittymä
- Kolme erilaista pelimuotoa
- Automaattinen pelin päättyminen 5 voiton jälkeen
- Reaaliaikainen pistelaskenta
- Pelihistorian seuranta
- Käyttää alkuperäistä pelilogiikkaa muuttamattomana

## Alkuperäinen CLI-versio

Voit yhä pelata alkuperäistä komentorivi-versiota:

```bash
poetry run python src/index.py
```
