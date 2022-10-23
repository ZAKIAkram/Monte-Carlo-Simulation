#!/usr/bin/env python3
"""
le module Draw , qui génère le gif de pi et les dix images
"""
import sys
import subprocess
from collections import namedtuple
from math import ceil
from copy import deepcopy
import approximate_pi

ROUGE = '255 0 0'
BLEU = '0 0 255'
BLANC = '255 255 255'
VERT = '0 255 0'
NOIR = '0 0 0'

Pixel = namedtuple("pixel", "x y couleur")

class Image:
    """
    UNe classe des images sous forme d'UNe liste
    """
    def __init__(self, taille_image, couleur):
        """constructeur"""
        self.taille = taille_image
        self.couleur = couleur
        self.matrice = [couleur for i in range(taille_image**2)]

    def __str__(self):
        """print(Image())"""
        return f"c'est UNe image carrée de taille {self.taille} et de couleur {self.couleur}"
    def iterator(self):
        """retourn un iterateur"""
        return iter(self.matrice)

    def ajouter_pixel(self, pixel):
        """ajouter UNe couleur d'UN pixel dans la matrice à sa position"""
        self.matrice[(pixel.x-1)*self.taille+(pixel.y-1)] = pixel.couleur


#présentation des chiffres en 7 segments
# les indices (des listes des booléens) sont les suivants:
#               ###0###
#               #     #
#               5     1
#               #     #
#               ###6###
#               #     #
#               4     2
#               #     #
#               ###3###

ZERO = [True, True, True, True, True, True, False]
UN = [False, True, True, False, False, False, False]
DEUX = [True, True, False, True, True, False, True]
TROIS = [True, True, True, True, False, False, True]
QUATRE = [False, True, True, False, False, True, True]
CINQ = [True, False, True, True, False, True, True]
SIX = [True, False, True, True, True, True, True]
SEPT = [True, True, True, False, False, False, False]
HUIT = [True, True, True, True, True, True, True]
NEUF = [True, True, True, True, False, True, True]
VIRGULE = [False, False, False, True, False, False, False]

DIC_CHIFFRES = {'0': ZERO,
                '1': UN,
                '2': DEUX,
                '3': TROIS,
                '4': QUATRE,
                '5': CINQ,
                '6': SIX,
                '7': SEPT,
                '8': HUIT,
                '9': NEUF,
                '.': VIRGULE
                }


def segments(taille_image):
    """retourne les paramètres des segments"""
    #la longueur du segment
    longueur_segment = int(taille_image*0.0225)
    #la largeur du segment
    largeur_segment = int(taille_image*0.00375)
    #longueur de la VIRGULE:
    longueur_virgule = int(taille_image*0.01125)
    #largeur de la VIRGULE
    largeur_virgule = int(taille_image*0.0075)
    return longueur_segment, largeur_segment, longueur_virgule, largeur_virgule


def coordonnees_afficheur(taille_image, chiffres_virgule):
    """
    retourne les coordonnees du premier pixel (celui en haut à gauche) du premier chiffre,
    c'est 3 dans notre cas
    """
    #première coordonnée du premier pixel NOIR
    premiere_ligne = int(taille_image*0.48)
    #afin de centrer le nombre pi dans l'image, on distingue les cas suivant
    if chiffres_virgule == 5:
        premiere_colonne = int(taille_image*0.35)
    elif chiffres_virgule == 4:
        premiere_colonne = int(taille_image*0.41)
    elif chiffres_virgule == 3:
        premiere_colonne = int(taille_image*0.43)
    elif chiffres_virgule == 2:
        premiere_colonne = int(taille_image*0.45)
    elif chiffres_virgule == 1:
        premiere_colonne = int(taille_image*0.47)
    return premiere_ligne, premiere_colonne

def division_zero(entier_1, entier_2):
    """
    c'est un fonction qui retourne zero quand on a une division par zero
    """
    try:
        return entier_1/entier_2
    except ZeroDivisionError:
        return 0

def afficher_chiffre(chiffre: list, image: Image, position, chiffres_virgule):
    """affiche un seul chiffre """
    taille_image = image.taille
    longueur_segment, largeur_segment = segments(taille_image)[0], segments(taille_image)[1]
    premiere_ligne, premiere_colonne = coordonnees_afficheur(taille_image, chiffres_virgule)
    espace = int(taille_image*0.00375)
#trace les indices 0, 6 et 3 horizontaux
    for _ in (0, 6, 3):
        if chiffre[_]:
            for k in range(premiere_ligne + int(division_zero(6, _)) * longueur_segment,
                           premiere_ligne + int(division_zero(6, _)) *
                           longueur_segment +largeur_segment + 1):
                for j in range(2 * position + premiere_colonne + largeur_segment, 2 * position +
                               premiere_colonne + longueur_segment + largeur_segment +  1):
                    image.ajouter_pixel(Pixel(k, j, NOIR))
#trace les segments d'indices 1 et 2 verticaux à droite
    for _ in range(1, 3):
        if chiffre[_]:
            for k in range(premiere_ligne + (_ - 1) * longueur_segment,
                           premiere_ligne + _ * longueur_segment + largeur_segment + 1):
                for j in range(2 * position + premiere_colonne + longueur_segment,
                               2 * position + premiere_colonne + longueur_segment +
                               largeur_segment + 1):
                    image.ajouter_pixel(Pixel(k, j, NOIR))
    for _ in range(4, 6):
        #trace les segments 4 et 5 (verticaux) à gauche
        if chiffre[_]:
            for k in range(premiere_ligne + (5 - _) * longueur_segment,
                           premiere_ligne + (6 - _) * longueur_segment + largeur_segment + 1):
                for j in range(2* position + premiere_colonne,
                               2 * position + premiere_colonne + largeur_segment + 1):
                    image.ajouter_pixel(Pixel(k, j, NOIR))
    position += longueur_segment + espace
    return position

def afficher_virgule(image: Image, position, chiffres_virgule):
    """affiche la virgule dans l'image"""
    taille_image = image.taille
    longueur_segment, longueur_virgule = segments(taille_image)[0], segments(taille_image)[2]
    largeur_virgule = segments(taille_image)[3]
    #les coordonnées sont toujours ceux du premier pixel (pas de la virgule)
    premiere_ligne, premiere_colonne = coordonnees_afficheur(taille_image, chiffres_virgule)
    espace = int(taille_image*0.00375)
    for k in range(premiere_ligne + 2 * longueur_segment - largeur_virgule, premiere_ligne +
                   2 * longueur_segment):
        for j in range(2 * position + premiere_colonne, 2 * position +
                       premiere_colonne + longueur_virgule + 1):
            image.ajouter_pixel(Pixel(k, j, NOIR))
    position += longueur_virgule + espace
    return position

def afficheur_7segments(chaine_nombre: str, image: Image, chiffres_virgule):
    """ la fonction qui permet de tracer le nombre pi à l'aide de l'affichage 7 segments"""
    #longueur de la troncature
    longueur_chaine = len(chaine_nombre)
    #la position du premier chiffre, dans notre cas, le premier chiffre est 3
    position = 0
    #espace entre les chiffres
    for i in range(longueur_chaine):
        if DIC_CHIFFRES[chaine_nombre[i]] == VIRGULE:
            position = afficher_virgule(image, position, chiffres_virgule)
        else:
            position = afficher_chiffre(DIC_CHIFFRES[chaine_nombre[i]], image,
                                        position, chiffres_virgule)

def transformer_point(point: approximate_pi.Point, taille_image):
    """
    la focntion qui transforme UN point en UN pixel
    """
    #mise à échelle des abscisses
    echelle_x = 2/taille_image
    #mise à echelle des ordonnées (le nouvel axe  se dirige vers bas)
    echelle_y = -2/taille_image
    pixel = Pixel(ceil((point.abscisse+1)/echelle_x),
                  ceil((point.ordonnee-1)/echelle_y), point.couleur)
    return pixel

def generate_ppm_file(numero_image, image: Image, nombre_points, chiffres_virgule):
    """
    c'est la fonction qui génère UNe image ppm
    """
    generateur = approximate_pi.monte_carlo(nombre_points)
    taille_image = image.taille
    for _ in range(nombre_points):
        image.ajouter_pixel(transformer_point(next(generateur), taille_image))
    approximation_pi = next(generateur)
    image_copie = deepcopy(image)
    pi_titre = f"{approximation_pi:.{chiffres_virgule}f}"
    new_pi = pi_titre.replace('.', '-')
    with open(f'img{numero_image -1}_{new_pi}.ppm', 'w') as fichier:
        fichier.write('P3\n')
        fichier.write(f'{taille_image} {taille_image}\n')
        fichier.write('255\n')
        afficheur_7segments(pi_titre, image_copie, chiffres_virgule)
        for _ in range(taille_image ** 2):
            fichier.write(image_copie.matrice[_]+'\n')

def main():
    """
    main function
    """
    if len(sys.argv) != 4 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print('utilisation:', sys.argv[0], 'taille_image nombre_points chiffres_après_virgule')
        sys.exit()
    try:
        taille_image = int(sys.argv[1])
        nombre_points = int(sys.argv[2])
        chiffres_virgule = int(sys.argv[3])
    except TypeError:
        print('Veuillez entrez des entiers')
    if taille_image < 100:
        raise ValueError(' Entrez un nombre >= 100')
    if nombre_points < 100:
        raise ValueError(' Entrez un nombre >= 100')
    if not 1 <= chiffres_virgule <= 5:
        raise ValueError(' Entrez un nombre entre 1 et 5')
    image = Image(taille_image, BLANC)
    for i in range(1, 11):
        generate_ppm_file(i, image, int(nombre_points * 0.1), chiffres_virgule)
    print('génération du GIF')
    subprocess.call('convert -delay 100 img*.ppm pi.gif', shell=True)

if __name__ == '__main__':
    main()
