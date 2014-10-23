from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.properties import (ListProperty, NumericProperty)

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner

# Import utilise pour l'interface.
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window


class Bouton(Button):
	coords = ListProperty([0, 0]) #deifinition du format des coordonnées (ligne/colonne)
	
class GrilleHalma(GridLayout):
	plateau_jeu = [ #definition de plateau de jeu
	1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 
	1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 
	1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 
	1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
	4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 
	4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 
	4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3,
	4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 
	]

	joueur_actuel = NumericProperty(1) #joueur qui a la main

	def __init__(self, *args, **kwargs):
		
		super(GrilleHalma, self).__init__(*args, **kwargs)
		#definition des couleurs, au format R,G,B,A, 0 designant une case vide, les chiffres allant de 1 à 4 parce que 4 joueurs
		fond = {0: ('img/btns/b0.png'), 1: ('img/btns/b1.png'), 2: ('img/btns/b2.png'),3: ('img/btns/b3.png'),4: ('img/btns/b4.png'),5: ('img/btns/b5.png')}
		#construction initiale du plateau, à partir de la liste "plateau de jeu"
		for ligne in range(16):
			for colonne in range(16):
				bouton = Bouton(coords=(ligne, colonne), size=(50,50)) #creation d'un widget Bouton
				bouton.bind(on_release=self.bouton_enfonce) #gestion de l'évenement, ici, "on_release" (au clic)
				bouton.background_normal = fond[self.plateau_jeu[16*ligne+colonne]] #coloration du bouton
				bouton.background_down = 'img/btns/b_au_clic.png' #coloration du bouton au clic
				self.add_widget(bouton) #ajout du widget (le bouton) au plateau
		
		fond2 = {1: (1, 0, 0, 1), 2: (0, 1, 0, 1),3: (1, 1, 0, 1),4: (0, 0, 1, 1)} #couleur du fond
		Window.clearcolor = fond2[self.joueur_actuel] # l'arrière plan a la couleur du pion qui doit jouer

	def bouton_enfonce(self, button):		
		ligne, colonne = button.coords # definition de ligne et colonnes, qui sont les coordonnées du bouton 	
		self.afficherPlateau()
		bouton_selectionne = self.plateau_jeu[16*ligne + colonne]
		pionDeplace = 0

		if bouton_selectionne == self.joueur_actuel: #si le clic est effectué sur un pion appartenant au joueur en cours
			self.masquerDeplacementsPossibles(ligne,colonne,0) # on efface toutes les anciennes propositions de deplacement (en bleu ciel)
			self.activerDeplacementsPossibles(ligne,colonne) # on affiche les propositions liées au bouton selectionné
			self.afficherPlateau() # on réaffiche le plateau 

		elif bouton_selectionne == 5: # si le clic est effectué sur une case de déplacement possible	
			self.masquerDeplacementsPossibles(ligne,colonne,1) # on masque les propositions de deplacement / efface l'ancienne position du pion(arguement "1")		
			self.plateau_jeu[16*ligne + colonne] = self.joueur_actuel
			self.afficherPlateau() # on affiche le plateau	
			pionDeplace = 1 # on signale qu'un pion a été déplacé, le tour de jeu va changer
			
		if pionDeplace == 1: # si un pion est deplacé, le tour de jeu change	

			self.joueur_actuel += 1
			if self.joueur_actuel > 4: # si le dernier joueur a joué, on recommence au joueur 1 
		  		self.joueur_actuel = 1		
		  		pionSelectionne = 0	
				
			fond2 = {1: (1, 0, 0, 1), 2: (0, 1, 0, 1),3: (1, 1, 0, 1),4: (0, 0, 1, 1)} #couleur du fond					
			Window.clearcolor = fond2[self.joueur_actuel] #on affecte la couleur du joueur courant au fond d'écran du jeu  	
			pionDeplace = 0
			self.verifierGagnant() # on vérifie si un joueur a gagné			

	def afficherPlateau(self):
		self.clear_widgets() # efface tout le plateau
		fond = {0: ('img/btns/b0.png'), 1: ('img/btns/b1.png'), 2: ('img/btns/b2.png'),3: ('img/btns/b3.png'),4: ('img/btns/b4.png'),5: ('img/btns/b5.png')} #couleur des pions
		fond_selectionne = {-1: ('img/btns/b1_pressed.png'), -2: ('img/btns/b2_pressed.png'),-3: ('img/btns/b3_pressed.png'),-4: ('img/btns/b4_pressed.png')} # couleurs des pions au clic

		# réaffichage du plateau (cf __init__)
		for ligne in range(16):
			
			for colonne in range(16):
				bouton = Bouton(coords=(ligne, colonne))
				bouton.bind(on_release=self.bouton_enfonce)
				plateau_jeu_index = self.plateau_jeu[16*ligne+colonne]
				if self.plateau_jeu[16*ligne+colonne] >= 0 :
					bouton.background_normal = fond[self.plateau_jeu[16*ligne+colonne]] #coloration du bouton
									
				else :
					bouton.background_normal = fond_selectionne[plateau_jeu_index]
				bouton.background_down = 'img/btns/b_au_clic.png'
				self.add_widget(bouton)


	def activerDeplacementsPossibles(self,ligne,colonne):
			
		if colonne != 15:		
			if self.plateau_jeu[16*ligne+colonne+1] == 0: # déplacement possible A DROITE
				self.plateau_jeu[16*ligne+colonne+1] = 5
				
		if colonne != 0:	
			if self.plateau_jeu[16*ligne+colonne-1] == 0:  #déplacement possible A GAUCHE
				self.plateau_jeu[16*ligne+colonne-1] = 5
				
		if ligne != 0:  											         #### déplacement EN HAUT
			if self.plateau_jeu[16*(ligne-1)+colonne] == 0:
				self.plateau_jeu[16*(ligne-1)+colonne] = 5	
		
			if colonne != 15:                                                   # déplacement HAUT / DROITE
				if self.plateau_jeu[16*(ligne-1)+colonne+1] == 0: 
					self.plateau_jeu[16*(ligne-1)+colonne+1] = 5
			
			if colonne != 0:													# déplacement HAUT / GAUCHE
				if self.plateau_jeu[16*(ligne-1)+colonne-1] == 0:  
					self.plateau_jeu[16*(ligne-1)+colonne-1] = 5						

		if ligne != 15:                                                 	##### déplacement possible EN BAS
			if self.plateau_jeu[16*(ligne+1)+colonne] == 0:   
				self.plateau_jeu[16*(ligne+1)+colonne] = 5
				
			if colonne != 15:
				if self.plateau_jeu[16*(ligne+1)+colonne+1] == 0 : # déplacement BAS / DROITE
					self.plateau_jeu[16*(ligne+1)+colonne+1] = 5
				
			if colonne != 0:
				if self.plateau_jeu[16*(ligne+1)+colonne-1] == 0 :  # déplacement BAS / GAUCHE
					self.plateau_jeu[16*(ligne+1)+colonne-1] = 5			

		self.plateau_jeu[16*ligne+colonne] = -(self.plateau_jeu[16*ligne+colonne]) # le pion selectionné passe en mode "selectionne", sa couleur va changer
	
		self.activerSautsPossibles(ligne,colonne)	



	def masquerDeplacementsPossibles(self,ligne,colonne,pionDeplace):
		for ligne in range(16):
			for colonne in range(16):
			
				if self.plateau_jeu[16*ligne+colonne] == 5: #si la case vaut 5 (possibilités de déplacement) ou 6 (possibilités de saut)
					self.plateau_jeu[16*ligne+colonne] = 0 # elle est vidée (vaut 0)

				elif self.plateau_jeu[16*ligne+colonne] < 0 and pionDeplace == 1: # si la case contient un pion selectionné ET le pion a été déplacé
					self.plateau_jeu[16*ligne+colonne] = 0 # elle est vidée (0)

				elif self.plateau_jeu[16*ligne+colonne] < 0 and pionDeplace == 0: #si la case contient un pion selectionné ET le pion n'a pas été déplacé
					self.plateau_jeu[16*ligne+colonne] = -(self.plateau_jeu[16*ligne+colonne]) # elle retrouve sa valeur initiale (deselection)
					
	def activerSautsPossibles(self,ligne,colonne):
		
		if colonne != 14 and colonne != 15:		
			if self.plateau_jeu[16*ligne+colonne+1] != 5 and self.plateau_jeu[16*ligne+colonne+1] != 0 and self.plateau_jeu[16*ligne+colonne+2] == 0: # saut possible A DROITE
				self.plateau_jeu[16*ligne+colonne+2] = 5
				self.activerSautsPossibles(ligne,colonne+2)
				
		if colonne != 0 and colonne != 1:	
			if self.plateau_jeu[16*ligne+colonne-1] != 5 and self.plateau_jeu[16*ligne+colonne-1] != 0 and self.plateau_jeu[16*ligne+colonne-2] == 0:  # saut possible A GAUCHE
				self.plateau_jeu[16*ligne+colonne-2] = 5
				self.activerSautsPossibles(ligne,colonne-2)
				
		if ligne != 0 and ligne != 1:  										    #### saut EN HAUT
			if self.plateau_jeu[16*(ligne-1)+colonne] != 5 and self.plateau_jeu[16*(ligne-1)+colonne] != 0 and self.plateau_jeu[16*(ligne-2)+colonne] == 0:
				self.plateau_jeu[16*(ligne-2)+colonne] = 5	
				self.activerSautsPossibles(ligne-2,colonne)
		
			if colonne != 14 and colonne != 15:                                                   # saut HAUT / DROITE
				if self.plateau_jeu[16*(ligne-1)+colonne+1] != 5 and self.plateau_jeu[16*(ligne-1)+colonne+1] != 0 and self.plateau_jeu[16*(ligne-2)+colonne+2] == 0: 
					self.plateau_jeu[16*(ligne-2)+colonne+2] = 5
					self.activerSautsPossibles(ligne-2,colonne+2)
			
			if colonne != 0 and colonne != 1:													# saut HAUT / GAUCHE
				if self.plateau_jeu[16*(ligne-1)+colonne-1] != 5 and self.plateau_jeu[16*(ligne-1)+colonne-1] != 0 and self.plateau_jeu[16*(ligne-2)+colonne-2] == 0:  
					self.plateau_jeu[16*(ligne-2)+colonne-2] = 5
					self.activerSautsPossibles(ligne-2,colonne-2)

		if ligne != 15 and ligne != 14:                                                 	##### saut possible EN BAS
			if self.plateau_jeu[16*(ligne+1)+colonne] != 5 and self.plateau_jeu[16*(ligne+1)+colonne] != 0 and self.plateau_jeu[16*(ligne+2)+colonne] == 0:   
				self.plateau_jeu[16*(ligne+2)+colonne] = 5
				self.activerSautsPossibles(ligne+2,colonne)
				
			if colonne != 14 and colonne != 15:
				if self.plateau_jeu[16*(ligne+1)+colonne+1] != 5 and self.plateau_jeu[16*(ligne+1)+colonne+1] != 0 and self.plateau_jeu[16*(ligne+2)+colonne+2] == 0: # saut BAS / DROITE
					self.plateau_jeu[16*(ligne+2)+colonne+2] = 5
					self.activerSautsPossibles(ligne+2,colonne+2)
				
			if colonne != 0 and colonne != 1:
				if self.plateau_jeu[16*(ligne+1)+colonne-1] != 5 and self.plateau_jeu[16*(ligne+1)+colonne-1] != 0 and self.plateau_jeu[16*(ligne+2)+colonne-2] == 0 :  # saut BAS / GAUCHE
					self.plateau_jeu[16*(ligne+2)+colonne-2] = 5
					self.activerSautsPossibles(ligne+2,colonne-2)

	def verifierGagnant(self):
			
		# si tous les pions rouges sont arrivés
		if self.plateau_jeu[206] == 1 and self.plateau_jeu[207] == 1 and self.plateau_jeu[221] == 1 and self.plateau_jeu[222] == 1 and self.plateau_jeu[223] == 1 and self.plateau_jeu[236] == 1 and self.plateau_jeu[237] == 1 and self.plateau_jeu[238] == 1 and self.plateau_jeu[239] == 1 and self.plateau_jeu[252] == 1 and self.plateau_jeu[253] == 1 and self.plateau_jeu[254] == 1 and self.plateau_jeu[255] == 1:
			popup = ModalView(size_hint=(0.6, 0.2))		
			victory_label = Label(text='Le joueur rouge a gagné !',font_size=30)		
			Window.clearcolor = (1, 1, 0, 1)
			popup.add_widget(victory_label)
			popup.bind(on_dismiss=self.reset) # lorsque le pop-up est fermée, on reset le plateau
			popup.open() # on ouvre la pop-up de victoire
		
		# si tous les pions verts sont arrivés
		if self.plateau_jeu[192] == 2 and self.plateau_jeu[193] == 2 and self.plateau_jeu[208] == 2 and self.plateau_jeu[209] == 2 and self.plateau_jeu[210] == 2 and self.plateau_jeu[224] == 2 and self.plateau_jeu[225] == 2 and self.plateau_jeu[226] == 2 and self.plateau_jeu[227] == 2 and self.plateau_jeu[240] == 2 and self.plateau_jeu[241] == 2 and self.plateau_jeu[242] == 2 and self.plateau_jeu[243] == 2:
			popup = ModalView(size_hint=(0.6, 0.2))		
			victory_label = Label(text='Le joueur vert a gagné !',font_size=30)		
			Window.clearcolor = (1, 1, 0, 1)
			popup.add_widget(victory_label)
			popup.bind(on_dismiss=self.reset) # lorsque le pop-up est fermée, on reset le plateau
			popup.open() # on ouvre la pop-up de victoire
		
		# si tous les pions jaunes sont arrivés		
		if self.plateau_jeu[0] == 3 and self.plateau_jeu[1] == 3 and self.plateau_jeu[2] == 3 and self.plateau_jeu[3] == 3 and self.plateau_jeu[16] == 3 and self.plateau_jeu[17] == 3 and self.plateau_jeu[18] == 3 and self.plateau_jeu[19] == 3 and self.plateau_jeu[32] == 3 and self.plateau_jeu[33] == 3 and self.plateau_jeu[34] == 3 and self.plateau_jeu[48] == 3 and self.plateau_jeu[49] == 3:
			popup = ModalView(size_hint=(0.6, 0.2))		
			victory_label = Label(text='Le joueur jaune a gagné !',font_size=30)		
			Window.clearcolor = (1, 1, 0, 1)
			popup.add_widget(victory_label)
			popup.bind(on_dismiss=self.reset) # lorsque le pop-up est fermée, on reset le plateau
			popup.open() # on ouvre la pop-up de victoire	
			
		# si tous les pions bleus sont arrivés
		if self.plateau_jeu[62] == 4 and self.plateau_jeu[63] == 4 and self.plateau_jeu[45] == 4 and self.plateau_jeu[46] == 4 and self.plateau_jeu[47] == 4 and self.plateau_jeu[28] == 4 and self.plateau_jeu[29] == 4 and self.plateau_jeu[30] == 4 and self.plateau_jeu[31] == 4 and self.plateau_jeu[12] == 4 and self.plateau_jeu[13] == 4 and self.plateau_jeu[14] == 4 and self.plateau_jeu[15] == 4:
			popup = ModalView(size_hint=(0.6, 0.2))		
			victory_label = Label(text='Le joueur bleu a gagné !',font_size=30)		
			Window.clearcolor = (1, 1, 0, 1)
			popup.add_widget(victory_label)
			popup.bind(on_dismiss=self.reset) # lorsque le pop-up est fermée, on reset le plateau
			popup.open()
						
	def reset(self, *args):
		self.plateau_jeu = [ #réinisialisation de plateau de jeu
		1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 
		1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 
		1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 
		1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
		4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 
		4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 
		4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3,
		4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 
		]
		self.joueur_actuel = 1
		Window.clearcolor = (1, 0, 0, 1) #réinitialisation du fond
		self.afficherPlateau()
		


class Interface(BoxLayout):
	pass

class HalmaApp(App):
	def build(self):
		self.icon = 'icon.ico'
		self.title = 'Halma'

		return Interface()

class ScreenManagerApp(App):
	pass	
		
if __name__ == '__main__':
		HalmaApp().run()
	
