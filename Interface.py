from tkinter import Tk, Label, Entry, Button, Frame

class SimulationMenu:
    def __init__(self):
        self.setup_ui()

    def setup_ui(self):
        # Configuração inicial da janela
        self.root = Tk()
        self.root.title("Simulação Kubernetes")
        self.root.geometry("400x350")
        self.root.configure(bg="#e0e0e0")

        # Configuração do frame principal
        self.frame = Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título
        Label(self.frame, text="Configuração da Simulação", font=("Helvetica", 16, "bold"), bg="#ffffff").grid(row=0, columnspan=2, pady=10)

        # Campos de entrada
        self.create_label_and_entry("Nome da Aplicação:", 1)
        self.create_label_and_entry("CPU:", 2)
        self.create_label_and_entry("RAM:", 3)
        self.create_label_and_entry("ROM:", 4)

        # Labels de feedback
        self.error_label = Label(self.frame, text="", fg="red", bg="#ffffff")
        self.error_label.grid(row=5, columnspan=2, pady=5)

        self.success_label = Label(self.frame, text="", fg="green", bg="#ffffff")
        self.success_label.grid(row=6, columnspan=2, pady=5)

        # Botão de início
        Button(self.frame, text="Iniciar", command=self.start_simulation, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        .grid(row=7, columnspan=2, pady=10)

        # Fechar aplicação de forma segura
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.mainloop()

    def create_label_and_entry(self, text, row):
        """Cria um par de Label e Entry para o formulário."""
        label = Label(self.frame, text=text, bg="#ffffff")
        label.grid(row=row, column=0, padx=10, pady=5, sticky='e')
        entry = Entry(self.frame)
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"entry_{row}", entry)

    def validate_inputs(self, app_name, cpu, ram, rom):
        """Valida os campos de entrada e retorna erros, se existirem."""
        if not app_name or not cpu or not ram or not rom:
            return "Erro: Todos os campos devem ser preenchidos."

        try:
            cpu = int(cpu)
            ram = int(ram)
            rom = int(rom)
        except ValueError:
            return "Erro: CPU, RAM e ROM devem ser números inteiros."

        return None

    def start_simulation(self):
        """Executa a lógica de inicialização da simulação."""
        app_name = self.entry_1.get()
        cpu = self.entry_2.get()
        ram = self.entry_3.get()
        rom = self.entry_4.get()

        error_message = self.validate_inputs(app_name, cpu, ram, rom)

        if error_message:
            self.error_label.config(text=error_message)
            self.success_label.config(text="")
        else:
            self.error_label.config(text="")
            self.success_label.config(text="Simulação iniciada com sucesso!")
            print(f"Simulação iniciada: {app_name}, CPU: {cpu}, RAM: {ram}, ROM: {rom}")

if __name__ == "__main__":
    SimulationMenu()
