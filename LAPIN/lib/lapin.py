#!/usr/bin/env python3
"""
🐇 Interpréteur du langage LAPIN
Langage d'Apprentissage de la Programmation INtutive
"""

import sys
import os
import re
import math
import random
import json
from datetime import datetime

class LapinInterpreter:
    def __init__(self, debug=False):
        self.variables = {}
        self.functions = {}
        self.output = []
        self.debug_mode = debug
        self.current_line = 0
        self.call_stack = []

        # Fonctions intégrées
        self.builtins = {
            'afficher': self.cmd_afficher,
            'ecrire': self.cmd_ecrire,
            'lire': self.cmd_lire,
            'lire_nombre': self.cmd_lire_nombre,
            'longueur': self.func_longueur,
            'liste': self.func_liste,
            'ajouter': self.func_ajouter,
            'nombre_aleatoire': self.func_nombre_aleatoire,
            'maintenant': self.func_maintenant,
            'texte_en_nombre': self.func_texte_en_nombre,
            'nombre_en_texte': self.func_nombre_en_texte,
            'arrondir': self.func_arrondir,
            'absolu': self.func_absolu,
        }

    def log_debug(self, message):
        if self.debug_mode:
            print(f"[DEBUG] {message}")

    def execute(self, code, filename="<inline>"):
        """Exécute le code LAPIN"""
        try:
            lines = code.split('\n')
            self.output = []

            i = 0
            while i < len(lines):
                self.current_line = i + 1
                line = lines[i].rstrip()

                # Ignorer les lignes vides et commentaires
                if not line or line.strip().startswith('#'):
                    i += 1
                    continue

                # Traitement spécial pour blocs
                if line.strip().startswith('fonction '):
                    i = self.process_function(lines, i)
                    continue
                elif line.strip().startswith('si '):
                    i = self.process_if(lines, i)
                    continue
                elif line.strip().startswith('tant que '):
                    i = self.process_while(lines, i)
                    continue
                elif line.strip().startswith('repeter '):
                    i = self.process_repeat(lines, i)
                    continue
                elif line.strip().startswith('pour chaque '):
                    i = self.process_foreach(lines, i)
                    continue

                # Exécuter une ligne simple
                result = self.execute_line(line.strip())
                if result is not None:
                    self.output.append(str(result))

                i += 1

            return True

        except Exception as e:
            error_msg = f"❌ ERREUR ligne {self.current_line}: {str(e)}"
            self.output.append(error_msg)
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return False

    def execute_line(self, line):
        """Exécute une seule ligne de code"""
        self.log_debug(f"Exécution: {line}")

        # AFFICHER / ÉCRIRE
        if line.startswith('afficher '):
            return self.cmd_afficher(line[9:])
        elif line.startswith('ecrire '):
            return self.cmd_ecrire(line[7:])

        # LECTURE
        elif line.startswith('lire '):
            var_name = line[5:].strip()
            value = self.cmd_lire()
            self.variables[var_name] = value
            return None
        elif line.startswith('lire_nombre '):
            var_name = line[12:].strip()
            value = self.cmd_lire_nombre()
            self.variables[var_name] = value
            return None

        # AFFECTATION
        elif ' = ' in line:
            parts = line.split(' = ', 1)
            var_name = parts[0].strip()
            expression = parts[1].strip()
            value = self.evaluate_expression(expression)
            self.variables[var_name] = value
            self.log_debug(f"Variable '{var_name}' = {value}")
            return None

        # APPEL DE FONCTION
        elif '(' in line and line.endswith(')'):
            func_name = line.split('(', 1)[0].strip()
            args_str = line[line.find('(')+1:line.rfind(')')]
            args = self.parse_arguments(args_str)

            if func_name in self.functions:
                return self.call_function(func_name, args)
            elif func_name in self.builtins:
                return self.builtins[func_name](*args)
            else:
                raise Exception(f"Fonction '{func_name}' non définie")

        # INCLURE
        elif line.startswith('inclure '):
            filename = line[8:].strip().strip('"')
            return self.include_file(filename)

        return None

    def evaluate_expression(self, expr):
        """Évalue une expression"""
        expr = expr.strip()

        # Chaîne littérale
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]

        # Nombre
        if re.match(r'^-?\d+(\.\d+)?$', expr):
            if '.' in expr:
                return float(expr)
            return int(expr)

        # Booléens
        if expr == 'vrai':
            return True
        if expr == 'faux':
            return False

        # Liste
        if expr.startswith('[') and expr.endswith(']'):
            items = expr[1:-1].split(',')
            return [self.evaluate_expression(item.strip()) for item in items if item.strip()]

        # Variable
        if expr in self.variables:
            return self.variables[expr]

        # Opérations mathématiques
        for op, func in [
            ('+', lambda a, b: a + b),
            ('-', lambda a, b: a - b),
            ('*', lambda a, b: a * b),
            ('/', lambda a, b: a / b if b != 0 else 0),
            ('%', lambda a, b: a % b),
            ('^', lambda a, b: a ** b)
        ]:
            if op in expr:
                parts = expr.split(op, 1)
                left = self.evaluate_expression(parts[0].strip())
                right = self.evaluate_expression(parts[1].strip())
                return func(left, right)

        # Comparaisons
        for op, func in [
            ('==', lambda a, b: a == b),
            ('!=', lambda a, b: a != b),
            ('<', lambda a, b: a < b),
            ('<=', lambda a, b: a <= b),
            ('>', lambda a, b: a > b),
            ('>=', lambda a, b: a >= b),
            ('et', lambda a, b: a and b),
            ('ou', lambda a, b: a or b)
        ]:
            if f' {op} ' in expr:
                parts = expr.split(f' {op} ', 1)
                left = self.evaluate_expression(parts[0].strip())
                right = self.evaluate_expression(parts[1].strip())
                return func(left, right)

        raise Exception(f"Expression non reconnue: {expr}")

    # Commandes intégrées
    def cmd_afficher(self, args_str):
        """Affiche du texte avec saut de ligne"""
        value = self.evaluate_expression(args_str)
        # Remplacer les variables dans les chaînes
        if isinstance(value, str):
            for var_name, var_value in self.variables.items():
                value = value.replace(var_name, str(var_value))
        return str(value)

    def cmd_ecrire(self, args_str):
        """Écrit du texte sans saut de ligne"""
        value = self.evaluate_expression(args_str)
        print(str(value), end='', flush=True)
        return None

    def cmd_lire(self):
        """Lit une ligne de texte"""
        return input()

    def cmd_lire_nombre(self):
        """Lit un nombre"""
        while True:
            try:
                return float(input())
            except ValueError:
                print("Veuillez entrer un nombre valide: ", end='')

    def func_longueur(self, obj):
        """Retourne la longueur d'une liste ou chaîne"""
        return len(obj)

    def func_liste(self, *args):
        """Crée une liste"""
        return list(args)

    def func_ajouter(self, liste, element):
        """Ajoute un élément à une liste"""
        liste.append(element)
        return liste

    def func_nombre_aleatoire(self, min_val=0, max_val=1):
        """Génère un nombre aléatoire"""
        if isinstance(min_val, int) and isinstance(max_val, int):
            return random.randint(min_val, max_val)
        return random.uniform(min_val, max_val)

    def func_maintenant(self):
        """Retourne l'heure actuelle"""
        return datetime.now().strftime("%H:%M:%S")

    def func_texte_en_nombre(self, texte):
        """Convertit du texte en nombre"""
        try:
            if '.' in texte:
                return float(texte)
            return int(texte)
        except:
            return 0

    def func_nombre_en_texte(self, nombre):
        """Convertit un nombre en texte"""
        return str(nombre)

    def func_arrondir(self, nombre, decimales=0):
        """Arrondit un nombre"""
        return round(nombre, decimales)

    def func_absolu(self, nombre):
        """Valeur absolue"""
        return abs(nombre)

    def process_function(self, lines, start_idx):
        """Traite la définition d'une fonction"""
        line = lines[start_idx].strip()
        # Format: fonction nom(param1, param2)
        match = re.match(r'fonction (\w+)\((.*?)\)', line)
        if not match:
            raise Exception("Syntaxe de fonction invalide")

        func_name = match.group(1)
        params = [p.strip() for p in match.group(2).split(',') if p.strip()]

        # Trouver le corps de la fonction
        body = []
        i = start_idx + 1
        depth = 1

        while i < len(lines) and depth > 0:
            line = lines[i].strip()
            if line.startswith('fonction ') or line.startswith('si ') or line.startswith('tant que ') or line.startswith('repeter ') or line.startswith('pour chaque '):
                depth += 1
            elif line == 'fin':
                depth -= 1
                if depth == 0:
                    break
            body.append(line)
            i += 1

        if depth != 0:
            raise Exception("Fonction non fermée par 'fin'")

        self.functions[func_name] = {
            'params': params,
            'body': body,
            'start_line': start_idx
        }

        self.log_debug(f"Définition fonction '{func_name}' avec {len(body)} lignes")
        return i + 1

    def call_function(self, func_name, args):
        """Appelle une fonction définie par l'utilisateur"""
        if func_name not in self.functions:
            raise Exception(f"Fonction '{func_name}' non trouvée")

        func = self.functions[func_name]

        if len(args) != len(func['params']):
            raise Exception(f"Nombre d'arguments incorrect pour '{func_name}'")

        # Sauvegarder l'état
        old_vars = self.variables.copy()
        old_line = self.current_line

        # Définir les paramètres comme variables locales
        for param_name, arg_value in zip(func['params'], args):
            self.variables[param_name] = arg_value

        self.call_stack.append(func_name)

        # Exécuter le corps
        result = None
        for line in func['body']:
            if line.strip():
                line_result = self.execute_line(line.strip())
                if line_result is not None:
                    result = line_result

        # Restaurer l'état
        self.variables = old_vars
        self.current_line = old_line
        self.call_stack.pop()

        return result

    def process_if(self, lines, start_idx):
        """Traite une condition si"""
        line = lines[start_idx].strip()
        # Format: si condition alors
        condition_str = line[3:].replace('alors', '').strip()
        condition = self.evaluate_expression(condition_str)

        # Trouver les blocs alors/sinon
        then_body = []
        else_body = []
        i = start_idx + 1
        depth = 1
        in_then = True

        while i < len(lines) and depth > 0:
            line = lines[i].strip()

            # Gérer l'imbrication
            if line.startswith('si ') or line.startswith('tant que ') or line.startswith('repeter ') or line.startswith('pour chaque ') or line.startswith('fonction '):
                depth += 1
            elif line == 'sinon' and depth == 1:
                in_then = False
                i += 1
                continue
            elif line == 'fin':
                depth -= 1
                if depth == 0:
                    break

            if in_then:
                then_body.append(line)
            else:
                else_body.append(line)

            i += 1

        # Exécuter le bon bloc
        if condition:
            for line in then_body:
                if line.strip():
                    self.execute_line(line.strip())
        else:
            for line in else_body:
                if line.strip():
                    self.execute_line(line.strip())

        return i + 1

    def process_while(self, lines, start_idx):
        """Traite une boucle tant que"""
        line = lines[start_idx].strip()
        # Format: tant que condition
        condition_str = line[9:].strip()

        # Trouver le corps
        body = []
        i = start_idx + 1
        depth = 1

        while i < len(lines) and depth > 0:
            line = lines[i].strip()
            if line.startswith('tant que ') or line.startswith('si ') or line.startswith('repeter ') or line.startswith('pour chaque ') or line.startswith('fonction '):
                depth += 1
            elif line == 'fin':
                depth -= 1
                if depth == 0:
                    break
            body.append(line)
            i += 1

        # Exécuter la boucle
        while self.evaluate_expression(condition_str):
            for line in body:
                if line.strip():
                    self.execute_line(line.strip())

        return i + 1

    def process_repeat(self, lines, start_idx):
        """Traite une boucle répéter"""
        line = lines[start_idx].strip()
        # Format: repeter X fois
        match = re.match(r'repeter (\d+) fois', line)
        if not match:
            raise Exception("Syntaxe de boucle invalide")

        count = int(match.group(1))

        # Trouver le corps
        body = []
        i = start_idx + 1
        depth = 1

        while i < len(lines) and depth > 0:
            line = lines[i].strip()
            if line.startswith('repeter ') or line.startswith('si ') or line.startswith('tant que ') or line.startswith('pour chaque ') or line.startswith('fonction '):
                depth += 1
            elif line == 'fin':
                depth -= 1
                if depth == 0:
                    break
            body.append(line)
            i += 1

        # Exécuter la boucle
        for _ in range(count):
            for line in body:
                if line.strip():
                    self.execute_line(line.strip())

        return i + 1

    def process_foreach(self, lines, start_idx):
        """Traite une boucle pour chaque"""
        line = lines[start_idx].strip()
        # Format: pour chaque element dans liste
        match = re.match(r'pour chaque (\w+) dans (\w+)', line)
        if not match:
            raise Exception("Syntaxe de boucle pour chaque invalide")

        var_name = match.group(1)
        list_name = match.group(2)

        if list_name not in self.variables:
            raise Exception(f"Liste '{list_name}' non définie")

        liste = self.variables[list_name]
        if not isinstance(liste, list):
            raise Exception(f"'{list_name}' n'est pas une liste")

        # Trouver le corps
        body = []
        i = start_idx + 1
        depth = 1

        while i < len(lines) and depth > 0:
            line = lines[i].strip()
            if line.startswith('pour chaque ') or line.startswith('si ') or line.startswith('tant que ') or line.startswith('repeter ') or line.startswith('fonction '):
                depth += 1
            elif line == 'fin':
                depth -= 1
                if depth == 0:
                    break
            body.append(line)
            i += 1

        # Exécuter la boucle
        for element in liste:
            self.variables[var_name] = element
            for line in body:
                if line.strip():
                    self.execute_line(line.strip())

        # Nettoyer la variable temporaire
        if var_name in self.variables and var_name != list_name:
            del self.variables[var_name]

        return i + 1

    def parse_arguments(self, args_str):
        """Parse les arguments d'une fonction"""
        if not args_str.strip():
            return []

        args = []
        current = ""
        depth = 0

        for char in args_str:
            if char == ',' and depth == 0:
                args.append(current.strip())
                current = ""
            else:
                if char == '(':
                    depth += 1
                elif char == ')':
                    depth -= 1
                current += char

        if current.strip():
            args.append(current.strip())

        return [self.evaluate_expression(arg) for arg in args]

    def include_file(self, filename):
        """Inclut un autre fichier LAPIN"""
        try:
            filepath = os.path.join(os.path.dirname(sys.argv[0]), filename)
            if not os.path.exists(filepath):
                filepath = filename

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            self.execute(content, filename)
            return f"Fichier '{filename}' inclus avec succès"
        except Exception as e:
            raise Exception(f"Erreur inclusion fichier '{filename}': {e}")

def main():
    """Point d'entrée principal"""
    import argparse

    parser = argparse.ArgumentParser(description='🐇 Interpréteur LAPIN')
    parser.add_argument('fichier', nargs='?', help='Fichier .lapin à exécuter')
    parser.add_argument('--debug', action='store_true', help='Mode debug')
    parser.add_argument('--version', action='store_true', help='Afficher la version')

    args = parser.parse_args()

    if args.version:
        print("🐇 LAPIN v1.0.0 - Langage d'Apprentissage de la Programmation INtutive")
        return

    interpreter = LapinInterpreter(debug=args.debug)

    if args.fichier:
        # Exécuter depuis un fichier
        try:
            with open(args.fichier, 'r', encoding='utf-8') as f:
                code = f.read()

            print(f"🐇 Exécution de {args.fichier}...")
            print("=" * 50)

            success = interpreter.execute(code, args.fichier)

            print("=" * 50)
            if success:
                print("✅ Programme exécuté avec succès")
            else:
                print("❌ Programme terminé avec des erreurs")

        except FileNotFoundError:
            print(f"❌ Fichier '{args.fichier}' introuvable")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Erreur: {e}")
            sys.exit(1)
    else:
        # Mode interactif
        print("🐇 LAPIN - Mode Interactif")
        print("Tapez 'quitter' pour sortir")
        print("-" * 30)

        while True:
            try:
                line = input("lapin> ").strip()
                if line.lower() in ['quitter', 'exit', 'quit']:
                    break
                if line:
                    interpreter.execute(line, "<interactif>")
                    for output in interpreter.output:
                        print(output)
                    interpreter.output = []
            except KeyboardInterrupt:
                print("\nAu revoir ! 👋")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()