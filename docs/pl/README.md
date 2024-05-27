# Dokumentacja

## Spis treści

1. [Przegląd](#przegląd)
2. [Stałe](#stałe)
3. [Plik: `main.py`](#plik-mainpy)
4. [Plik: `src/main.py`](#plik-srcmainpy)
5. [Plik: `src/version.py`](#plik-srcversionpy)
6. [Plik: `src/simulation/simulation.py`](#plik-srcsimulationsimulationpy)
7. [Plik: `src/simulation/simulation_physics.py`](#plik-srcsimulationsimulation_physicspy)
8. [Plik: `src/simulation/simulation_adsb.py`](#plik-srcsimulationsimulation_adsbpy)
9. [Plik: `src/simulation/simulation_state.py`](#plik-srcsimulationsimulation_statepy)
10. [Plik: `src/simulation/simulation_settings.py`](#plik-srcsimulationsimulation_settingspy)
11. [Plik: `src/simulation/simulation_widget.py`](#plik-srcsimulationsimulation_widgetpy)
12. [Plik: `src/simulation/simulation_render.py`](#plik-srcsimulationsimulation_renderpy)
13. [Plik: `src/simulation/simulation_fps.py`](#plik-srcsimulationsimulation_fpspy)
14. [Plik: `src/simulation/simulation_data.py`](#plik-srcsimulationsimulation_datapy)
15. [Plik: `src/aircraft/aircraft.py`](#plik-srcaircraftaircraftpy)
16. [Plik: `src/aircraft/aircraft_fcc.py`](#plik-srcaircraftaircraft_fccpy)
17. [Plik: `src/aircraft/aircraft_vehicle.py`](#plik-srcaircraftaircraft_vehiclepy)
18. [Wytyczne dotyczące współpracy](#wytyczne-dotyczące-współpracy)
19. [Licencja](#licencja)
20. [Referencje](#referencje)

## Przegląd

Dokumentacja ta zapewnia szczegółowy przegląd klas zdefiniowanych w projekcie Unmanned Aerial Vehicle (UAV) Collision Avoidance. Każda klasa jest opisana pod kątem swojego przeznaczenia, atrybutów i metod.

Klasy są zorganizowane w następujące kategorie:
- `main`: Punkt wejścia aplikacji.
- `simulation`: Klasy odpowiedzialne za przeprowadzanie symulacji.
- `aircraft`: Klasy reprezentujące UAV.

Wszystkie klasy korzystają z właściwości i setterów Pythona, wykorzystując mutexy i blokady mutexów w celu zapewnienia hermetyzacji i integralności danych.

## Stałe

- Przyspieszenie grawitacyjne: `9.81 m/s^2`
- Częstotliwość symulacji: `100 Hz`
- Częstotliwość renderowania symulacji: `100 Hz`
- Częstotliwość systemu ADS-B: `1 Hz`
- Opóźnienie samolotu w zmianie kąta przechylenia `1000 ms`
- Opóźnienie samolotu w zmianie kąta nachylenia `2000 ms`
- Maksymalne chwilowe przyspieszenie samolotu `2 m/s^2`

---

## Plik: `main.py`

### Funkcja: `main()`

**Opis**:
Plik `main.py` jest punktem wejścia aplikacji. Uruchamia on główne okno aplikacji i obsługuje argumenty wiersza poleceń.

---

## Plik: `src/main.py`

### Funkcja: `main()`

**Opis**:
Właściwy punkt wejścia aplikacji. Rozpoczyna instancję QtApplication. Parsuje argumenty i uruchamia symulację w odpowiednim trybie.

#### Metody:
- `run_simulation_tests(test_number : int)`: Obsługuje równolegle uruchamiane symulacje.

---

## Plik: `src/version.py`

### Funkcja: `get_version()`

**Opis**:
Parsuje aktualną wersję aplikacji z pliku [pyproject.toml](/pyproject.toml).

---

## Plik: `src/simulation/simulation.py`

### Klasa: `Simulation`

**Opis**:
Główna klasa odpowiedzialna za przeprowadzanie symulacji. Rozróżnia się dwa podstawowe tryby działania:
- **realtime**: Tworzy graficzny interfejs użytkownika i przeprowadza symulację czasu rzeczywistego.
- **headless**: Przeprowadza symulację w tle.

Klasa `Simulation` jest odpowiedzialna za tworzenie przypadków testowych, przeprowadzanie serii testów, tworzenie i eksportowanie zbiorów danych o symulacjach oraz tworzenie wykresów ścieżek przebytych przez samoloty bezzałogowe. Klasy o nazewnictwie pochodnym Simulation- są tworzone wg kompozycji w trakcie działania obiektu klasy `Simulation`.

#### Właściwości:
- `simulation_id`: Identyfikator symulacji.
- `hash`: Unikalny ciąg znaków hash symulacji.
- `headless`: Flaga reprezentująca czy symulacja jest uruchamiana w tle.
- `tests`: Flaga reprezentująca czy symulacja przeprowadza testy.
- `simulation_time`: Czas symulacji [s].
- `aircrafts`: Lista symulowanych samolotów.
- `state`: Stan symulacji.
- `imported_from_data`: Flaga reprezentująca czy symulacja została wczytana z pliku.
- `simulation_data`: Zawiera strukturę danych wczytanej symulacji.
- `simulation_physics`: Obiekt symulacji fizycznej.
- `simulation_adsb`: Obiekt symulacji systemu ADS-B.
- `simulation_widget`: Obiekt widżetu symulacji.
- `simulation_render`: Obiekt renderowania symulacji.
- `simulation_fps`: Obiekt liczenia klatek na sekundę.

#### Metody:
- `__init__(headless : bool, tests : bool, simulation_time : int) -> None`: Inicjalizuje nową instancję symulacji bez tworzenia obiektu jej stanu ani samolotów bezzałogowych.
- `obtain_simulation_id() -> int`: Uzyskuje identyfikator symulacji.
- `obtain_simulation_hash() -> str`: Uzyskuje unikalny ciąg znaków hash symulacji.
- `run() -> None`: Uruchamia odpowiedni typ symulacji.
- `run_gui(avoid_collisions : bool, load_latest_data_file : bool) -> None`: Jawnie uruchamia symulację w trybie czasu rzeczywistego z GUI.
- `run_headless(avoid_collisions : bool, aircrafts : List[Aircraft], test_index : int, aircraft_angle : float) -> SimulationData`: Jawnie uruchamia symulację w tle. Zwraca strukturę danych symulacji do przeprowadzenia sprawdzeń.
- `generate_test_aircrafts() -> List[Tuple[List[Aircraft], float]]`: Generuje losowy zestaw samolotów do testowania w parach wraz z kątem pomiędzy nimi w postaci listy list.
- `generate_consistent_list_of_aircraft_lists() -> List[Tuple[List[Aircraft], float]]`: Zwraca predefiniowany zestaw samolotów do testowania w parach wraz z kątem pomiędzy nimi w postaci listy list.
- `run_tests(begin_with_default_set : bool, test_number : int)`: Uruchamia symulację w tle w trybie sekwencyjnego testowania wykorzystując losową generację testów. Analizuje struktury danych zwrócone przez symulacje w tle. Eksportuje dane testów.
- `load_latest_simulation_data_file() -> bool`: Podejmuje próbę załadowania ostatniego wygenerowanego pliku danych symulacji (manualne nazwanie pliku simulation.csv nadpisze poszukiwanie). Zwraca prawdę jeśli wczytanie się powiedzie.
- `load_simulation_data_from_file(file_path : str, test_id : int, avoid_collisions : bool) -> bool`: Podejmuje próbę załadowania pliku o zadanej nazwie. Zwraca prawdę jeśli wczytanie się powiedzie.
- `stop()`: Zatrzymuje symulację o dowolnym trybie działania.
- `stop_realtime_simulation() -> None`: Zatrzymuje symulację czasu rzeczywistego.
- `stop_headless_simulation() -> None`: Zatrzymuje symulację w tle.
- `add_aircraft(aircraft : Aircraft) -> None`: Dodaje dany samolot do zainicjalizowanej listy samolotów.
- `remove_aircraft(aircraft : Aircraft) -> None`: Podejmuje próbę usunięcia wskazanego samolotu z listy samolotów.
- `setup_aircrafts(self, aircrafts : List[Aircraft]) -> None`: Inicjalizuje listę samolotów z zewnętrznej listy.
- `setup_debug_aircrafts(self, test_case : int) -> None`: Nadpisuje listę samolotów z listy testowej.
- `import_simulation_data(data : SimulationData) -> None`: Podejmuje próbę wczytania symulacji ze struktury danych.
- `check_simulation_data_correctness() -> bool`: Przeprowadza sprawdzenie zgodności stanu symulacji z oczekiwaną, wczytaną strukturą danych. Zwraca prawdę jeśli dane są poprawne.
- `export_visited_locations(simulation_data : SimulationData, test_index : int)`: Eksportuje odwiedzone lokalizacje z komputerów pokładowych samolotów. Podejmuje próbę wygenerowania wykresu przebytych ścieżek.

---

## Plik: `src/simulation/simulation_physics.py`

### Klasa: `SimulationPhysics`

**Opis**:
Pozwala na przeprowadzenie symulacji fizyki samolotów bezzałogowych. Tworzy wątek odpowiedzialny za symulację fizyczną, śledzi lokalizację samolotów oraz wykonuje na nich operacje w czasie. Imituje prawa fizyczne wpływające na ciała fizyczne poprzez wykorzystanie różniczkowania.

#### Właściwości:
- `aircrafts`: Lista symulowanych samolotów.
- `aircraft_vehicles`: Lista symulowanych reprezentacji fizycznych samolotów.
- `aircraft_fccs`: Lista symulowanych komputerów pokładowych samolotów.
- `simulation_state`: Stan symulacji.
- `cycles`: Liczba zliczonych cykli symulacji.

#### Metody:

- `__init__(aircrafts : List[Aircraft], simulation_state : SimulationState) -> None`: Inicjalizuje nową instancję symulacji fizycznej.
- `count_cycles() -> None`: Inkrementuje liczbę cykli symulacji i odświeża stan symulacji.
- `run() -> None`: Uruchamia symulację fizyczną.
- `mark_start_time() -> None`: Zapisuje czas rozpoczęcia symulacji.
- `mark_stop_time() -> None`: Zapisuje czas zakończenia symulacji.
- `cycle(elapsed_time : float) -> None`: Przeprowadza pojedynczy cykl symulacji fizycznej.
- `reset_aircrafts() -> None`: Resetuje wszystkie samoloty do stanu początkowego.
- `update_aircrafts_positions() -> bool`: Aktualizuje lokalizację wszystkich samolotów. Zwraca prawdę jeśli doszło do jakiejkolwiek kolizji.
- `update_aircrafts_speed_angles() -> None`: Aktualizuje prędkość i kąty wszystkich symulowanych samolotów.
- `test_speed() -> None`: Sprawdza geometryczną zgodność prędkości samolotów.

---

## Plik: `src/simulation/simulation_adsb.py`

### Klasa: `SimulationADSB`

**Opis**:
Pozwala na utworzenie wątku odpowiedzialnego za symulację systemu ADS-B (Automatic Dependent Surveillance-Broadcast). Zarządza komputerami pokładowymi (FCC) samolotów bezzałogowych w celu wysyłania danych unikania kolizji w razie potrzeby.

#### Właściwości:
- `aircrafts`: Lista symulowanych samolotów.
- `aircraft_vehicles`: Lista symulowanych reprezentacji fizycznych samolotów.
- `aircraft_fccs`: Lista symulowanych komputerów pokładowych samolotów.
- `simulation_state`: Stan symulacji.
- `adsb_cycles`: Liczbę zliczonych cykli systemu ADS-B.
- `minimal_relative_distance`: Najmniejsza znana względna odległość między dwoma samolotami.

#### Metody:
- `__init__(aircrafts : List[Aircraft], simulation_state : SimulationState) -> None`: Inicjalizuje nową instancję symulacji ADS-B.
- `count_adsb_cycles() -> None`: Inkrementuje liczbę cykli systemu ADS-B.
- `run() -> None`: Rozpoczyna symulację systemu ADS-B.
- `cycle() -> None`: Przebiega pojedynczy cykl systemu ADS-B.
- `print_adsb_report() -> None`: Wypisuje raport systemu ADS-B w postaci danych o samolotach.
- `reset_destinations() -> None`: Resetuje cele samolotów do stanu początkowego.

---

## Plik: `src/simulation/simulation_state.py`

### Klasa: `SimulationState`

**Opis**:
Przechowuje informacje o aktualnym stanie symulacji - zmienne dostępne dla wszystkich komponentów programu. Obsługuje zarówno symulacje czasu rzeczywistego, jak i w tle.

#### Właściwości:
- `simulation_settings`: Globalne ustawienia symulacji.
- `is_realtime`: Flaga reprezentująca czy symulacja jest czasu rzeczywistego.
- `avoid_collisions`: Flaga reprezentująca czy unikanie kolizji jest włączone.
- `override_avoid_collisions`: Flaga reprezentująca czy unikanie kolizji jest nadpisane i wyłączone.
- `minimum_separation`: Minimalna odległość między samolotami.
- `physics_cycles`: Liczba zliczonych cykli symulacji fizycznej.
- `is_paused`: Flaga reprezentująca czy symulacja jest wstrzymana.
- `is_running`: Flaga reprezentująca czy symulacja jest uruchomiona i nie skończyła się.
- `reset_demanded`: Flaga reprezentująca żądanie resetu symulacji.
- `pause_start_timestamp`: Czas rozpoczęcia ostatniego wstrzymania symulacji.
- `time_paused`: Łączny czas wstrzymania symulacji.
- `adsb_report`: Flaga reprezentująca czy raportowanie systemu ADS-B jest włączone.
- `collision`: Flaga reprezentująca czy doszło do kolizji.
- `first_cause_collision`: Flaga reprezentująca czy pierwszy samolot powoduje kolizję.
- `second_cause_collision`: Flaga reprezentująca czy drugi samolot powoduje kolizję.
- `fps`: Bieżąca liczba klatek na sekundę.

#### Metody:
- `__init__(simulation_settings : SimulationSettings, is_realtime : bool, avoid_collisions : bool) -> None`: Inicjalizuje nową instancję stanu symulacji.
- `toggle_avoid_collisions() -> None`: Przełącza flagę unikania kolizji.
- `toggle_pause() -> None`: Przełącza flagę wstrzymania symulacji.
- `reset() -> None`: Ustawia flagę resetu symulacji na prawdę.
- `apply_reset() -> None`: Przywraca flagę resetu symulacji na nieprawdę.
- `append_time_paused() -> None`: Dodaje czas wstrzymania symulacji do łącznego czasu wstrzymania.
- `toggle_adsb_report() -> None`: Przełącza flagę raportowania systemu ADS-B.
- `register_collision() -> None`: Rejestruje kolizję.
- `toggle_first_cause_collision() -> None`: Przełącza flagę powodowania kolizji przez pierwszy samolot.
- `toggle_second_cause_collision() -> None`: Przełącza flagę powodowania kolizji przez drugi samolot.
- `toggle_draw_fps() -> None`: Przełącza flagę wypisywania liczby klatek na sekundę.
- `toggle_draw_aircraft() -> None`: Przełącza flagę rysowania samolotów.
- `toggle_draw_grid() -> None`: Przełącza flagę rysowania siatki.
- `toggle_draw_path() -> None`: Przełącza flagę rysowania ścieżek przebytych dróg.
- `toggle_draw_speed_vectors() -> None`: Przełącza flagę rysowania wektorów prędkości.
- `toggle_draw_safe_zones() -> None`: Przełącza flagę rysowania stref bezpiecznych wokół samolotów.
- `toggle_draw_collision_detection() -> None`: Przełącza flagę rysowania detekcji kolizji.
- `toggle_optimize_drawing() -> None`: Przełącza flagę optymalizacji rysowania.
- `toggle_follow_aircraft() -> None`: Przełącza flagę śledzenia samolotu.
- `toggle_focus_aircraft() -> None`: Przełącza widok śledzonego pojazdu.
- `update_settings() -> None`: Aktualizuje ustawienia stanu symulacji.
- `update_render_settings() -> None`: Aktualizuje ustawienia renderowania symulacji.
- `update_simulation_settings() -> None`: Aktualizuje ustawienia symulacji.
- `update_adsb_settings() -> None`: Aktualizuje ustawienia systemu ADS-B.

---

## Plik: `src/simulation/simulation_settings.py`

### Klasa: `SimulationSettings`

**Opis**:
Klasa statyczna przechowująca stałe używane w programie oraz początkowe dane symulacji.

#### Static members:
- `screen_resolution`: Rozdzielczość ekranu.
- `resolution`: Rozdzielczość okna symulacji.
- `g_acceleration`: Przyspieszenie grawitacyjne.
- `simulation_frequency`: Częstotliwość symulacji .
- `simulation_threshold`: Opóźnienie pomiędzy cyklami symulacji.
- `gui_render_frequency`: Częstotliwość renderowania GUI.
- `gui_render_threshold`: Opóźnienie pomiędzy cyklami renderowania GUI.
- `adsb_threshold`: Opóźnienie pomiędzy cyklami systemu ADS-B.

#### Metody:
- `__init__()` : Inicjalizuje statyczną instancję ustawień symulacji.

---

## Plik: `src/simulation/simulation_widget.py`

### Klasa: `SimulationWidget`

**Opis**:
Umożliwia tworzenie interfejsu użytkownika w postaci widżetu - interaktywnego okna, które wizualizuje proces symulacji, umożliwia śledzenie wybranego samolotu i modyfikację jego planu lotu oraz decydowania o wykonaniu manewru unikania kolizji w razie wystąpienia takiej możliwości.

#### Właściwości:
- `aircrafts`: Lista symulowanych samolotów.
- `aircraft_vehicles`: Lista symulowanych reprezentacji fizycznych samolotów.
- `aircraft_fccs`: Lista symulowanych komputerów pokładowych samolotów.
- `simulation_fps`: Obiekt liczący liczbę klatek na sekundę.
- `simulation_state`: Stan symulacji.
- `window_width`: Szerokość okna symulacji.
- `window_height`: Wysokość okna symulacji.
- `screen_offset_x`: Offset ekranu w osi x.
- `screen_offset_y`: Offset ekranu w osi y.
- `icon`: Ikona (miniatura) symulacji.
- `moving_view_up`: Flaga reprezentująca czy widok jest przesuwany w górę.
- `moving_view_down`: Flaga reprezentująca czy widok jest przesuwany w dół.
- `moving_view_left`: Flaga reprezentująca czy widok jest przesuwany w lewo.
- `moving_view_right`: Flaga reprezentująca czy widok jest przesuwany w prawo.
- `steering_up`: Flaga reprezentująca sterowanie w górę `kurs 0`.
- `steering_down`: Flaga reprezentująca sterowanie w dół `kurs 180`.
- `steering_left`: Flaga reprezentująca sterowanie w lewo `kurs 270`.
- `steering_right`: Flaga reprezentująca sterowanie w prawo `kurs 90`.

#### Metody:
- `__init__(aircrafts : List[Aircraft], simulation_state : SimulationState) -> None`: Inicjalizuje nową instancję widżetu aplikacji.
- `generate_icon() -> None`: Generuje ikonę symulacji.
- `draw_aircraft(aircraft : AircraftVehicle, scale : float) -> None`: Rysuje samoloty w oknie symulacji.
- `draw_destinations(aircraft : AircraftVehicle, scale : float) -> None`: Rysuje cele samolotów w oknie symulacji.
- `draw_text(point : QVector3D, scale : float, text : str, color : QColor) -> None`: Wyświetla tekst w oknie symulacji.
- `draw_circle(point : QVector3D, size : float, scale : float, color : QColor) -> None`: Rysuje okrąg w oknie symulacji.
- `draw_disk(point : QVector3D, size : float, scale : float, color : QColor) -> None`: Rysuje koło w oknie symulacji.
- `draw_line(start : QVector3D, end : QVector3D, scale : float, color : QColor) -> None`: Rysuje linię w oknie symulacji.
- `draw_vector(start : QVector3D, vector : QVector3D, scale : float, color : QColor) -> None`: Rysuje wektor w oknie symulacji.
- `draw_collision_detection(scale : float) -> None`: Rysuje detekcję kolizji w oknie symulacji.
- `draw_grid(scale : float, x_offset : float, y_offset : float) -> None`: Rysuje siatkę w oknie symulacji.
- `update_moving_offsets() -> None`: Aktualizuje przesunięcia (offsety) okna symulacji.
- `update_steering() -> None`: Aktualizuje stan nadpisywania kursów samolotów.
- `center_offsets() -> None`: Wyśrodkowuje przesunięcia okna symulacji.
- `update_resolutions() -> None`: Aktualizuje rozdzielczość okna symulacji.
- `zoom(factor : float) -> None`: Przybliża lub oddala widok okna symulacji o podany współczynnik.
- `paintEvent(event : QPaintEvent) -> None`: Obsługuje zdarzenie rysowania okna symulacji.
- `mousePressEvent(event : QMouseEvent) -> None`: Obsługuje zdarzenie naciśnięcia przycisku myszy.
- `mouseReleaseEvent(event : QMouseEvent) -> None`: Obsługuje zdarzenie zwolnienia przycisku myszy.
- `mouseDoubleClickEvent(event : QMouseEvent) -> None`: Obsługuje zdarzenie podwójnego kliknięcia myszy.
- `wheelEvent(event : QWheelEvent) -> None`: Obsługuje zdarzenie przewijania kółkiem myszy (scroll).
- `keyPressEvent(event : QKeyEvent) -> None`: Obsługuje zdarzenie naciśnięcia klawisza.
- `keyReleaseEvent(event : QKeyEvent) -> None`: Obsługuje zdarzenie zwolnienia klawisza.
- `resizeEvent(event : QResizeEvent) -> None`: Obsługuje zdarzenie zmiany rozmiaru okna symulacji.
- `closeEvent(event : QCloseEvent) -> None`: Obsługuje zdarzenie zamknięcia okna symulacji.

---

## Plik: `src/simulation/simulation_render.py`

### Klasa: `SimulationRender`

**Opis**:
Umożliwia tworzenie wątku odpowiedzialnego za odświeżanie okna symulacji w `SimulationWidget`. Zarządza renderowaniem symulacji w czasie rzeczywistym.

#### Właściwości:
- `simulation_widget`: Widżet symulacji.
- `simulation_state`: Stan symulacji.

#### Metody:
- `__init__(simulation_widget : SimulationWidget, simulation_state : SimulationState) -> None`: Inicjalizuje nową instancję renderowania symulacji.
- `run() -> None`: Rozpoczyna renderowanie symulacji.

---

## Plik: `src/simulation/simulation_fps.py`

### Klasa: `SimulationFPS`

**Opis**:
Udostępnia interfejs do zliczania i wyświetlania liczby klatek generowanych na sekundę podczas symulacji czasu rzeczywistego.

#### Właściwości:
- `simulation_state`: Stan symulacji.
- `counted_frames`: Liczba zliczonych klatek.
- `previous_timestamp`: Poprzedni znacznik czasu.

#### Metody:
- `__init__(simulation_state : SimulationState) -> None`: Inicjalizuje nową instancję licznika FPS.
- `run() -> None`: Rozpoczyna liczenie klatek.
- `count_frame() -> None`: Inkrementuje liczbę zliczonych klatek.
- `reset_frames() -> None`: Resetuje licznik klatek.
- `counted_frames -> int`: Zwraca liczbę zliczonych klatek.

---

## Plik: `src/simulation/simulation_data.py`

### Klasa: `SimulationData`

**Opis**:
Pozwala na śledzenie danych związanych z symulacją, które są niezbędne do wczytywania i generowania testów. Przechowuje informacje o samolotach, ich lokalizacjach, prędkościach, celach, kątach i innych parametrach z początku i końca symulacji.

#### Właściwości:
- `aircraft_angle`: Kąt pomiędzy samolotami.
- `aircraft_1_initial_position`: Początkowa pozycja pierwszego samolotu.
- `aircraft_2_initial_position`: Początkowa pozycja drugiego samolotu.
- `aircraft_1_final_position`: Końcowa pozycja pierwszego samolotu.
- `aircraft_2_final_position`: Końcowa pozycja drugiego samolotu.
- `aircraft_1_initial_speed`: Początkowa prędkość pierwszego samolotu.
- `aircraft_2_initial_speed`: Początkowa prędkość drugiego samolotu.
- `aircraft_1_final_speed`: Końcowa prędkość pierwszego samolotu.
- `aircraft_2_final_speed`: Końcowa prędkość drugiego samolotu.
- `aircraft_1_initial_target`: Początkowy cel pierwszego samolotu.
- `aircraft_2_initial_target`: Początkowy cel drugiego samolotu.
- `aircraft_1_initial_roll_angle`: Początkowy kąt przechylenia pierwszego samolotu.
- `aircraft_2_initial_roll_angle`: Początkowy kąt przechylenia drugiego samolotu.
- `collision`: Flaga reprezentująca czy doszło do kolizji.
- `minimal_relative_distance`: Najmniejsza znana względna odległość między dwoma samolotami.

#### Metody:
- `__init__() -> None`: Inicjalizuje nową instancję danych symulacji.
- `reset() -> None`: Resetuje dane symulacji.

---

## Plik: `src/aircraft/aircraft.py`

### Klasa: `Aircraft`

**Opis**:
Reprezentuje symulowany UAV. Tworzy pola za pomocą kompozycji - obiekty klas `AircraftFCC` i `AircraftVehicle`. Reprezentuje samolot bezzałogowy jako obiekt fizyczny z komputerem pokładowym.

#### Właściwości:
- `aircraft_id`: Identyfikator samolotu.
- `vehicle`: Fizyczna reprezentacja samolotu.
- `fcc`: Komputer pokładowy samolotu.
- `initial_position`: Początkowa pozycja samolotu.
- `initial_target`: Początkowy cel samolotu.
- `initial_speed`: Początkowa prędkość samolotu.
- `initial_roll_angle`: Początkowy kąt przechylenia samolotu.

#### Metody:
- `__init__(aircraft_id : int, position : QVector3D, speed : float, initial_target : QVector3D, initial_roll_angle : float) -> None`: Inicjalizuje nową instancję samolotu bezzałogowego.
- `reset() -> None`: Resetuje samolot do stanu początkowego.

---

## Plik: `src/aircraft/aircraft_fcc.py`

### Klasa: `AircraftFCC`

**Opis**:
Reprezentuje komputer pokładowy samolotu bezzałogowego. Śledzi zaplanowaną trasę i ustawia odpowiednie parametry lotu.

#### Właściwości:
- `aircraft_id`: Identyfikator samolotu.
- `aircraft`: Rodzic komputera pokładowego - samolot.
- `destinations`: Kolejka celów do odwiedzenia.
- `destinations_history`: Lista odwiedzonych celów.
- `visited`: Lista odwiedzonych punktów w przestrzeni.
- `autopilot`: Flaga reprezentująca czy autopilot jest włączony.
- `ignore_destinations`: Flaga reprezentująca czy kolejka celów jest ignorowana.
- `initial_target`: Początkowy cel komputera pokładowego.
- `target_yaw_angle`: Docelowy kąt skrętu samolotu.
- `target_roll_angle`: Docelowy kąt przechylenia samolotu.
- `target_pitch_angle`: Docelowy kąt pochylenia samolotu.
- `target_speed`: Docelowa prędkość samolotu.
- `is_turning_right`: Flaga reprezentująca czy samolot skręca w prawo.
- `is_turning_left`: Flaga reprezentująca czy samolot skręca w lewo.
- `safe_zone_occupied`: Flaga reprezentująca czy strefa bezpieczna jest naruszona.
- `evade_maneuver`: Flaga reprezentująca czy wykonywany jest manewr unikania kolizji.
- `vector_sharing_resolution`: Rozdzielczość wektora współdzielenia [m].

#### Metody:
- `__init__(aircraft_id : int, initial_target : QVector3D) -> None`: Inicjalizuje nową instancję komputera pokładowego samolotu.
- `toggle_autopilot() -> None`: Przełącza flagę autopilota.
- `accelerate(acceleration : float) -> None`: Modyfikuje docelową prędkość o wskazaną wartość
- `check_new_destination(destination : QVector3D, first : bool) -> QVector3D`: Sprawdza czy podany cel jest poprawny i poprawia/zwraca go.
- `add_last_destination(destination : QVector3D) -> None`: Dopisuje podany cel na koniec kolejki celów.
- `add_first_destination(destination : QVector3D) -> None`: Dopisuje podany cel na początek kolejki celów.
- `append_visited() -> None`: Dopisuje aktualną lokalizację samolotu do listy odwiedzonych punktów.
- `normalize_angle(angle : float) -> float`: Normalizuje podany kąt i zwraca go w dziedzinie `[0, 360]`.
- `format_yaw_angle(angle : float) -> float`: Formatuje podany kąt i zwraca go w dziedzinie `[-180, 180]`.
- `apply_evade_maneuver(opponent_speed : QVector3D, miss_distance_vector : QVector3D, unresolved_region : float, time_to_closest_approach : float) -> None`: Stosuje manewr unikania kolizji korzystając z podejścia geometrycznego.
- `reset_evade_maneuver() -> None`: Resetuje wykonywanie manewru unikania kolizji.
- `find_best_roll_angle(current_yaw_angle : float, target_yaw_angle : float) -> float`: Oblicza i zwraca najlepszy kąt przechylenia samolotu.
- `find_best_yaw_angle(position : QVector3D, destination : QVector3D) -> float`: Oblicza i zwraca najlepszy w bieżącej chwili kąt skrętu samolotu.
- `find_best_pitch_angle(position : QVector3D, destination : QVector3D) -> float`: Oblicza i zwraca najlepszy w bieżącej chwili kąt pochylenia samolotu.
- `update_target_yaw_pitch_angles() -> None`: Odświeża docelowe kąty skrętu i pochylenia samolotu.
- `update_target_roll_angle() -> None`: Odświeża docelowy kąt przechylenia samolotu.
- `update() -> None`: Odświeża docelowe kąty komputera pokładowego.
- `update_target(target : QVector3D) -> None`: Ustala nowy chwilowy cel samolotu na wskazany w parametrze.
- `reset() -> None`: Resetuje komputer pokładowy samolotu do stanu początkowego.
- `load_initial_destination() -> None`: Ładuje początkowy cel samolotu jako pierwszy cel.

---

## Plik: `src/aircraft/aircraft_vehicle.py`

### Klasa: `AircraftVehicle`

**Opis**:
Reprezentuje UAV jako obiekt fizyczny. Przechowuje informacje o jego położeniu w przestrzeni i prędkości, a także o jego rozmiarze i bezwładności.

#### Właściwości statyczne:
- `roll_dynamic_delay`: Opóźnienie samolotu w zmianie kąta przechylenia [ms].
- `pitch_dynamic_delay`: Opóźnienie samolotu w zmianie kąta nachylenia [ms].
- `max_acceleration`: Maksymalne chwilowe przyspieszenie samolotu [m/s^2].

#### Właściwości:
- `aircraft_id`: Identyfikator samolotu.
- `position`: Lokalizacja samolotu.
- `speed`: Prędkość samolotu.
- `size`: Rozmiar samolotu.
- `roll_angle`: Kąt przechylenia samolotu.
- `initial_roll_angle`: Początkowy kąt przechylenia samolotu.
- `distance_covered`: Dystans przebyty przez samolot.

#### Metody:
- `__init__(aircraft_id : int, position : QVector3D, speed : float, size : float, roll_angle : float) -> None`: Inicjalizuje nową instancję fizycznej reprezentacji samolotu.
- `reset_distance_covered() -> None`: Resetuje dystans przebyty przez samolot.
- `move(dx : float, dy : float, dz : float) -> None`: Przemieszcza samolot o podane odległości.
- `roll(d_angle : float)`: Obraca samolot o podany kąt.

---

## Wytyczne dotyczące współpracy

Przed przystąpieniem do współpracy, proszę sprawdzić [CONTRIBUTING.md](/CONTRIBUTING.md).

Współpraca z projektem jest mile widziana. Proszę postępować zgodnie z poniższymi krokami:
1. Rozgałęź (fork) repozytorium.
2. Utwórz nową gałąź (branch) dla swojej funkcji lub poprawki błędu.
3. Prześlij PR z jasnym opisem swoich zmian wg szablonu [PULL_REQUEST_TEMPLATE.md](/PULL_REQUEST_TEMPLATE.md).

---

## Licencja

Projekt jest dostępny na licencji MIT. Więcej informacji można znaleźć w pliku [LICENSE](/LICENSE).

---

Po więcej informacji, odwiedź [repozytorium GitHub](https://github.com/mldxo/uav-collision-avoidance).

## Referencje

Wszystkie odnośniki do prac badawczych i wykorzystanych materiałów znajdują się poniżej.

- [Python3](https://www.python.org/)
- [PyPi](https://pypi.org/)
- [PyQt6](https://doc.qt.io/qtforpython-6/)
- [UAV Collision Avoidance Based on Geometric Approach](https://ieeexplore.ieee.org/document/4655013/)
- [Energy Efficient UAV Flight Control Method in an Environment with Obstacles and Gusts of Wind](https://www.mdpi.com/1638452/)
- [Kąty RPY](https://pl.wikipedia.org/wiki/K%C4%85ty_RPY)
