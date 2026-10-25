# Atsiskaitymai su Valera

Radoslav ir Valeros tarpusavio pavedimų balansas. Puslapis: https://daugpinigu.github.io/balansas/

## Kaip pridėti pavedimą

1. **Per puslapį** (patogiausia): užpildyk formą "Naujas pavedimas", spausk "Įrašyti GitHub'e". Atsidarys GitHub su paruoštu failu, spausk **Commit changes**. Reikia būti prisijungus prie GitHub kaip `daugpinigu`.
2. **Tiesiogiai GitHub'e**: sukurk naują failą `entries/<data>-<laikas>.json`:
   ```json
   {"date": "2026-10-23", "from": "R", "amount": 4955.39, "note": ""}
   ```
   `from`: `R` = Radoslav pervedė Valerai, `V` = Valera pervedė Radoslavui. `date` gali būti tuščia.
   Neprivalomas `"kind": "portfolio"` - vertė perduota natūra (žr. žemiau), rodoma atskirai.
3. **Pasakyk asistentui** pokalbyje, jis įrašys.

Po commit'o GitHub Actions per ~1 min perskaičiuoja `data.json` ir atnaujina puslapį. Jei įrašo failas su klaida, deploy'us sustoja ir puslapis lieka senas (žr. Actions skiltį).

## Natūra: Freedom24 portfelis

Valera 2026-10-25 perdavė Radoslavui natūra Freedom24 portfelį savo vardu (120 000 € nominalas). Portfelį valdo ir riziką prisiima Radoslav: kiek portfelis bus vertas, tiek Radoslav ir gaus. Knygoje tai įrašas `V→R 120 000` su `"kind": "portfolio"` - jis mažina balansą kaip pavedimas, bet puslapyje rodomas atskirai („Plius natūra“), o balanso skaičius reiškia skolą grynais.

Kai portfelis bus realiai pervestas Radoslavui: **nekurti naujo V→R įrašo** (dubliuotųsi). Redaguoti F24 įrašą: pastaboje įrašyti realią pervestą sumą ir datą. Balansas nesikeičia, skirtumas nuo 120 000 € (pelnas ar nuostolis) yra Radoslavo.

## Redaguoti ar ištrinti

Istorijoje prie kiekvieno įrašo yra nuoroda "GitHub", ji atidaro to įrašo failą redagavimui. Ištrinti: tame pačiame GitHub lange meniu "..." → Delete file.

## Struktūra

- `entries/*.json` - po vieną pavedimą faile (šaltinis)
- `build.py` - surenka į `_site/data.json`
- `index.html` - puslapis, skaito `data.json`
- `.github/workflows/deploy.yml` - build + GitHub Pages deploy
