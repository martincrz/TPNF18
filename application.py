from datetime import date
#!/usr/bin/python3

import psycopg2
import time


#creer la bdd si elle n'existe pas
#fontion qui permet de creer la base de donnees
def create_database():
    curseur.execute("CREATE TABLE Espece (nom VARCHAR PRIMARY KEY, CHECK (nom IN ('félin', 'canidé', 'reptile', 'rongeur', 'oiseau', 'autre')));")
    conn.commit()
    #ajout dans Espece des especes félin, canidé, reptile, rongeur, oiseau, autre
    curseur.execute("INSERT INTO Espece VALUES ('félin');")
    curseur.execute("INSERT INTO Espece VALUES ('canidé');")
    curseur.execute("INSERT INTO Espece VALUES ('reptile');")
    curseur.execute("INSERT INTO Espece VALUES ('rongeur');")
    curseur.execute("INSERT INTO Espece VALUES ('oiseau');")
    curseur.execute("INSERT INTO Espece VALUES ('autre');")
    conn.commit()
    #creation de la table Adresse
    curseur.execute("CREATE TABLE Adresse (id_adresse SERIAL PRIMARY KEY, num_rue INT, nom_rue VARCHAR, ville VARCHAR, UNIQUE (num_rue, nom_rue, ville));")
    conn.commit()
    #creation de la table Patient
    curseur.execute("CREATE TABLE Patient (id SERIAL PRIMARY KEY NOT NULL, nom VARCHAR NOT NULL, dateNaiss DATE NOT NULL, num_puce BIGINT UNIQUE, num_pass BIGINT UNIQUE, espece VARCHAR REFERENCES Espece(nom));")
    conn.commit()
    #creation de la table Procedure
    curseur.execute("CREATE TABLE Procedure (num SERIAL PRIMARY KEY, date DATE NOT NULL, heure TIME NOT NULL, patient INT REFERENCES Patient(id) NOT NULL, description TEXT, UNIQUE(date, heure, patient), CHECK(num>0));")
    conn.commit()
    #creation de la table Resultat analyse
    curseur.execute("CREATE TABLE Resultat_analyse (num SERIAL PRIMARY KEY,date DATE NOT NULL,heure TIME NOT NULL,patient INT REFERENCES Patient(id) NOT NULL,resultat TEXT NOT NULL);")
    conn.commit()
    #creation de la table Mesure
    curseur.execute("CREATE TABLE Mesure (num SERIAL PRIMARY KEY,date DATE NOT NULL,heure TIME NOT NULL,patient INT REFERENCES Patient(id) NOT NULL,taille INT,poids FLOAT,CHECK ( (taille IS NOT NULL) or (poids IS NOT NULL)));")
    conn.commit()
    #creation de la table Medicament
    curseur.execute("CREATE TABLE Medicament (nom_mol VARCHAR PRIMARY KEY, description TEXT);")
    conn.commit()
    #creation de la table Traitement
    curseur.execute("CREATE TABLE Traitement (num SERIAL PRIMARY KEY, date DATE NOT NULL, heure TIME NOT NULL, patient INT REFERENCES Patient(id) NOT NULL, dateDebut DATE NOT NULL, CHECK(dateDebut >= current_date));")
    conn.commit()
    #creation de la classe Autoriser
    curseur.execute("CREATE TABLE Autoriser (espece VARCHAR REFERENCES Espece(nom), medicament VARCHAR REFERENCES Medicament(nom_mol), PRIMARY KEY (espece, medicament));")
    conn.commit()
    #creation de la table Client
    curseur.execute("CREATE TABLE Client (id SERIAL PRIMARY KEY, nom VARCHAR NOT NULL, prenom VARCHAR NOT NULL, dateNaiss DATE NOT NULL, adresse INT REFERENCES Adresse(id) NOT NULL, numTel INT UNIQUE NOT NULL);")
    conn.commit()
    #creation de la table Personnel
    curseur.execute("CREATE TABLE Personnel (id SERIAL PRIMARY KEY, nom VARCHAR NOT NULL, prenom VARCHAR NOT NULL, dateNaiss DATE NOT NULL, adresse INT REFERENCES Adresse(id) NOT NULL, num_tel INT UNIQUE NOT NULL, poste VARCHAR NOT NULL, CHECK (poste IN ('veterinaire', 'assistant')));")
    conn.commit()
    #creation de la table Prescrire
    curseur.execute("CREATE TABLE Prescrire (medicament VARCHAR REFERENCES Medicament(nom_mol) NOT NULL, traitement INT REFERENCES Traitement(num), veterinaire INT REFERENCES Personnel(id) NOT NULL, quantite FLOAT, PRIMARY KEY (medicament, traitement));")
    conn.commit()
    #creation de la table Specialiser
    curseur.execute("CREATE TABLE Specialiser(personnel INT REFERENCES Personnel(id), espece VARCHAR REFERENCES Espece(nom), PRIMARY KEY (espece, personnel));")
    conn.commit()
    #creation de la table Observation
    curseur.execute("CREATE TABLE Observation (num SERIAL PRIMARY KEY, date DATE NOT NULL, heure TIME NOT NULL, description TEXT, personnel INT REFERENCES Personnel(id) NOT NULL, patient INT REFERENCES Patient(id) NOT NULL);")
    conn.commit()
    #creation de la table etre proprietaire
    curseur.execute("CREATE TABLE Etre_proprietaire (client INT REFERENCES Client(id) NOT NULL, patient INT REFERENCES Patient(id) NOT NULL, dateDebut DATE NOT NULL, dateFin DATE, CHECK (dateFin>dateDebut OR dateFin = NULL), PRIMARY KEY (client, patient));")
    conn.commit()
    #creation de la table suivre
    curseur.execute("CREATE TABLE suivre(patient INT REFERENCES Patient(id) NOT NULL, personnel INT REFERENCES Personnel(id) NOT NULL, debut DATE NOT NULL, fin DATE, PRIMARY KEY (patient, personnel), UNIQUE (patient, personnel, debut, fin), CHECK (fin>debut OR fin = NULL));")
    conn.commit()

def choixA1():
    #1. Insérer un membre du personnel
    print("1. Insérer un membre du personnel")
    #on demande a l'utilisateur de rentrer les informations du personnel
    nom = str(input("Nom : "))
    prenom = str(input("Prenom : "))
    dateNaiss = str(input("Date de naissance (aaaa-mm-jj) : "))

    #verifier type date, qu'elle est bien inférieur à la date actuelle


    print()
    num_rue = int(input("Numéro de rue : "))
    nom_rue = str(input("Nom de rue : "))
    ville = str(input("Ville : "))
    print()
    num_tel = int(input("Numéro de téléphone : "))
    poste = str(input("Poste : "))
    #on verifie que le poste est bien un poste de veterinaire ou d'assistant
    while poste != "veterinaire" and poste != "assistant":
        print("Incorrect (veterinaire ou assistant)")
        poste = str(input("Poste : "))
    #on verifie que le numero de telephone n'est pas deja dans la base de donnees
    try:
        curseur.execute("SELECT num_tel FROM Personnel WHERE num_tel = %s;" , (num_tel,))
        #s'il est déjà utilisé
        if curseur.fetchone() is not None:
            print("Ce numéro de téléphone est déjà utilisé")
            return


        #on verifie si le numero de rue et le nom de rue sont dans la base de donnees
        curseur.execute("SELECT id FROM Adresse WHERE num_rue = %s AND nom_rue = %s;" , (num_rue,nom_rue))

        #si cette adresse ne l'est pas, on l'ajoute
        if curseur.fetchone() is None:
            curseur.execute("INSERT INTO Adresse VALUES (DEFAULT, %s, %s, %s);" , (num_rue, nom_rue, ville))
            conn.commit()

        #on recupere l'id de l'adresse
        curseur.execute("SELECT id FROM Adresse WHERE num_rue = %s AND nom_rue = %s ;" , (num_rue,nom_rue) )
        id_adresse = curseur.fetchone()[0]

        #on insere le personnel dans la base de donnees
        #il faut trouver son identifiant (maximum + +1 des identifiants deja presents dans Client et Personnel)
        curseur.execute("SELECT MAX(id) FROM Client ;")
        id_max_client=curseur.fetchone()[0]
        curseur.execute("SELECT MAX(id) FROM Personnel ;")
        id_max_personnel=curseur.fetchone()[0]
        id_personnel = max(id_max_client,id_max_personnel) + 1

        curseur.execute("INSERT INTO Personnel VALUES (%s,%s,%s,%s,%s,%s,%s);", (id_personnel, nom, prenom, dateNaiss, id_adresse, num_tel, poste))
        conn.commit()
        print(f"{nom} {prenom} a bien été inséré en tant que nouveau membre du personnel\n\n")
    except psycopg2.Error as e:
        print("Error : %s" % e)



    print(f"Saisir la liste d'especes où {nom} {prenom} est spécialisé (saisir 'fin' pour quitter)")
    liste_espece = []
    while 'TRUE':
        espece = str(input("Saisir espece (félin, canidé, reptile, rongeur, oiseau, autre): "))
        #vérifier si possible
        if espece == 'fin':
            break
        if espece not in ('félin', 'canidé', 'reptile', 'rongeur', 'oiseau', 'autre'):
            print("Espece non correcte")
        else:
            liste_espece.append(espece)
    for e in liste_espece:
        try:
            curseur.execute("INSERT INTO Specialiser VALUES (%s,%s)", (id_personnel, e))
            conn.commit()
        except psycopg2.Error as erreur:
            print(erreur)

def choixA2():
    #2. Insérer un client
    print("2. Insérer un client")
    #on demande a l'utilisateur de rentrer les informations du client
    nom = str(input("Nom : "))
    prenom = str(input("Prenom : "))
    dateNaiss = str(input("Date de naissance (aaaa-mm-jj) : "))
    num_tel = int(input("Numéro de téléphone : "))
    print()
    num_rue = int(input("Numéro de rue : "))
    nom_rue = str(input("Nom de rue : "))
    ville = str(input("Ville : "))

    try :
        #on verifie que le numero de telephone n'est pas deja dans la base de donnees
        curseur.execute("SELECT numTel FROM Client WHERE numTel = %s;", (num_tel,))
        if curseur.fetchone() is not None:
            print("Ce numéro de téléphone est déjà utilisé")
            return
        #on verifie que le numero de rue et le nom de rue sont bien dans la base de donnees
        curseur.execute("SELECT id FROM Adresse WHERE num_rue = %s AND nom_rue = %s AND ville = %s;", (num_rue, nom_rue, ville))
        if curseur.fetchone() is None:
            curseur.execute("INSERT INTO Adresse (num_rue, nom_rue, ville) VALUES (%s, %s, %s);", (num_rue, nom_rue, ville))
            conn.commit()
        #on recupere l'id de l'adresse
        curseur.execute("SELECT id FROM Adresse WHERE num_rue = %s AND nom_rue = %s;", (num_rue, nom_rue))
        id_adresse = curseur.fetchone()[0]
        #on insere le client dans la base de donnees
        #chercher id_client max + 1 parmi les clients et les personnels
        curseur.execute("SELECT MAX(id) FROM Client ;")
        id_max_client=curseur.fetchone()[0]
        curseur.execute("SELECT MAX(id) FROM Personnel ;")
        id_max_personnel=curseur.fetchone()[0]
        id_client = max(id_max_client,id_max_personnel) + 1
        curseur.execute("INSERT INTO Client VALUES (%s, %s, %s, %s, %s, %s)" , (id_client, nom, prenom, dateNaiss, id_adresse, num_tel))
        conn.commit()
        print(f"{nom} {prenom} a bien été inséré en tant que nouveau client\n\n")
    except psycopg2.Error as e:
        print(e)

def choixA3():
    #3. Insérer une information de propriétaire pour un animal
    print("3. Insérer une information de propriétaire pour un animal")
    #on demande a l'utilisateur de rentrer les informations du proprietaire
    print("Information propriétaire- ")
    nom = str(input("   Nom : "))
    prenom = str(input("   Prenom : "))
    try:
        #verifie que le client existe
        curseur.execute("SELECT id FROM Client WHERE nom = %s AND prenom = %s;", (nom, prenom))
        if curseur.fetchone() is None:
            print("Ce client n'existe pas")
            return
        #on recupere l'id du client
        curseur.execute("SELECT id FROM Client WHERE nom = %s AND prenom = %s;", (nom, prenom))
        id_client = curseur.fetchone()[0]
        #on demande a l'utilisateur de rentrer les informations de l'animal
        print("Information animal-")
        nom_animal = str(input("   Nom de l'animal : "))
        dateNaiss = str(input("   Date de naissance (aaaa-mm-jj) : "))
        #verifie que l'animal existe dans la classe Patient
        curseur.execute("SELECT id FROM Patient WHERE nom = %s AND dateNaiss = %s;", (nom_animal, dateNaiss))
        if curseur.fetchone() is None:
            print("Cet animal n'existe pas")
            return
        #on recupere l'id de l'animal
        curseur.execute("SELECT id FROM Patient WHERE nom = %s AND dateNaiss = %s;", (nom_animal, dateNaiss))
        id_animal = curseur.fetchone()[0]
        #on insere le proprietaire dans la base de donnees
        dateDebut= str(input("Date de début (aaaa-mm-jj) : "))
        #logiquement, dateFin est null à l'insertion

        curseur.execute("INSERT INTO Etre_proprietaire VALUES(%s,%s,%s, NULL) ;", (id_client,id_animal, dateDebut) )
        conn.commit()
        print(f"{nom} {prenom} est maintenant proprietaire de {nom_animal} \n\n")
    except psycopg2.Error as e:
        print(e)

def choixA4():
    # 4. Insérer un animal
    #ajouter gestion erreur (try - except)
    print("4. Insérer un animal")
    #on demande a l'utilisateur de rentrer les informations de l'animal

    animal_nom = str(input("Nom : "))
    animal_dateNaiss = str(input("Date de naissance (aaaa-mm-jj) : "))

    question = input("L'animal a-t-il un numéro de puce ? ('o' ou 'n') - ")
    if question == 'o':
        num_puce = int(input("Numéro de puce :"))
    else:
        num_puce = None
    question = input("L'animal a-t-il un numéro de passeport ? ('o' ou 'n') - ")
    if question == 'o':
        num_pass = int(input("Numéro de passeport :"))
    else:
        num_pass = None
    espece = str(input("Espece : "))

    while espece not in ('félin', 'canidé', 'reptile', 'rongeur', 'oiseau', 'autre'):
        print("incorrect")
        espece = str(input("Espece : "))

    try:
        curseur.execute("SELECT id FROM Patient WHERE nom = %s AND dateNaiss = %s;", (animal_nom, animal_dateNaiss))

        if curseur.fetchone() is None:
            curseur.execute("INSERT INTO Patient VALUES (DEFAULT, %s,%s,%s,%s,%s);", (animal_nom, animal_dateNaiss, num_puce, num_pass, espece))
            conn.commit()
            print(f"{animal_nom} a bien été inséré en tant que nouveau patient\n\n")
        else :
            print("L'animal existe déjà")
            return
    except psycopg2.Error as e:
        print(e)


    # LUI AFFECTER UNE LISTE DE VETERINAIRES QUI LE SUIENT
    print("Saisir la liste des vétérinaires pour vont le suivre (saisir 'fin' pour quitter)")
    liste_veto = []
    while 'TRUE':
        nom_veto = str(input("Saisir nom veto : "))
        if nom_veto == 'fin':
            break
        prenom_veto = str(input("Saisir prenom veto : "))

        #verifie que le vétérinaire existe
        curseur.execute("SELECT id FROM Personnel WHERE nom = %s AND prenom = %s AND poste='veterinaire';", (nom_veto, prenom_veto))
        if curseur.fetchone() is None:
            print("Ce vétérinaire n'existe pas")
            break
        #on recupere l'id du vétérinaire
        curseur.execute("SELECT id FROM Personnel WHERE nom = %s AND prenom = %s AND poste='veterinaire';", (nom_veto, prenom_veto))
        id_veto = curseur.fetchone()[0]
        liste_veto.append(id_veto)


    #on recupere l'id de l'animal
    curseur.execute("SELECT id FROM Patient WHERE nom = %s AND dateNaiss = %s;", (animal_nom, animal_dateNaiss))
    id_animal = curseur.fetchone()[0]



    for veto in liste_veto:
        try:
            curseur.execute("INSERT INTO Suivre VALUES (%s, %s, current_date, NULL);", (id_animal, veto))
            conn.commit()
        except psycopg2.Error as erreur:
            print(erreur)
    print(f"{animal_nom} a été inséré, et rattaché à une liste de vétérinaires \n\n")

def choixA5():
    # 5. Insérer un médicament
    print("5. Insérer un médicament")
    #on demande a l'utilisateur de rentrer les informations du medicament
    nom_mol = input("Nom molécule : ")
    #on verifie que le medicament n'est pas deja dans la base de donnees
    curseur.execute("SELECT nom_mol FROM Medicament WHERE nom_mol = %s;", (nom_mol,))
    if curseur.fetchone() is not None:
        print("Ce médicament est déjà dans la base de données")
        return
    description = str(input("description : "))
    try:
        curseur.execute("INSERT INTO Medicament VALUES(%s, %s);", (nom_mol,description))
        conn.commit()
        print(f"{nom_mol} a bien été inséré en tant que nouveau medicament\n\n")
    except psycopg2.Error as e:
        print(e)

    # AJOUTER LES ESPECES AUTORISES A LE PRENDRE
    print("Saisir la liste d'especes autorisés pour ce médicament (saisir 'fin' pour quitter)")
    liste_espece = []
    while 'TRUE':
        espece = str(input("Saisir espece (félin, canidé, reptile, rongeur, oiseau, autre) : "))
        if espece == 'fin':
            break
        if espece not in ('félin', 'canidé', 'reptile', 'rongeur', 'oiseau', 'autre'):
            print("Espece non correcte")
        else :
            liste_espece.append(espece)

    for e in liste_espece:
        try:
            curseur.execute("INSERT INTO Autoriser VALUES (%s, %s)", (e,nom_mol))
            conn.commit()
        except psycopg2.Error as erreur:
            print(erreur)
    print("Les autorisations ont bien été saisi")

def choixA6():
    # 6. Insérer une entrée dans un dossier médical
    while 'TRUE':
        type = str(input("Type d'entrée (Mesure, Procedure, Traitement, Observation, Resultat analyse) : "))
        if (type != 'Mesure' and type != 'Procedure' and type != 'Traitement' and type != 'Observation' and type != "Resultat analyse"):
            print("incorrect")
            return
        else:
            break

    print()
    print("Donner les informations de l'animal en question")
    animal_nom = str(input("Nom : "))
    animal_dateNaiss = str(input("Date de naissance : "))


    #ajouter try/execpt
    curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;",(animal_nom, animal_dateNaiss))
    id_animal = curseur.fetchone()[0]
    #si cet animal n est pas dans la liste patient
    if id_animal is None:
        print("Cet animal n'est pas dans la liste patient, veuillez d'abord l'insérer\n\n")
        return
    curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;",(animal_nom, animal_dateNaiss))
    id_animal = curseur.fetchone()[0]

    curseur.execute("SELECT MAX(num) FROM Mesure ;")
    num_max_mesure = curseur.fetchone()[0]
    curseur.execute("SELECT MAX(num) FROM Traitement ;")
    num_max_traitement = curseur.fetchone()[0]
    curseur.execute("SELECT MAX(num) FROM Resultat_Analyse ;")
    num_max_Resultat_Analyse = curseur.fetchone()[0]
    curseur.execute("SELECT MAX(num) FROM procedure ;")
    num_max_procedure = curseur.fetchone()[0]
    num_saisi = max(num_max_mesure, num_max_traitement, num_max_Resultat_Analyse, num_max_procedure) + 1



    if type == 'Mesure':
        question = str(input("A-t-on saisi son poids ? ('o' ou 'n')"))
        if question == 'o':
            poids = float(input("Poids : "))
            question = str(input("A-t-on saisi sa taille ? ('o' ou 'n')"))
            if question == 'o':
                taille = int(input("Taille : "))
            else:
                taille = None
        else:
            poids = None
            taille = int(input("Taille : "))

        try:
            curseur.execute("INSERT INTO Mesure VALUES (%s, current_date, current_time, %s, %s, %s);", (num_saisi, id_animal, taille, poids))
            conn.commit()
        except Exception as e:
            print(e)

    elif type == 'Procedure':
        description = str(input("Saisir la description de la procédure : "))
        try:
            curseur.execute("INSERT INTO Procedure VALUES (%s, current_date, current_time,  %s, %s);", (num_saisi, id_animal, description))
            conn.commit()
        except Exception as e:
            print(e)

    elif type == 'Resultat analyse':
        resultat = str(input("Saisir le resultat de l'analyse : "))
        try:
            curseur.execute("INSERT INTO Resultat_Analyse VALUES (%s, current_date, current_time,  %s, %s);", (num_saisi, id_animal, resultat))
            conn.commit()
        except Exception as e:
            print(e)

    elif type == 'Traitement':
        try:
            dateDebut = str(input("Date de début (future): "))
            #si pas futur, va afficher l'erreur
            dateFin = str(input("Date de fin (future): "))

            nom_mol = str(input("Nom molécule prescrite : "))
            curseur.execute("SELECT nom_mol FROM Medicament WHERE nom_mol = %s;", (nom_mol,))
            if curseur.fetchone() is None:
                print("Ce médicament n'existe pas dans la base de données")
                return
            # il faut vérifier que cette molécule soit bien  autorisée pour l'espece de cet animal
            curseur.execute("SELECT espece FROM Patient WHERE nom=%s AND dateNaiss=%s;", (animal_nom, animal_dateNaiss))
            espece_animal = curseur.fetchone()[0]
            curseur.execute("SELECT espece FROM Autoriser WHERE medicament=%s;", (nom_mol,))
            liste_espece_autorisees = curseur.fetchone()[0]
            if espece_animal not in liste_espece_autorisees:
                print("Ce médicament n'est pas autorisé pour cette espèce d'animal\n\n")
                return

            quantite = int(input("Quantité prescrite : "))

            nom_personnel = str(input("Nom du vétérinaire qui a prescrit le traitement : "))
            #on peut aussi demander sa date de naissance

            curseur.execute("SELECT id FROM Personnel WHERE nom=%s;", (nom_personnel,))
            id_personnel = curseur.fetchone()[0]
            if not id_personnel:
                print("Ce personnel n'est pas dans la liste, veuillez d'abord l'insérer\n\n")
                return




            # il faut vérifier que le personnel soit bien un véto
            curseur.execute("SELECT poste FROM Personnel WHERE id=%s;", (id_personnel,))
            poste_personnel = curseur.fetchone()[0]
            if not poste_personnel == 'veterinaire':
                print("Ce personnel n'est pas un vétérinaire\n\n")
                return

            curseur.execute("INSERT INTO Traitement VALUES (%s, current_date, current_time, %s, %s, %s);",  (num_saisi, id_animal, dateDebut, dateFin))
            conn.commit()

            curseur.execute("INSERT INTO Prescrire VALUES (%s, %s, %s, %s);", (nom_mol, num_saisi, id_personnel, quantite))
            conn.commit()
        except Exception as e:
            print(e)

    elif type == 'Observation':
        nom_personnel = str(input("Saisir le NOM du personnel qui réalise l'observation : "))
        prenom_personnel = str(input("Saisir le PRENOM du personnel qui réalise l'observation : "))
        curseur.execute("SELECT id FROM Personnel WHERE nom=%s;", (nom_personnel,))
        id_personnel = curseur.fetchone()[0]
        if not id_personnel:
            print("Ce personnel n'est pas dans la liste, veuillez d'abord l'insérer\n\n")
            return
        description = str(input("Saisir la description : "))
        try:
            curseur.execute("INSERT INTO Observation VALUES (%s, current_date, current_time, %s, %s, %s);", (num_saisi, description, id_personnel, id_animal))
            conn.commit()
        except Exception as e:
            print(e)

    else:
        print("Sortie sous-menu")
        return

def choixB1():
    #1. Lister les quantités de médicaments consommés pour une période donnée.
    dateDebut = str(input("Date de début : "))
    dateDebut = date(int(dateDebut[:4]), int(dateDebut[5:7]), int(dateDebut[8:]))
    dateFin = str(input("Date de fin : "))
    dateFin = date(int(dateFin[:4]), int(dateFin[5:7]), int(dateFin[8:]))

    try:
        curseur.execute("SELECT medicament, quantite, datedebut, datefin FROM Prescrire AS P JOIN TRAITEMENT AS T ON P.traitement=T.num WHERE (%s<datedebut AND ((datefin BETWEEN %s AND %s) OR (datefin IS NULL) OR (datefin>= %s))) OR (datedebut BETWEEN %s AND %s);  ", (dateDebut, dateDebut, dateFin,dateFin, dateDebut,dateFin))
        res = curseur.fetchall()
        if res is None :
            print("Aucun Traitement dans cette periode")
            return
        # affichage

        print(f"Du {dateDebut} à {dateFin}, voici les quantités de médicaments consommés :\n")

        for raw in res:
            debut_periode = dateDebut
            fin_periode = dateFin
            if dateDebut < raw[2] :
               debut_periode = raw[2]
            if dateFin > raw[3] :
               fin_periode = raw[3]
            quantite_prescrite = raw[1] * (fin_periode - debut_periode ).days
            print(f"{raw[0]} :\n   {quantite_prescrite} g")

        time.sleep(5)

    except Exception as e:
        print(e)

def choixB2():
    #2. Lister le nombre de traitements prescrits au cours d'une période donnée.
    dateDebut = str(input("Date de début : "))
    dateFin = str(input("Date de fin : "))
    try:
        curseur.execute("SELECT COUNT(*) FROM Traitement AS T WHERE (%s<datedebut AND ((datefin BETWEEN %s AND %s) OR (datefin IS NULL) OR (datefin>= %s))) OR (datedebut BETWEEN %s AND %s);", (dateDebut, dateDebut, dateFin,dateFin, dateDebut,dateFin))

        # affichage
        res = curseur.fetchall()[0]
        print(f"Nombre de traitements prescrits durant cette période : {res[0]}")
        time.sleep(3)
    except Exception as e:
        print(e)

def choixB3():
    #3. Lister les procédures effectuées sur un animal donné, avec et triées par date.
    nom_animal = str(input("Nom de l'animal : "))
    dateNaiss = str(input("Date de naissance de l'animal : "))
    try:
        #trouver id de l'animal
        curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        id_animal = curseur.fetchone()[0]
        if id_animal is None:
            print("Cet animal n'est pas dans la liste, veuillez d'abord l'insérer\n\n")
            return

        curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        id_animal = curseur.fetchone()[0]



        curseur.execute("SELECT date, heure, description FROM Procedure WHERE patient=%s ORDER BY date;", (id_animal,))
        # affichage
        res = curseur.fetchall()
        print(f"Procedures effectuées sur {nom_animal}\n")
        for raw in res:
            print(f"Le {raw[0]} à {raw[1]} : {raw[2]},")
        time.sleep(3)
    except psycopg2.Error as e:
        print(e)

def choixB4():
    #4. Compter le nombre d'animaux traités groupés par espèce. #on suppose animaux traités = animaux qui sont/étaient clients
    try:
        curseur.execute("SELECT espece, COUNT(id) FROM PATIENT GROUP BY espece ORDER BY count DESC;;")
        # affichage
        res = curseur.fetchall()
        for raw in res:
            print(f"{raw[0]} : {raw[1]}")

        print("\n\nSi la question refere seulement aux animaux qui ont déjà subi un traitement : \n")
        curseur.execute("SELECT espece, count(espece) FROM PATIENT WHERE id IN (SELECT DISTINCT patient from traitement) GROUP BY espece ORDER BY count desc;")
        res = curseur.fetchall()
        for raw in res:
            print(f"{raw[0]} : {raw[1]}")

        time.sleep(5)

    except Exception as e:
        print(e)

def choixB5():
    # 5. Lister les animaux ayant appartenus à un client donné, triés par date d'adoption, avec le nom
    #et prénom du client, et les informations d'identification de l'animal, sa date de naissance et
    #son espèce.

    nom_client = str(input("Nom du client : "))
    prenom_client = str(input("Prénom du client : "))
    try:
        #verifie que le client existe

        curseur.execute("SELECT id FROM Client WHERE nom = %s AND prenom = %s;", (nom_client, prenom_client))

        if curseur.fetchone() is None:
            print("Ce client n'existe pas")
            return

        curseur.execute("SELECT C.nom, C.prenom, EP.datedebut, P.nom,  P.datenaiss, P.num_puce, P.num_pass, P.espece FROM PATIENT AS P JOIN ETRE_PROPRIETAIRE AS EP ON P.id=EP.PATIENT INNER JOIN CLIENT AS C ON C.id=EP.CLIENT WHERE C.nom=%s and C.prenom=%s ORDER BY EP.datedebut;", (nom_client, prenom_client))
        # affichage
        res = curseur.fetchall()
        print(f"\n{prenom_client} {nom_client} a été /est le propriétaire de : ")
        for raw in res:
            print(f"\n{raw[3]} \n     Espece : {raw[7]}\n     Né le : {raw[4]}\n     Adopté le : {raw[2]}\n     Puce : {raw[5]}\n     Passeport : {raw[6]}")
            time.sleep(5)
    except psycopg2.Error as e:
        print(e)

def choixB6():
    #6. Même requête, pour les animaux appartenant actuellement au client.
    nom_client = str(input("Nom du client : "))
    prenom_client = str(input("Prénom du client : "))
    try:
        curseur.execute("SELECT C.nom, C.prenom, EP.datedebut, P.nom, P.datenaiss, P.num_puce, P.num_pass, P.espece FROM PATIENT AS P JOIN ETRE_PROPRIETAIRE AS EP ON P.id=EP.PATIENT INNER JOIN CLIENT AS C ON C.id=EP.CLIENT WHERE C.nom=%s AND C.prenom=%s AND EP.datefin IS NULL ORDER BY EP.datedebut", (nom_client, prenom_client))
        # affichage
        res = curseur.fetchall()
        for raw in res:
            print(f"\n{raw[3]} \n     Espece : {raw[7]}\n     Né le : {raw[4]}\n     Adopté le : {raw[2]}\n     Puce : {raw[5]}\n     Passeport : {raw[6]}")
            time.sleep(5)
    except Exception as e:
        print(e)

def choixB7():
    #7. Même requête, pour les animaux ayant appartenu mais n'appartenant plus au client.
    nom_client = str(input("Nom du client : "))
    prenom_client = str(input("Prénom du client : "))
    try:
        curseur.execute("SELECT C.nom, C.prenom, EP.datedebut, P.nom, P.datenaiss, P.num_puce, P.num_pass, P.espece, EP.datefin FROM PATIENT AS P JOIN ETRE_PROPRIETAIRE AS EP ON P.id=EP.PATIENT INNER JOIN CLIENT AS C ON C.id=EP.CLIENT WHERE C.nom=%s AND C.prenom=%s AND EP.datefin<=current_date ORDER BY EP.datedebut", (nom_client, prenom_client))
        # affichage
        res = curseur.fetchall()
        if res is None:
            print("Aucun animal n'a été appartenu par ce client et ne lui appartient plus ")
        for raw in res:
            print(f"\n{raw[3]} \n     Espece : {raw[7]}\n     Né le : {raw[4]}\n     Adopté le : {raw[2]}\n     Fin le : {raw[8]}\n     Puce : {raw[5]}\n     Passeport : {raw[6]}")
            time.sleep(5)
    except Exception as e:
        print(e)

def choixB8():
    # 8.Lister l'évolution de croissance taille et poids d'un animal donné, par ordre chronologique.
    nom_animal = str(input("Nom de l'animal : "))
    dateNaiss = str(input("Date de naissance de l'animal : "))
    try:
        #trouver id de l'animal
        curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        if curseur.fetchone() is None:
            print("Cet animal n'est pas dans la liste, veuillez d'abord l'insérer\n\n")
            return

        curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        id_animal = curseur.fetchone()[0]

        curseur.execute("SELECT id, nom, M.taille, M.poids FROM PATIENT JOIN MESURE AS M ON M.PATIENT=id WHERE nom=%s AND dateNaiss=%s ORDER BY M.date;", (nom_animal,dateNaiss))
        # affichage
        res = curseur.fetchall()
        animal=""
        print("Animal | Taille | Poids \n")
        for raw in res:
            if animal!=raw[1]:
                print(f"{raw[1]} : \n           {raw[2]}     {raw[3]}")
            else :
                print(f"           {raw[2]}     {raw[3]}")
            animal = raw[1]
        time.sleep(3)

    except psycopg2.Error as e:
        print(e)

def choixB9():
    # 9. Lister les traitements subis par un animal donné avec leurs dates, triés chronologiquement, sans plus de détails.
    nom_animal = str(input("Nom de l'animal : "))
    dateNaiss = str(input("Date de naissance de l'animal : "))
    try:
        #trouver id de l'animal
        curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        if curseur.fetchone() is None:
            print("Cet animal n'est pas dans la liste, veuillez d'abord l'insérer\n\n")
            time.sleep(2)
            return

        curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        id_animal = curseur.fetchone()[0]

        curseur.execute("SELECT num, datedebut FROM Traitement t, Patient p WHERE p.id =%s ORDER BY datedebut;",(id_animal,))
        # affichage
        res = curseur.fetchall()
        for raw in res:
            print(f"Traitement n°{raw[0]} daté du {raw[1]}")
        time.sleep(3)
    except psycopg2.Error as e:
        print(e)

def choixB10():
    #10. Lister les traitements en cours pour un animal donné, avec leurs dates, avec le détail des prescriptions (médicaments et quantités par jour).
    nom_animal = str(input("Nom de l'animal : "))
    dateNaiss = str(input("Date de naissance de l'animal : "))
    try:
        #trouver id de l'animal
        curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        if curseur.fetchone() is None:
            print("Cet animal n'est pas dans la liste, veuillez d'abord l'insérer\n\n")
            time.sleep(2)
            return

        curseur.execute("SELECT id FROM Patient WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        id_animal = curseur.fetchone()[0]

        curseur.execute("SELECT datedebut, datefin, medicament, quantite FROM Traitement t INNER JOIN Prescrire p ON p.traitement=t.num WHERE patient=%s AND (datefin>=current_date OR datefin IS NULL) ORDER BY datedebut;" , (id_animal,))
        print("test")
        # affichage
        res = curseur.fetchall()
        print(f"{nom_animal}")
        for raw in res:
            if raw[1] is None:
                print(f"Doit prendre du {raw[2]}, {raw[3]}g/j, tous les jours depuis le {raw[0]}")
            else :
                print(f"Doit prendre du {raw[2]}, {raw[3]}g/j, depuis le {raw[0]} jusqu'au {raw[1]}")
        time.sleep(3)
    except psycopg2.Error as e:
        print(e)

def choixB11():
    # 11. Lister les membres de personnel spécialisés dans les reptiles, avec leur poste et toutes leurs informations.
    try:

        curseur.execute("SELECT DISTINCT nom, prenom, datenaiss, num_tel, poste, num_rue, nom_rue, ville FROM Personnel INNER JOIN Specialiser ON Personnel.id=Specialiser.personnel INNER JOIN Adresse ON Adresse.id = Personnel.adresse WHERE espece='reptile';")
        # affichage
        res = curseur.fetchall()
        print("nom | prenom | datenaiss | num_tel | poste | num_rue | nom_rue | ville \n")
        for raw in res:
            print(raw[0], raw[1], raw[2], raw[3], raw[4], raw[5], raw[6], raw[7])
        time.sleep(3)
    except Exception as e:
        print(e)

def choixB12():
    # 12. Afficher la liste des animaux ayant été suivis par un vétérinaire donné au cours du dernier mois.
    try:
        nom = str(input("Nom veto: "))
        prenom = str(input("Prenom veto : "))

        curseur.execute("SELECT id FROM Personnel WHERE nom=%s AND prenom=%s;", (nom,prenom))

        if curseur.fetchone() is None:
            print("Ce personnel n'est pas dans la liste, veuillez d'abord l'insérer\n\n")
            time.sleep(2)
            return

        curseur.execute("SELECT id FROM Personnel WHERE nom=%s AND prenom=%s;", (nom,prenom))
        id_personnel = curseur.fetchone()[0]
        # il faut vérifier que le personnel soit bien un véto
        curseur.execute("SELECT poste FROM Personnel WHERE id=%s;", (id_personnel,))
        poste_personnel = curseur.fetchone()[0]
        if  poste_personnel != 'veterinaire':
            print("Ce personnel n'est pas un vétérinaire\n\n")
            time.sleep(2)
            return

        id_veterinaire=id_personnel


        curseur.execute("SELECT DISTINCT nom FROM Patient INNER JOIN Suivre ON Suivre.patient=Patient.id WHERE Suivre.personnel=%s AND (Suivre.fin IS NULL OR (Suivre.fin>=(current_date-30) AND Suivre.fin <= current_date)) ;", (id_veterinaire,))

        # affichage
        res = curseur.fetchall()
        print(f"Voici la liste des animaux suivi par {nom} {prenom} durant au moins le dernier mois")
        for raw in res:
            print(raw[0])
        time.sleep(3)
    except psycopg2.Error as e:
        print(e)

def choixB13():
    # 13. Afficher la liste des vétérinaires ayant suivi un animal donné, avec et triés par leur date de suivi le plus récent.");
    nom_animal = str(input("Nom animal : "))
    dateNaiss = str(input("Date de naissance de l'animal : "))
    try:
        # trouver id
        curseur.execute("SELECT id FROM PATIENT WHERE nom=%s AND dateNaiss=%s;", (nom_animal,dateNaiss))
        id_animal = curseur.fetchone()[0]
        if id_animal is None:
            print("Cet animal n'est pas dans la liste, veuillez d'abord l'insérer\n\n")
            time.sleep(2)
            return



        curseur.execute("SELECT nom, prenom FROM Personnel p INNER JOIN Suivre s ON s.personnel = p.id WHERE s.patient = %s ORDER BY s.debut DESC; ", (id_animal,))
        # affichage
        res = curseur.fetchall()
        for raw in res:
            print(raw[0], raw[1])
        time.sleep(3)
    except psycopg2.Error as e:
        print(e)

#fonction main
def main():


    while 'TRUE':
        print("\n\n* * * * * * * * * * * MENU * * * * * * * * * * *\n")
        print("1. Operation d'insertion")
        print("2. Operation de sélection")
        print()
        sous_menu = int(input("Choix : "))
        print()
        while sous_menu == 1:
            print("\n\n* * * * * * * * * * * MENU INSERTION * * * * * * * * * * *\n")
            print(
                "1. Insérer un membre du personnel \n2. Insérer un client \n3. Insérer une information de propriétaire pour un animal \n4. Insérer un animal \n5. Insérer un médicament \n6. Insérer une entrée dans un dossier médical");
            print()
            choix = int(input("Choix : "))
            print()

            if choix == 1:
                choixA1()

            elif choix == 2:
                choixA2()

            elif choix == 3:
                choixA3()

            elif choix == 4:
                choixA4()

            elif choix == 5:
                choixA5()

            elif choix == 6:
                choixA6()

            else:
                print("Choix invalide")
                break

        while sous_menu == 2:
            print("\n\n* * * * * * * * * * * MENU SELECTION * * * * * * * * * * *\n")
            print("1. Lister les quantités de médicaments consommés pour une période donnée.")
            print("2. Lister le nombre de traitements prescrits au cours d'une période donnée.")
            print("3. Lister les procédures effectuées sur un animal donné, avec et triées par date. ")
            print("4. Compter le nombre d'animaux traités groupés par espèce.")
            print("5. Lister les animaux ayant appartenus à un client donné, triés par date d'adoption, avec le nom et prénom du client, et les informations d'identification de l'animal, sa date de naissance et son espèce.")
            print("6. Même requête, pour les animaux appartenant actuellement au client.")
            print("7. Même requête, pour les animaux ayant appartenu mais n'appartenant plus au client.")
            print("8. Lister l'évolution de croissance taille et poids d'un animal donné, par ordre chronologique.")
            print("9. Lister les traitements subis par un animal donné avec leurs dates, triés chronologiquement, sans plus de détails. ")
            print("10. Lister les traitements en cours pour un animal donné, avec leurs dates, avec le détail des prescriptions (médicaments et quantités par jour). ")
            print("11. Lister les membres de personnel spécialisés dans les reptiles, avec leur poste et toutes leurs informations.")
            print("12. Afficher la liste des animaux ayant été suivis par un vétérinaire donné au cours du dernier mois. ")
            print("13. Afficher la liste des vétérinaires ayant suivi un animal donné, avec et triés par leur date de suivi le plus récent.")
            print()
            choix = int(input("Choix : "))
            print()

            if choix == 1:
                choixB1()

            elif choix == 2:
                choixB2()

            elif choix == 3:
                choixB3()

            elif choix == 4:
                choixB4()

            elif choix == 5:
                choixB5()

            elif choix == 6:
                choixB6()

            elif choix == 7:
                choixB7()

            elif choix == 8:
                choixB8()

            elif choix == 9:
                choixB9()

            elif choix == 10:
                choixB10()

            elif choix == 11:
                choixB11()

            elif choix == 12:
                choixB12()

            elif choix == 13:
                choixB13()

            else:
                print("Choix invalide")
                break

#execution main
if __name__ == "__main__":
    try:
        HOST = "tuxa.sme.utc"
        USER = "nf18a030"
        PASSWORD = "rxpg5LER"
        DATABASE = "dbnf18a030"
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
        curseur = conn.cursor()
        main()
    except BaseException as e:
        print("Error: %s" % e)
        exit(1)
