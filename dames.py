#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
   Projet Dames 2020 - Licence Informatique UNC

   Fichier d'implémentation des règles du jeu de dames
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


#Variable...
# joueur1_pion_ids et joueur2_pion_ids sont des variables créées pour évite
# s'il y un changement ou un ajout de devoir les changer toute une par une
#donc de ne pas les ecrire en dire 
pions_and_dames_id = (1,2,11,12)
pions_id = (1,2)
dames_id = (11,12)
joueur1_pion_ids = (1,11)
joueur2_pion_ids = (2,12)
#------------------------------------------------------------
# Fonctions de base (ne dépendent pas d'autres fonctions)
#------------------------------------------------------------

def coordonneesValides(plateau,x,y):#3
	"""
    Fonction qui vérifie que les coordonnées (x,y) correspondent bien à une case (noire) du plateau
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées d'une case
	Résultat : un booléen valant True si il s'agit d'une case (noire) du plateau et False sinon
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : *
    """
	if x >= 0 and y >= 0:
		if len(plateau)-1 >= x and len(plateau)-1 >= y:
			#Les casses noirs ont un décalage de 1 en fonction de si x est paire
			if x%2 == 0:
				if y%2 != 0:
					return True
			else:
				if y%2 == 0:
					return True
	return False

def diagonale(x,y,z,t):#4
	"""
    Fonction qui vérifie que deux cases de coordonnées respectives (x,y)
	et (z,t) sont sur une même diagonale (quelque soit le plateau)
	Paramètres :
		- x,y les coordonnées d'une case
		- z,t les coordonnées d'une autre case
	Résultat : un entier indiquant le sens du déplacement (x,y)->(z,t)
        - 0 si les deux coordonnées ne sont pas sur la même diagonale
        - 1 s'il s'agit de la diagonale 1
        - 2 s'il s'agit de la diagonale 2
        - 3 s'il s'agit de la diagonale 3
        - 4 s'il s'agit de la diagonale 4
	Difficulté : **
    """
	differenceX = x - z 
	differenceY = y - t

	#il sont en diagonale si il on le meme décalage entre X est Y  
	if abs(differenceX) != abs(differenceY) or differenceX==0 and differenceY == 0:
		return 0

	if differenceX < 0:
		if differenceY < 0:
			res = 3
		else:
			res = 4
	else:
		if differenceY < 0:
			res = 2
		else:
			res = 1
			
	return res

def pionDuJoueur(plateau,joueurCourant,x,y):#5
	"""
    Fonction qui vérifie si un pion/dame situé(e) sur la case de coordonnées (x,y)
	appartient au joueur actuellement en train de jouer
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- joueurCourant : le numéro du joueur en train de jouer
		- x,y les coordonnées (valides) d'une case
	Résultat : un booléen valant True si le pion/dame en (x,y) appartient
	au joueur courant et False s'il n'appartient pas au joueur courant ou s'il
	n'y a pas de pion sur cette case
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : *
    """
    # joueur1_pion_ids et joueur2_pion_ids sont des variables créées en haut du script
	#cela évite s'il y un changement ou un ajout de devoir les changer toute une par une 
    
	if joueurCourant == 1:
		ids_pions = joueur1_pion_ids
	else:
		ids_pions = joueur2_pion_ids

	if plateau[x][y] in ids_pions:
		return True

	return False


def enleverPionsPriseMultiple(plateau,priseMultiple):#6
	"""
	Fonction qui enlève du plateau tous les pions pris lors d'une "prise multiple"
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- priseMultiple : liste de coordonnées des pions/dames pris(es) durant une "prise multiple"
	Résultat : La fonction ne retourne rien mais modifie
		- plateau : en enlevant les pions pris
		- priseMultiple : en vidant cette liste
	Difficulté : **
	"""
	for u,v in priseMultiple:
		plateau[u][v] = 0
	priseMultiple.clear()

def changementEnDame(plateau,joueurCourant,x,y):#7
	"""
    Fonction qui transforme un pion en dame lorsque le pion d'un joueur est
	arrivé sur la dernière rangée du plateau.
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- joueurCourant : le numéro du joueur en train de jouer
		- x,y les coordonnées (valides) d'une case
	Résultat : un booléen valant True si il y avait un pion en (x,y) qui a été
	changé en dame (le plateau a été modifié) et False sinon
	Difficulté : *
	"""
	# 0 = case vide
	#
	#joueur 1(noir): id pions = 1
	#				 id dame = 11
	#
	#joueur 2(noir): id pions = 2
	#				 id dame = 12

	if joueurCourant == 1: joueur_pion_id, joueur_dame_id, plateau_index  = joueur1_pion_ids[0],joueur1_pion_ids[1], len(plateau)-1
	else:  joueur_pion_id, joueur_dame_id, plateau_index = joueur2_pion_ids[0],joueur2_pion_ids[1], 0

	if x == plateau_index:
		res = True
		if plateau[x][y] == joueur_pion_id:
			plateau[x][y] = joueur_dame_id
	else:
		res = False

	return res
	

#------------------------------------------------------------------------
# Fonct. de traitements intermédiaires (utilisent des fonct. précédentes)
#------------------------------------------------------------------------

def caseSuivanteDiag(plateau,x,y,diag, nb_casses_suivant = 0):#8
	"""
    Fonction qui renvoie les coordonnées de la case suivant la case (x,y) sur la diagonale diag
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées d'une case
		- diag : un entier correspondant à l'une des quatre diagonales possibles (1,2,3 ou 4)
	Résultat : un couple (z,t) correspondant aux coordonnées de la case suivante
	si elle existe et None si cette case n'existe pas (hors plateau)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : *
	"""
	if coordonneesValides(plateau,x,y) == False:
		return None
	if diag == 1:
		z, t = x- (1+ nb_casses_suivant), y-(1+ nb_casses_suivant)
	elif diag == 2:
		z, t = x- (1+ nb_casses_suivant), y+1+ nb_casses_suivant
	elif diag == 3:
		z, t = x+ 1+ nb_casses_suivant, y+1+ nb_casses_suivant
	else:
		z, t = x+ 1+ nb_casses_suivant, y-(1+ nb_casses_suivant)
	
	if coordonneesValides(plateau,z,t) == False:
		return None
	return z,t


#need
def nbCasesVidesDiag(plateau,x,y,diag,limite = False):#9
	"""
    Fonction qui renvoie le nombre de cases vides à partir de la case (x,y) jusqu'au prochain obstacle
	(pion ou bord du plateau) sur la diagonale diag
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées d'une case
		- diag : un entier correspondant à l'une des quatre diagonales possibles (1,2,3 ou 4)
	Résultat : un entier correspondant au nombre de cases vides
	(0 s'il n'y en a aucune dans la direction diag)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
    """
	flag = True
	i = 0
	while flag:
		res = caseSuivanteDiag(plateau,x,y,diag)
		if res == None:
			flag = False
		else:
			x,y = res
			if plateau[x][y] == 0:
				i+=1
				if limite:
					flag = False
			else:
				flag = False
	return i


def nbCases(plateau,x,y,z,t):#9bis
	"""
    Fonction qui renvoie le nombre de cases à partir de la case (x,y) jusqu'a (z,t)
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées d'une case
		- z,t les coordonnées d'une case
	Résultat : un entier correspondant au nombre de cases vides
	(0 s'il n'y en a aucune dans la direction diag)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
    """
	
	i = 0
	diag = diagonale(z,t,x,y)
	if diag != 0:
		flag = True
		while flag:
			res = caseSuivanteDiag(plateau,z,t,diag)
			if res == None or x == z and y == t:
				flag = False
			else:
				z,t = res
				i+=1

	return i
		

def prochainPionDiag(plateau,x,y,diag):#10
	"""
    Fonction qui renvoie les coordonnées du prochain pion sur la diagonale diag
	à partir de (x,y).
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées d'une case
		- diag : un entier correspondant à l'une des quatre diagonales possibles (1,2,3 ou 4)
	Résultat : un couple (z,t) correspondant aux coordonnées du prochain pion
	sur la diagonale diag (None s'il n'y a plus de pion après x,y sur cette diagonale)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
	"""
	flag = True

	
	while flag:
		res = caseSuivanteDiag(plateau,x,y,diag)
		if res == None:
			return None
		else:
			x,y = res
			if plateau[x][y] in pions_and_dames_id:
				flag = False
	return x,y

def deplacementPossible(plateau,x,y):#11
	"""
	Fonction qui vérifie si un pion/dame à la position (x,y) du plateau peut
	se déplacer (sans réaliser de prise de pion/dame) :
		- en avant sur une case suivante en diagonale pour un pion
		- en avant ou en arrière sur une case suivante ou éloignée pour une dame
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées (valides) d'une case
	Résultat : un booléen valant True si il y a bien un pion/dame en (x,y) et
	qu'il peut se déplacer et False sinon
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
	"""
	#joueur 1(noir): id pions = 1
	#				 id dame = 11
	#
	#joueur 2(noir): id pions = 2
	#				 id dame = 12
 
	if plateau[x][y] in pions_and_dames_id:
		if plateau[x][y] in dames_id:
			res = _deplacementPossibleBoucle(plateau,x,y,1,5,False)
		elif plateau[x][y] == joueur1_pion_ids[0]:
			res = _deplacementPossibleBoucle(plateau,x,y,3,5,True)
		elif plateau[x][y] == joueur2_pion_ids[0]:
			res = _deplacementPossibleBoucle(plateau,x,y,1,3,True)
	else:
		res = False
	return res 

def _deplacementPossibleBoucle(plateau,x,y,diag,diag_max,limite):
	res = False
	while res == False and diag < diag_max:
		if nbCasesVidesDiag(plateau,x,y,diag,limite) > 0:
			res = True
		diag += 1
	return res

def pionPrisePossibleDiag(plateau,x,y,diag):#12
	"""
    Fonction qui vérifie si il y a un *pion* en (x,y) et s'il peut prendre un pion ou une dame
	*adverse* dans la diagoniale diag (i.e pion sur la case suivante, et case derrière libre).
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case du *pion*
		- diag : un entier correspondant à l'une des quatre diagonales possibles (1,2,3 ou 4)
	Résultat : un couple (u,v) correspondant aux coordonnées du pion ou de la dame prenable
	(None s'il n'y a pas de *pion* en (x,y) ou si il ne peut pas prendre de pion ou de dame
	sur cette diagonale)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
    """
    #joueur 1(noir): id pions = 1
	#				 id dame = 11
	#
	#joueur 2(noir): id pions = 2
	#				 id dame = 12
    

	ids = joueur1_pion_ids[0] , joueur2_pion_ids[0]
		
	cell = caseSuivanteDiag(plateau,x,y,diag)
	if cell != None and plateau[x][y] != 0:
		
		if plateau[x][y] == ids[0]:
			pion_adverse = joueur2_pion_ids
		elif plateau[x][y] == ids[1]:
			pion_adverse = joueur1_pion_ids

		z1,t1 = cell
		cell = caseSuivanteDiag(plateau,z1,t1,diag)
		if cell != None:
			z2,t2 = cell
			if plateau[z1][t1] in pion_adverse and plateau[z2][t2] == 0:
				return z1,t1
	return None
        
        
    


def pionPrisePossible(plateau,x,y):#13
	"""
    Fonction qui construit la liste des coordonnées des pions ou des dames adverses
	qu'un *pion* situé en (x,y) peut prendre (toutes diagonales confondues).
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case du *pion*
	Résultat : une liste de coordonnées (u,v) correspondant aux positions des
	pions ou des dames prenables par un *pion* en (x,y). La liste renvoyée sera vide
	si le *pion* ne peut rien prendre et contiendra au maximum quatre coordonnées
	(une prise possible par diagonale)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
    """
	list_pions_posible = []
	for diag in range(1,5):
		res = pionPrisePossibleDiag(plateau,x,y,diag)
		if res != None:
			list_pions_posible.append(res)
	return list_pions_posible


def damePrisePossibleDiag(plateau,x,y,diag):#14
	"""
    Fonction qui vérifie si il y a une *dame* en (x,y) et si elle peut prendre un pion ou une dame
	*adverse* dans la diagoniale diag (i.e pion sur l'une des cases suivantes, et case derrière libre).
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case de la *dame*
		- diag : un entier correspondant à l'une des quatre diagonales possibles (1,2,3 ou 4)
	Résultat : un couple (u,v) correspondant aux coordonnées du pion ou de la dame prenable
	(None s'il n'y a pas de *dame* en (x,y) ou si elle ne peut pas prendre de pion ou de dame
	sur cette diagonale)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
	"""
	res = prochainPionDiag(plateau,x,y,diag)
	if res != None:
		u,v = res
		res = caseSuivanteDiag(plateau,u,v,diag)
		if res != None:
			z,t = res 
			if plateau[z][t] == 0:
				return u,v

	return None
     

def damePrisePossible(plateau,x,y):#15
	"""
    Fonction qui construit la liste des coordonnées des pions ou des dames adverses
	qu'une *dame* située en (x,y) peut prendre (toutes diagonales confondues).
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case du *pion*
	Résultat : une liste de coordonnées (u,v) correspondant aux positions des
	pions ou des dames prenables par une *dame* en (x,y). La liste renvoyée sera vide
	si la *dame* ne peut rien prendre et contiendra au maximum quatre coordonnées
	(une prise possible par diagonale)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
    """
	liste_prise_Possible = []
	for diag in range(1,5):
		res = damePrisePossibleDiag(plateau,x,y,diag)
		if res != None:
			liste_prise_Possible.append(res)
	return liste_prise_Possible

def prisePossibleDiag(plateau,x,y,diag):#16
	"""
    Fonction qui vérifie si il y a un pion ou une dame en (x,y) et si il/elle peut prendre un pion ou une dame
	*adverse* dans la diagoniale diag (i.e pion sur l'une des cases suivantes, et case derrière libre).
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case du pion ou de la dame
		- diag : un entier correspondant à l'une des quatre diagonales possibles (1,2,3 ou 4)
	Résultat : un couple (u,v) correspondant aux coordonnées du pion ou de la dame prenable
	(None s'il n'y a pas de pion ou de dame en (x,y) ou si il/elle ne peut pas prendre de pion ou de dame
	sur cette diagonale)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : *
    """
    
	if plateau[x][y] in pions_id:
		prise_Possible = pionPrisePossibleDiag(plateau,x,y,diag)
	elif plateau[x][y] in dames_id:
		prise_Possible = damePrisePossibleDiag(plateau,x,y,diag)
	else:
		prise_Possible = None
	return prise_Possible

def prisePossible(plateau,x,y):#17
	"""
    Fonction qui construit la liste des coordonnées des pions ou des dames adverses
	qu'un pion ou une dame situé(e) en (x,y) peut prendre (toutes diagonales confondues).
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case du *pion*
	Résultat : une liste de coordonnées (u,v) correspondant aux positions des
	pions ou des dames prenables par un pion ou une dame en (x,y). La liste renvoyée sera vide
	si le pion ou la dame ne peut rien prendre et contiendra au maximum quatre coordonnées
	(une prise possible par diagonale)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : *
    """

	if plateau[x][y] in pions_and_dames_id:
		liste_prise_Possible = []
		for diag in range(1,5):
			res = prisePossibleDiag(plateau,x,y,diag)
			if res != None:
				liste_prise_Possible.append(res)
	else:
		liste_prise_Possible == []

	return liste_prise_Possible


def prisePossibleDest(plateau,x,y,z,t):#18
	"""
    Fonction qui vérifie si il y a un pion ou une dame en (x,y), si il/elle peut prendre un pion ou une dame
	*adverse* et se poser en (z,t).
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case du pion ou de la dame
		- z,t les coordonnées de la case destination
	Résultat : un couple (u,v) correspondant aux coordonnées du pion ou de la dame prenable
	(None s'il n'y a pas de pion ou de dame en (x,y) ou si il/elle ne peut pas prendre de pion ou de dame
	et se poser en (z,t))
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : ***
    """
	if coordonneesValides(plateau,z,t) and plateau[z][t] == 0:
		
		if plateau[x][y] in joueur1_pion_ids:
			pion_adverse = joueur2_pion_ids
		elif plateau[x][y] in joueur2_pion_ids:
			pion_adverse = joueur1_pion_ids
		else:
			return None
		diag = diagonale(x,y,z,t)
		if diag == 0: return None

		if plateau[x][y] in pions_id:
			res = pionPrisePossibleDiag(plateau,x,y,diag)
			if res != None:
				if plateau[res[0]][res[1]] in pion_adverse and caseSuivanteDiag(plateau,res[0],res[1],diag) == (z,t): 
					return res
						
		elif plateau[x][y] in dames_id:
			res = damePrisePossibleDiag(plateau,x,y,diag)
			if res != None:
				if plateau[res[0]][res[1]] in pion_adverse and caseSuivanteDiag(plateau,res[0],res[1],diag) == (z,t): 
					return res
		
		#im herree
	return None

	
	

def jouable(plateau,x,y):#19
	"""
    Fonction qui vérifie si un pion ou une dame à la position (x,y) peut jouer
	(i.e. se déplaer ou réaliser une prise)
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case du pion ou de la dame
	Résultat : un booléen valant True si le pion ou la dame peut jouer et False sinon
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : *
    """
	if plateau[x][y] in pions_and_dames_id:
		res = deplacementPossible(plateau,x,y)
		if res == False:
			temp = prisePossible(plateau,x,y)
			if temp != []:
				res = True
	else:
		res = False
	return res
			

def realiserDeplacement(plateau,x,y,z,t):#20
	"""
    Fonction qui vérifie et réalise le déplacement d'un pion ou d'une dame situé(e) en (x,y)
	vers la case (z,t). Le cas échéant la transformation du pion en dame doit être réalisée.
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- x,y les coordonnées de la case du pion ou de la dame
		- z,t les coordonnées de la case destination
	Résultat : un booléen valant True si le déplacement a été réalisé
	et False si le déplacement n'est pas autorisé
	Difficulté : **
    """
	res = False
	if coordonneesValides(plateau,z,t) and  coordonneesValides(plateau,x,y) and plateau[z][t] == 0:
		diag = diagonale(x,y,z,t)
		if diag == 0: return False

		if plateau[x][y] in pions_id and caseSuivanteDiag(plateau,x,y,diag) == (z,t):
			if plateau[x][y] == joueur2_pion_ids[0] and diag in (1,2) or plateau[x][y] == joueur1_pion_ids[0] and diag in (3,4):
				res = True
			else:
				res = False
		elif plateau[x][y] in dames_id:
			uv = prochainPionDiag(plateau,x,y,diag)
			
			if uv != None:
				u,v = uv
				nb_case1 = nbCasesVidesDiag(plateau,x,y,diag)
				diag = diagonale(z,t,x,y)
				nb_case2 = nbCases(plateau,x,y,z,t)
				if nb_case1 >= nb_case2:
					res = True
			else:
				res = True
			
		


		if res == True:
				plateau[z][t],plateau[x][y] = plateau[x][y],0 


				if plateau[z][t] == joueur1_pion_ids[0]:
					changementEnDame(plateau,1,z,t)
				elif plateau[z][t] == joueur2_pion_ids[0]:
					changementEnDame(plateau,2,z,t)
			
	return res


def realiserPrise(plateau,joueurCourant,x,y,z,t,priseMultiple):#21
	"""
    Fonction qui réalise une prise de pion/dame si celle-ci est autorisée.
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- joueurCourant : le (numéro du) joueur qui réalise ce coup
		- x,y les coordonnées de la case de départ
		- z,t les coordonnées de la case d'arrivée
		- priseMultiple : liste de coordonnées des pions/dames déjà pris durant une "prise multiple"
	Résultat :
		- si la prise est réalisable
			- le plateau est modifié : déplacement du pion, tranformation éventuelle en Dame, enlèvement du pion/dame adverse ou ajout dans la liste priseMultiple
			- si la prise multiple est terminée, les pions pris sont enlevés du plateau et la liste priseMultiple est vidée
			- la fonction renvoie True
		- sinon la fonction renvoie False
	Difficulté : ***
	"""
	res = False
	if coordonneesValides(plateau,x,y) and  coordonneesValides(plateau,z,t):
		
		if abs(z-x) <= 1:
			return False
		
		
		uv = prisePossibleDest(plateau,x,y,z,t)
		if uv != None:
			res = True
			u,v = uv 
			plateau[z][t],plateau[x][y] = int(plateau[x][y]),0
			if prisePossible(plateau,z,t)  == [(u,v)]:
				plateau[u][v] = 0
				enleverPionsPriseMultiple(plateau,priseMultiple)
				
			else:
				plateau[u][v] = -int(plateau[u][v])
				priseMultiple.append((u,v))
    
			if plateau[z][t] == joueur1_pion_ids[0]:
				changementEnDame(plateau,1,z,t)
			elif plateau[z][t] == joueur2_pion_ids[0]:
				changementEnDame(plateau,2,z,t)
	return res
		
		

#------------------------------------------------------------
# Fonctions principales (utilisées par les interfaces de jeu)
#------------------------------------------------------------

def initialisePlateau(dim):#1
	"""
    Fonction qui crée et renvoie un plateau de taille (dim x dim)
	sous forme d'une matrice (liste de listes) avec placement des pions
	de chaque joueur : une case sur deux
        1 pour un pion du joueur1
        2 pour un pion du joueur2
        0 pour une case vide
    Aucun pion n'est placé sur les deux lignes centrales du plateau
    Paramètres :
		- dim : la dimension (nombre pair) du plateau
    résultat : un plateau dimxdim avec les pions des deux joueurs placés
	Difficulté : **
    """

	if dim < 4:
		dim = 4

	plateau = []
	#creation du plateau avec que des 0
	ligne = [0]*dim
	for hauteur in range(dim):
		plateau.append(list(ligne))

	#ajout des pions du joueur 1

	for i in range((len(plateau)//2 - 1)):
		for j in range(0,len(plateau[i])-1,2):
			if i%2 == 0:
				plateau[i][j+1] = joueur1_pion_ids[0]
			else:
				plateau[i][j] = joueur1_pion_ids[0]


	#ajout des pions du joueur 2

	for i in range(-1,-len(plateau)//2,-1):
		for j in range(0,len(plateau[i])-1,2):
			if i%2 == 0:
				plateau[i][j+1] = joueur2_pion_ids[0]
			else:
				plateau[i][j] = joueur2_pion_ids[0]

	
	return plateau
 
def choisirCase(plateau,phase):#2
	"""
    Fonction d'entrée/sortie, qui demande au joueur de saisir au clavier les
	coordonnées d'une case sous forme de deux entiers et renvoie ces coordonnées.
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- phase : numéro de phase (1 si on demande les coordonnées du pion à déplacer
		et 2 si on demande la case d'arrivée)
	Résultat : un couple d'entiers correspondant aux coordonnées de la case et
	(None,None) si les valeurs saisies ne sont pas convertibles en entiers.
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : *
    """
	
	if phase == 1:
			x = input("Quel est la coordonnée X du pion")
			y = input("Quel est la coordonnée Y du pion")
	elif phase == 2:
			x = input("Quel est la coordonnée X de la case d'arrivée")
			y = input("Quel est la coordonnée Y de la case d'arrivée")

	if type(x) == int and type(y) == int:
		return x,y

	return (None,None)


def verifierPionChoisi(plateau,joueurCourant,x,y):#22
	"""
    Fonction qui vérifie que les coordonnées (x,y) correspondent à celles d'un pion
	ou du dame jouable.
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- joueurCourant : le numéro du joueur en train de jouer
		- x,y les coordonnées d'une case
	Résultat : un entier valant :
        - 1 si la case choisit n'est pas valide (pas une case, pas une case noire)
        - 2 si il n'y a pas de pion (du joueur) en (x,y)
        - 3 si le pion n'est pas jouable
        - 4 si la règle de prise obligatoire n'est pas respectée (option)
        - 5 si la règle de prise majoritaire n'est pas respectée (option)
        - 10 si le pion ou la dame en (x,y) peut-être joué(e)
	ATTENTION : cette fonction ne modifie pas le plateau
	Difficulté : **
    """
	# 0 = case vide
	#
	#joueur 1(noir): id pions = 1
	#				 id dame = 11
	#
	#joueur 2(noir): id pions = 2
	#				 id dame = 12
	if type(plateau[x][y]) != int:
		return 1
	if coordonneesValides(plateau,x,y) == False:
		return 1

	if pionDuJoueur(plateau,joueurCourant,x,y) == False:
		return 2
		
	if jouable(plateau,x,y) == False:
		return 3

	return 10

def realiserAction(plateau,joueurCourant,x,y,z,t,priseMultiple):#23
	"""
    Fonction qui réalise un coup (déplacement ou prise) si celui-ci est autorisé.
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- joueurCourant : le (numéro du) joueur qui réalise ce coup
		- x,y les coordonnées de la case de départ
		- z,t les coordonnées de la case d'arrivée
		- priseObligatoire : un booléen indiquant si ce coup s'inscrit dans une prise multiple
	Résultat :
		- 0 : les coordonnées ne correspondent pas à des cases (noires) du tableau
		- 1 : déplacement interdit (ex. pas en diagonale, présence d'un pion sur la case d'arrivée, etc.)
		- 4 (optionnel) : déplacement interdit car la règle de prise obligatoire n'est pas respectée
		- 5 (optionnel) : déplacement interdit car la règle de prise majoritaire n'est pas respectée
		- 10 : déplacement réalisé
		- 11 : prise de pion/dame réalisée
		- 12 : prise de pion/dame réalisée avec nouvelle prise attendue (prise multiple)
		- 13 : le joueur a récupéré une dame
		Dans les cas 10, 11, 12 et 13 le plateau a été modifié
	Difficulté : ***
    """

	res = 0
	if coordonneesValides == False:
		return 0
	if diagonale == 0:
		return 1
	len_prise_mult = len(priseMultiple)
	if realiserPrise(plateau,joueurCourant,x,y,z,t,priseMultiple):
		if len(priseMultiple) > len_prise_mult:
			res = 12
		else:
			res = 11
	elif realiserDeplacement(plateau,x,y,z,t):
		res = 10
		if res in (10,11):
			pass#res = 13
	return res 

def finDePartie(plateau,joueurCourant):#24
	"""
    Fonction qui vérifie si le joueur adverse a perdu.
	Rappel : un joueur a perdu s'il n'a plus de pion sur le plateau ou s'il ne
	peut plus bouger aucun pion.
	Paramètres :
		- plateau : le plateau (matrice nxn)
		- joueurCourant : le (numéro du) joueur courant
    Résultat :
      - 1 si l'adversaire du joueur courant n'a plus de pion sur le plateau
      - 2 si l'adversaire du joueur courant ne peut plus bouger aucun pion
      - 0 sinon (le joueur adverse n'a pas perdu)
	Difficulté : **
    """
	pass
			

#------------------------------------------------------------
# programme de test
#------------------------------------------------------------

if __name__=='__main__':
	plateau = initialisePlateau(8)
	#1 - tests de la fonction initialiserPlateau(dim)
	assert initialisePlateau(0)==[[0,1,0,1],[0,0,0,0],[0,0,0,0],[2,0,2,0]],"Test invalide : initialiserPlateau"#plateau 4x4
	assert initialisePlateau(4)==[[0,1,0,1],[0,0,0,0],[0,0,0,0],[2,0,2,0]],"Test invalide : initialiserPlateau"#plateau 4x4
	assert initialisePlateau(6)==[[0,1,0,1,0,1],[1,0,1,0,1,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,2,0,2,0,2],[2,0,2,0,2,0]],"Test invalide : initialiserPlateau"#plateau 6x6
	assert initialisePlateau(8)==[[0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [2, 0, 2, 0, 2, 0, 2, 0], [0, 2, 0, 2, 0, 2, 0, 2], [2, 0, 2, 0, 2, 0, 2, 0]],"Test invalide : initialiserPlateau"

	#3 - tests de la fonction coordonneesValides(plateau,x,y)
	assert coordonneesValides(plateau,1,0)==True,"Test invalide : coordonneesValides (plateau 8)"
	assert coordonneesValides(plateau,2,4)==False,"Test invalide : coordonneesValides (plateau 8)"
	assert coordonneesValides(plateau,6,5)==True,"Test invalide : coordonneesValides (plateau 8)"
	assert coordonneesValides(plateau,6,6)==False,"Test invalide : coordonneesValides (plateau 8)"
	assert coordonneesValides(plateau,3,1)==False,"Test invalide : coordonneesValides (plateau 8)"
	assert coordonneesValides(plateau,3,2)==True,"Test invalide : coordonneesValides (plateau 8)"
	assert coordonneesValides(plateau,3,3)==False,"Test invalide : coordonneesValides (plateau 8)"
	assert coordonneesValides(plateau,3,4)==True,"Test invalide : coordonneesValides (plateau 8)"
	plateau = initialisePlateau(6)
	assert coordonneesValides(plateau,0,0)==False,"Test invalide : coordonneesValides (plateau 6)"
	assert coordonneesValides(plateau,1,0)==True,"Test invalide : coordonneesValides (plateau 6)"
	assert coordonneesValides(plateau,2,4)==False,"Test invalide : coordonneesValides (plateau 6)"
	assert coordonneesValides(plateau,6,5)==False,"Test invalide : coordonneesValides (plateau 6)"
	assert coordonneesValides(plateau,-1,2)==False,"Test invalide : coordonneesValides (plateau 6)"
	assert coordonneesValides(plateau,2,-1)==False,"Test invalide : coordonneesValides (plateau 6)"
	plateau = initialisePlateau(8)
 	#4 - tests de la fonction diagonale(x,y,z,t)
	assert diagonale(0,1,1,0) == 4,"Test invalide : diagonale"
	assert diagonale(2,3,0,1) == 1,"Test invalide : diagonale"
	assert diagonale(6,5,4,7) == 2,"Test invalide : diagonale"
	assert diagonale(1,0,9,8) == 3,"Test invalide : diagonale"
	assert diagonale(6,5,4,5) == 0,"Test invalide : diagonale"
	assert diagonale(6,5,6,5) == 0,"Test invalide : diagonale"
  	#5 - tests de la fonction pionDuJoueur(plateau,joueurCourant,x,y)
	assert pionDuJoueur(plateau,1,0,1) == True,"Test invalide : pionDuJoueur"
	assert pionDuJoueur(plateau,1,1,0) == True,"Test invalide : pionDuJoueur"
	assert pionDuJoueur(plateau,2,0,1) == False,"Test invalide : pionDuJoueur"
	assert pionDuJoueur(plateau,2,7,7) == False,"Test invalide : pionDuJoueur"
	assert pionDuJoueur(plateau,2,7,4) == True,"Test invalide : pionDuJoueur"
	#6 - tests de la fonction enleverPionsPriseMultiple(plateau,priseMultiple)
	
	#7 - tests de la fonction changementEnDame(plateau,joueurCourant,x,y)

	if coordonneesValides(plateau,7,0):
		plateau[7][0] = 1
	if coordonneesValides(plateau,0,1):
		plateau[0][1] = 2
	assert changementEnDame(plateau,1,0,1) == False,"Test invalide : changementEnDame"
	assert changementEnDame(plateau,1,7,0) == True,"Test invalide : changementEnDame"
	assert changementEnDame(plateau,2,7,4) == False,"Test invalide : changementEnDame"
	assert changementEnDame(plateau,2,0,1) == True,"Test invalide : changementEnDame"
	print(plateau)
	#tests de la fonction caseSuivanteDiag(plateau,x,y,diag)#8
	assert caseSuivanteDiag([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],0,1,1)==None,"Test invalide : caseSuivanteDiag"#bord haut du plateau
	assert caseSuivanteDiag([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2,1,4)==(3,0),"Test invalide : caseSuivanteDiag"#diagonale 4 ok

	#tests de la fonction nbCasesVidesDiag(plateau,x,y,diag)#9
	assert nbCasesVidesDiag([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],0,1,1)==0,"Test invalide : nbCasesVidesDiag" #bord
	assert nbCasesVidesDiag([[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,0,0,0]],0,3,4)==2,"Test invalide : nbCasesVidesDiag" #2 cases vide puis pion

	#tests de la fonction prochainPionDiag(plateau,x,y,diag)#10
	assert prochainPionDiag([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],2,3,1)==None,"Test invalide : prochainPionDiag" #plus de pion sur diagonale 1
	assert prochainPionDiag([[0,0,0,0],[0,0,11,0],[0,0,0,0],[0,0,0,0]],0,1,3)==(1,2),"Test invalide : prochainPionDiag" #pion direct sur diagonale 3

	#tests de la fonction deplacementPossible(plateau,x,y)#11
	assert deplacementPossible([[0,0,0,0],[1,0,0,0],[0,2,0,0],[0,0,0,0]],1,0)==False,"Test invalide : deplacementPossible" #pion 1 ne peut pas bouger
	assert deplacementPossible([[0,1,0,1],[0,0,12,0],[0,2,0,0],[0,0,0,0]],1,2)==True,"Test invalide : deplacementPossible" #dame 2 peut bouger

	#tests de la fonction pionPrisePossibleDiag(plateau,x,y,diag)#12
	assert pionPrisePossibleDiag([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],1,2,1)==None,"Test invalide : pionPrisePossibleDiag" #pas de pion en (x,y)
	assert pionPrisePossibleDiag([[0,0,0,0],[0,0,0,0],[0,2,0,0],[1,0,0,0]],3,0,2)==(2,1),"Test invalide : pionPrisePossibleDiag" #prise possible

	#tests de la fonction pionPrisePossible(plateau,x,y)#13
	assert pionPrisePossible([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],1,2)==[],"Test invalide : pionPrisePossible" #pas de pion en (x,y)
	assert pionPrisePossible([[0,2,0,2],[0,0,1,0],[0,2,0,2],[0,0,0,0]],1,2)==[(2,1)],"Test invalide : pionPrisePossible" #pion en (x,y) et un pion adverses à prendre

	#tests de la fonction damePrisePossibleDiag(plateau,x,y,diag)#14
	assert damePrisePossibleDiag([[0,0,0,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]],1,2,1)==None,"Test invalide : pionPrisePossibleDiag" #pas de dame en (x,y)
	assert damePrisePossibleDiag([[0,0,0,11],[0,0,0,0],[0,2,0,0],[0,0,0,0]],0,3,4)==(2,1),"Test invalide : pionPrisePossibleDiag" #dame en (x,y) et pion (éloigné) à prendre

	#tests de la fonction damePrisePossible(plateau,x,y)#15
	assert damePrisePossible([[0,0,0,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]],1,2)==[],"Test invalide : damePrisePossible" #pas une dame en (x,y)
	assert damePrisePossible([[0,0,0,11],[0,0,2,0],[0,0,0,0],[0,0,0,0]],0,3)==[(1,2)],"Test invalide : damePrisePossible" #dame en (x,y) et un pion à prendre

	#tests de la fonction prisePossibleDiag(plateau,x,y,diag)#16
	assert prisePossibleDiag([[0,0,0,0],[0,0,1,0],[0,0,0,0],[2,0,0,0]],3,0,2)==None,"Test invalide : prisePossibleDiag"#rien à prendre pour un pion
	assert prisePossibleDiag([[0,0,0,0],[0,0,1,0],[0,0,0,0],[12,0,0,0]],3,0,2)==(1,2),"Test invalide : prisePossibleDiag"#Dame peut prendre pion

	#tests de la fonction prisePossible(plateau,x,y)#17
	assert prisePossible([[0,0,0,0],[0,0,1,0],[0,0,0,0],[2,0,0,0]],3,0)==[],"Test invalide : prisePossible"#rien à prendre pour un pion
	assert prisePossible([[0,0,0,0,0,0],[0,0,0,0,2,0],[0,1,0,1,0,0],[0,0,2,0,0,0],[0,0,0,1,0,0],[0,0,0,0,0,0]],3,2) in [[(2,1),(4,3)],[(4,3),(2,1)]],"Test invalide : prisePossible"#2 pèces à prendre pour un pion

	#tests de la fonction prisePossibleDest(plateau,x,y,z,t)#18
	assert prisePossibleDest([[0,0,0,0],[0,0,0,0],[0,1,0,0],[2,0,0,0]],3,0,0,3)==None,"Test invalide : prisePossibleDest"#case destination invalide
	assert prisePossibleDest([[0,0,0,0],[0,0,1,0],[0,0,0,0],[12,0,0,0]],3,0,0,3)==(1,2),"Test invalide : prisePossibleDest"#Dame peut prendre pion

	#tests de la fonction jouable(plateau,x,y)#19
	assert jouable([[0,0,0,1],[1,0,1,0],[0,2,0,0],[0,0,0,0]],2,1)==False,"Test invalide : jouable"#pion non jouable
	assert jouable([[0,0,0,1],[1,0,0,0],[0,2,0,0],[0,0,0,0]],2,1)==True,"Test invalide : jouable"#pion jouable

	#tests de la fonction realiserDeplacement(plateau,x,y,z,t)#20
	assert realiserDeplacement([[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,0,0,0]],3,0,1,2)==False,"Test invalide : realiserDeplacement"#déplacement interdit
	assert realiserDeplacement([[0,0,0,0],[0,0,0,0],[0,0,0,0],[2,0,0,0]],3,0,2,1)==True,"Test invalide : realiserDeplacement"#déplacement interdit

	#tests de la fonction realiserPrise(plateau,joueurCourant,x,y,z,t,priseMultiple)#21
	assert realiserPrise([[0,1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],1,0,1,2,3,[])==False,"Test invalide : realiserPrise"#rien à prendre
	assert realiserPrise([[0,0,0,0],[0,0,2,0],[0,0,0,1],[0,0,0,0]],1,2,3,0,1,[])==True,"Test invalide : realiserPrise"#prise pion en arrière

	#tests de la fonction verifierPionChoisi(plateau,joueurCourant,x,y)#22
	assert verifierPionChoisi([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],1,0,0)==1,"Test invalide : verifierPionChoisi"#pas une case noire
	assert verifierPionChoisi([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],1,0,1)==2,"Test invalide : verifierPionChoisi"#pas de pion sur la case

	#tests de la fonction realiserAction(plateau,joueurCourant,x,y,z,t,priseMultiple)#23
	assert realiserAction([[0,1,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],1,0,1,3,4,[])==0,"Test invalide : realiserAction" #déplacement hors plateau
#	assert realiserAction([[0,0,0,0],[1,0,0,0],[0,2,0,0],[0,0,0,0]],1,1,0,3,2,[])==13,"Test invalide : realiserAction"#prise de pion+transformaiton pion -> dame

	#tests de la fonction finDePartie(plateau,joueurCourant)#24
	#assert finDePartie([[0,1,0,1],[0,0,0,0],[0,2,0,0],[0,0,0,0]],1)==0,"Test invalide : finDePartie" #l'adversaire peut jouer (se déplacer)
	#assert finDePartie([[0,0,0,0],[0,0,0,0],[0,1,0,0],[2,0,2,0]],2)==2,"Test invalide : finDePartie"