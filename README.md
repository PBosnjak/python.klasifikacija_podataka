Raspoznavanje uzoraka i strojno učenje: projektni zadatak
=========================================================

Petar Bošnjak, 1. godina diplomskog studija računarstva, smjer DRB


----------
Tema projektnog zadatka jest klasifikacija podataka analize testova krvi i tumorskih markera. Testovi su rađeni na skupini pacijenata sa dijagnosticiranim tumorom dojke, placebo skupini, te skupini pacijenata sa benignim tumorom. 

Cilj je ustanoviti može li se poboljšati dijagnoza tumora kombinirajući testove tumorskih markera Ca 15-3 i CEA sa rutinskim testovima krvi. 

Korišteni testovi i značenje njihovih kratica mogu se pronaći u dokumentu [Abbreviations.docx](https://gitlab.com/PBosnjak/RUSU_projekt/blob/master/Pisani_dio/Abbreviations.docx)


----------
Za klasifikator odabran je RandomForrest klasifikator zbog svoje mogućnosti određivanja značajnosti pojedinog ulaza u klasifikator (*feature importance*). To nam omogućuje izbacivanje pojedinog testa krvi i samim time smanjuje potrošnju vremena i resursa. 

Za evaluaciju modela korišteni su *accuracy*, *recall* i *precision* parametri.
Prvo smo *10-fold* cross-validacijom došli do optimalnog broja estimatora (drveća) u odabranom klasifikatoru, koristeći formulu 

> result = (recall[i] + accuracy[i] + precision[i]) / 3 za i = [10,300]


Odabirom najoptimalijeg broja estimatora, napravili smo *fit* na sve podatke te poredali ulaze s obzirom na njihovu značajnost. Daljnjim odabirom N značajki (N = [20,10,5,2]) napravili smo cross-validaciju za odabranih N značajki.
Rezultati su spremljeni u [Output.xlsx](https://gitlab.com/PBosnjak/RUSU_projekt/blob/master/Prezentacija/Output.xlsx)

U rezultatima se pod 

 - "Data" nalaze korišteni ulazi (*features*) u klasifikatoru, 
 - "Best Score" nalazi najbolji rezultat po kojemu smo odabrali broj estimatora u klasifikatoru,
 - "Accuracy" - parametar za "Best Score",
 - "Recall" - parametar za "Best Score",
 - "Precision" - parametar za "Best Score"

----------
U folderu [graphs](https://gitlab.com/PBosnjak/RUSU_projekt/tree/master/Prezentacija/graphs) možemo vidjeti grafički prikaz rezultata za *accuracy*, *recall* i *precision* parametre za svaki testirani broj estimatora i odabranih N značajnih ulaza.

![Primjer grafa za accuracy parametar za 10 najznačajnihi ulaza.](https://gitlab.com/PBosnjak/RUSU_projekt/raw/master/Prezentacija/graphs/10_accuracy.png)