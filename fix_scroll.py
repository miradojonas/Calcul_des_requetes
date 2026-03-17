import re

with open("main_gui.py", "r", encoding="utf-8") as f:
    text = f.read()

scroll_code = """        self.derniere_figure = None
        
        # --- Configuration du scroll global ---
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Support mouse wheel
        def _on_mousewheel(event):
            # Windows/Mac
            if event.num == 4 or event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.canvas.yview_scroll(1, "units")
                
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Button-4>", _on_mousewheel) # Linux
        self.canvas.bind_all("<Button-5>", _on_mousewheel) # Linux

        self.container = tk.Frame(self.canvas)
        self.container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        # Create a window in canvas and bind its width to canvas width
        self.canvas_window = self.canvas.create_window((0, 0), window=self.container, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))"""

# Replace derniere_figure = None block
text = text.replace("        self.derniere_figure = None", scroll_code)

# Now we need to replace parent 'self' with 'self.container' for widgets defined directly in __init__
# Widgets are tk.Label, tk.LabelFrame, tk.Button, tk.Frame
text = text.replace("titre = tk.Label(self,", "titre = tk.Label(self.container,")
text = text.replace("info = tk.Label(self,", "info = tk.Label(self.container,")
text = text.replace("cadre_scenarios = tk.LabelFrame(self,", "cadre_scenarios = tk.LabelFrame(self.container,")
text = text.replace("cadre_couts = tk.LabelFrame(self,", "cadre_couts = tk.LabelFrame(self.container,")
text = text.replace("cadre_capacites = tk.LabelFrame(self,", "cadre_capacites = tk.LabelFrame(self.container,")
text = text.replace("cadre_demandes = tk.LabelFrame(self,", "cadre_demandes = tk.LabelFrame(self.container,")
text = text.replace("self.btn_calculer = tk.Button(self,", "self.btn_calculer = tk.Button(self.container,")
text = text.replace("self.btn_export = tk.Button(self,", "self.btn_export = tk.Button(self.container,")
text = text.replace("self.btn_export_csv = tk.Button(self,", "self.btn_export_csv = tk.Button(self.container,")
text = text.replace("frame_bas = tk.Frame(self)", "frame_bas = tk.Frame(self.container)")

with open("main_gui.py", "w", encoding="utf-8") as f:
    f.write(text)

