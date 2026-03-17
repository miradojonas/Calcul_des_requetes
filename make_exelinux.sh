#!/bin/bash
# Script d'installation et de compilation pour Linux (Ubuntu, Debian, Mint...)

echo "=========================================================="
echo "    COMPILATION DE L'APPLICATION LOGISTIQUE POUR LINUX    "
echo "=========================================================="
echo ""

# Vérification de l'installation de Python 3 et de l'environnement virtuel
if ! command -v python3 &> /dev/null; then
    echo "❌ Erreur: Python 3 n'est pas installé sur ce système."
    echo "Installez-le avec: sudo apt install python3 python3-venv python3-pip python3-tk"
    exit 1
fi

echo "📦 1. Installation des dépendances systèmes nécessaires..."
sudo apt-get update
sudo apt-get install -y python3-venv python3-tk python3-dev || echo "Note: L'installation système a rencontré un avertissement mais on continue."

echo "🌱 2. Création de l'environnement virtuel local..."
python3 -m venv build_env
source build_env/bin/activate

echo "📥 3. Installation des packages Python requis..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo "🔨 4. Lancement de la compilation PyInstaller..."
# Utilisation de --collect-all pulp car cette bibliothèque dépend de fichiers binaires externes pour le solveur
# On force l'inclusion de matplotlib et de ses backends graphiques (sinon les graphiques ne s'affichent pas en .exe)
pyinstaller --noconsole \
            --onefile \
            --clean \
            --collect-all pulp \
            --collect-all matplotlib \
            --hidden-import="matplotlib.backends.backend_tkagg" \
            --hidden-import="matplotlib.backends.backend_pdf" \
            --hidden-import="numpy" \
            --name "OptiLogistique_Linux" \
            main_gui.py

echo "🧹 5. Nettoyage des fichiers temporaires de compilation..."
deactivate
rm -rf build_env
rm -rf build/
rm -f OptiLogistique_Linux.spec

echo ""
echo "✅ TERMINÉ AVEC SUCCÈS !"
echo "=========================================================="
echo "🎉 L'exécutable autonome a été généré dans le dossier 'dist/'"
echo "👉 Vous pouvez le lancer en double-cliquant dessus ou via le terminal :"
echo "   ./dist/OptiLogistique_Linux"
echo "=========================================================="
