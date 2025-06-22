import random
import tkinter as tk
from tkinter import StringVar
from tkinter import IntVar
from entity import Entity
from importer import Importer
from stable_marriage2 import StableMarriage
import copy

class Window:

    # -------------------------
    # Initialisation de l'objet
    # -------------------------
    def __init__(self):

        # Liste des infos du model
        self.student_list = []
        self.school_list = []
        self.school_panel_list = []
        self.student_panel_list = []

        # Fenêtre principale
        self.root = tk.Tk()
        self.root.title("Parcoursup 2.0")
        self.root.geometry("800x600")

        # ===== Titre =====
        self.titre = tk.Label(self.root, font=("Arial", 18, "bold"))
        self.titre.pack(side="top", pady=10)

        # ===== Corps principal =====
        self.create_panel_3sections()
        self.create_panel_tab()

        # ===== Pied de page =====
        footer = tk.Frame(self.root)
        footer.pack(side="bottom", fill="x", pady=10, padx=10)

        self.btn_previous = tk.Button(footer, text="Previous")
        self.btn_previous.pack(side="left")

        self.btn_next = tk.Button(footer, text="Next")
        self.btn_next.pack(side="right")
    
    # -------------------------
    # Creation du panel en 3 parties
    # -------------------------
    def create_panel_3sections(self):
        self.panel_3sections = tk.Frame(self.root)

        # Section droite
        self.right_section = tk.Frame(self.panel_3sections, bg="lightblue", relief="groove", borderwidth=2)
        self.right_section.pack(side="right", fill="both", expand=True, padx=(0, 5))

        # Section gauche (divisée en deux)
        left_section = tk.Frame(self.panel_3sections)
        left_section.pack(side="left", fill="both", expand=True)

        self.left_top = tk.Frame(left_section, bg="lightgreen", relief="groove", borderwidth=2)
        self.left_top.pack(side="top", fill="both", expand=False, pady=(0, 5))

        self.left_bottom = tk.Frame(left_section, bg="lightyellow", relief="groove", borderwidth=2)
        self.left_bottom.pack(side="bottom", fill="both", expand=True)

    # -------------------------
    # Creation du panel en tableau
    # -------------------------
    def create_panel_tab(self):
        self.panel_tab = tk.Frame(self.root)

        # Colonne gauche avec les boutons
        left_controls = tk.Frame(self.panel_tab, bg="lightgreen", width=150)
        left_controls.pack(side="left", fill="y", padx=5, pady=5)

        tk.Button(left_controls, text="Importer", command=lambda: self.import_json()).pack(pady=5, fill="x")
        tk.Button(left_controls, text="Aléatoire", command=lambda: self.fill_preferences_randomly()).pack(pady=5, fill="x")

        # Partie droite : zone scrollable
        right_table_container = tk.Frame(self.panel_tab)
        right_table_container.pack(side="right", fill="both", expand=True)

        # Conteneur pour le canvas et la scrollbar horizontale
        canvas_container = tk.Frame(right_table_container)
        canvas_container.pack(side="top", fill="both", expand=True)

        # Scrollbar verticale (à droite du canvas)
        vbarY = tk.Scrollbar(canvas_container, orient="vertical")
        vbarY.pack(side="right", fill="y")

        # Canvas
        canvas = tk.Canvas(canvas_container, bg='lightblue', width=300, height=300,
                scrollregion=(0, 0, 30000, 30000))
        canvas.pack(side="left", fill="both", expand=True)
        vbarY.config(command=canvas.yview)

        # Scrollbar horizontale (en bas, dans le conteneur principal)
        vbarX = tk.Scrollbar(right_table_container, orient="horizontal")
        vbarX.pack(side="bottom", fill="x")
        vbarX.config(command=canvas.xview)

        # Configuration des commandes de défilement
        canvas.config(yscrollcommand=vbarY.set, xscrollcommand=vbarX.set)

        # Créer une frame à l'intérieur du canvas pour contenir le "tableau"
        self.table_frame = tk.Frame(canvas, bg="lightblue")
        canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
    

    # -------------------------
    # Changer de panel
    # -------------------------
    def set_panel(self, panel_name):
        self.hide_all_panels()

        panel = getattr(self, panel_name, None)
        if panel:
            panel.pack(expand=True, fill="both", padx=10, pady=10)
        else:
            raise ValueError(f"Panel '{panel_name}' not found.")
        
    #==================================================== | Nettoyage | =========================================================
    
    # -------------------------
    # Nettoyer le panel en 3 partie
    # -------------------------
    def clean_panel(self):
        self.removeContent(self.right_section)
        self.removeContent(self.left_top)
        self.removeContent(self.left_bottom)
    
    # -------------------------
    # Cacher tous les panels
    # -------------------------
    def hide_all_panels(self):
        for panel_attr in ["panel_3sections", "panel_tab"]:
            panel = getattr(self, panel_attr, None)
            if panel:
                panel.pack_forget()

    # -------------------------
    # retirer les elements d'un panel
    # -------------------------
    def removeContent(self, cadre):
        for widget in cadre.winfo_children():
            widget.destroy()
    
    # -------------------------
    # Nettoyer un tableau
    # -------------------------
    def clean_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
    
    #==================================================== | Pages | =========================================================

    # -------------------------
    # Page import des écoles
    # -------------------------
    def page_import_school(self):

        # event
        self.current_page = self.page_import_school
        self.btn_previous.configure(command=lambda: self.page_import_student())
        self.btn_next.configure(command=lambda: self.page_import_student_preferences())
        
        # Reset
        self.set_panel("panel_3sections")
        self.clean_panel()

        self.titre.configure(text="Etape 2 : Ajoutez vos écoles")

        # Section droite
        tk.Label(self.right_section, text="Liste des écoles", bg="lightblue").pack(pady=10)
        for school in self.school_list:
            self.add_school_item(school)

        # Section gauche - haut
        tk.Label(self.left_top, text="Importer les écoles à partir d'un fichier", bg="lightgreen").pack(pady=10)
        tk.Button(self.left_top, text="Choisir un fichier", command=lambda: self.import_json()).pack()

        # Section gauche - bas
        tk.Label(self.left_bottom, text="Ajouter une école via le formulaire", bg="lightyellow").pack(pady=10)
        self.input_school_name = self.add_input(self.left_bottom, "Nom école:", StringVar())
        self.input_school_capacity = self.add_input(self.left_bottom, "Capacité:", IntVar())
        tk.Button(self.left_bottom, text="Ajouter", command=lambda: self.btn_add_school()).pack(side="bottom")
    
    # -------------------------
    # Page import des élèves
    # -------------------------
    def page_import_student(self):

        # event
        self.current_page = self.page_import_student
        self.btn_previous.configure(command=lambda: "")
        self.btn_next.configure(command=lambda: self.page_import_school())

        # Reset
        self.set_panel("panel_3sections")
        self.clean_panel()

        self.titre.configure(text="Etape 1 : Ajoutez vos étudiants")

        # Section droite
        tk.Label(self.right_section, text="Liste des etudiants", bg="lightblue").pack(pady=10)
        for student in self.student_list:
            self.add_student_item(student)

        # Section gauche - haut
        tk.Label(self.left_top, text="Importer les étudiants à partir d'un fichier", bg="lightgreen").pack(pady=10)
        tk.Button(self.left_top, text="Choisir un fichier", command=lambda: self.import_json()).pack()

        # Section gauche - bas
        tk.Label(self.left_bottom, text="Ajouter un étudiant via le formulaire", bg="lightyellow").pack(pady=10)
        self.input_student_last_name = self.add_input(self.left_bottom, "Nom étudiant:", StringVar())
        self.input_student_first_name = self.add_input(self.left_bottom, "Prénom étudiant:", StringVar())
        tk.Button(self.left_bottom, text="Ajouter", command=lambda: self.btn_add_student()).pack(side="bottom")
    
    # -------------------------
    # Page import des préférences d'élèves
    # -------------------------
    def page_import_student_preferences(self):
        # Event handlers
        self.current_page = self.page_import_student_preferences
        self.btn_previous.configure(command=lambda: self.save_and_switch_page("student", self.page_import_school))
        self.btn_next.configure(command=lambda: self.save_and_switch_page("student", self.page_import_school_preferences))

        # Reset
        self.set_panel("panel_tab")
        self.titre.configure(text="Etape 3 : Ajoutez les préférences des étudiants")
        self.render_preference_table("student")

    # -------------------------
    # Page import des préférences d'écoles
    # -------------------------
    def page_import_school_preferences(self):
        self.current_page = self.page_import_school_preferences
        # Event handlers
        self.btn_previous.configure(command=lambda: self.save_and_switch_page("school", self.page_import_student_preferences))
        self.btn_next.configure(command=lambda: self.save_and_switch_page("school", self.page_result_student))

        # Reset
        self.set_panel("panel_tab")
        self.titre.configure(text="Etape 4 : Ajoutez les préférences des écoles")
        self.render_preference_table("school")

    # -------------------------
    # Page des résultats avec des choix etudiant
    # -------------------------  
    def page_result_student(self):
        self.btn_previous.configure(command=lambda: self.page_import_school_preferences())
        self.btn_next.configure(command=lambda: self.page_result_school())
        self.titre.configure(text="Resultat choix par les étudiants:")
        self.set_panel("panel_tab")
        self.clean_table()

        marriage = StableMarriage(self.student_list, self.school_list)
        res = marriage.selection_student()
        self.afficher_resultat(res[2], res[1], res[-1])


    # -------------------------
    # Page des résultats avec des choix etudiant
    # -------------------------  
    def page_result_school(self):
        self.btn_previous.configure(command=lambda: self.page_result_student())
        self.btn_next.configure(command=lambda: "")
        self.titre.configure(text="Resultat choix par les écoles:")
        self.set_panel("panel_tab")
        self.clean_table()
        
        marriage = StableMarriage(self.student_list, self.school_list)
        res = marriage.selection_school()
        self.afficher_resultat(res[0], res[1], res[-1])

    #==================================================== | Calculs | =========================================================

    # -------------------------
    # Sauvegarde des préférences + changement de page
    # -------------------------

    def afficher_resultat(self, school_liste, student_list, unused):
        # Efface le contenu précédent du tableau
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Couleurs
        COLOR_HEADER = "lightblue"
        COLOR_ASSIGNED = "white"
        COLOR_UNASSIGNED = "#ffcccc"  # Rouge clair
        FONT_HEADER = ('Helvetica', 10, 'bold')

        # Construire les données des écoles (acceptées)
        result = {}
        for school in school_liste:
            accepted_students = [student for student in school.preferences.values() if student is not None]
            sorted_students = sorted(accepted_students, key=lambda s: s.id)
            title = f"{school.name}  ({len(sorted_students)}/{school.capacity})"
            result[title] = [student.str_compact() for student in sorted_students]

        # Étudiants non affectés
        result["Étudiants non affectés"] = [student.str_compact() for student in sorted(student_list, key=lambda s: s.id)]

        # Affichage : une colonne par école + 1 pour les non affectés
        for col, title in enumerate(result.keys()):
            # En-tête
            tk.Label(self.table_frame, text=title, borderwidth=1, relief="solid", width=25,
                    bg=COLOR_HEADER, font=FONT_HEADER).grid(row=0, column=col, sticky="nsew")

            # Lignes (étudiants)
            students = result[title]
            bg_color = COLOR_UNASSIGNED if title == "Étudiants non affectés" else COLOR_ASSIGNED
            for row, student in enumerate(students):
                tk.Label(self.table_frame, text=student, borderwidth=1, relief="solid", width=25,
                        bg=bg_color).grid(row=row + 1, column=col, sticky="nsew")



    # -------------------------
    # Sauvegarde des préférences + changement de page
    # -------------------------
    def save_and_switch_page(self, save_mode, page_name_func):
        self.validate_preferences(save_mode)
        page_name_func()


    # -------------------------
    # Création du tableau
    # -------------------------
    def render_preference_table(self, mode):
        self.set_panel("panel_tab")
        self.clean_table()  # à créer si pas déjà fait
        self.preferences_entries = {}

        # Définir lignes et colonnes selon le mode
        if mode == "student":
            rows = self.student_list
            cols = self.school_list
            get_preferences = lambda obj: obj.get_preference()
        elif mode == "school":
            rows = self.school_list
            cols = self.student_list
            get_preferences = lambda obj: obj.get_preference()
        else:
            raise ValueError("Mode inconnu")

        # En-têtes de colonnes
        for col_idx, col_obj in enumerate(cols):
            titre = tk.Label(
                self.table_frame,
                text=col_obj.str_compact(),
                borderwidth=1,
                relief="solid",
                width=15,
                bg="lightblue",
                anchor="w"
            )
            titre.grid(row=0, column=col_idx + 1)

        # Lignes + champs
        for row_idx, row_obj in enumerate(rows):
            titre = tk.Label(
                self.table_frame,
                text=row_obj.str_compact(),
                borderwidth=1,
                relief="solid",
                width=15,
                bg="lightblue",
                anchor="w"
            )
            titre.grid(row=row_idx + 1, column=0)

            pref_list = get_preferences(row_obj)

            for col_idx, col_obj in enumerate(cols):
                entry = tk.Entry(self.table_frame, width=5, justify="center")
                entry.grid(row=row_idx + 1, column=col_idx + 1)
                self.preferences_entries[(row_idx, col_idx)] = entry

                # Pré-remplissage si col_obj présent dans les préférences
                if pref_list:
                    if col_obj.id in pref_list:
                        rank = pref_list.index(col_obj.id)
                        entry.insert(0, str(rank))

    # -------------------------
    # Import a partir d'un Json
    # -------------------------    
    def import_json(self):
        importer = Importer(self.root)
        schools, students = importer.charger_fichier()
        for student in students:
            self.student_list.append(student)
        for school in schools:
            self.school_list.append(school)
        self.current_page()
    
    # -------------------------
    # Remplis le tableau des préférences aléatoirement
    # ------------------------- 
    def fill_preferences_randomly(self):
        if not hasattr(self, "preferences_entries"):
            return

        # Déterminer les dimensions du tableau
        row_indices = set(row for (row, _) in self.preferences_entries.keys())
        col_indices = set(col for (_, col) in self.preferences_entries.keys())
        num_cols = len(col_indices)

        for row in row_indices:
            values = list(range(num_cols))
            random.shuffle(values)  # permutation aléatoire

            for col, val in zip(sorted(col_indices), values):
                entry = self.preferences_entries.get((row, col))
                if entry:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(val))
        
    #==================================================== | Ajout | =========================================================

    # -------------------------
    # Sauvegarde des préférences
    # -------------------------
    def validate_preferences(self, mode):
        if mode == "student":
            targets = self.student_list
            sources = self.school_list
        elif mode == "school":
            targets = self.school_list
            sources = self.student_list
        else:
            raise ValueError("Mode inconnu")

        for row_idx, target in enumerate(targets):
            raw = {}
            for col_idx, source in enumerate(sources):
                entry = self.preferences_entries.get((row_idx, col_idx))
                if entry:
                    val = entry.get().strip()
                    if val.isdigit():
                        rank = int(val)
                        if rank not in raw:
                            raw[rank] = source.id
            preferences = [raw[k] for k in sorted(raw)]
            target.set_preference(preferences)
            #setattr(target, attr, preferences)

    # -------------------------
    # Ajout de label
    # -------------------------

    def add_student_item(self, student_object):
        student_panel = tk.Frame(self.right_section, bg="lightblue")
        student_panel.pack(fill="x", pady=2)

        # Label à gauche
        tk.Label(student_panel, text=str(student_object)).grid(row=0, column=0, sticky="w", padx=5)
        
        # Bouton à droite
        tk.Button(
            student_panel,
            text="Suppr " + str(student_object.id),
            command=lambda: self.remove_student_item(student_object, student_panel)
        ).grid(row=0, column=1, sticky="e", padx=5)

    def add_school_item(self, school_object):
        school_panel = tk.Frame(self.right_section, bg="lightblue")
        school_panel.pack(fill="x", pady=2)

        # Label à gauche
        tk.Label(school_panel, text=str(school_object)).grid(row=0, column=0, sticky="w", padx=5)
        
        # Bouton à droite
        tk.Button(
            school_panel,
            text="Suppr " + str(school_object.id),
            command=lambda: self.remove_school_item(school_object, school_panel)
        ).grid(row=0, column=1, sticky="e", padx=5)

    def remove_student_item(self, student_object, student_panel):
        student_panel.destroy()
        # for school in self.school_list:
        #     if student_object.id in school.student_preferences:
        #         school.student_preferences.remove(student_object.id)
        #         school.set_preference(school.student_preferences)
        self.student_list.remove(student_object)

    def remove_school_item(self, school_object, school_panel):
        school_panel.destroy()
        # for student in self.student_list:
        #     if school_object.id in student.school_preferences:
        #         student.school_preferences.remove(school_object.id)
        #         student.set_preference(student.school_preferences)
        self.school_list.remove(school_object)
    
    # -------------------------
    # Ajout d'objet school à la liste
    # -------------------------
    def btn_add_school(self):
        # recuperation des valeurs du formulaire
        school_name = self.input_school_name.get()
        try:
            school_capacity = int(self.input_school_capacity.get())
        except (ValueError, TypeError):
            school_capacity = 0

        # creation de l'objet
        new_school = Entity(
            school_name,
            school_capacity,
            []
        )
        self.school_list.append(new_school)
        self.add_school_item(new_school)
    
    # -------------------------
    # Ajout d'objet student à la liste
    # -------------------------
    def btn_add_student(self):
        # recuperation des valeurs du formulaire
        student_first_name = self.input_student_first_name.get()
        student_last_name = self.input_student_last_name.get()

        # creation de l'objet
        new_student = Entity(student_first_name + " " + student_last_name,1, [])
        self.student_list.append(new_student)
        self.add_student_item(new_student)
        
    # -------------------------
    # Ajout de champs de texte avec légende
    # -------------------------
    def add_input(self, cadre, nom, var):
        tk.Label(cadre, text=nom, bg="lightyellow").pack()
        nom_entree = tk.Entry(cadre, width=30, textvariable=var)
        nom_entree.pack()
        return nom_entree

    # -------------------------
    # Lancer le programme
    # -------------------------
    def run(self):
        self.root.mainloop()
    
    def create_random_test_data(self):
        schools = [School(f"École {i+1}", 10, []) for i in range(3)]
        for school in schools:
            school.preferences
        students = [Student(f"Prenom{i}", f"Nom{i}", []) for i in range(8)]
        random.shuffle(students)
        return {
            schools[0]: students[:3],
            schools[1]: students[3:4],
            schools[2]: students[4:]
        }
    


# Création et exécution de l'application
if __name__ == "__main__":
    app = Window()
    app.page_import_student()
    app.run()
