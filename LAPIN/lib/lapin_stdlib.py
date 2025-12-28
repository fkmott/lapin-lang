#!/usr/bin/env python3
"""
Bibliothèque standard LAPIN
"""

import math
import random
import time
import os
import sys

class LapinStdLib:
    """Fonctions standard pour LAPIN"""

    @staticmethod
    def afficher(*args):
        """Affiche des valeurs avec saut de ligne"""
        print(" ".join(str(arg) for arg in args))

    @staticmethod
    def ecrire(*args):
        """Écrit des valeurs sans saut de ligne"""
        print(" ".join(str(arg) for arg in args), end="")

    @staticmethod
    def lire():
        """Lit une ligne depuis l'entrée"""
        return input()

    @staticmethod
    def lire_nombre():
        """Lit un nombre depuis l'entrée"""
        while True:
            try:
                return float(input())
            except ValueError:
                print("Nombre invalide. Réessayez: ", end="")

    @staticmethod
    def longueur(chaine_ou_liste):
        """Retourne la longueur d'une chaîne ou liste"""
        return len(chaine_ou_liste)

    @staticmethod
    def liste(*elements):
        """Crée une nouvelle liste"""
        return list(elements)

    @staticmethod
    def ajouter(liste, element):
        """Ajoute un élément à une liste"""
        liste.append(element)
        return liste

    @staticmethod
    def enlever(liste, index):
        """Enlève un élément d'une liste"""
        if 0 <= index < len(liste):
            return liste.pop(index)
        return None

    @staticmethod
    def obtenir(liste, index):
        """Obtient un élément d'une liste"""
        if 0 <= index < len(liste):
            return liste[index]
        return None

    @staticmethod
    def definir(liste, index, valeur):
        """Définit un élément d'une liste"""
        if 0 <= index < len(liste):
            liste[index] = valeur
        return liste

    @staticmethod
    def nombre_aleatoire(min_val=0, max_val=1):
        """Retourne un nombre aléatoire"""
        if isinstance(min_val, int) and isinstance(max_val, int):
            return random.randint(min_val, max_val)
        return random.uniform(min_val, max_val)

    @staticmethod
    def attendre(secondes):
        """Attend un nombre de secondes"""
        time.sleep(secondes)

    @staticmethod
    def maintenant():
        """Retourne l'heure actuelle"""
        return time.strftime("%H:%M:%S")

    @staticmethod
    def date():
        """Retourne la date actuelle"""
        return time.strftime("%d/%m/%Y")

    @staticmethod
    def texte_en_nombre(texte):
        """Convertit un texte en nombre"""
        try:
            if '.' in texte:
                return float(texte)
            return int(texte)
        except:
            return 0

    @staticmethod
    def nombre_en_texte(nombre):
        """Convertit un nombre en texte"""
        return str(nombre)

    @staticmethod
    def majuscules(texte):
        """Convertit en majuscules"""
        return texte.upper()

    @staticmethod
    def minuscules(texte):
        """Convertit en minuscules"""
        return texte.lower()

    @staticmethod
    def arrondir(nombre, decimales=0):
        """Arrondit un nombre"""
        return round(nombre, decimales)

    @staticmethod
    def absolu(nombre):
        """Valeur absolue"""
        return abs(nombre)

    @staticmethod
    def racine(nombre):
        """Racine carrée"""
        return math.sqrt(nombre) if nombre >= 0 else 0

    @staticmethod
    def puissance(base, exposant):
        """Puissance"""
        return base ** exposant

    @staticmethod
    def est_nombre(valeur):
        """Vérifie si c'est un nombre"""
        return isinstance(valeur, (int, float))

    @staticmethod
    def est_texte(valeur):
        """Vérifie si c'est un texte"""
        return isinstance(valeur, str)

    @staticmethod
    def est_liste(valeur):
        """Vérifie si c'est une liste"""
        return isinstance(valeur, list)

    @staticmethod
    def executer_fichier(nom_fichier):
        """Exécute un autre fichier LAPIN"""
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return ""