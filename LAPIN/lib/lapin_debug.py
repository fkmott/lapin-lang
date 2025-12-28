#!/usr/bin/env python3
"""
🐇 LAPIN - Version Debug
Interpréteur simplifié avec messages d'erreur clairs
"""

import sys

def main():
    print("🐇 LAPIN DEBUG - Version 1.0")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python lapin_debug.py <fichier.lapin>")
        return
    
    filename = sys.argv[1]
    print(f"Lecture du fichier: {filename}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        variables = {}
        line_num = 0
        
        for line in lines:
            line_num += 1
            original_line = line.rstrip()
            line = original_line.strip()
            
            # Ignorer les lignes vides et commentaires
            if not line or line.startswith('#'):
                print(f"[{line_num:3d}] # {original_line}")
                continue
            
            print(f"[{line_num:3d}] > {original_line}")
            
            try:
                # Commande AFFICHER
                if line.startswith('afficher '):
                    text = line[9:]
                    if text.startswith('"') and text.endswith('"'):
                        text = text[1:-1]
                    # Remplacer les variables
                    for var, val in variables.items():
                        text = text.replace(var, str(val))
                    print(f"      {text}")
                
                # Commande ÉCRIRE
                elif line.startswith('ecrire '):
                    text = line[7:]
                    if text.startswith('"') and text.endswith('"'):
                        text = text[1:-1]
                    print(text, end='')
                
                # Affectation de variable
                elif '=' in line:
                    parts = line.split('=', 1)
                    var_name = parts[0].strip()
                    value_expr = parts[1].strip()
                    
                    # Chaîne de caractères
                    if value_expr.startswith('"') and value_expr.endswith('"'):
                        variables[var_name] = value_expr[1:-1]
                        print(f"      Variable '{var_name}' = '{variables[var_name]}'")
                    
                    # Nombre entier
                    elif value_expr.isdigit():
                        variables[var_name] = int(value_expr)
                        print(f"      Variable '{var_name}' = {variables[var_name]}")
                    
                    # Nombre décimal
                    elif value_expr.replace('.', '', 1).isdigit() and value_expr.count('.') == 1:
                        variables[var_name] = float(value_expr)
                        print(f"      Variable '{var_name}' = {variables[var_name]}")
                    
                    # Variable existante
                    elif value_expr in variables:
                        variables[var_name] = variables[value_expr]
                        print(f"      Variable '{var_name}' = {variables[var_name]} (copié de '{value_expr}')")
                    
                    # Booléen
                    elif value_expr in ['vrai', 'faux']:
                        variables[var_name] = value_expr == 'vrai'
                        print(f"      Variable '{var_name}' = {variables[var_name]}")
                    
                    else:
                        print(f"      ⚠️  Expression non reconnue: '{value_expr}'")
                
                # LIRE
                elif line.startswith('lire '):
                    var_name = line[5:].strip()
                    variables[var_name] = input("? ")
                    print(f"      Variable '{var_name}' = '{variables[var_name]}'")
                
                # Autre
                else:
                    print(f"      ⚠️  Commande non reconnue")
            
            except Exception as e:
                print(f"      ❌ Erreur: {e}")
        
        print("\n" + "=" * 50)
        print("✅ Programme terminé")
        print(f"Variables finales: {variables}")
        
    except FileNotFoundError:
        print(f"❌ Fichier '{filename}' introuvable")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

if __name__ == "__main__":
    main()