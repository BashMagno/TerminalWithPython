import tkinter as tk
from tkinter import scrolledtext
import os

class TerminalEmulator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Terminal Emulator")
        self.geometry("800x600")

        self.input = tk.Entry(self, font=("Courier New", 12), bg="black", fg="white")
        self.input.pack(fill="x", side="top")

        self.output = scrolledtext.ScrolledText(self, wrap="word", font=("Courier New", 12), bg="black", fg="white")
        self.output.pack(fill="both", expand=True)

        self.input.bind("<Return>", self.process_command)
        self.input.bind("<Tab>", self.autocompletar)

        self.current_directory = os.getcwd()  # Ruta actual del sistema

        self.output.insert("end", f"$ {self.current_directory}$ ")

        # Crear un menú
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Añadir una opción "Clear" al menú
        clear_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Clear", menu=clear_menu)
        clear_menu.add_command(label="Clear Screen", command=self.clear_screen)

        # Atar Ctrl+L para borrar la pantalla
        self.bind("<Control-l>", self.clear_screen)

    def process_command(self, event):
        command = self.input.get()
        self.output.insert("end", f"\n$ {command}\n")

        if command == "exit":
            self.quit()
        elif command.startswith("ls"):
            ruta = command.split(" ")[1] if len(command.split(" ")) > 1 else self.current_directory
            self.listar_directorios(ruta)
        elif command.startswith("cd"):
            ruta = command.split(" ")[1] if len(command.split(" ")) > 1 else None
            self.cambiar_directorio(ruta)
        else:
            self.execute_command(command)

        self.input.delete(0, "end")
        self.output.see("end")

    def execute_command(self, command):
        try:
            result = os.popen(command).read()
            self.output.insert("end", result)
        except Exception as e:
            self.output.insert("end", str(e))

    def listar_directorios(self, ruta='.'):
        try:
            directorios = [nombre for nombre in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, nombre))]
            self.output.insert("end", "\nDirectorios encontrados:\n")
            for directorio in directorios:
                self.output.insert("end", directorio + "\n")
        except Exception as e:
            self.output.insert("end", str(e))

    def cambiar_directorio(self, ruta):
        try:
            if ruta:
                os.chdir(ruta)
                self.current_directory = os.getcwd()
            else:
                self.output.insert("end", "Error: Debes proporcionar una ruta válida.\n")
        except Exception as e:
            self.output.insert("end", str(e))

    def autocompletar(self, event):
        current_text = self.input.get()
        tokens = current_text.split()
        current_token = tokens[-1] if tokens else ""

        files = os.listdir(self.current_directory)
        matches = [f for f in files if f.startswith(current_token)]

        if len(matches) == 1:
            completed_command = " ".join(tokens[:-1] + [matches[0]])
            self.input.delete(0, tk.END)
            self.input.insert(0, completed_command)

    def clear_screen(self, event=None):
        self.output.delete(1.0, tk.END)
        self.output.insert("end", f"$ {self.current_directory}$ ")

if __name__ == "__main__":
    app = TerminalEmulator()
    app.mainloop()
