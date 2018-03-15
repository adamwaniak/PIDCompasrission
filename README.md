# PIDCompasrission
Cel badań:
Dobór optymalnych parametrów dla regulatorów P, PI, PID.
Porównanie regulatorów P, PI, PID dla prostego obiektu cieplnego.


## Opis symulatora i systemu procesu

Zadaniem symulacji jest dobór optymalnych parametrów dla regulatorów P, PI, PID oraz sprawdzenie który z nich najlepiej nada się do kontrolowania temperatury pomieszczenia. Zakładamy, że regulator kontroluje moc klimatyzatora, więc może ogrzewać oraz chłodzić pomieszczenie.

## Model:

y’(t) = ay(t) + u(t) + z(t)

W ramach doświadczenia przeprowadzimy parę symulacji. Będziemy posługiwać się następującymi parametrami:
* d – temperatura zadana
* T – czas pracy symulatora
* y0 – temperatura początkowa
* h – krok procesu
* a – parametr równania różniczkowego
* u – moc klimatyzatora
* z – zakłócenia addytywne
Symulator automatycznie dobiera optymalne parametry na podstawie kryterium jakości, którym jest , gdzie e(t) = d – y(t), im niższa wartość tym lepszy regulator. Kryterium jakości posłuży nam jeszcze do porównywania regulatorów P, PI, PID.

Wartości jakie mogą przyjmować parametry członów regulatora to:
* Dla członu proporcjonalnego, parametr P – od 0 do 9 z krokiem 1
* Dla członu całkującego, parametr I – od 0 do 9 z krokiem 0.1
* Dla członu różniczkującego, parametr D – od 0 do 1 z krokiem 0.1
* Ograniczenia wprowadzone są po to, aby skrócić czas symulacji.

## Plan badań symulacyjnych

Dla każdej symulacji: T = 10, y0 = 15, h=0.01, a = -1/10, 10 ≥ u ≥ -10
Symulacje:
1. Stała temperatura zadana: d = 20, z = 0
2. Rosnąca temperatura zadana (1 stopień co 1 sekundę od d = 20), z = 0
3. Spadająca temperatura zadana (2 stopnie co 1 sekundę od d = 20), z = 0
4. Losowa temperatura zadana (od 15 do 25 zmieniająca się co 1 sekundę), z = 0
5. Stała temperatura zadana z zakłóceniami: d = 20, -5 ≤ z ≤ 5 
