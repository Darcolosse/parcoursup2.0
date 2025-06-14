import tkinter as tk
from tkinter import filedialog, messagebox
import json
from student import Student
from school import School

class Importer:
    def __init__(self, parent_window=None):
        self.parent = parent_window or tk.Tk()
    
    @staticmethod
    def importer(file_path: str):
        data = json.load(file_path)
        return [School(school['name'], school['capacity'], school["student_preferences"], {key: None for key in school["student_preferences"]}) for school in data['schools']],               [Student(student['first_name'], student['last_name'], student["school_preferences"]) for student in data['students']]

    def charger_fichier(self):
        filepath = filedialog.askopenfilename(
            parent=self.parent,
            title="Sélectionner un fichier JSON",
            filetypes=[("Fichiers JSON", "*.json")]
        )
        if not filepath:
            return [], []  # utilisateur a annulé

        try:
            with open(filepath, 'r', encoding='utf-8') as file_path:
                return  Importer.importer(file_path)

        except Exception as e:
            messagebox.showerror("Erreur de lecture", f"Impossible de lire le fichier : {e}")
            return [], []