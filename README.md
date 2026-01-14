# SUML_Text_Detection_v2 — Desktop OCR (EasyOCR)

Aplikacja desktopowa do rozpoznawania tekstu (OCR) z obrazu.

**Autorzy (numery indeksów):** s24710, s22884, s25510  
**Model:** EasyOCR

---

## Struktura projektu (MVC)
SUML_Text_Detection_v2/
controller/ (init.py, controller.py) # sterowanie, logika aplikacji
model/ (init.py, model.py) # OCR (EasyOCR), przetwarzanie
view/ (init.py, main_view.py, tags.py) # UI
resources/ (fonts/, images/) # zasoby
main.py # start aplikacji

---

## Uruchomienie

### Windows (setup)
Na Windows dostępny będzie **instalator** (setup .exe/.msi).  
Uruchamiasz instalator → instalujesz → odpalasz aplikację z Menu Start.

### Linux/macOS (z kodu)
```bash
git clone <URL_REPO>
cd SUML_Text_Detection_v2
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py

Użycie

    1. Uruchom aplikację

    2. Wybierz źródło (obraz)

    3. Odczytaj wynik OCR w oknie aplikacji

Wymagania (SUML)

    1. Repo GitHub + README (ten plik)

    2. Przenośność: Windows через setup, інші ОС через запуск з коду

    3. Modularność: podział controller/model/view

    4. PEP8 + pylint min. 8.0

    pylint controller model view

Linki

    1. EasyOCR: https://github.com/JaidedAI/EasyOCR

    2. pylint: https://pypi.org/project/pylint/