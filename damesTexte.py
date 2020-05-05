#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
   Projet Dames 2020 - Licence Informatique UNC

   Programme principal du jeu de dames en mode texte
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from ansiColor import *
from dames import *

def affichePlateau(plateau,numJoueur,msg='',x=None,y=None,sauts=0):#fonction donnée
    """
    affiche un jeu de dames
    paramètres:     plateau : un plateau (damier) avec les pions
                    message: une chaine de caractères contenant un message à afficher
                    sauts: nombre de lignes à sauter à la fin de l'affichage
    La fonction ne retourne rien mais affiche le labyrinthe à l'écran
    """
    clearscreen()
    print(msg)
    print("C'est au tour de ",end='')
    pcouleur('joueur',numJoueur,0,1)
    print(" de jouer")
    dim=len(plateau)
    #affichage de l'en-tête du plateau--------------------
    print('   ',end='')
    for i in range(dim):
        print(" "+str(i+1)+(3-len(str(i+1)))*' ',end='')
    print()
    print("  "+"+---"*dim,end='');print("+")
    #affichage des lignes du plateau----------------------
    for i in range(dim):
        print((2-len(str(i+1)))*' '+str(i+1),end='')
        for j in range(dim):
            print("|",end='')
            if (i+j)%2==0:#case blanche
                coulFond=GRIS;coulCar=NOIR;style=AUCUN
                pcouleur('   ',coulCar,coulFond,style)
            elif plateau[i][j]==0 : #case noire sans pion
                print("   ",end='')
            else : #case noire avec pion
                coulFond=ROUGE if plateau[i][j]%2 else VERT
                if i==x and j==y:
                    coulFond=LROUGE if plateau[i][j]%2 else LVERT
                coulCar=NOIR;style=GRAS
                pcouleur(' ',coulCar,coulFond,style)
                pcouleur((' ' if plateau[i][j]<10 else 'D'),coulCar,coulFond,style)
                pcouleur(' ',coulCar,coulFond,style)
        print("|"+str(i+1))
        print("  "+"+---"*dim,end='');print("+")
    print('   ',end='')
    for i in range(dim):
        print(" "+str(i+1)+(3-len(str(i+1)))*' ',end='')
    for i in range(sauts):
        print()
    print()

# demarre la partie en mode texte
def jouer(plateau):
    """
    lance le jeu de dames en mode texte, il faut que le plateau et
    les 2 joueurs aient été créés avant ce lancement
    paramètre: plateau: une vue texte du plateau
    la fonction ne retourne rien mais effectue une partie de dames
    """
    #règle -> les verts commencent toujours
    joueurCourant=2

    # premier affichage du jeu
    affichePlateau(plateau,joueurCourant)
    fini=False
    phase=1
    priseMultiple=[]
    while not fini: # tant qu'aucun joueur n'a gagné
        a,b=choisirCase(plateau,phase) # le joueur choisit un pion
        #===========================CHOIX CASE DE DEPART=============================
        if phase==1:
            x,y=a,b
            res=verifierPionChoisi(plateau, joueurCourant, x, y)
            # traitement du résultat de l'ordre pour afficher le bon message à l'utilisateur
            if res==0:
                message="Saisie incorrecte"
            elif res==1:
                message="Case invalide"
            elif res==2:
                message="Vous n'avez pas de pion sur cette case"
            elif res==3:
                message="Votre pion ne peut pas bouger"
            elif res==4:
                message="Rappel de règle : la prise est obligatoire"
            elif res==5:
                message="Rappel de règle : la prise majoritaire est obligatoire"
            else:
                message=""
            if res not in [10]:
                x,y=None,None
            else :
                phase=2
        #===========================CHOIX CASE DESTINATION===========================
        else:
            z,t=a,b
            res=realiserAction(plateau,joueurCourant,x,y,z,t,priseMultiple)# déplacement ou prise
            # traitement du résultat de l'ordre pour afficher le bon message à l'utilisateur
            if res==0:
                message="Saisie incorrecte"
            elif res==1:
                message="Ce déplacement n'est pas permis"
            elif res==4:
                message="Rappel de règle : la prise est obligatoire"
            elif res==5:
                message="Rappel de règle : la prise majoritaire est obligatoire"
            elif res==10:
                message="Le joueur s'est déplacé"
            elif res in [11,12]:
                message="Le joueur a pris un pion/une dame à l'adversaire"
            elif res==13:
                message="Le joueur a récupéré une dame"
            if res==12:
                x,y=z,t
            elif res in [10,11,13]:
                x,y=None,None
                phase=1
                res2=finDePartie(plateau,joueurCourant)
                if res2:
                    message="Le joueur "+('BLANC' if joueurCourant==2 else 'NOIR')+" a gagné!"
                    fini=True
                joueurCourant=(1 if joueurCourant==2 else 2) #changement de joueur
        #Affichage du plateau=============================
        affichePlateau(plateau,joueurCourant,message,x,y)
    # la partie est terminer
    print("Merci au revoir")

#------------------------------
# programme principal
#------------------------------

if __name__=='__main__':
    print("Bienvenue dans le jeu de dames")
    p=initialisePlateau(10)
    jouer(p)
