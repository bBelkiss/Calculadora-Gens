import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence, ImageOps


class GeneratorsCalculatorUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.generadores = {
            "Trigo": 100, "Melon": 250, "Calabaza": 550, "Hongos": 850, "Hongo rojo": 1300,
            "Miel": 1500, "Algas": 2420, "Carbón": 3100, "Hierro": 4000, "Oro": 4300,
            "Lapislázuli": 6100, "Redstone": 7000, "Diamantes": 8100, "Esmeraldas": 9100,
            "Netherrack": 9800, "Cuarzo": 10100, "Oro infernal": 11900, "Ladrillos": 12900,
            "Magma": 13500, "Piedra luminosa": 15000, "Escombros": 15800, "Prismarina": 16350,
            "Ladrillos marinos": 17000, "Prismarina oscura": 17900, "Linterna marina": 18900,
            "Hielo": 19710, "Esponja": 20950, "Corales": 22000, "Endstone": 22600,
            "Ladrillos del end": 23800, "Purpur": 25000, "Ladrillos de purpur": 27200,
            "Obsidiana": 29800, "Obsidiana llorosa": 30250, "Pizarra": 32500
        }
        self.cantidad_generadores = {}

        self.title("Calculadora de Generadores")
        self.geometry("400x300")
        self.configure(bg="#FFFFFF")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Arial", 10), background="#FFFFFF", foreground="#333")
        style.configure("TButton", font=("Arial", 10), background="#DEFDF2", foreground="black")
        style.map("TButton", background=[("active", "#DEFDF2")])

        self.label_generador = ttk.Label(self, text="Selecciona el tipo de generador:")
        self.label_generador.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.combo_generador = ttk.Combobox(self, values=list(self.generadores.keys()), state="readonly")
        self.combo_generador.current(0)
        self.combo_generador.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        self.label_cantidad = ttk.Label(self, text="Cantidad de generadores:")
        self.label_cantidad.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_cantidad = ttk.Entry(self)
        self.entry_cantidad.grid(row=1, column=1, padx=10, pady=5, sticky="e")

        self.label_tiempo = ttk.Label(self, text="Tiempo en minutos:")
        self.label_tiempo.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.entry_tiempo = ttk.Entry(self)
        self.entry_tiempo.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        self.button_agregar = ttk.Button(self, text="Agregar Generador", command=self.agregar_generador)
        self.button_agregar.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.button_calcular = ttk.Button(self, text="Calcular", command=self.calcular_activaciones)
        self.button_calcular.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.button_quitar = ttk.Button(self, text="Quitar Generador", command=self.quitar_generador)
        self.button_quitar.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.resultado_label = tk.Label(self, text="", font=("Arial", 9), bg="#FFFFFF", fg="#333", anchor="w", justify="left")
        self.resultado_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.gif_label = tk.Label(self, bg="#FFFFFF")
        self.gif_label.place(x=250, y=120)  # coords
        self.load_gif("dab.gif")

    def load_gif(self, gif_path):
        self.gif_image = Image.open(gif_path)

        self.gif_frames = []
        for frame in ImageSequence.Iterator(self.gif_image):
            resized_frame = frame.resize((80, 80))
            bg_frame = Image.new("RGBA", resized_frame.size, "#FFFFFF")
            merged_frame = Image.alpha_composite(bg_frame, resized_frame.convert("RGBA"))
            self.gif_frames.append(ImageTk.PhotoImage(merged_frame))

        self.current_frame = 0
        self.update_gif()

    def update_gif(self):
        self.gif_label.config(image=self.gif_frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.after(100, self.update_gif)

    def agregar_generador(self):
        tipo_generador = self.combo_generador.get()
        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad < 0:
                raise ValueError
            self.cantidad_generadores[tipo_generador] = cantidad
            messagebox.showinfo("Información", f"Generador de {tipo_generador} agregado.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido para la cantidad.")

    def quitar_generador(self):
        tipo_generador = self.combo_generador.get()
        if tipo_generador in self.cantidad_generadores:
            del self.cantidad_generadores[tipo_generador]
            messagebox.showinfo("Información", f"Generador de {tipo_generador} quitado.")
        else:
            messagebox.showinfo("Información", f"No hay generador de {tipo_generador} agregado.")

    def calcular_activaciones(self):
        try:
            tiempo_minutos = int(self.entry_tiempo.get())
            if tiempo_minutos < 0:
                raise ValueError
            resultado = "Resultados:\n"
            for tipo_generador, cantidad in self.cantidad_generadores.items():
                if tipo_generador in self.generadores:
                    generacion_por_20_segundos = self.generadores[tipo_generador]
                    generacion_total = generacion_por_20_segundos * 3 * tiempo_minutos * cantidad
                    resultado += f"- {cantidad} generador(es) de {tipo_generador}: {generacion_total} dinero.\n"
                else:
                    resultado += f"- No se encontró información para el generador de {tipo_generador}.\n"
            self.resultado_label.config(text=resultado)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un número válido para el tiempo.")

if __name__ == "__main__":
    app = GeneratorsCalculatorUI()
    app.mainloop()
