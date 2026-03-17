import re

with open("main_gui.py", "r") as f:
    content = f.read()

# Make sure csv is imported
if "import csv" not in content:
    content = "import csv\n" + content

# Add the exporter_csv method if not present
if "def exporter_csv(self):" not in content:
    csv_method = """    def exporter_csv(self):
        result_text = self.resultats_text.get(1.0, "end").strip()
        if not result_text:
            messagebox.showwarning("Warning", "Veuillez lancer le calcul avant d'exporter.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for line in result_text.split('\\n'):
                    writer.writerow([line])
            messagebox.showinfo("Succès", "Export CSV réussi!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export CSV: {e}")

"""
    content = content.replace("    def exporter_pdf(self):", csv_method + "    def exporter_pdf(self):")

# Add the CSV button
if "Exporter en CSV" not in content:
    btn_code = """        btn_export = tk.Button(scroll_frame, text="Exporter en PDF", command=self.exporter_pdf)
        btn_export.pack(pady=5)
        
        btn_csv = tk.Button(scroll_frame, text="Exporter en CSV", command=self.exporter_csv)
        btn_csv.pack(pady=5)"""
    content = re.sub(r' +btn_export = tk\.Button.*?pack\(pady=5\)', btn_code, content, flags=re.DOTALL)


# Update the lancer_calcul to include centres actifs
if "centres_actifs" not in content and "resultats['centres_actifs']" not in content:
    nouvel_affichage = """            affichage = f"Cout total (incl. fixes et penalites): {resultats['cout_total']}€\\n\\n"
            affichage += "Répartition optimale:\\n"
            for k, v in resultats["affectations"].items():
                affichage += f"  - R_{k[0]} vers C_{k[1]} : {v} unités\\n"
                
            if "centres_actifs" in resultats:
                affichage += "\\nCentres Actifs:\\n"
                for c, actif in resultats["centres_actifs"].items():
                    statut = "Actif" if actif == 1 else "Inactif"
                    affichage += f"  - Centre {c}: {statut}\\n"

            if resultats.get("depassement"):
                affichage += "\\nDépassements de pénalité (90%):\\n"
                for c, dep in resultats["depassement"].items():
                    affichage += f"  - Centre {c} dépassé de {dep} unités\\n"
"""
    # Simply replace the block where it formats affichage
    pattern = r' +affichage = f"Cout total: {resultats\[\'cout_total\'\]}€\\n\\n".*?Dépassements.*?:\\n.*?unités\\n"'
    
    # Let's try to just replace the whole affichage block if it exists.
    # Actually, it's safer to just do a string replace if we know what it looks like
