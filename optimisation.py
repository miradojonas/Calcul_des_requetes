# Partie optimisation : couche modélisation et optimisation
import pulp

"""
fonction qui modélise et résout le problème d'optimisation logistique
prend en paramètre les dictionnaires de données dans data.py et retourne le solution
"""
def resoudre_probleme(demandes, capacites, couts):
    #initialisation du modèle et on veut minimiser le coût total
    modele = pulp.LpProblem("Optimisation_Logistique_Numerique", pulp.LpMinimize)

    #Liste des régions et des centres pour facilité le code
    regions = list(demandes.keys())
    centres = list(capacites.keys())


    #2) Creation des variables de décision : x_ij
    #x_R1_C1 : nombres de requêtes de la région R1 traités par le centre C1
    #lowBound=0 : signifie qu'on ne peut pas envoyer une quantité négative de requêtes
    #cat='Continuous' : signifie que la variables peut être un nombre décimal (Integer pour des entiers purs)
    x = pulp.LpVariable.dicts("x", (regions, centres), lowBound=0, cat='Continuous')

    # 3) Fonction objectif (Coût total à minimiser)
    # Sommes des (x_ij * cout_ij) pour toutes les régions et tous les centres
    modele += pulp.lpSum(x[i][j] * couts[i][j] for i in regions for j in centres), "Cout_Total"

    # 4) Contraintes mathématiques
    #Contrainte A: Tous les demandes de chaque région doivent être traité
    #Pour chaque région, la somme des requêtes envoyés vers C1, C2 et C3 doit être égale à la demande de la region
    for i in regions :
        modele += pulp.lpSum(x[i][j] for j in centres) == demandes[i], f"Demande_satisfaite_{i}"

    #Contrainte B: Les capacités des centres ne doivent pas être dépassés
    # Pour chaque centre, la somme des requêtes de R1, R2, R3 et R4 doit être inférieure ou égale à sa capacité
    for j in centres :
        modele += pulp.lpSum(x[i][j] for i in regions) <= capacites[j], f"Capacite_respectee_{j}"
    
    # 5) Resolution du probleme
    # Le solveur va chercher la meilleure valeur pour chaque x_ij
    modele.solve()

    #6) Recuperation des résultats
    # On vérifie si le solveur a trouvé une solution optimale
    statut = pulp.LpStatus[modele.status]

    #Dictionnaire pour stocker les résultats
    resultats = {
        "statut": statut,
        "cout_total": pulp.value(modele.objective),
        "repartition": {}
    }

    # Si la solution est optimal, on extrait le nombre de requêtes alloués pour chaque route
    if statut == "Optimal":
        for i in regions:
            resultats["repartition"][i] = {}
            for j in centres:
                resultats["repartition"][i][j] = x[i][j].varValue #valeur de la variable x_ij
    return resultats

if __name__ == "__main__":
    from data import DEMANDES_INITIALES, CAPACITES_INITIALES, COUTS_INITIAUX
    
    print("Démarrage du calcul d'optimisation local...")
    solution = resoudre_probleme(DEMANDES_INITIALES, CAPACITES_INITIALES, COUTS_INITIAUX)
    
    print(f"\nStatut de la solution : {solution['statut']}")
    if solution['statut'] == "Optimal":
        print(f"Coût Total Optimal : {solution['cout_total']} €")
        print("\nRépartition détaillée des flux (x_ij) :")
        for region, centres in solution['repartition'].items():
            for centre, valeur in centres.items():
                if valeur > 0: # On n'affiche que les routes utilisées
                    print(f" - {region} envoie {valeur} requêtes au centre {centre}")