#!/bin/bash
echo "Démarrage de l'application Logistique..."

# Se déplacer dans le dossier du script
cd "$(dirname "$0")"

# Créer l'environnement virtuel si besoin
if [ ! -d "venv" ]; then
    echo "Première exécution : installation des dépendances..."
    python3 -m venv venv
    source venv/bin/activate
    pip install pulp matplotlib
else
    source venv/bin/activate
fi

# Lancer l'application
python3 main_gui.py
