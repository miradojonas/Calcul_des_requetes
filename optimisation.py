# Partie optimisation : couche modélisation et optimisation
import pulp
from data import LATENCES, LATENCE_MAX, ENERGIE, ENERGIE_MAX, COUTS_FIXES

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

    #Contrainte supplementaire : variable supplémentaires pour la pénalité (Dépassement > 90%)
    #Variables pour savoir combien de requêtes dépassent les 90%

    # --- EXTENSION : Variables binaires d'activation (Section 1.1) ---
    # y_C1 = 1 si le centre est allumé, 0 sinon
    y = pulp.LpVariable.dicts("y", centres, cat='Binary')

    depassement = pulp.LpVariable.dicts("depassement", centres, lowBound=0, cat='Continuous')

    # 3) Fonction objectif (Coût total à minimiser)
    # Sommes des (x_ij * cout_ij) pour toutes les régions et tous les centres
    # Somme des (x_ij * cout_ij) + une penalité de 5 euro(arbitraire) par requête au-déla de 90% de capacité
    cout_transport = pulp.lpSum(x[i][j] * couts[i][j] for i in regions for j in centres)
    cout_penalite = pulp.lpSum(depassement[j] * 5 for j in centres)
    # --- EXTENSION : Coût fixe d'activation dans objectif (Section 1.2) ---
    cout_fixes = pulp.lpSum(y[j] * COUTS_FIXES[j] for j in centres)
    
    # --- EXTENSION : Distance réseau (Section 3.2) ---
    # Remplace la Latence Maximale (3.1) qui bloquait le modèle. 
    # On ajoute au coût objectif une pénalité proportionnelle à la latence ("distance", avec alpha = 0.1)
    alpha = 0.1
    cout_latence = pulp.lpSum(alpha * LATENCES[i][j] * x[i][j] for i in regions for j in centres)

    modele += cout_transport + cout_penalite + cout_fixes + cout_latence, "Cout_Total"


    # 4) Contraintes mathématiques
    #Contrainte A: Tous les demandes de chaque région doivent être traité
    #Pour chaque région, la somme des requêtes envoyés vers C1, C2 et C3 doit être égale à la demande de la region
    for i in regions :
        modele += pulp.lpSum(x[i][j] for j in centres) == demandes[i], f"Demande_satisfaite_{i}"

    #Contrainte B: Les capacités des centres ne doivent pas être dépassés
    # Pour chaque centre, la somme des requêtes de R1, R2, R3 et R4 doit être inférieure ou égale à sa capacité
    for j in centres :
        modele += pulp.lpSum(x[i][j] for i in regions) <= capacites[j], f"Capacite_respectee_{j}"
    
    # Partie F du projet( Le centre C3 ne peut pas traiter les requêtes de R4)
    modele += x['R4']['C3'] == 0 , "Interdiction_R4_C3"

    # Contrainte D : Un centre ne peut pas traiter plus de 60% des requêtes d'une même region
    # Ce contrainte valide aussi la demande "chaque région est desservie par au moins 2 centres"
    for i in regions:
        for j in centres:
            # 0,6 equivaut à 60%
            modele += x[i][j] <= 0.6 * demandes[i], f"Max_60pc_{i}_{j}"

    
    # Contraine E : calcul du dépassement au déla de 90% de la capacité
    # La somme des requêtes vers un centre - 90% de sa capacité <= variable de dépassement
    for j in centres :
        seuil_90 = 0.90 * capacites[j]
        modele += pulp.lpSum(x[i][j] for i in regions) - seuil_90 <= depassement[j], f"Calcul du depassement_{j}"

    # --- EXTENSION : Contrainte Energétique (Section 2) ---
    # La somme des (requêtes traitées par C * énergie de C) <= ENERGIE_MAX
    energie_totale = pulp.lpSum(x[i][j] * ENERGIE[j] for i in regions for j in centres)
    modele += energie_totale <= ENERGIE_MAX, "Limite_Energie_Globale"

    # La section 3.1 (Latence stricte) a été remplacée par la section 3.2 (Distance réseau) dans la fonction objectif
    # car une limitation stricte de latence empêchait de satisfaire R4 selon la combinaison des contraintes métiers.

    # --- EXTENSION : Liaison variables y et x (Section 1.1) ---
    # Si x > 0 alors y doit être = 1 (et un centre activé doit avoir au moins 200 requêtes)
    for j in centres:
        modele += pulp.lpSum(x[i][j] for i in regions) <= capacites[j] * y[j], f"Liaison_Activation_Capacite_{j}"
        modele += pulp.lpSum(x[i][j] for i in regions) >= 200 * y[j], f"Liaison_Activation_Minimum_200_{j}"

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
        "repartition": {},
        "depassement": {}
    }

    # Si la solution est optimal, on extrait le nombre de requêtes alloués pour chaque route
    if statut == "Optimal":
        for i in regions:
            resultats["repartition"][i] = {}
            for j in centres:
                resultats["repartition"][i][j] = x[i][j].varValue #valeur de la variable x_ij
        
        for j in centres:
            resultats["depassement"][j] = depassement[j].varValue # valeur du depassement
            
        resultats["centres_actifs"] = {j: y[j].varValue for j in centres}

            
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