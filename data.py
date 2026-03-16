# Dictionnaires contenant les données initiales du problème logistique
"""
 1) Demandes en requêtes de chaque région (R1, R2, R3, R4)
 Clé : Nom de la region, Valeur : Nombre de requêtes
"""
DEMANDES_INITIALES = {
    'R1' : 1200,
    'R2' : 900,
    'R3' : 700,
    'R4' : 600
}

"""
Capactités maximales de traitement pour chaque centre
Clé : Nom du centre, Valeur : Capacité maximale
"""
CAPACITES_INITIALES = {
    'C1' : 1500,
    'C2' : 1200,
    'C3' : 1000
}

"""
Couts unitaires de traitement
pour envoyer 1 requête de la region i vers le centre j

COUTS[Region][Centre] = coût unitaire
"""
COUTS_INITIAUX = {
    'R1' : {'C1': 5, 'C2': 6, 'C3': 7},
    'R2' : {'C1': 4, 'C2': 5, 'C3': 6},
    'R3' : {'C1': 6, 'C2': 4, 'C3': 5},
    'R4' : {'C1': 8, 'C2': 7, 'C3': 6}
}