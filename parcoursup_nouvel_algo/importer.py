import tkinter as tk
from tkinter import filedialog, messagebox
import json
from entity import Entity

class Importer:
    def __init__(self, parent_window=None):
        self.parent = parent_window or tk.Tk()
    
    @staticmethod
    def importer(file_path: str):
        data = json.load(file_path)
        school_list = [
                Entity(
                    school['name'],
                    school['capacity'],
                    school["preferences"],
                    is_student=False
                ) for school in data['schools']
            ]
        student_list = [
                Entity(
                    student['name'],
                    student['capacity'],
                    student["preferences"],
                    is_student=True
                ) for student in data['students']
            ]
        return school_list, student_list

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