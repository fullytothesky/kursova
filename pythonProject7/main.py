import tkinter as tk
from tkinter import messagebox
import numpy as np
import os

from MatrixSolver import MatrixSolverGUI


def main():
    root = tk.Tk()               #Створення головного вікна програми за допомогою класу Tk з бібліотеки Tkinter. Об'єкт root представляє головне вікно програми.
    app = MatrixSolverGUI(root)  #Створення об'єкта MatrixSolverGUI, який є інстанцією класу MatrixSolverGUI. При створенні об'єкта передається посилання на головне вікно root. Це викликає метод __init__ класу MatrixSolverGUI для налаштування графічного інтерфейсу.
    root.mainloop()              #Запуск головного циклу подій (main event loop) для програми. Цей цикл забезпечує постійне відслідковування та обробку подій, таких як кліки миші, натискання клавіш, зміна розміру вікна тощо.


if __name__ == "__main__":
    main()