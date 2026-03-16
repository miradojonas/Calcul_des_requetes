#Pour la visualisation des données
import matplotlib.pyplot as plt
import numpy as np

"""
Fonction qui génère deux graphique qui analyse la solution optimale:
1- Comparaison entre la charge réelle et la capacité  max des centres
2- Repartition géographique
"""

def afficher_graphiques(resultats, capacites_max):
    # On s'assure qu'on a bien une solution valide
    if resultats['statut'] != 'Optimal':
        print("Erreur : valeur non optimal, impossible de tracer les graphiques")
        return
    
    repartition = resultats['repartition']
    regions = list(repartition.keys())
    # Recupération de la liste des centres (C1,C2,C3) à partir de la première region
    centres = list(repartition[regions[0]].keys())

    # PREPARATION DE LA FIGURE GLOBALE
    plt.figure(figsize=(12,5))

    # GRAPHIQUE 1: Utilisation des capacitéz
    
    #Calcul de la somme reçues par chaque centre
    charges = {c: 0 for c in centres}
    for r in regions:
        for c in centres:
            charges[c] += repartition[r][c]

    noms_centres = list(charges.keys())
    valeurs_charges = list(charges.values())
    valeurs_max = [capacites_max[c] for c in noms_centres]

    plt.subplot(1, 2, 1) #Position : 1ère ligne, 2 colonnes, 1er graphe
    x = np.arange(len(noms_centres))
    largeur = 0.35 #Largeur des barres

    # Dessin des barres (Cote à cote : charge vs capacité)
    plt.bar(x - largeur/2, valeurs_charges, largeur, label='Charge calculée', color='cornflowerblue')
    plt.bar(x + largeur/2, valeurs_max, largeur, label='Capacité maximale', color='lightgray')

    plt.ylabel('Nombre de requêtes')
    plt.title('Taux d\'occupation des data centers')
    plt.xticks(x, noms_centres)
    plt.legend()

    # GRAPHIQUE 2:repartition par régions
    plt.subplot(1, 2, 2) #Position : 1ère ligne, 2 colonne, 2è graphe

    # Graphiques en barres empilées
    bottom = np.zeros(len(regions))
    couleurs = ['#ff9999', '#66b3ff', '#99ff99'] # Une couleur par centre

    for idx, c in enumerate(centres):
        # On extrait combien chaque région envoie à ce centre spécifique
        valeurs_centre = [repartition[r][c] for r in regions]
        plt.bar(regions, valeurs_centre, bottom=bottom, label=c, color=couleurs[idx])
        bottom += np.array(valeurs_centre) # on empile pour le prochain centre

    plt.ylabel('Total des requêtes envoyées')
    plt.title('Destination des requêes par région')
    plt.legend(title="Centres de traitement")

    # Ajustement de l'espacemen et affichage
    plt.tight_layout()
    plt.show()