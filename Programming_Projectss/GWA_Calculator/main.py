import customtkinter as ctk
from tkinter import messagebox
import os
import sys

def resource_path(relative_path):
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Subject:
    def __init__(self, name, units, grade):
        self.name = name
        self.units = float(units)
        self.grade = float(grade)

class GwaCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GWA Calculator")
        self.geometry("420x500")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.iconbitmap(resource_path("icon.ico"))

        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon not loaded: {e}")
            pass  # Continue without icon

        self.subjects = []
        
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the 3-column layout
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Subject Name Entry
        self.subject_name_entry = ctk.CTkEntry(input_frame, placeholder_text="Subject Name")
        self.subject_name_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Units Entry
        self.units_entry = ctk.CTkEntry(input_frame, placeholder_text="Units")
        self.units_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Grade Entry
        self.grade_entry = ctk.CTkEntry(input_frame, placeholder_text="Grade")
        self.grade_entry.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Make columns expand equally
        input_frame.grid_columnconfigure(0, weight=1)
        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(2, weight=1)

        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, padx=10, fill="x")
        # Add Subs
        self.add_button = ctk.CTkButton(button_frame, text="Add Subject", command=self.add_subject)
        self.add_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        #Calculate
        self.calculate_button = ctk.CTkButton(button_frame, text="Calculate GWA", command=self.calculate_gwa)
        self.calculate_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_subjects)
        self.clear_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Expanded cols
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)
        # Labels
        labels_frame = ctk.CTkFrame(self)
        labels_frame.pack(padx=10, fill="x")

        # List of Subjects Label
        self.list_of_subjects_label = ctk.CTkLabel(labels_frame, text="Subjects")
        self.list_of_subjects_label.grid(row=0, column=0, padx=5, sticky="w")

        # Units
        self.units_label = ctk.CTkLabel(labels_frame, text="Units")
        self.units_label.grid(row=0, column=1, padx=5, sticky="w")

        # Grades
        self.grades_label = ctk.CTkLabel(labels_frame, text="Grades")
        self.grades_label.grid(row=0, column=2, padx=5, sticky="w")

        # Cols
        labels_frame.grid_columnconfigure(0, weight=1)
        labels_frame.grid_columnconfigure(1, weight=1)
        labels_frame.grid_columnconfigure(2, weight=1)

        # Tkinter Listbox
        import tkinter as tk
        self.subject_listbox = tk.Listbox(self)
        self.subject_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        
    def add_subject(self):
        name = self.subject_name_entry.get()
        units = self.units_entry.get()
        grade = self.grade_entry.get()

        if not name or not units or not grade:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        
        try:
            
            self.subject_listbox.configure(font=("Courier New", 15))
            subject =  Subject(name, float(units), float(grade))
            self.subjects.append(subject)
            line = f"{subject.name.ljust(20)} {str(subject.units).ljust(20)} {subject.grade}"
            self.subject_listbox.insert("end", line )
            self.subject_listbox.itemconfig("end", {'bg': 'grey', 'fg': 'black'})
            self.subject_name_entry.delete(0, "end")
            self.units_entry.delete(0, "end")
            self.grade_entry.delete(0, "end")
        except ValueError:
            messagebox.showerror("Input Error", "Units and Grade must be numbers.")
    def calculate_gwa(self):
        if not self.subjects:
            messagebox.showwarning("Calculation Error", "No subjects added.")
            return
        
        total_weighted = sum(sub.grade * sub.units for sub in self.subjects)
        total_units = sum(sub.units for sub in self.subjects)
        gwa = total_weighted / total_units if total_units > 0 else 0

        if gwa < 3.0:
            remarks = "Passed"
            if 1.0 <= gwa <= 1.3:
                award = "President's Lister"
            elif 1.31 <= gwa <= 1.5:
                award = "Deans Lister"
            else:
                award = "None"
            messagebox.showinfo("GWA Result", f"GWA: {gwa:.2f}\nRemarks: {remarks}\nAward: {award}")
        else:
            remarks = "Failed"
            messagebox.showinfo("GWA Result", f"GWA: {gwa:.2f}\nRemarks: {remarks}")

    def clear_subjects(self):
        self.subjects.clear()
        self.subject_listbox.delete(0, ctk.END)
        self.result_label.configure(text="")
        self.subject_name_entry.delete(0, ctk.END)
        self.units_entry.delete(0, ctk.END)
        self.grade_entry.delete(0, ctk.END)

if __name__ == "__main__":
    app = GwaCalculator()
    app.mainloop() 



