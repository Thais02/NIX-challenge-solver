# NIX-challenge-solver
Een script/bot om de NIX challenge van het CBL automatisch te spelen.
De bot is getest met de editie van 2022.

## Vereisten
- Chrome webbrowser
- Een slecht moreel kompas

## Gebruik
In het `Releases` tablad is een standalone .exe beschikbaar, dit bestand is te gebruiken zonder Python interpreter.

Zorg ervoor dat `config.py` in dezelfde map staat bij het uitvoeren.

`faces.pkl` moet ook in dezelfde map staan, anders wordt het nieuw aangemaakt.

## Instellingen
Het bestand `config.py` bevat alle instellingen die je aan kan passen:
- PERSON - De persoonsgegevens die in het winactie-formulier ingevuld moeten worden, dit is een verwijzing naar een Python class die het volgende moet bevatten:
  - VOORNAAM
  - ACHTERNAAM
  - EMAIL - In dit email-adres kan je een `{}` plaatsen om hier een willekeurig 6-cijferig getal te plaatsen elk spel
  - KETEN_ID - Plek in lijst van winkels in het formulier, tellen begint bij 0! Dus de 1ste winkel is 0, de 2e is 1, enz.
  - PLAATSNAAM
  - WINKELNAAM
- URL - Dit kan bijvoorbeeld `https://nixchallenge.nl/` of je finale-link zijn
- GAMES_TO_PLAY - Het aantal volledige spellen om te spelen
- AUTO_CLICK - Speel het spel helemaal zelf, anders geeft de bot hints welk antwoord je zelf moet aanklikken
- AUTO_FINAL - Probeer de finale automatisch te spelen (experimenteel)
- KEEP_OPEN - Houd de browser van elk spel open
- DOWNLOAD - Download de foto's van nieuwe gezichten naar de map `persons`
- FILL_FORM - Vul het winactie-formulier automatisch in met de gegevens van PERSON
- SEND_FORM - Verzend het formulier automatisch

## Trainen en faces.pkl
Het bestand `faces.pkl` bevat alle bekende gezichten van de bot.
Verwijder of hernoem dit bestand om de bot opnieuw te laten trainen.

De versie van `faces.pkl` in deze repository bevat 138 gezichten uit de 2022 editie.
