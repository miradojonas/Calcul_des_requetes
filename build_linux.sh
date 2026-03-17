#!/bin/bash
echo "=== Compilation de l'application Logistique pour LINUX ==="
# Vérification et création d'un environnement virtuel si besoin
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "Installation des dépendances..."
pip install pulp matplotlib pyinstaller
echo "Création de l'exécutable Linux..."
pyinstaller --noconsole --onefile --collect-all pulp --name "Logistique_Optimisation_Linux" main_gui.py
echo "=== Terminé ! L'exécutable se trouve dans le dossier 'dist' ==="
