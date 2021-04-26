# Zadanie: monitorowanie czasu spędzonego przez osobę w budynku.

Zadanie praktyczne wykonane w języku Python na potrzeby pierwszego etapu rekrutacji w firmie SolarWinds.

## Table of contents
* [Opis projektu](#opis-projektu)
* [Założenia](#założenia)
* [Uruchomienie programu](#uruchomienie-programu)
* [Użyte technologie i szczegóły techniczne](#użyte-technologie-i-szczegóły-techniczne)
* [Przykłady działania programu](#przykłady-działania-programu)
* [Posłowie](#posłowie)

## Opis projektu

Zadanie polegało na stworzeniu oprogramowania do monitoringu czasu spędzonego przez osobę w budynku biurowym. Osoba posiada identyfikator, a drzwi posiadają czytnik kart. Źródło danych stanowił plik .csv, zawierający informację czasową o interakcji (identyfikator <-> drzwi), status tej interakcji (wejście/wyjście) oraz kod identyfikujący dane drzwi. 

Pozostałe informacje znajdują się w pliku .pdf z treścią zadania. 

Poniżej zostały zamieszczone informacje o założeniach - treść zadania nie stanowiła o szczegółach i interpretacji różnych zjawisk, które mogłyby przytrafić się w świecie rzeczywistym. Przyjęte założenia starają się je regulować, a często również objaśniać.

## Założenia

Podczas tworzenia programu, należało przyjąć szereg założeń i interpretacji zjawisk nieopisanych w wymaganiach projektu, co zresztą sprzyjało kreatywności.

Dane w pliku nie muszą być sortowane (według daty) - program sam je posortuje lokalnie na swoje potrzeby.

Za ilość czasu spędzonego w budynku przyjęto bezwzględną różnicę czasu - pierwszego i ostatniego wpisu z pliku - w danym dniu. Dzień może stanowić dowolona prawidłowa data. 

Zgodnie z treścią zadania: "biurowiec posiada wejście główne z czytnikiem identyfikatorów oraz wejście przez garaż", zatem przyjęto, że wejście główne posiada czytnik identyfikatorów, zaś garaż nie, co implikuje istnienie sytuacji niezarejestrowanego wejścia przez garaż.

Przyjąłem domyślny format każdej linii pliku jako: `yyyy-mm-dd hh:mm:ss ;Reader *;*/numer piętra/*/*`, jednak program jest odporny na pewne modyfikacje (np. inny znak zamiast średnika) lub na inny format identyfikatora drzwi - w takim przypadku nie będzie w stanie rozpoznać numeru piętra. Dopuszczalne jest, by pierwsza linia pliku nie zawierała konkretnych danych, a np. nazwy kolumn. Jeśli podczas wczytywania linii pliku, okaże się, że jej format jest inny niż ogólnie przyjęty (nawet spoza dopuszczalnych modyfikacji) lub jawnie błędny (np. zła data) to dana linia zostanie pominięta, a program będzie kontynuował swoje zadanie.

Uznałem czas pracy w ciągu dnia za jednoznaczny, gdy ostatnim zdarzeniem w ciągu dnia jest exit (z budynku) - jeśli program wraz z identyfikatorem drzwi poznał numer piętra, to exit musi być oczywiście z piętra 0. 

W przeciwnym wypadku zostaje wypisane `i`.

## Uruchomienie programu

Program wykorzystuje funkcje z modułu `datetime`. Zatem w przypadku, gdy nie jest on dostępny na Twoim komputerze, a chcesz pobrać ten program, zainstaluj go, np. poprzez `pip`:
```bash
   pip install datetime
```
Żeby zacząć korzystać z programu, możesz np. sklonować to repozytorium: wejdź do folderu lokalnego gdzie chcesz go umieścić i w terminalu wpisz:
```bash
   git clone https://github.com/wszlosek/Solarwinds-task
```
Jeśli nie chcesz klonować repozytorium, możesz również manualnie pobrać ZIPa tego projektu z Githuba wraz ze wszystkimi jego plikami.

Mając dostęp do projektu, możesz go uruchomić:
```bash
   python3 main.py
```
## Użyte technologie i szczegóły techniczne
Program został napisany w języku Python (w wersji 3.7). Do działania potrzebuje dostępu do wspomnianego wcześniej modułu `datetime`.

## Przykłady działania programu

Plik wejściowy przyjmuje domyślnie nazwę `input.csv`, wyniki zapisuje w pliku `result`.

#### Przykład 1
```txt
    # plik input.csv
    
    2016-07-21 15:35:39  ;Reader entry;E/0/KD1/7-9
    2017-07-23 15:37:39  ;Reader exit;E/1/KD1/7-3
    2017-07-23 16:38:39  ;Reader exit;E/0/KD1/7-9
    2017-08-23 16:39:40  ;Reader exit;E/2/KD1/7-10
    2017-08-23 16:40:40  ;Reader exit;E/1/KD1/5-3
    2017-08-23 17:40:40  ;Reader exit;E/1/KD1/5-1
    2017-08-24 17:41:42  ;Reader entry;E/0/KD1/7-9
    2017-08-24 17:42:45  ;Reader entry;E/2/KD1/7-2
    2017-08-28 15:35:39  ;Reader entry;E/0/KD1/7-9
    2017-08-28 16:31:30  ;Reader entry;E/1/KD1/7-3
    2017-08-28 17:00:57  ;Reader exit;E/0/KD1/8-8
```

```txt
    # plik result
    
    Day 2016-07-21 Work 0:00:00 ut i 00:00:00 -08:00:00
    Day 2017-07-23 Work 1:01:00 w ut 01:01:00 -06:59:00
    Day 2017-08-23 Work 1:01:00 ut i
    Day 2017-08-24 Work 0:01:03 ut i 01:02:03 -14:57:57
    Day 2017-08-28 Work 1:25:18 ut 01:25:18 -06:34:42
```

#### Przykład 2
```txt
    # plik input.csv (nieposortowane dane z błędnymi liniami)
    
    Date;Event;Gate
    2017-08-23 11:39:40  ;Reader exit;E/2/KD1/7-10
    2017-08-23 16:40:40  ;Reader exit;E/1/KD1/5-3
    2017-08-23 17:40:40  ;Reader exit;E/1/KD1/5-1
    2017-08-23 17:41:42  ;Reader entry;E/0/KD1/7-9
    2017-08-23 23:42:45  ;Reader entry;E/2/KD1/7-2
    2017-08-28 15:35:39  ;Reader entry;E/0/KD1/7-9
    2017-08-26 16:31:30  ;Reader entry;E/1/KD1/7-3
    2017-08-28 17:00:57  ;Reader exit;E/0/KD1/8-8
    sdsada

    asadasdnmamndamsdasmndsamdmnasndmsamdnasmdamna
    2016-08-26 15:35:39  ;Reader entry;E/0/KD1/7-9
    2017-07-23 15:37:39  ;Reader exit;E/1/KD1/7-3
    2017-07-23 15:37:39  ;Reader exE/1/KD1/7-3
    2017-08-26 16:38:39  ;Reader exit;E/0/KD1/7-9
```
```txt
    # plik result
    
    Day 2016-08-26 Work 0:00:00 ut i 00:00:00 -08:00:00
    Day 2017-07-23 Work 0:00:00 w ut i 00:00:00 -08:00:00
    Day 2017-08-23 Work 12:03:05 ot i
    Day 2017-08-26 Work 0:07:09 w ut 12:10:14 -03:49:46
    Day 2017-08-28 Work 1:25:18 ut 01:25:18 -06:34:42
```

## Posłowie
Obecna wersja projektu została przesłana do firmy SolarWinds.

26 kwietnia, 2021.
