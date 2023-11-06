import sys
import tkinter as tk
from tkinter import Menu
from tkinter import scrolledtext

# Para abrir y guardar  archivos
from tkinter import filedialog as fd

# Para mostrar ventana de opciones
from tkinter import simpledialog


class EditorTexto(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("750x600")
        self.title("Editor de texto")
        self.resizable(0,0)

        self._filename = ""
        self._is_guardado = False
       
        
        self._crear_componentes()

    # Definir metodos
    def _crear_componentes(self):

        # MENU PRINCIPAL
        menu_principal = Menu(self)
        sub_menu = Menu(menu_principal, tearoff=False)
        sub_menu.add_command(label="Abrir",command= self._abrir_comprobar)
        sub_menu.add_command(label="Guardar", command=self._guardar)
        sub_menu.add_command(label="Guardar como...", command=self._guardar_como)

        sub_menu.add_separator()
        sub_menu.add_command(label="Salir", command=self._salir_comprobar)

        menu_principal.add_cascade(menu=sub_menu, label="Archivo")
        
        self.config(menu=menu_principal)

        # FRAME BOTONES
        frame_botones = tk.LabelFrame(self)

        boton_abrir = tk.Button(frame_botones, text="Abrir", height=2, width=18, command=self._abrir_comprobar)
        boton_abrir.grid(row=0, column=0, sticky="NSWE", padx=5, pady=5)

        boton_guardar = tk.Button(frame_botones, text="Guardar",height=2, command=self._guardar)
        boton_guardar.grid(row=1, column=0, sticky="NSWE", padx=5, pady=5)

        boton_guardar_como = tk.Button(frame_botones, text="Guardar como...", height=2, command=self._guardar_como)
        boton_guardar_como.grid(row=2, column=0, sticky="NSWE", padx=5, pady=5)

            #Mostramos el frame
        frame_botones.pack(side="left", fill="y")

        # FRAME CAMPO DE TEXTO
        frame_campo = tk.LabelFrame(self)

        self._scroll = scrolledtext.ScrolledText(frame_campo, width=72, height=37, wrap=tk.WORD)
        
        # El método que se ejecutará cada vez que se escriba en el  ScrolledText.
        self._scroll.bind("<KeyPress>", self._update_guardado)
        self._scroll.grid(row=0, column=0)

            #Mostramos el frame
        frame_campo.pack()
    
    # Salir de la ventana
    def _salir_comprobar(self):
        if self._filename == "" :
            if len(self._scroll.get("1.0", tk.END)) > 1:
                res = self._mostrar_ventana_opciones()
                if res == "Guardar" :
                    self._guardar_como()
                    self.title(f"Editor de texto - {self._filename}")
                elif res == "No guardar":
                    self._salir()

            else:
                 self._salir()
        elif self._is_guardado:
            self._salir()

        else:
            res = self._mostrar_ventana_opciones()
            if res == "Guardar" :
                self._guardar()
                self._salir()
            elif res == "No guardar":
                self._salir()

    def _salir(self):
        self.quit()
        self.destroy()
        sys.exit()

    def _update_guardado(self, event):
        self._is_guardado = False
        self.title(f"*Editor de texto - {self._filename}")

    def _mostrar_ventana_opciones(self):
        # Crea una nueva ventana de diálogo.
        dialogo = tk.Toplevel(self)
        dialogo.geometry("238x80")
        dialogo.title("Editor")
        dialogo.resizable(0,0)
        
        # Hace que la ventana de diálogo sea modal.
        # significa que el usuario no podrá interactuar con la ventana principal hasta que se cierre la ventana de diálogo.
        dialogo.grab_set()

        opcion_elegida = tk.StringVar()

        etiqueta = tk.Label(dialogo,text="¿Quieres guardar los cambios?",font=("Helvetica", 12, "normal"))
        etiqueta.grid(row=0,column=0, columnspan=3, padx=5, pady=5)


        def elegir_opcion(opcion):
            opcion_elegida.set(opcion)
            dialogo.destroy()

        opciones = ["Guardar", "No guardar", "Cancelar"]
        # Crea un botón para cada opción.
        col = 0
        for opcion in opciones:
            boton = tk.Button(dialogo, text=opcion, command=lambda opcion=opcion: elegir_opcion(opcion), width=8, height=2)
            boton.grid(row=1,column=col)
            col=col+1

        # Espera a que se cierre la ventana de diálogo.
        self.wait_window(dialogo)

        return opcion_elegida.get()


    def _abrir_comprobar(self):
        if self._filename == "" :
            if len(self._scroll.get("1.0", tk.END)) > 1:
                res = self._mostrar_ventana_opciones()
                if res == "Guardar" :
                    self._guardar_como()
                    self.title(f"Editor de texto - {self._filename}")
                elif res == "No guardar":
                    self._abrir_archivo()
            else:
                 self._abrir_archivo()
                 
        elif self._is_guardado:
             self._abrir_archivo()

        else:
            res = self._mostrar_ventana_opciones()
            if res == "Guardar" :
                self._guardar()
            elif res == "No guardar":
                self._abrir_archivo()
             
    def _abrir_archivo(self):
        # Para abrir archivos
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        name = fd.askopenfilename(title="Abrir un archivo",initialdir='/',filetypes=filetypes)
        
        if name and name != self._filename:
            with open(name, "r") as file:
                self.title(f"Editor de texto - {name}")
                self._scroll.delete('1.0', tk.END)
                self._scroll.insert(tk.INSERT, file.read())
        
            self._filename = name
            self._is_guardado = True


    def _guardar_como(self):
        files = [('Text Document', '*.txt'), ('Python Files', '*.py')] 
        filepath = fd.asksaveasfile(filetypes = files, defaultextension = files)
        if filepath != None: 
            with open(filepath.name, "w") as file:
                    file.write(self._scroll.get("1.0", tk.END))

            with open(filepath.name, "r") as file:
                        self._scroll.delete('1.0', tk.END)

                        self.title(f"Editor de texto - {filepath.name}")
                        self._scroll.insert(tk.INSERT, file.read())

            self._filename = filepath.name         

    def _guardar(self):
        if self._filename == "":
            self._guardar_como()
        elif not self._is_guardado:
            with open(self._filename, "w") as file:
                file.write(self._scroll.get("1.0", tk.END))

        self._is_guardado = True

        


if __name__ == "__main__":
    edit = EditorTexto()
    edit.mainloop()


