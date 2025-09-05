# Wer wird Millionär Quiz (Python → EXE)

Dieses Repo enthält das komplette WWM-Spiel mit Jokern und Gewinnleiter.

## Nutzung
1. Dieses Repo zu GitHub hochladen
2. Unter `.github/workflows/build.yml` ist eine GitHub Action eingerichtet
3. Auf GitHub unter **Actions** → Workflow „Build WWM EXE“ → **Run workflow**
4. Nach 2-3 Minuten steht unter **Artifacts** eine lauffähige `WWM-Quiz.exe` zum Download

## Fragen hinzufügen
Die Fragen stehen in einer JSON-Datei. Beispiel:
```json
[
  {
    "frage": "Wie heißt die Hauptstadt von Frankreich?",
    "antworten": ["Paris","Berlin","Rom","Madrid"],
    "loesung": "Paris"
  }
]
```
Beim Start im Spiel: „Fragen laden“ → Datei auswählen.
