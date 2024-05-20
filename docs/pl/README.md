# Dokumentacja

> [!WARNING]
> Dokumentacja jest w trakcie tłumaczenia na język polski.

## Spis treści

1. [Przegląd](#przegląd)
2. [Plik: `main.py`](#plik-mainpy)
3. [Plik: `src/main.py`](#plik-srcmainpy)
4. [Plik: `src/version.py`](#plik-srcversionpy)
5. [Plik: `src/simulation/simulation.py`](#plik-srcsimulationsimulationpy)
6. [Plik: `src/simulation/simulation_physics.py`](#plik-srcsimulationsimulation_physicspy)
7. [Plik: `src/simulation/simulation_adsb.py`](#plik-srcsimulationsimulation_adsbpy)
8. [Plik: `src/simulation/simulation_state.py`](#plik-srcsimulationsimulation_statepy)
9. [Plik: `src/simulation/simulation_settings.py`](#plik-srcsimulationsimulation_settingspy)
10. [Plik: `src/simulation/simulation_widget.py`](#plik-srcsimulationsimulation_widgetpy)
11. [Plik: `src/simulation/simulation_render.py`](#plik-srcsimulationsimulation_renderpy)
12. [Plik: `src/simulation/simulation_fps.py`](#plik-srcsimulationsimulation_fpspy)
13. [Plik: `src/simulation/simulation_data.py`](#plik-srcsimulationsimulation_datapy)
14. [Plik: `src/aircraft/aircraft.py`](#plik-srcaircraftaircraftpy)
15. [Plik: `src/aircraft/aircraft_fcc.py`](#plik-srcaircraftaircraft_fccpy)
16. [Plik: `src/aircraft/aircraft_vehicle.py`](#plik-srcaircraftaircraft_vehiclepy)
17. [Wytyczne dotyczące współpracy](#wytyczne-dotyczące-współpracy)
18. [Licencja](#licencja)
19. [Referencje](#referencje)

## Przegląd

Dokumentacja ta zapewnia szczegółowy przegląd klas zdefiniowanych w projekcie Unmanned Aerial Vehicle (UAV) Collision Avoidance. Każda klasa jest opisana pod kątem swojego przeznaczenia, atrybutów i metod.

Klasy są zorganizowane w następujące kategorie:
- `main`: Punkt wejścia aplikacji.
- `simulation`: Klasy odpowiedzialne za przeprowadzanie symulacji.
- `aircraft`: Klasy reprezentujące UAV.

Wszystkie klasy korzystają z właściwości i setterów Pythona, wykorzystując mutexy i blokady mutexów do zapewnienia hermetyzacji i integralności danych.

---

## Plik: `main.py`

### Funkcja: `main()`

**Description**:
Plik `main.py` jest punktem wejścia aplikacji. Uruchamia on główne okno aplikacji i obsługuje argumenty wiersza poleceń.