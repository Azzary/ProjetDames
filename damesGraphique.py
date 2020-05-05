#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
   Projet Dames 2020 - Licence Informatique UNC

   Programme principal du jeu de dames en mode graphique
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from dames import *
import pygame
import time
import sys
import os


AUCUNE=0
ALPHA=1
NUMERIQUE=2

class DamesGraphique(object):#OK
    """Classe simple d'affichage et d'interaction pour le jeu de dames."""

    def __init__(self, plateau, titre="Jeu de dames de l'UNC", size=(1000, 800), couleur=(209,238,238),prefixeImage="./images"):
        """Method docstring."""
        self.messageInfo=None
        self.plateau=plateau
        self.plateau[5][6] = 12
        self.joueurCourant=2
        self.priseMultiple=[]
        self.fini=False
        self.couleurTexte=couleur
        self.dim=len(self.plateau)
        self.titre=titre
        pygame.init()
		#lecture du logo de l'UNC
        self.icone=pygame.image.load(os.path.join(prefixeImage,'logo.jpeg'))
        pygame.display.set_icon(self.icone)
        fenetre = pygame.display.set_mode(size,pygame.RESIZABLE|pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface=pygame.display.get_surface()
        self.miseAjourParametres()
        self.afficheJeu()

    def miseAjourParametres(self):
        """
        permet de mettre à jour les paramètre d'affichage en cas de redimensionnement de la fenêtre
        """
        self.surface=pygame.display.get_surface()
        self.hauteur=self.surface.get_height()*9//10
        self.largeur=self.hauteur
        self.deltah=self.hauteur//(self.dim+2)
        self.deltal=self.largeur//(self.dim+2)
        self.finh=self.deltah*(self.dim+1)
        self.finl=self.deltal*(self.dim+1)
        self.tailleFont=min(self.deltah,self.deltal)*1//2

    def afficheMessage(self,ligne,texte,images=[],couleur=None):
        """
        affiche un message en mode graphique à l'écran
        """
        font = pygame.font.Font(None, self.tailleFont)
        if couleur==None:
            couleur=self.couleurTexte
        posy=self.finh+self.deltah*(ligne-1)
        posx=self.deltal//3

        listeTextes=texte.split('@img@')
        for msg in listeTextes:
            if msg!='':
                texte=font.render(msg,1,couleur)
                textpos=texte.get_rect()
                textpos.y=posy
                textpos.x=posx
                self.surface.blit(texte,textpos)
                posx+=textpos.width
            if images!=[]:
                surface=images.pop(0)
                debuty= posy-(self.deltah//3)
                self.surface.blit(surface,(posx,debuty))
                posx+=surface.get_width()

    def afficheMessageInfo(self,numLigne=2):
        """
        affiche un message d'information aux joueurs
        """
        if self.messageInfo!=None:
            self.afficheMessage(numLigne,self.messageInfo,self.imgInfo)
        self.messageInfo=None
        self.imgInfo=None

    def affichePlateau(self,prefixImage="./images",x=None,y=None):
        """
        affiche le plateau
        """
        diff=7 # réduction de la taille des pions
        for i in range(self.dim):
            for j in range(self.dim):
                #try:
                    #carte=getVal(self.laMatrice,i,j)
                    #s=self.surfaceCarte(carte)
                    #if s==None:
                    #    self.surface.fill((0,0,0),((j+1)*self.deltal,(i+1)*self.deltah,self.deltal,self.deltah))
                    #else:
				#affichage de la case blanc/noir=====================================
                if (i+j)%2 :
                    img=pygame.image.load(os.path.join(prefixImage,'caseNoire.png'))
                else :
                    img=pygame.image.load(os.path.join(prefixImage,'caseBlanche.png'))
                s=pygame.transform.smoothscale(img,(self.deltal,self.deltah))
                self.surface.blit(s,((j+1)*self.deltal,(i+1)*self.deltah))
				#affichage du pion/dame==============================================
                if plateau[i][j]:
                    if i==x and j==y :
                        if plateau[i][j]==1:
                            img=pygame.image.load(os.path.join(prefixImage,'pionNoirSelection.png'))
                        elif plateau[i][j]==2:
                            img=pygame.image.load(os.path.join(prefixImage,'pionBlancSelection.png'))
                        elif plateau[i][j]==11:
                            img=pygame.image.load(os.path.join(prefixImage,'dameNoireSelection.png'))
                        elif plateau[i][j]==12:
                            img=pygame.image.load(os.path.join(prefixImage,'dameBlancheSelection.png'))
                    else:
                        if plateau[i][j]==1:
                            img=pygame.image.load(os.path.join(prefixImage,'pionNoir.png'))
                        elif plateau[i][j]==2:
                            img=pygame.image.load(os.path.join(prefixImage,'pionBlanc.png'))
                        elif plateau[i][j]==11:
                            img=pygame.image.load(os.path.join(prefixImage,'dameNoire.png'))
                        elif plateau[i][j]==12:
                            img=pygame.image.load(os.path.join(prefixImage,'dameBlanche.png'))
                        elif plateau[i][j]==-1:
                            img=pygame.image.load(os.path.join(prefixImage,'pionNoirPris.png'))
                        elif plateau[i][j]==-2:
                            img=pygame.image.load(os.path.join(prefixImage,'pionBlancPris.png'))
                        elif plateau[i][j]==-11:
                            img=pygame.image.load(os.path.join(prefixImage,'dameNoirePrise.png'))
                        elif plateau[i][j]==-12:
                            img=pygame.image.load(os.path.join(prefixImage,'dameBlancheprise.png'))
                    s=pygame.transform.smoothscale(img,(self.deltal-diff,self.deltah-diff))
                    self.surface.blit(s,((j+1)*self.deltal+diff//2,(i+1)*self.deltah+diff//2))

    def getCase(self,pos):
        """
        transforme une position de souris en coordonnées de case du plateau.
        Si on clique hors du plateau la fonction retourne (-1,-1)
        si on clique sur une case du plateau la fonction retourne les coordonnées x,y de la case
        """
        if pos[0]<0 or pos[0]>self.finl or pos[1]<0 or pos[1]>self.finh:
            return (-1,-1)
        x=pos[1]//self.deltah
        y=pos[0]//self.deltal
        return (x-1,y-1)

    def afficheJeu(self,x=None,y=None):
        """
        affiche l'ensemble du jeu (plateau + message)
        """
        self.surface.fill((0,0,0))
        self.affichePlateau(x=x,y=y)
        self.afficheMessageInfo(2)
        pygame.display.flip()

    def demarrer(self):
        """
        démarre l'environnement graphique et la boucle d'écoute des événements
        """
        self.joueurCourant=2
        self.phase=1#choisir un pion
        pygame.time.set_timer(pygame.USEREVENT+1,100)
        while(True):
            ev=pygame.event.wait()
            if ev.type in (pygame.QUIT, pygame.KEYDOWN):
                break
            if ev.type==pygame.USEREVENT+1:
                pygame.display.flip()
            if ev.type==pygame.VIDEORESIZE:
                fenetre=pygame.display.set_mode(ev.size,pygame.RESIZABLE|pygame.DOUBLEBUF)
                self.miseAjourParametres()
                self.afficheJeu()
            if ev.type==pygame.MOUSEBUTTONDOWN:
                if self.fini:
                    continue
                (a,b)=self.getCase(ev.pos)
                if self.phase==1:#choix d'un pion
                    x,y=a,b
                    res=verifierPionChoisi(self.plateau, self.joueurCourant, x, y)
                    if res==0:
                        self.messageInfo="Saisie incorrecte"
                        self.imgInfo=[]
                    elif res==1:
                        self.messageInfo="Veuillez cliquer sur une case noire"
                        self.imgInfo=[]
                    elif res==2:
                        self.messageInfo="Il n'y a pas de pion "+('blanc' if self.joueurCourant==2 else 'noir')+" sur cette case"
                        self.imgInfo=[]
                    elif res==3:
                        self.messageInfo="Ce pion ne peut pas bouger"
                        self.imgInfo=[]
                    elif res==4:
                        self.messageInfo="Rappel de règle : la prise est obligatoire"
                        self.imgInfo=[]
                    elif res==5:
                        self.messageInfo="Rappel de règle : la prise majoritaire est obligatoire"
                        self.imgInfo=[]
                    if res not in [10]:
                        x,y=None,None
                    else:
                        self.phase=2
                else: # on est dans la phase 2
                    z,t=a,b
                    res=realiserAction(self.plateau,self.joueurCourant,x,y,z,t,self.priseMultiple)
                    if res==0:
                        self.messageInfo="Saisie incorrecte"
                        self.imgInfo=[]
                    elif res==1:
                        self.messageInfo="Ce déplacement n'est pas permis"
                        self.imgInfo=[]
                    elif res==4:
                        self.messageInfo="Rappel de règle : la prise est obligatoire"
                        self.imgInfo=[]
                    elif res==5:
                        self.messageInfo="Rappel de règle : la prise majoritaire est obligatoire"
                        self.imgInfo=[]
                    elif res==10:
                        self.messageInfo="Le joueur s'est déplacé"
                        self.imgInfo=[]
                    elif res in [11,12]:
                        self.messageInfo="Le joueur a pris un pion/une dame à son adversaire"
                        self.imgInfo=[]
                    elif res ==13:
                        self.messageInfo="Le joueur a récupéré une dame"
                        self.imgInfo=[]
                    if res==12:
                        x,y=z,t
                    elif res in [10,11,13]:
                        x,y=None,None
                        self.phase=1
                        res2=finDePartie(self.plateau,self.joueurCourant)
                        if res2:
                            self.messageInfo="Le joueur "+('BLANC' if self.joueurCourant==2 else 'NOIR')+" a gagné!"
                            self.imgInfo=[]
                        self.joueurCourant=(1 if self.joueurCourant==2 else 2) #changement de joueur
                self.afficheJeu(x,y)
            pygame.display.flip()
        pygame.quit()


#------------------------------
# programme principal
#------------------------------

if __name__=='__main__':
    print("Bienvenue dans le jeu de dames")
    plateau=initialisePlateau(8)
    #initialisation de l'affichage
    g=DamesGraphique(plateau)
    #démarrage de la partie
    g.demarrer()
