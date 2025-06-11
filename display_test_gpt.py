import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, font
import json
import os

class BoletimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Boletim Escolar")
        self.root.geometry("1280x720")

        self.periodos = {}

        self.final_media_label = tk.Label(root, text="Média Final: --", font=("Arial", 20, "bold"))
        self.final_media_label.place(relx=0.95, rely=0.0, x=-20, y=20, anchor="ne")

        self.main_frame = tk.Frame(root)
        self.main_frame.place(relx=0.0, rely=0.0, relwidth=0.75, relheight=1.0)
        self.main_frame.pack_propagate(False)

        self.canvas = tk.Canvas(self.main_frame)
        self.scroll_y = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10, anchor="sw")

        self.btn_stack_frame = tk.Frame(self.bottom_frame)
        self.btn_stack_frame.pack(side="left", anchor="sw")

        self.btn_add_periodo = tk.Button(self.btn_stack_frame, text="Adicionar Período", command=self.adicionar_periodo, width=20)
        self.btn_add_periodo.pack(pady=5)

        self.btn_salvar = tk.Button(self.btn_stack_frame, text="Salvar Boletim", command=self.salvar_boletim, width=20)
        self.btn_salvar.pack(pady=5)

        self.btn_carregar = tk.Button(self.btn_stack_frame, text="Carregar Boletim", command=self.carregar_boletim, width=20)
        self.btn_carregar.pack(pady=5)

        self.atualizar_interface()

    def atualizar_interface(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for periodo, materias in self.periodos.items():
            frame_periodo = tk.LabelFrame(
                self.scroll_frame,
                text=periodo,
                padx=10,
                pady=10,
                font=("Arial", 14, "bold")
            )
            frame_periodo.pack(fill="x", pady=5, padx=10)

            if materias:
                header_frame = tk.Frame(frame_periodo)
                header_frame.pack(fill="x", padx=5)
                headers = ["Matéria", "Nota", "Créditos", "Situação"]
                widths = [30, 10, 10, 15]
                for i, (h, w) in enumerate(zip(headers, widths)):
                    lbl = tk.Label(header_frame, text=h, font=("Arial", 12, "bold"),
                                   width=w, anchor="center", justify="center",
                                   bd=1, relief="solid")
                    lbl.grid(row=0, column=i, padx=1, pady=1)

            for idx, materia in enumerate(materias):
                row_container = tk.Frame(frame_periodo)
                row_container.pack(fill="x", padx=5, pady=1)

                row_frame = tk.Frame(row_container)
                row_frame.pack(side="left")

                # Matéria largura fixa igual ao cabeçalho
                tk.Label(row_frame, text=materia['nome'], font=("Arial", 12), width=30,
                         anchor="w", bd=1, relief="solid").grid(row=0, column=0, padx=1)

                tk.Label(row_frame, text=materia['nota'], font=("Arial", 12), width=10,
                         anchor="center", justify="center", bd=1, relief="solid").grid(row=0, column=1, padx=1)

                tk.Label(row_frame, text=materia['cr'], font=("Arial", 12), width=10,
                         anchor="center", justify="center", bd=1, relief="solid").grid(row=0, column=2, padx=1)

                tk.Label(row_frame, text=materia['situacao'], font=("Arial", 12), width=15,
                         anchor="center", justify="center", bd=1, relief="solid").grid(row=0, column=3, padx=1)

                btn_remover = tk.Button(row_container, text="Remover", command=lambda p=periodo, m=materia: self.remover_materia(p, m), width=10)
                btn_remover.pack(side="right", padx=5)

            botoes_frame = tk.Frame(frame_periodo)
            botoes_frame.pack(pady=10)

            btn_add_materia = tk.Button(botoes_frame, text="Adicionar Matéria", command=lambda p=periodo: self.adicionar_materia(p))
            btn_add_materia.pack(side="left", padx=10)

            btn_remover_periodo = tk.Button(botoes_frame, text="Remover Período", command=lambda p=periodo: self.remover_periodo(p))
            btn_remover_periodo.pack(side="left", padx=10)

            info_text = "Média do Período: -- | Média Acumulada: -- | Créditos Acumulados: -- | Créditos Obtidos: --"
            lbl_info = tk.Label(frame_periodo, text=info_text, font=("Arial", 10, "italic"))
            lbl_info.pack(pady=5)

            lbl_reprovacoes = tk.Label(frame_periodo, text="Total de Reprovações: --", font=("Arial", 10, "italic"))
            lbl_reprovacoes.pack(pady=(0, 5))

    def adicionar_periodo(self):
        self.root.lift()
        nome_periodo = simpledialog.askstring("Novo Período", "Digite o nome do período:", parent=self.root)
        if nome_periodo:
            if nome_periodo in self.periodos:
                messagebox.showerror("Erro", "Período já existe.")
            else:
                self.periodos[nome_periodo] = []
                self.atualizar_interface()

    def adicionar_materia(self, periodo):
        self.root.lift()
        nome = simpledialog.askstring("Adicionar Matéria", "Nome da matéria:", parent=self.root)
        nota = simpledialog.askstring("Adicionar Matéria", "Nota:", parent=self.root)
        cr = simpledialog.askstring("Adicionar Matéria", "Créditos:", parent=self.root)
        situacao = simpledialog.askstring("Adicionar Matéria", "Situação:", parent=self.root)

        if nome and nota and cr and situacao:
            self.periodos[periodo].append({
                "nome": nome,
                "nota": nota,
                "cr": cr,
                "situacao": situacao
            })
            self.atualizar_interface()

    def remover_materia(self, periodo, materia):
        self.periodos[periodo].remove(materia)
        self.atualizar_interface()

    def remover_periodo(self, periodo):
        del self.periodos[periodo]
        self.atualizar_interface()

    def salvar_boletim(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.periodos, f, indent=4, ensure_ascii=False)
                messagebox.showinfo("Sucesso", "Boletim salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao salvar", str(e))

    def carregar_boletim(self):
        filepath = filedialog.askopenfilename(defaultextension=".json", filetypes=[("Arquivos JSON", "*.json")])
        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.periodos = json.load(f)
                self.atualizar_interface()
                messagebox.showinfo("Sucesso", "Boletim carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro ao carregar", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BoletimApp(root)
    root.mainloop()
