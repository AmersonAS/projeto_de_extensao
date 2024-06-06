import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import time
from database import DatabaseManager  # Certifique-se de importar a classe DatabaseManager

class TemperatureMonitor:
    def __init__(self):
        self.temperature_history = []

    def record_temperature(self, temperature):
        self.temperature_history.append(temperature)

    def get_temperature_history(self):
        return self.temperature_history

def gerar_temperatura_simulada():
    return random.uniform(18, 25)  # Temperatura mais realista

class App:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Monitor de Temperatura")
        self.root.geometry("600x500")

        self.db_manager = DatabaseManager()
        self.db_manager.create_table()

        self.load_avatar("avatar.png")

        self.temperature_monitor = TemperatureMonitor()

        self.temperature_label = tk.Label(self.root, text="Temperatura atual:")
        self.temperature_label.pack()

        self.temperature_var = tk.StringVar()
        self.temperature_entry = tk.Entry(self.root, textvariable=self.temperature_var, state='readonly')
        self.temperature_entry.pack()

        self.adjusting_label = tk.Label(self.root, text="", fg="red")
        self.adjusting_label.pack()

        self.history_label = tk.Label(self.root, text="Histórico de Temperaturas:")
        self.history_label.pack()

        self.history_listbox = tk.Listbox(self.root, width=50, height=10)
        self.history_listbox.pack()

        self.figure, self.ax = plt.subplots(figsize=(8, 5))
        self.line, = self.ax.plot([], [], marker='o', linestyle='-', color='blue')
        self.ax.set_xlabel('Leituras')
        self.ax.set_ylabel('Temperatura (°C)')
        self.ax.set_title('Histórico de Temperaturas')

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.root.after(30000, self.update_temperature_and_graph)

    def load_avatar(self, path):
        if os.path.exists(path):
            self.avatar_img = Image.open(path)
            self.avatar_img = self.avatar_img.resize((100, 100))
            self.avatar_photo = ImageTk.PhotoImage(self.avatar_img)
            self.avatar_label = tk.Label(self.root, image=self.avatar_photo)
            self.avatar_label.pack()
        else:
            messagebox.showerror("Erro", "Arquivo avatar.png não encontrado.")

    def generate_temperature(self):
        temperature = gerar_temperatura_simulada()
        self.temperature_monitor.record_temperature(temperature)
        self.db_manager.insert_temperature(temperature)
        self.update_display()
        self.adjust_temperature()

    def adjust_temperature(self):
        self.adjusting_label.config(text="Ajustando para a temperatura ideal...")
        self.root.after(3000, self.set_ideal_temperature)


    def set_ideal_temperature(self):
        ideal_temperature = 22.0  # Temperatura ideal
        self.temperature_monitor.record_temperature(ideal_temperature)
        self.db_manager.insert_temperature(ideal_temperature)
        self.update_display()
        self.adjusting_label.config(text="")

    def update_display(self):
        self.temperature_var.set(f"{self.temperature_monitor.temperature_history[-1]:.2f} °C")
        self.history_listbox.delete(0, tk.END)
        for temperature in self.temperature_monitor.temperature_history:
            self.history_listbox.insert(tk.END, f"{temperature:.2f} °C")

    def update_temperature_and_graph(self):
        self.generate_temperature()
        
        x_data = range(1, len(self.temperature_monitor.temperature_history) + 1)
        y_data = self.temperature_monitor.temperature_history

        self.line.set_data(x_data, y_data)
        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw()

        self.root.after(30000, self.update_temperature_and_graph)

def main():
    root = tk.Tk()
    app = App(root, username="Teste")
    root.mainloop()

if __name__ == "__main__":
    main()
