from tkinter import Tk, Label, Entry, Button, Frame, StringVar

class Menu:
    def __init__(self):
        self.root = Tk()
        self.root.title("Simulação")
        self.root.geometry("400x350")
        self.root.configure(bg="#e0e0e0")

        self.frame = Frame(self.root, bg="#ffffff", bd=2, relief="groove")
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.title_label = Label(self.frame, text="Configuração da Simulação", font=("Helvetica", 16, "bold"), bg="#ffffff")
        self.title_label.grid(row=0, columnspan=2, pady=10)

        self.app_name_label = Label(self.frame, text="Nome da Aplicação:", bg="#ffffff")
        self.app_name_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.app_name_entry = Entry(self.frame)
        self.app_name_entry.grid(row=1, column=1, padx=10, pady=5)

        self.cpu_label = Label(self.frame, text="CPU:", bg="#ffffff")
        self.cpu_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.cpu_entry = Entry(self.frame)
        self.cpu_entry.grid(row=2, column=1, padx=10, pady=5)

        self.ram_label = Label(self.frame, text="RAM:", bg="#ffffff")
        self.ram_label.grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.ram_entry = Entry(self.frame)
        self.ram_entry.grid(row=3, column=1, padx=10, pady=5)

        self.rom_label = Label(self.frame, text="ROM:", bg="#ffffff")
        self.rom_label.grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.rom_entry = Entry(self.frame)
        self.rom_entry.grid(row=4, column=1, padx=10, pady=5)

        self.error_label = Label(self.frame, text="", fg="red", bg="#ffffff")
        self.error_label.grid(row=5, columnspan=2, pady=5)

        self.start_button = Button(self.frame, text="Iniciar", command=self.on_start, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.start_button.grid(row=6, columnspan=2, pady=10)

        self.success_label = Label(self.frame, text="", fg="green", bg="#ffffff")
        self.success_label.grid(row=7, columnspan=2, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        self.root.mainloop()

    def on_start(self):
        app_name = self.app_name_entry.get()
        cpu = self.cpu_entry.get()
        ram = self.ram_entry.get()
        rom = self.rom_entry.get()

        if not app_name or not cpu or not ram or not rom:
            self.error_label.config(text="Erro: Todos os campos devem ser preenchidos.")
            self.success_label.config(text="")
            print("Erro: Todos os campos devem ser preenchidos.")
        else:
            try:
                cpu = int(cpu)
                ram = int(ram)
                rom = int(rom)
            except ValueError:
                self.error_label.config(text="Erro: CPU, RAM e ROM devem ser números inteiros.")
                self.success_label.config(text="")
                print("Erro: CPU, RAM e ROM devem ser números inteiros.")
                return

            self.error_label.config(text="")
            self.success_label.config(text="Adicionado com sucesso!")
            print(f"Simulação iniciada com {app_name}, CPU: {cpu}, RAM: {ram}, ROM: {rom}")