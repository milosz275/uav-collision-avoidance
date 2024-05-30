# UAV Collision Avoidance

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/mldxo/uav-collision-avoidance/blob/master/README.md)
[![Build](https://github.com/mldxo/uav-collision-avoidance/actions/workflows/python-app.yml/badge.svg)](https://github.com/mldxo/uav-collision-avoidance/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/mldxo/uav-collision-avoidance/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/mldxo/uav-collision-avoidance/actions/workflows/github-code-scanning/codeql)
[![Documentation Status](https://readthedocs.org/projects/uav-collision-avoidance/badge/?version=latest)](https://uav-collision-avoidance.readthedocs.io/en/latest/?badge=latest)
[![wersja PyPI](https://badge.fury.io/py/uav-collision-avoidance.svg)](https://badge.fury.io/py/uav-collision-avoidance)

[![Otwórz w GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/mldxo/uav-collision-avoidance)

Implementacja algorytmu unikania kolizji dla dronów w przestrzeni 3D bazująca na podejściu geometrycznym.

- [Github](https://github.com/mldxo/uav-collision-avoidance)
- [PyPI](https://pypi.org/project/uav-collision-avoidance)

## Praca badawcza

### Wstęp

`UAV Collision Avoidance` to projekt badawczy, którego celem jest zaimplementowanie algorytmu unikania kolizji dla dronów w przestrzeni 3D bazującego na podejściu geometrycznym. Projekt jest realizowany w ramach pracy licencjackiej na kierunku Informatyka na Wydziale Matematyczno-Przyrodniczym UKSW. Aplikacja implementuje funkcjonalne obliczenia fizyczne, skalowalny interfejs graficzny, realistyczny system unikania kolizji bazujący na symulacji systemu ADS-B oraz planowanie lotu używając prostej procedury komputera pokładowego. Program oferuje wielowątkową symulację czasu rzeczywistego umożliwiającą interakcję z samolotami oraz liniowo renderowaną symulację pozwalającą na szybkie testowanie skuteczności algorytmów.

### Dokumentacja

- [Dokumentacja](/docs/pl/README.md)
- [Wiki](https://github.com/mldxo/uav-collision-avoidance/wiki)

### Założenia

1. Definicja systemu: System jest zdefiniowany jako przestrzeń trójwymiarowa (3D) używając układu współrzędnych XYZ. X i Y reprezentują płaską poziomą płaszczyznę, podczas gdy Z reprezentuje wysokość nad poziomem morza.
2. Symulacja fizyki: Fizyka jest symulowana poprzez różniczkowanie części sekundy zgodnie z odpowiednimi wzorami. Fizyka bezzałogowych statków powietrznych (UAV) jest rozważana względem układu odniesienia Ziemi, oddzielonego od układu statku powietrznego i układu odniesienia do wiatru. Przestrzeń 3D w założeniu jest płaska, krzywizna Ziemi nie jest brana pod uwagę. Podczas zyskiwania lub tracenia wysokości prędkość samolotów jest zachowana. Rozważany jest układ RPY.[^6]
3. Charakterystyka statków powietrznych: Statki powietrzne są uważane za drony z poziomym startem i lądowaniem (HTOL). Mogą poruszać się tylko w kierunku swoich wektorów prędkości. Forma statku powietrznego jest przybliżona do sfery.
4. Środowisko: Przestrzeń jest współdzielona przez dwa lub trzy drony. Nie zakłada się obecności innych obiektów, przeszkód ani podmuchów wiatru.
5. Aerodynamika: Nie zakłada się obecności siły nośnej aerodynamicznej. Podczas skręcania samolot zawsze przyjmuje maksymalny kąt zmiany na jaki pozwala fizyka, respektując bezwład maszyny przy obracaniu. Obowiązują maksymalne kąty natarcia i wychylenia - odpowiednio przedziały `-45°, 45°` i `-90°, 90°`, przy czym dodatni kąt natarcia oznacza lot w górę, a dodatni kąt wychylenia oznacza pochylenie na prawe skrzydło. Kąty nie są przybliżane dla zachowania realizmu.
6. Jednostki miary: Domyślnymi jednostkami odległości są metry $\pu{m}$, prędkość mierzona jest w metrach na sekundę $\pu{m/s}$, a czasy klatki reprezentowane są w milisekundach $\pu{ms}$.

### Algorytmy

Wykrywanie i unikanie kolizji opierają się na podejściu geometrycznym. Algorytmy zostały przedstawione w cytowanej pracy[^4]. Wykrywanie kolizji różnicuje między kolizją a kolizją czołową. Ta druga obowiązuje, gdy drony nie mają odległości między swoimi środkami mas w miejscu spodziewanej kolizji, a pierwsza, gdy jest to każdy inny rodzaj kontaktu.

### Wyniki

Podejście geometryczne okazuje się przydatne w wykrywaniu i unikaniu kolizji. System jest w stanie unikać kolizji w większości przypadków. System nie jest doskonały i może zawodzić w niektórych scenariuszach, zwłaszcza gdy samoloty są zbyt blisko siebie w momencie wykrycia konfliktu. System jest energooszczędny i może być używany przy ocenie prawdziwych scenariuszy.

Zaproponowany system generacji i oceny przypadków testowych jest prosty i skuteczny. Umożliwia szybkie testowanie skuteczności systemu w różnych scenariuszach. System może być dalej rozwijany, aby uwzględniać bardziej przypadki i dodatkowe parametry.

## Projekt Python

### Technologie

Projekt Python3[^1] jest przygotowany jako pakiet PyPI[^2]. Do implementacji graficznego interfejsu użytkownika (GUI) wykorzystano PySide6[^3] (biblioteka Pythona Qt6).

### Struktury

Aplikacja została stworzona bazując na dwóch typach obiektów: symulacji i statku powietrznego. Symulacja jest tworzona zależnie od danych początkowych, udostępniając interfejs w czasie rzeczywistym bądź liniowe renderowanie przypadku testowego. Statek powietrzny składa się z dwóch elementów, fizycznej reprezentacji samolotu bezzałogowego (UAV) oraz komputera pokładowego, który jest kontrolowany przez wątek ADS-B. Badania nad systemami UAV były możliwe dzięki drugiej pracy[^5].

### Argumenty wywołania aplikacji

Obecnie dostępne jest osiem możliwych argumentów wywołania aplikacji:
- domyślny (bez argumentów) - uruchamia symulację GUI; unikanie kolizji można osiągnąć naciskając T, gdy strefy bezpieczeństwa dronów zostały naruszone
- realtime [nazwa_pliku] [indeks_testu] [unikanie_kolizji] - uruchamia symulację GUI; nazwa pliku może być sprecyzowana i domyślnie odnosi się do najnowszego pliku danych symulacyjnych; indeks testu może być określony i domyślnie wynosi 0; unikanie kolizji może być określone i domyślnie jest wyłączone
- headless - uruchamia fizyczną symulację z ADS-B i algorytmem unikania kolizji w tle
- tests [liczba_testów] - uruchamia pełne testy porównujące skuteczność algorytmu unikania kolizji, domyślna liczba testów wynosi 15
- ongoing - uruchamia domyślną liczbę testów równolegle (liczba rdzeni procesora) porównując skuteczność algorytmu unikania kolizji do momentu przerwania Ctrl+C
- load [nazwa_pliku] [indeks_testu] - wczytuje i przeprowadza symulację w tle z pliku, gdy jest określony, w przeciwnym razie wczytuje domyślny przykładowy przypadek testowy z katalogu danych `/data`; indeks testu może być określony i domyślnie wynosi 0
- help [argument_aplikacji] - wyświetla komunikat pomocy dla argumentu aplikacji; domyślnie wyświetla listę wszystkich argumentów
- version - wyświetla informacje o wersji aplikacji

### Skróty klawiszowe

Program w wersji real-time wyposażono w sposób interakcji użytkownika z symulowanym środowiskiem.

> [!NOTE]
> Samolot 0 oznacza pierwszy samolot, a samolot 1 oznacza drugi samolot.

- Lewy przycisk myszy (LPM) - dodaje nowy punkt na początek trasy samolotu 0 w lokalizacji kursora
- Prawy przycisk myszy (PPM) - dodaje nowy punkt na koniec trasy samolotu 0 w lokalizacji kursora
- Środowy przycisk myszy (ŚPM) - teleportuje samolot 0 w lokalizację kursora
- Koło myszy - przybliża i oddala widok
- Klawisze plus/minus (+/-) - przybliża i oddala widok (szybciej niż koło myszy)
- Strzałki (↑ ↓ → ←) - przesuwa widok w zadaną stronę
- F1 - przełącza raportowanie informacji ADS-B samolotu 0
- F2/F3 - zwalnia/przyspiesza docelową prędkość samolotu 0
- Klawisz N - przełącza śledzenie widoku samolotu 0/1 (domyślnie wyłączone)
- Klawisz M - przełącza widok śledzonego samolotu 0/1 (domyślnie samolot 0)
- Klawisz O - przełącza tryb powodowania kolizji dla samolotu 0 z samolotem 1 (domyślnie wyłączone)
- Klawisz P - przełącza tryb powodowania kolizji dla samolotu 1 z samolotem 0 (domyślnie wyłączone)
- Klawisz T - uruchamia procedurę unikania kolizji dla samolotów 0 i 1 (domyślnie wyłączone)
- Klawisze WSAD - nadpisują chwilowy kurs samolotu 0 - odpowiednio 0, 180, 270 i 90 stopni
- Klawisz R - resetuje symulację do stanu początkowego
- Ukośnik (/) - pauzuje symulację
- Klawisz Esc - kończy symulację i zamyka aplikację

### Instalacja

Zainstaluj pakiet z PyPI:

```bash
pip install uav-collision-avoidance
```

#### Zależności Debian 12

Dla systemu Debian 12 wymagane jest zainstalowanie pakietów:

```bash
sudo apt-get install libgl1 libxcb-xinerama0
```

Przed uruchomieniem aplikacji w tle, wykonaj następującą instrukcję:

```bash
export QT_QPA_PLATFORM=offscreen
```

### Użycie

Uruchom aplikację za pomocą jednego z poniższych poleceń:

```bash
uav-collision-avoidance
```

```bash
uav-collision-avoidance realtime [nazwa_pliku] [indeks_testu] [unikanie_kolizji]
```

```bash
uav-collision-avoidance headless
```

```bash
uav-collision-avoidance tests [liczba_testów]
```

```bash
uav-collision-avoidance ongoing
```

```bash
uav-collision-avoidance load [nazwa_pliku] [indeks_testu]
```

```bash
uav-collision-avoidance help [argument_aplikacji]
```

>[!NOTE]
> Pomoc jest wyświetlana w języku angielskim.

```bash
uav-collision-avoidance version
```

### Budowanie (build)

Aby zbudować aplikację, wykonaj poniższe grupy poleceń zależnie od systemu:

<p align="left">
    <img width="30px" alt="Bash" style="padding-right:10px;" src="https://skillicons.dev/icons?i=bash" />
</p>

```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py [argument]
```

<p align="left">
    <img width="30px" alt="Powershell" style="padding-right:10px;" src="https://skillicons.dev/icons?i=powershell" />
</p>

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py [argument]
```

### Uwagi

Trójwymiarowa (3D) przestrzeń świata jest rzutowana na płaską powierzchnię poprzez spłaszczenie osi Z (wysokość). Przy starcie programu, widok jest niezależny od symulowanych pojazdów latających i może być przesuwany strzałkami. W celu wyśrodkowania widoku na samolocie, należy nacisnąć przycisk `N`.

Nie została zachowana jedna konwencja nazewnictwa, ponieważ biblioteka PySide6 jest sformatowana w stylu Qt6, a nie w stylu Pythona.

## Nadchodzące aktualizacje

- [ ] ADS-B: Optymalizacja dobierania kątów przez FCC (komputer pokładowy)
- [ ] Renderowanie: Optymalizacja wyśrodkowanego widoku
- [x] Wiki: Dokumentacja

## Autorzy

[Miłosz Maculewicz](https://github.com/mldxo)

## Licencja

Sprawdź [LICENSE](/LICENSE).

## Referencje

<p align="left">
    <img width="30px" alt="Aircraft icon" style="padding-right:10px;" src="/assets/aircraft.png" />
</p>

Ikona drona wykonana przez Anthony Lui <a href="https://thenounproject.com/browse/icons/term/drone/" target="_blank" title="Drone Icons">Noun Project</a> (CC BY 3.0)

Wszystkie odnośniki do prac badawczych i wykorzystanych materiałów znajdują się poniżej.

[^1]: [Python3](https://www.python.org/)
[^2]: [PyPI](https://pypi.org/)
[^3]: [PyQt6](https://doc.qt.io/qtforpython-6/)
[^4]: [UAV Collision Avoidance Based on Geometric Approach](https://ieeexplore.ieee.org/document/4655013/)
[^5]: [Energy Efficient UAV Flight Control Method in an Environment with Obstacles and Gusts of Wind](https://www.mdpi.com/1638452/)
[^6]: [Kąty RPY](https://pl.wikipedia.org/wiki/K%C4%85ty_RPY)
