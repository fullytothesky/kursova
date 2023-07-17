

import tkinter as tk
from tkinter import messagebox
import numpy as np
import os


class MatrixSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Solver")

        # Method selection
        self.method_var = tk.StringVar()
        method_frame = tk.LabelFrame(root, text="Method")
        method_frame.pack(padx=10, pady=10)

        tk.Radiobutton(method_frame, text="Jordan-Gauss", variable=self.method_var,
                       value="JordanGauss").pack(anchor="w")
        tk.Radiobutton(method_frame, text="LUP Decomposition", variable=self.method_var,
                       value="LUP").pack(anchor="w")

        # Matrix entry or generation selection
        self.entry_var = tk.StringVar()
        entry_frame = tk.LabelFrame(root, text="Matrix Entry")
        entry_frame.pack(padx=10, pady=10)

        tk.Radiobutton(entry_frame, text="Enter Matrix", variable=self.entry_var,
                       value="Enter").pack(anchor="w")
        tk.Radiobutton(entry_frame, text="Generate Matrix", variable=self.entry_var,
                       value="Generate").pack(anchor="w")

        # Matrix size selection
        self.size_var = tk.StringVar()
        size_frame = tk.LabelFrame(root, text="Matrix Size")
        size_frame.pack(padx=10, pady=10)

        for i in range(2, 11):
            tk.Radiobutton(size_frame, text=f"{i}x{i}", variable=self.size_var,
                           value=f"{i}").pack(anchor="w")

        # Solve button
        solve_btn = tk.Button(root, text="Solve", command=self.solve_matrix)
        solve_btn.pack(pady=10)

    def solve_matrix(self):
        method = self.method_var.get()
        entry_type = self.entry_var.get()
        size = int(self.size_var.get())

        if method == "" or entry_type == "" or size == 0:
            messagebox.showerror("Error", "Please select method, matrix entry, and size.")
            return

        if entry_type == "Enter":
            matrix_dialog = MatrixEntryDialog(self.root, size, method, self.display_result)
            matrix_dialog.show()
        else:
            matrix = self.generate_matrix(size)
            if method == "JordanGauss":
                inv_matrix = self.solve_jordan_gauss(matrix)
            else:
                inv_matrix = self.solve_lup(matrix)
            self.display_result(matrix, inv_matrix)

    def generate_matrix(self, size):
        matrix = np.random.rand(size, size)
        return matrix

    def solve_jordan_gauss(self, matrix):
        n = matrix.shape[0]
        augmented_matrix = np.concatenate((matrix, np.identity(n)), axis=1)

        for i in range(n):
            max_index = np.argmax(abs(augmented_matrix[i:, i])) + i
            if augmented_matrix[max_index, i] == 0:
                messagebox.showerror("Error", "Matrix is singular. Jordan-Gauss method cannot be applied.")
                return None

            augmented_matrix[[i, max_index]] = augmented_matrix[[max_index, i]]

            pivot = augmented_matrix[i, i]
            augmented_matrix[i] /= pivot
            for j in range(n):
                if j != i:
                    factor = augmented_matrix[j, i]
                    augmented_matrix[j] -= factor * augmented_matrix[i]

        return augmented_matrix[:, n:]

    def solve_lup(self, matrix):
        n = matrix.shape[0]
        LU = matrix.copy()
        P = np.eye(n)

        for k in range(n - 1):
            max_index = np.argmax(abs(LU[k:, k])) + k
            if LU[max_index, k] == 0:
                messagebox.showerror("Error", "Matrix is singular. LUP decomposition method cannot be applied.")
                return None

            LU[[k, max_index]] = LU[[max_index, k]]
            P[[k, max_index]] = P[[max_index, k]]

            for i in range(k + 1, n):
                LU[i, k] /= LU[k, k]
                for j in range(k + 1, n):
                    LU[i, j] -= LU[i, k] * LU[k, j]

        L = np.tril(LU, k=-1) + np.eye(n)
        U = np.triu(LU)

        inv_matrix = np.zeros_like(matrix)

        for i in range(n):
            b = np.zeros(n)
            b[i] = 1
            y = np.linalg.solve(L, P.dot(b))
            x = np.linalg.solve(U, y)
            inv_matrix[:, i] = x

        return inv_matrix

    def display_result(self, matrix, inv_matrix):
        if matrix is None:
            return

        result_dialog = ResultDialog(self.root, matrix, inv_matrix)

        # Save matrices to a text file
        file_path = "matrix_result.txt"
        with open(file_path, "w") as file:
            file.write("Matrix:\n")
            file.write(self.format_matrix(matrix))
            file.write("\n\nInverse Matrix:\n")
            file.write(self.format_matrix(inv_matrix))

        result_dialog.show()

        # Delete the text file
        os.remove(file_path)

    def format_matrix(self, matrix):
        rows, cols = matrix.shape
        formatted_matrix = ""
        for i in range(rows):
            for j in range(cols):
                formatted_matrix += f"{matrix[i, j]:.4f}  "
            formatted_matrix += "\n"
        return formatted_matrix


class MatrixEntryDialog:
    def __init__(self, root, size, method, callback):
        self.root = root
        self.method = method
        self.callback = callback

        self.dialog = tk.Toplevel(root)
        self.dialog.title("Matrix Entry")

        entry_frame = tk.Frame(self.dialog)
        entry_frame.pack(padx=10, pady=10)

        self.entry_vars = []

        for i in range(size):
            row_vars = []
            for j in range(size):
                entry = tk.Entry(entry_frame, width=10)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_vars.append(entry)

            self.entry_vars.append(row_vars)

        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(pady=10)

        submit_btn = tk.Button(btn_frame, text="Submit", command=self.submit)
        submit_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.cancel)
        cancel_btn.pack(side="left", padx=5)

    def submit(self):
        try:
            matrix = [[float(entry.get()) for entry in row_vars] for row_vars in self.entry_vars]
            matrix = np.array(matrix)
            if self.method == "JordanGauss":
                inv_matrix = MatrixSolverGUI(self.root).solve_jordan_gauss(matrix)
            else:
                inv_matrix = MatrixSolverGUI(self.root).solve_lup(matrix)
            self.callback(matrix, inv_matrix)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid matrix entry. Please enter valid numbers.")

    def cancel(self):
        self.dialog.destroy()

    def show(self):
        self.dialog.wait_window()


class ResultDialog:
    def __init__(self, root, matrix, inv_matrix):
        self.root = root
        self.matrix = matrix
        self.inv_matrix = inv_matrix

        self.dialog = tk.Toplevel(root)
        self.dialog.title("Result")

        result_frame = tk.Frame(self.dialog)
        result_frame.pack(padx=10, pady=10)

        matrix_text = tk.Text(result_frame, width=70, height=10)
        matrix_text.pack()

        matrix_text.insert(tk.END, "Matrix:\n")
        matrix_text.insert(tk.END, self.format_matrix(matrix))

        inv_matrix_text = tk.Text(result_frame, width=70, height=10)
        inv_matrix_text.pack()

        inv_matrix_text.insert(tk.END, "Inverse Matrix:\n")
        inv_matrix_text.insert(tk.END, self.format_matrix(inv_matrix))

        verify_btn = tk.Button(self.dialog, text="Verify", command=self.verify_result)
        verify_btn.pack(pady=10)

        ok_btn = tk.Button(self.dialog, text="OK", command=self.close_dialog)
        ok_btn.pack(pady=10)

    def format_matrix(self, matrix):
        rows, cols = matrix.shape
        formatted_matrix = ""
        for i in range(rows):
            for j in range(cols):
                formatted_matrix += f"{matrix[i, j]:.2f}  "
            formatted_matrix += "\n"
        return formatted_matrix

    def verify_result(self):
        product = np.dot(self.matrix, self.inv_matrix)
        identity = np.eye(self.matrix.shape[0])
        if np.allclose(product, identity):
            messagebox.showinfo("Verification", "The result is correct.")
        else:
            messagebox.showinfo("Verification", "The result is incorrect.")

    def close_dialog(self):
        self.dialog.destroy()




