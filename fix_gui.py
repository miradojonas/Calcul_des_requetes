import re
import os

with open("main_gui.py", "r", encoding="utf-8") as f:
    text = f.read()

# Importer csv et filedialog si on en a besoin
if "import csv" not in text:
    text = "import csv\n" + text

if "exporter_csv" not in text:
    csv_fct = """    def exporter_csv(self):
        result_text = self.resultats_text.get(1.0, "end").strip()
        if not result_text or "Cout total" not in result_text:
            messagebox.showwarning("Warning", "Veuillez lancer le calcul avant d'exporter.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], title="Exporter en CSV")
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                for line in result_text.split('\\n'):
                    writer.writerow([line])
            messagebox.showinfo("Succès", "Export CSV réussi!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export CSV: {e}")

"""
    text = text.replace("    def appliquer_scenario(self, event):", csv_fct + "    def appliquer_scenario(self, event):")

if "Exporter en CSV" not in text:
    old_btn = r'self\.btn_export_pdf = tk\.Button\(self, text="Exporter en PDF", command=self\.exporter_pdf\)\n\s+self\.btn_export_pdf\.pack\(pady=5\)'
    new_btn = """self.btn_export_pdf = tk.Button(self, text="Exporter en PDF", command=self.exporter_pdf)
        self.btn_export_pdf.pack(pady=5)
        self.btn_export_csv = tk.Button(self, text="Exporter en CSV", command=self.exporter_csv)
        self.btn_export_csv.pack(pady=5)"""
    
    if not re.search(old_btn, text):
        # Maybe it's called btn_export
        old_btn2 = r'self\.btn_export = tk\.Button\(self, text="Exporter en PDF", command=self\.exporter_pdf\)\n\s+self\.btn_export\.pack\(pady=10\)'
        new_btn2 = """self.btn_export = tk.Button(self, text="Exporter en PDF", command=self.exporter_pdf)
        self.btn_export.pack(pady=5)
        self.btn_export_csv = tk.Button(self, text="Exporter en CSV", command=self.exporter_csv)
        self.btn_export_csv.pack(pady=5)"""
        text = re.sub(old_btn2, new_btn2, text)
    else:
        text = re.sub(old_btn, new_btn, text)

# Update display logic
if "centres_actifs" not in text:
    old_affichage = """            affichage = f"Cout total: {resultats['cout_total']}€\\n\\n"
            affichage += "Répartition optimale:\\n"
            for k, v in resultats["affectations"].items():
                affichage += f"  - R_{k[0]} vers C_{k[1]} : {v} unités\\n"
"""
    new_affichage = """            affichage = f"Cout total: {resultats['cout_total']}€ (incl. coûts fixes)\\n\\n"
            affichage += "Répartition optimale:\\n"
            for k, v in resultats["affectations"].items():
                affichage += f"  - R_{k[0]} vers C_{k[1]} : {v} unités\\n"
            
            if "centres_actifs" in resultats:
                affichage += "\\nCentres Actifs (Coûts fixes de 5000€ chacun) :\\n"
                for c, actif in resultats["centres_actifs"].items():
                    statut = "Actif" if actif == 1 else "Inactif"
                    affichage += f"  - Centre {c}: {statut}\\n"
"""
    text = text.replace(old_affichage, new_affichage)

with open("main_gui.py", "w", encoding="utf-8") as f:
    f.write(text)

