# main_gui.py
import tkinter as tk
from tkinter import messagebox
from data import DEMANDES_INITIALES, CAPACITES_INITIALES, COUTS_INITIAUX
from optimisation import resoudre_probleme
from visualisation import afficher_graphiques

class ApplicationLogistique(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Optimisation d'un système logistique numérique")
        self.geometry("700x600")
        
        # --- Interface (Widgets) ---
        titre = tk.Label(self, text="Modélisation Logistique", font=("Helvetica", 16, "bold"))
        titre.pack(pady=10)
        
        info = tk.Label(self, text="Calcul de la répartition optimale des requêtes sous contraintes.\nTechnologie : Python / PuLP", justify="center")
        info.pack(pady=10)

        # Cadre pour les demandes
        cadre_demandes = tk.LabelFrame(self, text="Demandes")
        cadre_demandes.pack(pady=10, padx=10, fill="x")

        self.entries_demandes = {}
        regions = ['R1', 'R2', 'R3', 'R4']

        #Champ de saisie pour chaque region, pré-rempli avec les données dans data.py
        for i, reg in enumerate(regions):
            tk.Label(cadre_demandes, text=reg).grid(row=0, column=i*2, padx=5, pady=5)
            entry = tk.Entry(cadre_demandes, width=10)
            entry.insert(0, str(DEMANDES_INITIALES[reg])) # Valeur par défaut
            entry.grid(row=0, column=i*2 + 1, padx=5, pady=5)
            self.entries_demandes[reg] = entry
        
        # Bouton pour lancer le calcul
        self.btn_calculer = tk.Button(self, text="Lancer l'Optimisation", command=self.lancer_calcul, bg="lightblue", font=("Arial", 12))
        self.btn_calculer.pack(pady=20)
        
        # Zone de texte pour afficher les résultats
        self.resultats_text = tk.Text(self, height=12, width=70, state=tk.DISABLED)
        self.resultats_text.pack(pady=10)

    def lancer_calcul(self):
        """Fonction appelée quand on clique sur le bouton"""
        try:
            # On appelle le programme qu'on a fait tout à l'heure
            #solution = resoudre_probleme(DEMANDES_INITIALES, CAPACITES_INITIALES, COUTS_INITIAUX)
            
            # On met à jour l'affichage
            # On recupère les valeurs tapées par l'utilisateur
            nouvelles_demandes= {
                'R1' : int(self.entries_demandes['R1'].get()),
                'R2' : int(self.entries_demandes['R2'].get()),
                'R3' : int(self.entries_demandes['R3'].get()),
                'R4' : int(self.entries_demandes['R4'].get())
            }

            solution = resoudre_probleme(nouvelles_demandes, CAPACITES_INITIALES, COUTS_INITIAUX)
            
            self.resultats_text.config(state=tk.NORMAL)
            self.resultats_text.delete(1.0, tk.END) # On efface le texte précédent
            
            if solution['statut'] == "Optimal":
                affichage = f"--- RÉSULTAT OPTIMAL TROUVÉ ---\n"
                affichage += f"Coût global minimum : {solution['cout_total']} €\n\n"
                affichage += "Plan d'acheminement :\n"
                
                for r, centres in solution["repartition"].items():
                    for c, val in centres.items():
                        if val > 0:
                            affichage += f" • {val} requêtes de {r} traitées par {c}\n"
            else:
                affichage = "Erreur : Impossible de trouver une solution (Capacités insuffisantes ?)"
                
            self.resultats_text.insert(tk.END, affichage)
            self.resultats_text.config(state=tk.DISABLED)
            
            # Si le calcul a marché, on affiche le graphique
            if solution['statut'] == "Optimal":
                afficher_graphiques(solution, CAPACITES_INITIALES)

        except Exception as e:
            messagebox.showerror("Erreur de calcul", f"Une erreur s'est produite :\n{e}")

# Lancement de l'application
if __name__ == "__main__":
    app = ApplicationLogistique()
    app.mainloop()