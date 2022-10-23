#!/usr/bin/env python3
"""
nouveau projet, nouvelle idée
"""
import sys
from random import uniform
from math import sqrt

#couleurs qu'on va utiliser
ROUGE = '255 0 0'
BLEU = '0 0 255'
BLANC = '255 255 255'
VERT = '0 255 0'
NOIR = '0 0 0'

class Point:
    """
    une classe des points colorés
    """
    def __init__(self, abscisse, ordonnee, couleur: str):
        """
         un point ici est defini par ses coordonnées cartesiennes, et pas sa couleur
        """
        self.abscisse = abscisse
        self.ordonnee = ordonnee
        self.couleur = couleur
    def contient(self, rayon):
        """
        verifie si le point est dans le cercle de rayon 'rayon' ou non
        """
        return sqrt(self.abscisse**2+self.ordonnee**2) <= rayon
    def colorer(self, rayon, couleur_1, couleur_2):
        """
        colore le point selon son appartenance au cercle de rayon
        """
        #Dans notre cas, appartient au cercle veut dire est dans le cercle
        if self.contient(rayon):
            self.couleur = couleur_1
        else:
            self.couleur = couleur_2
        return self

def monte_carlo(nombre_points):
    """
    Retourne l'approximation de pi et génère les points avec lesquels on l'a calculée
    """
    compteur = 0
    for _ in range(nombre_points):
        point = Point(uniform(-1, 1), uniform(-1, 1), None)
        point.colorer(1, ROUGE, BLEU)
        if point.couleur == ROUGE:
            compteur += 1
        yield point
    approximation = 4*compteur/nombre_points
    yield approximation

def main():
    """main function"""
    nombre_points = int(sys.argv[1])
    generateur = monte_carlo(nombre_points)
    for _ in range(nombre_points+1):
        approximation = next(generateur)
    print(approximation)

if __name__ == '__main__':
    main()
