# Modélisation et Optimisation d'un Système Logistique Numérique

Ce projet résout un problème d'optimisation linéaire et en nombres entiers mixtes (MILP) basé sur le routage de requêtes informatiques entre 4 régions (R1-R4) et 3 centres de données (C1-C3).

## 🚀 Fonctionnalités

1. **Modèle Mathématique de Base** :
   - Satisfaction de toutes les demandes.
   - Respect des capacités des centres.
   - Limitation à 60% des requêtes par région vers un même centre.
2. **Extensions Avancées (Examen Supplémentaire)** :
   - **Latence maximale** (Les de 35ms sont bloqués).
   - **Énergie** (Respect d'un plafond énergétique global de 7000 unités).
   - **Activation des Serveurs (MIP)** (Variables Binaires & Coûts fixes pour les serveurs actifs).
   - *Pénalité* de 5€ par requête au-delà de 90% d'utilisation d'un même centre.
3. **Interface Graphique (Tkinter)** :
   - Modification en temps réel des données d'entrée.
   - Application de 5 scénarios de crise instantanément.
4. **Visualisation & Exports** :
   - Graphiques générés avec Matplotlib.
   - Exports au format **PDF** et de rapports data brutes au format **CSV**. 

## 🛠️ Pré-requis

 
## Démarrage rapide sous Linux
Pour lancer le projet instantanément sur n'importe quel ordinateur Linux (Ubuntu, Mint, etc), un script automatique se charge de tout :
```bash
./demarrer_logistique.sh
```

Si vous souhaitez exécuter le projet depuis le code source :
```bash
# Activation de l'environnement
source venv/bin/activate

# Installation des dépendances
pip install pulp matplotlib
```

## ▶️ Utilisation

Pour lancer l'interface graphique :
```bash
python3 main_gui.py
```

## 📦 Création d'un exécutable

L'application peut être rendue standalone (sans besoin de Python installé) grâce à `PyInstaller`.
Pour construire l'exécutable localement :

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --collect-all pulp --name "Logistique_Optimisation" main_gui.py
```
*(Le fichier généré se trouvera dans le dossier `dist/`)*

### Multi-Plateforme (Linux & Windows)
Notez que `pyinstaller` **ne peut pas** faire de la "cross-compilation". C'est-à-dire que pour obtenir un `.exe` Windows, vous devez exécuter la commande de génération **sous Windows**. 

Pour vous faciliter la tâche, j'ai créé 2 petits scripts automatiques. Il suffit de les double-cliquer selon votre système d'exploitation :
- **Sous Linux** : Lancez simplement `build_linux.sh` (ou via le terminal : `./build_linux.sh`). 
- **Sous Windows** : Transférez ce dossier sur un PC Windows et double-cliquez sur `build_windows.bat`.

Dans les deux cas, le script installera tout seul l'environnement de travail et l'exécutable (`.exe` ou binaire Linux) sera généré dans le dossier `dist/`.
