CREATE TABLE Espece
(nom VARCHAR PRIMARY KEY,
CHECK (nom IN ('félin', 'canidé', 'reptile', 'rongeur', 'oiseau', 'autre'))
);
INSERT INTO Espece VALUES('félin');
INSERT INTO Espece VALUES('canidé');
INSERT INTO Espece VALUES('reptile');
INSERT INTO Espece VALUES('rongeur');
INSERT INTO Espece VALUES('oiseau');
INSERT INTO Espece VALUES('autre');

CREATE TABLE Adresse (
id SERIAL PRIMARY KEY,
num_rue INT,
nom_rue VARCHAR,
ville VARCHAR,
UNIQUE (num_rue, nom_rue, ville)
);
INSERT INTO Adresse VALUES (DEFAULT, 2, 'Rue Roger Couttolenc', 'Compiègne');
INSERT INTO Adresse VALUES(DEFAULT, 15,'Rue Napoleon', 'Paris');

CREATE TABLE Patient
(id SERIAL PRIMARY KEY NOT NULL,
nom VARCHAR NOT NULL,
dateNaiss DATE NOT NULL,
num_puce BIGINT UNIQUE,
num_pass BIGINT UNIQUE,
espece VARCHAR REFERENCES Espece(nom)
);


INSERT INTO Patient VALUES (DEFAULT, 'Garfield', '2007-11-20', NULL, 486846, 'félin');
INSERT INTO Patient VALUES (DEFAULT, 'Tigrou', '2015-03-11', NULL, NULL, 'oiseau');

CREATE TABLE Procedure (
num SERIAL PRIMARY KEY,
date DATE NOT NULL,
heure TIME NOT NULL,
patient INT REFERENCES Patient(id) NOT NULL,
description TEXT,
UNIQUE(date, heure, patient),
CHECK(num>0)
);

INSERT INTO Procedure VALUES (DEFAULT, '2022-11-09', '12:24:12', 1, 'Procedure effectue sur Rex pour prevenir d une tumeure');
INSERT INTO Procedure VALUES(DEFAULT, current_date, current_time, 2, 'procedure de verification mensuelle');

CREATE TABLE Resultat_analyse (
num SERIAL PRIMARY KEY,
date DATE NOT NULL,
heure TIME NOT NULL,
patient INT REFERENCES Patient(id) NOT NULL,
resultat TEXT NOT NULL);

INSERT INTO Resultat_analyse VALUES(DEFAULT, current_date, current_time, 1, 'positif a la rage');

CREATE TABLE Mesure (
num SERIAL PRIMARY KEY,
date DATE NOT NULL,
heure TIME NOT NULL,
patient INT REFERENCES Patient(id) NOT NULL,
taille INT,
poids FLOAT,
CHECK ( (taille IS NOT NULL) or (poids IS NOT NULL))
);

INSERT INTO Mesure VALUES (DEFAULT, current_date, current_time, 1, NULL, 24);

CREATE TABLE Medicament (
nom_mol VARCHAR PRIMARY KEY,
description TEXT);
INSERT INTO Medicament VALUES('Doliprane', 'contre la fievre et toux');

CREATE TABLE Traitement (
num SERIAL PRIMARY KEY,
date DATE NOT NULL,
heure TIME NOT NULL,
patient INT REFERENCES Patient(id) NOT NULL,
dateDebut DATE NOT NULL,
CHECK(dateDebut >= current_date));

INSERT INTO Traitement VALUES (DEFAULT, current_date, current_time, 1, '2022-12-24');

CREATE TABLE Autoriser (
espece VARCHAR REFERENCES Espece(nom),
medicament VARCHAR REFERENCES Medicament(nom_mol),
PRIMARY KEY (espece, medicament));

INSERT INTO Autoriser VALUES('félin', 'Doliprane');

CREATE TABLE Client (
id SERIAL PRIMARY KEY,
nom VARCHAR NOT NULL,
prenom VARCHAR NOT NULL,
dateNaiss DATE NOT NULL,
adresse INT REFERENCES Adresse(id) NOT NULL,
numTel INT UNIQUE NOT NULL);

CREATE TABLE Personnel (
id SERIAL PRIMARY KEY,
nom VARCHAR NOT NULL,
prenom VARCHAR NOT NULL,
dateNaiss DATE NOT NULL,
adresse INT REFERENCES Adresse(id) NOT NULL,
num_tel INT UNIQUE NOT NULL,
poste VARCHAR NOT NULL,
CHECK (poste IN ('veterinaire', 'assistant')));
-- manque contrainte (voir en dessous)

INSERT INTO Client VALUES (DEFAULT, 'Benzema','Karim', '1993-04-16', 1, 0675894120);
INSERT INTO Client VALUES (DEFAULT, 'Lloris','Hugo', '1975-02-20', 2, 0758496521);
INSERT INTO Personnel VALUES (DEFAULT, 'Dupont','Pierre', '1987-11-01', 2, 0748596312,'assistant');
INSERT INTO Personnel VALUES (DEFAULT, 'Dupond','Jacques', '1975-02-20', 1, 0659741548, 'veterinaire');

CREATE TABLE Prescrire (
medicament VARCHAR REFERENCES Medicament(nom_mol) NOT NULL,
traitement INT REFERENCES Traitement(num),
veterinaire INT REFERENCES Personnel(id) NOT NULL,
quantite FLOAT,
PRIMARY KEY (medicament, traitement));
--manque contrainte (voir en dessous)

INSERT INTO Prescrire VALUES ('Doliprane', 1, 2, 500);

CREATE TABLE Specialiser(
personnel INT REFERENCES Personnel(id),
espece VARCHAR REFERENCES Espece(nom),
PRIMARY KEY (espece, personnel));

INSERT INTO Specialiser VALUES (2, 'félin');

CREATE TABLE Observation (
num SERIAL PRIMARY KEY,
date DATE NOT NULL,
heure TIME NOT NULL,
description TEXT,
personnel INT REFERENCES Personnel(id) NOT NULL,
patient INT REFERENCES Patient(id) NOT NULL);

INSERT INTO Observation VALUES(DEFAULT, current_date, current_time,'Observation faite sur Rex par Jacques Dupond', 2,1);

CREATE TABLE Etre_proprietaire (
client INT REFERENCES Client(id) NOT NULL,
patient INT REFERENCES Patient(id) NOT NULL,
dateDebut DATE NOT NULL,
dateFin DATE,
CHECK (dateFin>dateDebut OR dateFin = NULL),
PRIMARY KEY (client, patient));
-- manque contrainte (voir en dessous)

INSERT INTO etre_proprietaire VALUES (2,1,'2014-01-12', NULL);

CREATE TABLE suivre(
patient INT REFERENCES Patient(id) NOT NULL,
personnel INT REFERENCES Personnel(id) NOT NULL,
debut DATE NOT NULL,
fin DATE,
PRIMARY KEY (patient, personnel),
UNIQUE (patient, personnel, debut, fin),
CHECK (fin>debut OR fin = NULL));
-- manque contrainte (voir en dessous)

INSERT INTO Suivre VALUES (2,2,'2018-12-14', NULL);