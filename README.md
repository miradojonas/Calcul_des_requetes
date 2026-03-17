# Modélisation et Optimisation d'un Système Logistique Numérique

Ce projet résout un problème d'optimisation linéaire et en nombres entiers mixtes (MILP) basé sur le routage de requêtes informatiques entre 4 régions (R1-R4) et 3 centres de données (C1-C3).

## 🚀 Fonctionnalités et Contraintes Métier

1. **Modèle Mathématique de Base (Partie A à D)** :
   - Satisfaction de toutes les demandes régionales.
   - Respect strict des capacités maximales de chaque centre.
2. **Contraintes Supplémentaires Métier (Partie F)** :
   - **Limitation géographique** : Un centre ne peut pas traiter plus de 60% des requêtes d'une même région (ce qui garantit implicitement que chaque région est desservie par au moins 2 centres).
   - **Interdiction technique** : Le centre C3 est dans l'incapacité matérielle de recevoir les requêtes de la région R4.
   - **Pénalité de charge** : Une surtaxe financière (variable de dépassement) est appliquée si un centre dépasse 90% de sa capacité maximale.
3. **Extensions Avancées (Examen Supplémentaire Phase Finale)** :
   - **Activation Binaire ($y_j$)** : Les serveurs disposent d'un statut Actif/Inactif et nécessitent au moins 200 requêtes pour être allumés.
   - **Coût Fixe d'Activation** : S'il est allumé, le serveur ajoute un coût fixe lourd à la fonction objectif (ex: 1000€ pour C1).
   - **Contrainte Énergétique** : Plafond d'énergie globale fixé à 7000 unités pour forcer une démarche éco-responsable de l'algorithme.
   - **Distance Réseau (Latence intégrée)** : Afin d'éviter un conflit insoluble avec les interdictions matérielles, la latence n'est pas une limite bloquante, mais a été intégrée à la fonction de coût. Le solveur pénalise proportionnellement les flux lents.
4. **Interface Graphique (Tkinter)** :
   - Saisie et modification interactive des paramètres de l'algorithme.
   - Menu déroulant avec 5 scénarios de crise instantanés.
5. **Visualisation & Exports** :
   - Tableaux et Bar Charts via Matplotlib.
   - Exports configurés pour la génération de rapport format **PDF** et **CSV**.

## 🧠 Méthode de Résolution (Comment le programme résout le problème ?)

Le cœur de l'application repose sur la **Programmation Linéaire en Nombres Entiers Mixtes (MILP)**, résolue par un solveur mathématique professionnel.

1. **Les Variables de décision** : Le programme modélise des variables continues $x_{ij}$ représentant le "flux" (nombre de requêtes envoyées de la région $i$ au centre $j$). Pour respecter les conditions avancées, il utilise également des variables binaires entières $y_j \in \{0, 1\}$ définissant l'état allumé ou éteint d'un serveur.
2. **La Fonction Objectif** : Le but ultime du solveur est de *minimiser* la valeur d'une immense équation comprenant :
   * Les coûts de base (nombre de requêtes traitées $\times$ coût unitaire défini).
   * L'addition des coûts fixes des serveurs qui ont été activés (multipliés par $y_j$).
   * Des pénalités financières dynamiques (dépassement des fameux 90% d'utilisation).
   * Un amortisseur de distance réseau (pénalité relative à la latence $x_{ij} \times \text{latence} \times \alpha$).
3. **Application des Contraintes** : Les règles du monde réel imposées (capacités, énergie, 60% max) sont traduites en inéquations mathématiques ("la somme des variables vers un centre $\le$ capacité"). 
4. **Résolution Algorithmique** : Grâce à la bibliothèque Python `PuLP`, le problème est encapsulé puis soumis au moteur **CBC MILP Solver**. Ce dernier utilise la méthode du *"Simplexe"* et parcourt l'arbre des solutions possibles ("*Branch and Bound*"). Il garantit de trouver mathématiquement **la meilleure répartition absolue en quelques millisecondes**, ou de prouver que la combinaison de contraintes est impossible ("*Infeasible*") si les utilisateurs dictent des règles contradictoires.

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
