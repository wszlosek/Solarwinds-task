Zadanie wykonane w języku Python 3.7 z użyciem modułów time oraz datetime.

Przyjęte założenia:

- dane w pliku nie muszą być sortowane (według daty), program je posortuje

- za ilość czasu spędzonego w budynku przyjęto bezwzględną różnicę czasu
skrajnych wpisów w danym dniu

- dzień może stanowić dowolona prawidłowa data

- wejście główne posiada czytnik identyfikatorów, zaś garaż niekoniecznie

- format */numer piętra/*/* nie jest wymagany, lecz w innym wypadku,
program nie będzie w stanie wyznaczyć numeru piętra

- linie w pliku nie muszą być poprawne (błędny format, zła data itp.) - gdy nie
są, program je pomija, kontynuując pracę

- czas pracy w ciągu dnia jest jednoznaczny, gdy oba następujące przypadki wystąpią:
a) istnieje minimum jedno entry wśród statusów (wejście do biura),
b) ostatnim zdarzeniem w ciągu dnia musi być exit (z budynku), jeśli znany jest numer piętra,
to exit musi być oczywiście z piętra 0.
Jeśli którykolwiek z tych przypadków nie zachodzi, to zostaje wypisane "i".