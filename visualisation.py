#Pour la visualisation des données
import matplotlib.pyplot as plt
import numpy as np

"""
Fonction qui génère deux graphique qui analyse la solution optimale:
1- Comparaison entre la charge réelle et la capacité  max des centres
2- Repartition géographique
"""

def afficher_graphiques(resultats, capacites_max, couts_unitaires):
    # On s'assure qu'on a bien une solution valide
    if resultats['statut'] != 'Optimal':
        print("Erreur : valeur non optimal, impossible de tracer les graphiques")
        return
    
    repartition = resultats['repartition']
    regions = list(repartition.keys())
    # Recupération de la liste des centres (C1,C2,C3) à partir de la première region
    centres = list(repartition[regions[0]].keys())

    # PREPARATION DE LA FIGURE GLOBALE
    fig = plt.figure(figsize=(12, 8))

    # GRAPHIQUE 1: Utilisation des capacitéz
    
    #Calcul de la somme reçues par chaque centre
    charges = {c: 0 for c in centres}
    for r in regions:
        for c in centres:
            charges[c] += repartition[r][c]

    noms_centres = list(charges.keys())
    valeurs_charges = list(charges.values())
    valeurs_max = [capacites_max[c] for c in noms_centres]

    plt.subplot(2, 2, 1) #Position : 1ère ligne, 2 colonnes, 1er graphe
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
    plt.subplot(2, 2, 2) #Position : 1ère ligne, 2 colonne, 2è graphe

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

    # Tableau recapitulatif des couts unitaires
    ax_tableau = plt.subplot(2, 1, 2) # Position : 2 lignes au total, 1 grande colonne, 2è postion
    ax_tableau.axis('off') # On cache les axes

    donnees_tableau = [] # Calcul du cout total de chaque region

    for r in regions:
        cout_region = 0
        detail = [] # Info de qui envoie combien à quel prix

        for c in centres:
            quantite = repartition[r][c]
            if quantite > 0:
                prix_unitaire = couts_unitaires[r][c]
                cout_total_trajet = quantite * prix_unitaire
                cout_region += cout_total_trajet
                detail.append(f"{quantite} vers {c}")
        
        # Ajout de la ligne région, détail, cout total
        donnees_tableau.append([r, " + ".join(detail), f"{cout_region} euro"])

    # 2) Construction du tableau graphique
    colonnes = ["Régions", "Répartition des requêtes", "Coût engendré"]

    tableau = ax_tableau.table(
        cellText=donnees_tableau,
        colLabels=colonnes,
        cellLoc='center',
        loc='center',
        bbox=[0.1, 0.1, 0.8, 0.8] # Définit la taille de la boite du tableau[x, y, largeur, hauteur]
    )

    tableau.auto_set_font_size(False)
    tableau.set_fontsize(10)
    ax_tableau.set_title("Tableau récapitulatif des couts par régions", fontweight='bold', pad=20)
    

    # Ajustement de l'espacemen et affichage
    plt.tight_layout()
    plt.show()