# BVGly

The goal of this project is to bring access to bvg/vbb connection information
to python, to the cli and maybe more.

## fahrinfo.bvg.de

https://fahrinfo.bvg.de/Fahrinfo/bin/query.bin/dox?protocol=https:&


## Data

http://berlin.appsandthecity.net/daten/
https://daten.berlin.de/datensaetze/vbb-fahrplan-2013
https://github.com/mphasize/vbb-hafas-docs
https://pypi.python.org/pypi/vbbvg/0.0.1
https://github.com/deeplook/vbbvg/blob/master/vbbvg/vbbvg.py


## Example

Query available connections from friedrichstr. to krumme lanke in 5minutes.

```
fahrinfo.py 's friedrichst' 'u krumme lanke' 5m
--------------------------------------------------------------------------------
S+U Friedrichstr. Bhf (Berlin) ab 19:22 Gl. 3 pünktlich RE2 Ri. Wismar, Bahnhof Alternative Abfahrten: RB14 ab 19:33, RE1 ab 19:37, RE1 ab 20:07, RE7 ab 20:11, RE2 ab 20:22 an 19:30 Gl. 3 pünktlich S+U Zoologischer Garten Bhf (Berlin)
ab 19:37 pünktlich U9 Ri. S+U Rathaus Steglitz (!) alle 5 - 10 Minuten an 19:40 pünktlich U Spichernstr. (Berlin)
ab 19:44 U3 Ri. U Krumme Lanke (Berlin) Alternative Abfahrten: U3 ab 19:49, U3 ab 19:54, U3 ab 19:59, U3 ab 20:11, U3 ab 20:21 an 20:03 U Krumme Lanke (Berlin)
--------------------------------------------------------------------------------
S+U Friedrichstr. Bhf (Berlin) ab 19:23 Gl. 11 ca. +1 Min. S25 Ri. S Teltow Stadt Alternative Abfahrten: S1 ab 19:26, S2 ab 19:28, S1 ab 19:36, S2 ab 19:38, S25 ab 19:43 an 19:26 Gl. 11 ca. +1 Min. S+U Potsdamer Platz Bhf (Berlin)
5 Min. Fußweg S+U Potsdamer Platz (Bln) [U2]
ab 19:31 pünktlich U2 Ri. U Ruhleben (Berlin) (!) alle 5 Minuten an 19:39 pünktlich U Wittenbergplatz (Berlin)
ab 19:41 U3 Ri. U Krumme Lanke (Berlin) Alternative Abfahrten: U3 ab 19:46, U3 ab 19:51, U3 ab 19:56, U3 ab 20:08, U3 ab 20:18 an 20:03 U Krumme Lanke (Berlin)
--------------------------------------------------------------------------------
S+U Friedrichstr. Bhf (Berlin) ab 19:26 Gl. 11 pünktlich S1 Ri. S Wannsee Bhf (Berlin) Alternative Abfahrten: S1 ab 19:36, S1 ab 19:46, S1 ab 19:56, S1 ab 20:06, S1 ab 20:16 an 19:55 Gl. 1 pünktlich S Mexikoplatz (Berlin)
ab 20:05 Bus 118 Ri. Rathaus Zehlendorf Alternative Abfahrten: Bus 622 ab 20:13, Bus 118 ab 20:23, Bus 622 ab 20:36, Bus 118 ab 20:43, Bus 118 ab 21:03 an 20:07 U Krumme Lanke (Berlin)
--------------------------------------------------------------------------------
S+U Friedrichstr. Bhf (Berlin) ab 19:28 Gl. 11 pünktlich S2 Ri. S Lichtenrade (Berlin) Alternative Abfahrten: S1 ab 19:36, S2 ab 19:38, S25 ab 19:43, S1 ab 19:46, S2 ab 19:48 an 19:31 Gl. 11 pünktlich S+U Potsdamer Platz Bhf (Berlin)
5 Min. Fußweg S+U Potsdamer Platz (Bln) [U2]
ab 19:36 pünktlich U2 Ri. U Theodor-Heuss-Platz (Berlin) (!) alle 5 Minuten an 19:44 pünktlich U Wittenbergplatz (Berlin)
ab 19:46 U3 Ri. U Krumme Lanke (Berlin) Alternative Abfahrten: U3 ab 19:51, U3 ab 19:56, U3 ab 20:08, U3 ab 20:18, U3 ab 20:28 an 20:08 U Krumme Lanke (Berlin)
```
