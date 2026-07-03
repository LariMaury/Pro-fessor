import customtkinter as ctk
import pandas as pd
import os
from tkinter import messagebox, filedialog

# Configuração visual
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class LauncherConfig(ctk.CTk):
    """Primeira janela: Fixa os valores e permite escolher a planilha da turma"""
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.geometry("450x420")
        self.resizable(False, False)
        
        self.caminho_planilha = "" # Guardará o arquivo selecionado

        ctk.CTkLabel(self, text="Configuração da Etapa", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        # Botão para selecionar o arquivo da turma
        self.btn_selecionar = ctk.CTkButton(self, text="Selecionar Planilha da Turma", fg_color="#CF31A0", hover_color="#770755", command=self.escolher_arquivo)
        self.btn_selecionar.pack(pady=10)
        
        # Label que mostra qual planilha está ativa
        self.lbl_arquivo_status = ctk.CTkLabel(self, text="Nenhuma planilha selecionada", font=ctk.CTkFont(size=11, slant="italic"), text_color="gray")
        self.lbl_arquivo_status.pack(pady=2)

        # Campos de valores fixos
        ctk.CTkLabel(self, text="Valor do Caderno:").pack(pady=5)
        self.txt_valor = ctk.CTkEntry(self, placeholder_text="Ex: 5")
        self.txt_valor.pack(pady=2)

        ctk.CTkLabel(self, text="Total de Atividades:").pack(pady=5)
        self.txt_total = ctk.CTkEntry(self, placeholder_text="Ex: 15")
        self.txt_total.pack(pady=2)

        # Botão de iniciar
        self.btn_iniciar = ctk.CTkButton(self, text="Iniciar Lançamento", command=self.confirmar)
        self.btn_iniciar.pack(pady=25)

    def escolher_arquivo(self):
        # Abre a janela do Windows para você escolher o arquivo .xlsx
        arquivo = filedialog.askopenfilename(
            title="Selecione a planilha da turma",
            filetypes=[("Arquivos do Excel", "*.xlsx")]
        )
        if arquivo:
            self.caminho_planilha = arquivo
            nome_limpo = os.path.basename(arquivo) # Pega só o nome do arquivo, sem o caminho gigante
            self.lbl_arquivo_status.configure(text=f"Ativa: {nome_limpo}", text_color="#27AE60")

    def confirmar(self):
        if not self.caminho_planilha:
            messagebox.showerror("Erro", "Por favor, selecione a planilha da turma antes de iniciar.")
            return
            
        try:
            valor_max = float(self.txt_valor.get().replace(",", "."))
            total_ativ = int(self.txt_total.get())
            if total_ativ <= 0:
                messagebox.showerror("Erro", "O total de atividades deve ser maior que 0.")
                return
            
            # Fecha esta tela de configuração e abre a de lançamento
            self.destroy()
            self.callback(valor_max, total_ativ, self.caminho_planilha)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, preencha os campos com números válidos.")

class GerenciadorNotas(ctk.CTk):
    """Segunda janela: Fluxo de alunos baseado na planilha escolhida"""
    def __init__(self, valor_max, total_ativ, caminho_planilha):
        super().__init__()
        self.valor_max = valor_max
        self.total_ativ = total_ativ
        self.caminho_planilha = caminho_planilha
        
        self.title("Lançador de Notas")
        self.geometry("500x420")
        self.resizable(False, False)

        self.index_atual = 0
        self.carregar_planilha()

        # Interface
        nome_turma = os.path.basename(self.caminho_planilha)
        self.lbl_info = ctk.CTkLabel(
            self, 
            text=f"Turma: {nome_turma}  |  Caderno: {self.valor_max} pts  |  Atividades: {self.total_ativ}", 
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.lbl_info.pack(pady=10)

        self.lbl_aluno_titulo = ctk.CTkLabel(self, text="ALUNO ATUAL:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_aluno_titulo.pack(pady=2)
        
        self.lbl_nome_aluno = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=22, weight="bold"), text_color="#2b76be")
        self.lbl_nome_aluno.pack(pady=10)

        self.lbl_feitas = ctk.CTkLabel(self, text=f"Quantas atividades foram realizadas? (Máx: {self.total_ativ})")
        self.lbl_feitas.pack(pady=5)
        self.txt_feitas = ctk.CTkEntry(self, placeholder_text="Digite a quantidade")
        self.txt_feitas.pack(pady=5)
        
        self.txt_feitas.bind("<Return>", lambda event: self.salvar_e_proximo())

        self.btn_salvar = ctk.CTkButton(self, text="Salvar e Próximo Aluno", fg_color="#4CAF50", hover_color="#388E3C", command=self.salvar_e_proximo)
        self.btn_salvar.pack(pady=20)

        self.lbl_progresso = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=11))
        self.lbl_progresso.pack(side="bottom", pady=15)

        self.atualizar_aluno_na_tela()

    def carregar_planilha(self):
        self.df = pd.read_excel(self.caminho_planilha)
        
        # Validação simples para ajudar a professora se ela esquecer de estruturar a planilha nova
        if "Nome" not in self.df.columns:
            messagebox.showerror("Erro Crítico", "A planilha selecionada precisa ter uma coluna escrita 'Nome' na primeira linha.")
            self.destroy()
            return
            
        if "Nota" not in self.df.columns:
            self.df["Nota"] = ""

    def atualizar_aluno_na_tela(self):
        total_alunos = len(self.df)
        
        if self.index_atual < total_alunos:
            nome_aluno = self.df.iloc[self.index_atual]["Nome"]
            self.lbl_nome_aluno.configure(text=str(nome_aluno))
            self.lbl_progresso.configure(text=f"Aluno {self.index_atual + 1} de {total_alunos}")
            self.txt_feitas.delete(0, "end")
            self.txt_feitas.focus()
        else:
            self.lbl_nome_aluno.configure(text="Fim da lista!", text_color="green")
            self.txt_feitas.configure(state="disabled")
            self.btn_salvar.configure(state="disabled")
            self.lbl_progresso.configure(text="Concluído! Todas as notas foram integradas ao arquivo.")
            messagebox.showinfo("Sucesso", f"Lançamento finalizado na planilha:\n{os.path.basename(self.caminho_planilha)}")

    def salvar_e_proximo(self):
        try:
            feitas = int(self.txt_feitas.get())
            if feitas < 0 or feitas > self.total_ativ:
                messagebox.showerror("Erro", f"A quantidade deve ser entre 0 e {self.total_ativ}.")
                return

            nota_final = (feitas * self.valor_max) / self.total_ativ
            self.df.at[self.index_atual, "Nota"] = round(nota_final, 2)
            
            # Salva exatamente na planilha que você escolheu lá no começo
            self.df.to_excel(self.caminho_planilha, index=False)

            self.index_atual += 1
            self.atualizar_aluno_na_tela()

        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite um número inteiro válido.")

def iniciar_sistema(valor_max, total_ativ, caminho_planilha):
    app_principal = GerenciadorNotas(valor_max, total_ativ, caminho_planilha)
    app_principal.mainloop()

if __name__ == "__main__":
    config_tela = LauncherConfig(iniciar_sistema)
    config_tela.mainloop()