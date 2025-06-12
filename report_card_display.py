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
        period_name = simpledialog.askstring("Nome do Período", "Digite o nome do novo período:")
        if not period_name:
            return

        if any(p.name == period_name for p in self.report_card.periods):
            messagebox.showerror("Erro", "Já existe um período com esse nome.")
            return
        
        self.period_count += 1

        new_period = Period(period_name)
        self.report_card.insert_period(new_period)

        self.add_gui_period(period_name)
        messagebox.showinfo("Sucesso!", "Período carregado com sucesso!")




    # Add Period GUI Function
    def add_gui_period(self, period_name):
        period = next((p for p in self.report_card.periods if p.name == period_name), None)
        if period is None:
            return

        frame = tk.LabelFrame(self.period_display_frame, text=period_name, padx=10, pady=10, font=("Arial", 14))
        frame.pack(fill="x", pady=10, padx=10)

        if not period.subjects:
            label = tk.Label(frame, text="(Nenhuma matéria ainda)", font=("Arial", 12))
            label.pack(anchor="w")
        else:
            header = tk.Frame(frame)
            header.pack(fill="x", pady=(0, 5))
            tk.Label(header, text="Matéria", width=37, anchor="w", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(header, text="Nota", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(header, text="Créditos", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(header, text="Resultado", width=14, anchor="center", font=("Arial", 12, "bold")).pack(side="left")

            for subject in period.subjects:
                row = tk.Frame(frame)
                row.pack(fill="x", pady=2)

                tk.Label(row, text=str(subject.name), width=41, anchor="w", font=("Arial", 12)).pack(side="left")
                tk.Label(row, text=str(subject.grade), width=16, anchor="center", font=("Arial", 12)).pack(side="left")
                tk.Label(row, text=str(subject.credits), width=15, anchor="center", font=("Arial", 12)).pack(side="left")
                tk.Label(row, text="Aprovado" if subject.result else "Reprovado", width=16, anchor="center", font=("Arial", 12)).pack(side="left")

                remove_button = tk.Button(row, text="Remover", font=("Arial", 10),
                                  command=lambda s=subject, p=period: self.remove_subject(p, s))
                remove_button.pack(side="left", padx=5)

        # Insert Subject Button
        add_subject_btn = tk.Button(frame, text="Adicionar Matéria", font=("Arial", 12),
                                    command=lambda p=period: self.add_subject_dialog(p))
        add_subject_btn.pack(anchor="w", pady=(5, 0))

        # Remove Period Button
        remove_btn = tk.Button(frame, text="X", font=("Arial", 12, "bold"), fg="red",
                               command=lambda p=period: self.remove_period(p))
        remove_btn.place(relx=1.0, x=0, y=0, anchor="ne")

        # Period Footer Information
        stats_frame = tk.Frame(frame)
        stats_frame.pack(fill="x", pady=10)

        # Calculate Stats Functions Call
        index = self.report_card.periods.index(period) + 1

        period_average = period.calculate_period_average()
        period_credits = period.calculate_period_credits()
        earned_period_credits = period.calculate_period_earned_credits()
        period_fails = period.calculate_period_fails()
        total_average = self.report_card.calculate_current_total_average(index)
        total_credits = self.report_card.calculate_current_total_credits(index)
        total_earned_credits = self.report_card.calculate_current_total_earned_credits(index)
        total_reprov = self.report_card.calculate_current_total_fails(index)

        stats_text = (
            f"Média do Período: {period_average:.2f}   Créditos do Período: {period_credits:.2f}   Créditos Obtidos: {earned_period_credits:.2f}   Reprovações: {period_fails:}\n"
            f"Média Total: {total_average:.2f}    Créditos Acumulados: {total_credits:.2f}   CRO Total: {total_earned_credits:.2f}   Total de Reprovações: {total_reprov}"
        )
        tk.Label(stats_frame, text=stats_text, font=("Arial", 10, "bold"), anchor="center").pack()

    def add_subject_dialog(self, period):
        # Subject Insertion Window
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Adicionar matéria - {period.name}")
        dialog.geometry("350x250")
        dialog.grab_set()  # modal

        tk.Label(dialog, text="Nome da Matéria:").pack(pady=5)
        entry_name = tk.Entry(dialog)
        entry_name.pack(pady=5, fill="x", padx=10)

        tk.Label(dialog, text="Nota:").pack(pady=5)
        entry_grade = tk.Entry(dialog)
        entry_grade.pack(pady=5, fill="x", padx=10)

        tk.Label(dialog, text="Créditos:").pack(pady=5)
        entry_credits = tk.Entry(dialog)
        entry_credits.pack(pady=5, fill="x", padx=10)

        def on_add():
            try:
                name = entry_name.get().strip()
                grade = float(entry_grade.get())
                credits = float(entry_credits.get())
                if not name:
                    raise ValueError("Nome da matéria vazio")

                subject = Subject(name, grade, credits)
                period.insert_subject(subject)

                dialog.destroy()
                # Display refresh
                for widget in self.period_display_frame.winfo_children():
                    widget.destroy()
                for p in self.report_card.periods:
                    self.add_gui_period(p.name)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar matéria: {e}")

        btn_add = tk.Button(dialog, text="Adicionar", command=on_add)
        btn_add.pack(pady=10)

    # Remove Subject Function
    def remove_subject(self, period, subject):
        confirm = messagebox.askyesno("Confirmar", f"Remover a matéria '{subject.name}'?")
        if confirm:
            period.delete_subject(subject)
    
            # Refresh Display
            for widget in self.period_display_frame.winfo_children():
                widget.destroy()
            for p in self.report_card.periods:
                self.add_gui_period(p.name)


    def remove_period(self, period):
        confirm = messagebox.askyesno("Confirmar", f"Remover o período '{period.name}'?")
        if confirm:
            self.report_card.delete_period(period)
            self.period_count -= 1

            # Refresh Display
            for widget in self.period_display_frame.winfo_children():
                widget.destroy()
            for p in self.report_card.periods:
                self.add_gui_period(p.name)

        messagebox.showinfo("Sucesso!", "Período removido com sucesso!")


    # Load Periods Function
    def load_report_card_periods(self):
        self.report_card.load_from_file_json("report_card_save.json")
        for widget in self.period_display_frame.winfo_children():
            widget.destroy()
        self.period_count = 0

        for period in self.report_card.periods:
            self.period_count += 1
            self.add_gui_period(period.name)
        
        messagebox.showinfo("Sucesso!", "Período carregado com sucesso!")
    
    # Save Report Card Function
    def save_report_card_to_file(self):
        self.report_card.save_to_file_json("report_card_save.json")
        messagebox.showinfo("Sucesso", "Boletim salvo com sucesso!")

def startWindow():
    root = tk.Tk()
    app = BoletimApp(root)
    root.mainloop()