class Disciplina:
    def __init__(self, nome, creditos, nota):
        self.nome = nome
        self.creditos = creditos
        self.nota = nota

    def aprovado(self):
        return self.nota >= 5


class Periodo:
    def __init__(self, nome):
        self.nome = nome
        self.disciplinas = []

    def adicionar_disciplina(self, disciplina):
        self.disciplinas.append(disciplina)

    def media_periodo(self):
        if not self.disciplinas:
            return 0
        soma = sum(d.nota * d.creditos for d in self.disciplinas)
        total_creditos = sum(d.creditos for d in self.disciplinas)
        return soma / total_creditos if total_creditos > 0 else 0

    def creditos_obtidos(self):
        return sum(d.creditos for d in self.disciplinas if d.aprovado())


class Boletim:
    def __init__(self):
        self.periodos = []

    def adicionar_periodo(self, periodo):
        self.periodos.append(periodo)

    def media_final(self):
        soma_ponderada = 0
        total_creditos = 0
        for periodo in self.periodos:
            for d in periodo.disciplinas:
                soma_ponderada += d.nota * d.creditos
                total_creditos += d.creditos
        return soma_ponderada / total_creditos if total_creditos > 0 else 0

    def creditos_totais_obtidos(self):
        return sum(p.creditos_obtidos() for p in self.periodos)

    def exibir_boletim(self):
        print("\n==== BOLETIM UNIVERSITÁRIO ====\n")
        for p in self.periodos:
            print(f"Período: {p.nome}")
            for d in p.disciplinas:
                status = "Aprovado" if d.aprovado() else "Reprovado"
                print(f"  - {d.nome}: Nota {d.nota}, Créditos {d.creditos}, {status}")
            print(f"  Média do período: {p.media_periodo():.2f}")
            print(f"  Créditos obtidos: {p.creditos_obtidos()}")
            print()
        print("==== RESUMO FINAL ====")
        print(f"Créditos acumulados: {self.creditos_totais_obtidos()}")
        print(f"Média final ponderada: {self.media_final():.2f}")


def main():
    boletim = Boletim()
    num_periodos = int(input("Quantos períodos deseja adicionar? "))

    for i in range(num_periodos):
        nome_periodo = input(f"\nDigite o nome do {i + 1}º período: ")
        periodo = Periodo(nome_periodo)

        num_disciplinas = int(input(f"Quantas disciplinas no {nome_periodo}? "))
        for j in range(num_disciplinas):
            print(f"\nDisciplina {j + 1}:")
            nome = input("  Nome: ")
            creditos = int(input("  Créditos: "))
            nota = float(input("  Nota: "))
            disciplina = Disciplina(nome, creditos, nota)
            periodo.adicionar_disciplina(disciplina)

        boletim.adicionar_periodo(periodo)

    boletim.exibir_boletim()


if __name__ == "__main__":
    main()
