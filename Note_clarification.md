## Résumé sujet

L’application de gestions de la clinique veterinaire devra gérer les données relatives aux **Patients**, **Espèces** traités par le cabinet, **Client**, **Personnel** (*Vétérinaire* ou *Assistant*), le stock de **Médicament** et le **Dossier Médicale** de chaque Patients contenant les informations suivantes : **Mesures** du *poids* et de la *taille*, **Procédure**, **Résultats** **Anayse**, **Observation** suite à une consultation et le **Traitement** préscrit par le Vétérinaire.

## Liste des objets gérés par la BDD et leurs contraintes

1. **Patients** (#id : int,  nom : string, date de naissance : int[4] , numéro puce : int, numéro passeport : int) 
    - Le patient est d’une **Espèce**  ( * 1)
    - Le patient a un ou plusieurs propriétaires qui est/sont **Client**  (1..n  1..n)
        - avec une date de début et une date de fin
    - Le patient possède un **DossierMedical** (1 1)
    - Le patient est suivi par un ou plusieurs vétérinaires qui font parti du **Personnel** ( * 1..n)
        - avec une date de début de suivi et une date de fin
    
    <aside>
    💡 O*n pourra vérifier que dateFin > dateDebut, avec dateFin pouvant être NULL.
    On devra faire une contrainte telle que les suivis se font seulement par du personnel dont le poste est vétérinaire.
    Date : int de 4 caractères pour représenter uniquement l’année, peut être NULLE.
    Numéros possiblement NULL*
    
    </aside>
    
    ---
    
2. **Espèce** (#nom  string)
    
    *Parmi (félins, canidés, reptiles, rongeurs, oiseaux, autres)*
    
    A*utres est dispo uniquement pour le patient et pas pour la spécialité du veto*
    
    ---
    
3. **Individu** (#nom :string , #prénom : string , date de naissance : date, adresse : string, telephone : int[10])
    
    <aside>
    💡 On remarque que les clients et le personnel ont presque les mêmes attributs, on décide donc de les faire hériter (héritage exclusif) d’une classe mère qu’on nomme **Individu**.
    
    </aside>
    
    - Classes filles :
        - **Client** ( )
        - **Personnel** (poste enum {vétérinaire ,assistant} )
            - spécialité parmi les **Espèce** * 1
            
        
        ---
        
    
    <aside>
    💡 *On peut encore améliorer le modèle en créant un type adresse(*num_rue : integer, nom_rue : varchar, ville : varchar*) pour pouvoir être certain des types insérés par l’utilisateur et ne pas avoir de case multivaluée et être en 1ère forme normale.*
    
    On pourra vérifier que le client n’est pas un personnel soignant grace à son adresse qui est unique.
    
     
    
    </aside>
    
4. **DossierMedical** ()
    - est composé de plusieurs **EntreeSaisie**
        - Pour chaque entrée, on veut garder la date et l’heure
        - On ajoute un numéro pour connaitre le nombre de fois qu’on saisit cette entrée
        
    
    ---
    
5. **EntreeSaisie**( #num int, date date, heure hour)
    
    <aside>
    💡 Les mesure de taille/poids, les traitements, les résultats d’analyse, les observations et les
    
    procédures sont des entrées de saisie. Ce sont des classes filles, on a donc :
    
    </aside>
    
    1. **Mesure** (poids int, taille int)
        
        <aside>
        💡 avec *(poids, taille) NOT NULL : le couple n’est pas null, au moins l’un des deux a été saisi ou les deux, avec la prescription du traitement réalisé seulement par un vétérinaire*
        
        </aside>
        
    2. **Procedure** (titre string, description text)
    3. **ResultatAnalyse** (resultat text)
    4. **Observation** ( description text)
        - faite par un membre du **Personnel** ( * 1)
    5. **Traitement** (dateDebut date, duree int)
        - Prescrit un ou plusieurs **Medicament** (*  1..n )
            - avec une quantité
        
    
    ---
    
6. **Médicament (#** nom de la molécule : string , description : txt)
    - n’est autorisé que pour certaines **Espèce  * ***

## Liste du personnel appelés à modifier et consulter les données

Seul les **Veterinaires** et les **Assistants** peuvent modifier et consulter les propriétés des classes : **Patients**, **Client**, **Mesure**, **Procedure**, **ResultatAnalyse**, **Observation.**

Les **Veterinaires** peuvent modifier alors que les **Assistants** peuvent seulement consulter les classe : **Espece**, **Traitement**, **Medicament**.

Seul les Veterinaires peuvent modifier et consulter la classe : **Personnel.**

## Liste des fonctions que les utilisateurs pourront utiliser

**Duree**(DateFin - DateDebut)

La méthode **Duree** peut seulement être utilisé dans la classe **Traitement** avec les propriétés *DateDebut* et *DateFin.*

- **{commentaire READ.ME}**
    
    Les classes DossierMedical et EntréeSaisie sont des classes utilisées pour faciliter la lecture de l’UML. Lors du passage au MLD, de par leurs cardinalitées, elles disparaitront. Les entrées de saisies (Mesure, Procedure, ResultatAnalyse et Traitement) auront chacunes un lien vers Patient.
