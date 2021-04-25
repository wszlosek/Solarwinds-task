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

Za ilość czasu spędzonego w budynku przyjęto bezwzględną różnicę czasu - pierwszego i ostatniego wpisu z pliku - w danym dniu. 

Zgodnie z treścią zadania: "biurowiec posiada wejście główne z czytnikiem identyfikatorów oraz wejście przez garaż", zatem przyjęto, że wejście główne posiada czytnik identyfikatorów, zaś garaż nie, co implikuje istnienie sytuacji niezarejestrowanego wejścia przez garaż.

Przyjąłem domyślny format każdej linii pliku jako: `yyyy-mm-dd hh:mm:ss ;Reader *;*/numer piętra/*/*`, jednak program jest odporny na pewne modyfikacje (np. inny znak zamiast średnika) lub na inny format identyfikatora drzwi - w takim przypadku nie będzie w stanie rozpoznać numeru piętra. Dopuszczalne jest, by pierwsza linia pliku nie zawierała konkretnych danych, a np. nazwy kolumn. Jeśli podczas wczytywania linii pliku, okaże się, że jej format jest inny niż ogólnie przyjęty (nawet spoza dopuszczalnych modyfikacji) lub jawnie błędny (np. zła data) to dana linia zostanie pominięta, a program będzie kontynuował swoje zadanie.

Uznałem czas pracy w ciągu dnia za jednoznaczny, gdy oba następujące przypadki wystąpią: musi istnieć minimum jedno entry wśród statusów (wejście do biura), jako, że nie znaliśmy konkretnego identyfikatora drzwi wejściowych (poza tym ktoś mógł wejść nierejestrując się: przez garaż), to nie można bardziej szczegółowo określić poprawności oraz ostatnim zdarzeniem w ciągu dnia musi być exit (z budynku) - jeśli program wraz z identyfikatorem drzwi poznał numer piętra, to exit musi być oczywiście z piętra 0. Jeśli którykolwiek z tych przypadków nie zachodzi, to zostaje wypisane `i`.

## Uruchomienie programu

Program wykorzystuje funkcje z modułów `time` i `datetime`. Zatem w przypadku, gdy nie są one dostępne na Twoim komputerze, a chciałbyś pobrać ten program, powinieneś je zainstalować, np poprzez `pip`:
```bash
   pip install time datetime
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
Program został napisany w języku Python (w wersji 3.7). Do działania potrzebuje dostępu do wspomnianych wcześniej modułów: `time` i `datetime`.

## Przykłady działania programu

Plik wejściowy przyjmuje domyślnie nazwę `input.csv`, wyniki zapisuje w pliku `result`.

#### Przykład 1
```txt
    # plik input.csv
    
```

## Posłowie
Obecna wersja projektu została przesłana do firmy SolarWinds.

26 kwietnia, 2021.
