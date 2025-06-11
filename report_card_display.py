import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, font as tkfont
import json
import os
from report_card import Subject, Period, ReportCard

class BoletimApp:
    def __init__(self, root):
        # Main presets
        self.root = root
        self.root.title("Boletim Escolar")
        self.root.geometry("1280x720")

        self.period_count = 0

        # Report Card Program Integration
        self.report_card = ReportCard()
        
        # Frames Creation Functions Call
        self.create_main_frames()
        self.create_period_display_area()

        # Report Card Buttons Font
        self.button_font = tkfont.Font(family="Arial", size=50)
        self.root.bind("<Configure>", self.update_button_font)

        # Buttons
        self.add_period_button = tk.Button(self.aux_frame, text="Adicionar Período", font=self.button_font, command=self.add_period)
        self.add_period_button.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.8, relheight=0.1)

        self.load_report_card = tk.Button(self.aux_frame, text="Carregar Boletim", font=self.button_font, command=self.load_report_card_periods)
        self.load_report_card.place(relx=0.5, rely=0.68, anchor="center", relwidth=0.8, relheight=0.1)

        self.save_report_card = tk.Button(self.aux_frame, text="Salvar Boletim", font=self.button_font, command=self.save_report_card_to_file)
        self.save_report_card.place(relx=0.5, rely=0.56, anchor="center", relwidth=0.8, relheight=0.1)


    # Main Frames Creation Function
    def create_main_frames(self):
        self.main_frame = tk.Frame(self.root, bd=10, relief="sunken")
        self.main_frame.place(relx=0, rely=0, relwidth=0.8, relheight=1.0)

        self.aux_frame = tk.Frame(self.root, bd=10, relief="sunken")
        self.aux_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=1.0)

    # Periods Frame
    def create_period_display_area(self):
        self.period_display_frame = tk.Frame(self.main_frame)
        self.period_display_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Button Dinamic Font Size Function
    def update_button_font(self, event=None):
        height = self.aux_frame.winfo_height()
        width = self.aux_frame.winfo_width()
        avg = (width + height) / 2

        new_font_size = max(10, int(avg * 0.02))
        self.button_font.configure(size=new_font_size)

    # Add Periods Function
    def add_period(self):
        self.period_count += 1
        period_name = f"Período {self.period_count}"

        new_period = Period(period_name)
        self.report_card.insert_period(new_period)

        self.add_gui_period(period_name)
        print("período adicionado com sucesso!\n")

    # Add Period GUI Function
    def add_gui_period(self, period_name):
        # Encontra o período pelo nome
        period = next((p for p in self.report_card.periods if p.name == period_name), None)
        if period is None:
            return

        frame = tk.LabelFrame(self.period_display_frame, text=period_name, padx=10, pady=10, font=("Arial", 14))
        frame.pack(fill="x", pady=10, padx=10)

        if not period.subjects:
            label = tk.Label(frame, text="(Nenhuma matéria ainda)", font=("Arial", 12))
            label.pack(anchor="w")
            return
        
        header = tk.Frame(frame)
        header.pack(fill="x", pady=(0, 5))
        tk.Label(header, text="Matéria", width=37, anchor="w", font=("Arial", 12, "bold")).pack(side="left")
        tk.Label(header, text="Nota", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")
        tk.Label(header, text="Créditos", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")
        tk.Label(header, text="Resultado", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")

        # Lista de matérias
        for subject in period.subjects:
            row = tk.Frame(frame)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=str(subject.name), width=41, anchor="w", font=("Arial", 12)).pack(side="left")
            tk.Label(row, text=str(subject.grade), width=16, anchor="center", font=("Arial", 12)).pack(side="left")
            tk.Label(row, text=str(subject.credits), width=15, anchor="center", font=("Arial", 12)).pack(side="left")
            tk.Label(row, text=str("Aprovado" if subject.result else "Reprovado"), width=16, anchor="center", font=("Arial", 12)).pack(side="left")


    # Load Periods Function
    def load_report_card_periods(self):
        self.report_card.load_from_file_json("report_card_save.json")
        for widget in self.period_display_frame.winfo_children():
            widget.destroy()
        self.period_count = 0

        for period in self.report_card.periods:
            self.period_count += 1
            self.add_gui_period(period.name)
        print("período carregado com sucesso!\n")
    
    # Save Report Card Function
    def save_report_card_to_file(self):
        self.report_card.save_to_file_json("report_card_save.json")
        messagebox.showinfo("Sucesso", "Boletim salvo com sucesso!")

def startWindow():
    root = tk.Tk()
    app = BoletimApp(root)
    root.mainloop()