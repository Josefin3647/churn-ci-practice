# 1 – CI tar för lång tid
Etikett: bygg

Varje push installerar pandas och scikit-learn från noll. Själva träningen tar bara ett par
sekunder, så nästan hela körtiden är paketinstallation. Utvecklarna sitter och väntar.

**Uppgift:** återanvänd nedladdade paket mellan körningar.

**Tips:** `actions/setup-python` har inbyggd cache för pip. Vad ska cachenyckeln bygga på,
så att cachen byts ut när beroendena ändras men inte annars?

**Klart när:**
- [x] Andra körningen efter ändringen visar att cachen återställdes (sök efter `cache` i loggen).
- [x] Du har antecknat körtiden före och efter här (används i A1).

## Resultat
Lade till `cache: "pip"` och `cache-dependency-path: pyproject.toml` i
`actions/setup-python`. Cachen återställs i andra körningen
(`Cache restored from key: setup-python-Linux-x64-24.04-Ubuntu-python-3.13.16-pip-…`).

Mätt på tre steg (setup-python + pip install + Post setup-python), fyra körningar var:

| | Utan cache (#5) | Med cache (#8) |
| --- | --- | --- |
| Summa per körning | 19, 25, 16, 22 s | 15, 22, 26, 18 s |
| Snitt | 20,5 s | 20,25 s |
| varav setup-python | 0 s | 3,25 s |
| varav pip install | 20,5 s | 17 s |

**Slutsats:** cachen fungerar, men ger ingen mätbar vinst. Den sparar cirka 3,5 s nedladdning i `pip install`, men kostar cirka 3 s att återställa. Skillnaden i snitt (0,25 s) är mindre än variationen mellan körningar (cirka 10 s). Den stora posten är installationen av paketen, inte nedladdningen.
