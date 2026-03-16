from data import DEMANDES_INITIALES, CAPACITES_INITIALES, COUTS_INITIAUX
from optimisation import resoudre_probleme
from visualisation import afficher_graphiques

solution = resoudre_probleme(DEMANDES_INITIALES, CAPACITES_INITIALES, COUTS_INITIAUX)
afficher_graphiques(solution, CAPACITES_INITIALES)
print("Graphiques affichés avec succès")
