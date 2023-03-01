# TPNF18
NF18 - Conception d'une BDD relationnel pour une agence de vétérinaire

## Name
VetoGestion

## Description
L'objectif est de réaliser une application de gestion pour une clinique vétérinaire que l'on nommera VetoGestion. L'administrateur de la clinique souhaite pouvoir gérer ses patients (animaux), ses clients, son personnel soignant ainsi que les médicaments administrés. Les clients et les personnels ont tous des noms, prénoms, date de naissance, une adresse et un numéro de téléphone. Les personnels ont en plus un poste (vétérinaire ou assistant) et une spécialité : les espèces animales qu'ils savent le mieux traiter. La clinique se spécialise dans le traitement d'animaux domestiques de petites et moyennes tailles, ils peuvent être des félins, des canidés, des reptiles, des rongeurs, ou des oiseaux. Exceptionnellement, elle peut traiter des animaux qui ne figurent pas parmi ces catégories et les regroupe dans une classe « autres ».
Pour chaque animal traité, la clinique souhaite garder son nom, son espèce, sa date de naissance (qui peut être juste une année, ou inconnue), le numéro de sa puce d'identification (s'il en a), son numéro de passeport (s'il en a), la liste de ses propriétaires et la période durant laquelle l'animal était avec eux, ainsi que la liste des vétérinaires qui l'ont suivi et quand est-ce qu'ils l'ont fait. Il faut noter que le personnel de la clinique ne doit pas avoir d'animaux de compagnie traités dans la clinique.
La clinique souhaite aussi garder le dossier médical de ses patients. Un dossier médical contient plusieurs entrées de différents types :

Une mesure de sa taille ou de son poids.
Un traitement prescrit avec la date de début, la durée, le nom et la quantité à prendre par jour pour chaque médicament prescrit (on peut prescrire plusieurs molécules dans un traitement). Seul un vétérinaire peut prescrire un traitement.
Des résultats d'analyses (sous forme de lien vers un document électronique)
Une observation générale faite lors d'une consultation et qui l'a faite.
Une procédure réalisée sur le patient avec sa description.

Pour chaque entrée, on veut garder la date et l'heure auxquelles elle a été saisie.
Enfin, les médicaments sont identifiés par le nom de la molécule et sont accompagnés de quelques lignes de texte décrivant leurs effets. Un médicament n'est autorisé que pour certaines espèces.

## Installation
Pour que notre application fonctionne, il faudrait installer :

python3
postgreSQL


## Usage
Le gestionnaire de la clinique veut pouvoir ajouter et mettre à jour la liste des personnels, des clients, des animaux traités et les médicaments utilisés. Il doit aussi pouvoir obtenir facilement des rapports d'activité et des informations statistiques, comme les quantités de médicaments consommés, le nombre de traitement ou de procédure effectuées dans la clinique, ou encore des statistiques sur les espèces d'animaux traités.

## Authors and acknowledgment
CREUZE Martin, MOUAKHAR Mohamed Aziz, ROYER Mathis, VOLTIGEUR Lilian

## Commentaires
Les classes DossierMedical et EntréeSaisie sont des classes utilisées pour faciliter la lecture de l’UML. Lors du passage au MLD, de par leurs cardinalitées, elles disparaitront. Les entrées de saisies (Mesure, Procedure, ResultatAnalyse et Traitement) auront chacunes un lien vers Patient.
