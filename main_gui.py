# main_gui.py
import tkinter as tk
from tkinter import messagebox
from data import DEMANDES_INITIALES, CAPACITES_INITIALES, COUTS_INITIAUX
from optimisation import resoudre_probleme
from visualisation import afficher_graphiques
from tkinter import ttk

class ApplicationLogistique(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Optimisation d'un système logistique numérique")
        self.geometry("1000x2000")
        
        # --- Interface (Widgets) ---
        titre = tk.Label(self, text="Modélisation Logistique", font=("Helvetica", 16, "bold"))
        titre.pack(pady=10)
        
        info = tk.Label(self, text="Calcul de la répartition optimale des requêtes sous contraintes.\nTechnologie : Python / PuLP", justify="center")
        info.pack(pady=10)

        # Partie E : Scénario et analyse de sensibilité
        cadre_scenarios = tk.LabelFrame(self, text="Scénarios Prédefinis")
        cadre_scenarios.pack(pady=5, padx=10, fill="x")

        # Menu déroulant
        self.list_scenarios = [
            "0) Situation initiale",
            "1) Augmentation de 20% des requêtes",
            "2) Réduction de 25% de la capacité de C2",
            "3) Augmentation de 30% des coûts de C3",
            "4) Indisponibilité temporaire de C1"
        ]
        self.combo_scenarios = ttk.Combobox(cadre_scenarios, values=self.list_scenarios, width=40, state="readonly")
        self.combo_scenarios.current(0) # Premier scénario par défaut
        self.combo_scenarios.pack(side=tk.LEFT, padx=10, pady=10)

        # Bouton pour changer de scénario
        btn_changer_scenario = tk.Button(cadre_scenarios, text="Appliquer le scénario", command=self.appliquer_scenario)
        btn_changer_scenario.pack(side=tk.LEFT, padx=10, pady=10)


        # Cadre pour les coûts unitaires
        cadre_couts = tk.LabelFrame(self, text="Coûts unitaires de traitement")
        cadre_couts.pack(pady=10, padx=10, fill="x")

        self.entries_couts = {}
        # Affichage des en-têtes des colonnes (C1, C2, C3)
        tk.Label(cadre_couts, text="Départ/Arrivée", font=("Helvetica", 10, "italic")).grid(row=0, column=0, padx=5, pady=5)
        centres = ['C1', 'C2', 'C3']
        regions = ['R1', 'R2', 'R3', 'R4']
        for j, c in enumerate(centres):
            tk.Label(cadre_couts, text=c, font=("Helvetica", 10, "italic")).grid(row=0, column=j+1, padx=5, pady=5)

        # On parcourt pour chaque region, et pour chaque region, chaque centre
        for i, r in enumerate(regions):
            self.entries_couts[r] = {}
            # Nom de la region
            tk.Label(cadre_couts, text=r, font=("Helvetica", 10, "bold")).grid(row=i+1, column=0, padx=5, pady=5)

            for j, c in enumerate(centres):
                entry = tk.Entry(cadre_couts, width=10) #Champ de saisie
                # Valeur par defaut depuis le dictionnaire data.py
                valeur_initiale = COUTS_INITIAUX[r][c]
                entry.insert(0, str(valeur_initiale))
                entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                self.entries_couts[r][c] = entry # Sauvegarde de l'entrée


        # Cadre pour les capacités
        cadre_capacites = tk.LabelFrame(self, text="Capacités par centre")
        cadre_capacites.pack(pady=10, padx=10, fill="x")

        self.entries_capacites = {}
        centres = ['C1', 'C2', 'C3']

        # Champ de saisie pour chaque centre
        for i, centre in enumerate(centres):
            tk.Label(cadre_capacites, text=centre).grid(row=0, column=i*2, padx=5, pady=5)
            entry = tk.Entry(cadre_capacites, width=10)
            entry.insert(0, str(CAPACITES_INITIALES[centre])) # Valeur par défaut
            entry.grid(row=0, column=i*2 + 1, padx=5, pady=5)
            self.entries_capacites[centre] = entry

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

    def appliquer_scenario(self):
        choix = self.combo_scenarios.get()
        # On remet les valeurs de bases d'abord avant de passer au suite
        for r in ['R1', 'R2', 'R3', 'R4']:
            self.entries_demandes[r].delete(0, tk.END)
            self.entries_demandes[r].insert(0, str(DEMANDES_INITIALES[r]))

            for c in ['C1', 'C2', 'C3']:
                self.entries_couts[r][c].delete(0, tk.END)
                self.entries_couts[r][c].insert(0, str(COUTS_INITIAUX[r][c]))

        for c in ['C1', 'C2', 'C3']:
            self.entries_capacites[c].delete(0, tk.END)
            self.entries_capacites[c].insert(0, str(CAPACITES_INITIALES[c])) 

        # Vient ensuite la modification en fonction du scénario choisie
        if "1) Augmentation de 20% des requêtes" in choix:
            for r in ['R1', 'R2', 'R3', 'R4']:
                new_d = int(DEMANDES_INITIALES[r] * 1.20)
                self.entries_demandes[r].delete(0, tk.END)
                self.entries_demandes[r].insert(0, str(new_d))

        elif "2) Réduction de 25% de la capacité de C2" in choix:
            new_cap = int(CAPACITES_INITIALES['C2'] * 0.75)
            self.entries_capacites['C2'].delete(0, tk.END)
            self.entries_capacites['C2'].insert(0, str(new_cap))
        
        elif "3) Augmentation de 30% des coûts de C3" in choix:
            for r in ['R1', 'R2', 'R3', 'R4']:
                newc_cout = round(COUTS_INITIAUX[r]['C3'] * 1.30, 2)
                self.entries_couts[r]['C3'].delete(0, tk.END)
                self.entries_couts[r]['C3'].insert(0, str(newc_cout))
        
        elif "4) Indisponibilité temporaire de C1" in choix:
            self.entries_capacites['C1'].delete(0, tk.END)
            self.entries_capacites['C1'].insert(0, "0")

        messagebox.showinfo("Scénario chargé", f"La scénario a été changé aux données de saisie.\nCliquez sur 'lancer l'optimisation'")

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

            nouvelles_capacites = {
                'C1' : int(self.entries_capacites['C1'].get()),
                'C2' : int(self.entries_capacites['C2'].get()),
                'C3' : int(self.entries_capacites['C3'].get())
            }

            #  On recupère les valeurs depuis l'interface
            nouveaux_couts = {}
            for r in ['R1', 'R2', 'R3', 'R4']:
                nouveaux_couts[r] = {}
                for c in ['C1', 'C2', 'C3']:
                    nouveaux_couts[r][c] = float(self.entries_couts[r][c].get()) # float car les couts peuvent être decimaux

            solution = resoudre_probleme(nouvelles_demandes, nouvelles_capacites, nouveaux_couts)

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
                
                affichage += "\n PÉNALITÉS ET DÉPASSEMENTS (> 90%) ---\n"
                for c, val in solution.get("depassement", {}).items():
                    if val > 0:
                        affichage += f"Le centre {c} dépasse sa limite de {val} requêtes (Pénalité ajoutée)\n"
                    else:
                        affichage += f"Le centre {c} est dans la norme (< 90% de capacité)\n"
            else:
                affichage = "Erreur : Impossible de trouver une solution (Capacités insuffisantes)"
                
            self.resultats_text.insert(tk.END, affichage)
            self.resultats_text.config(state=tk.DISABLED)
            
            # Si le calcul a marché, on affiche le graphique
            if solution['statut'] == "Optimal":
                afficher_graphiques(solution, nouvelles_capacites)

        except Exception as e:
            messagebox.showerror("Erreur de calcul", f"Une erreur s'est produite :\n{e}")

# Lancement de l'application
if __name__ == "__main__":
    app = ApplicationLogistique()
    app.mainloop()