import json
import socket
import tkinter as tk
from tkinter import ttk, messagebox
from codage import checksum_encode


class UDPClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Calculator Client")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Server configuration
        self.SERVER_IP = "127.0.0.1"
        self.SERVER_PORT = 5005

        # Create socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(5)

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10), padding=5)
        style.configure("TRadiobutton", background="#f0f0f0")

        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame,
                                text="Binary Calculator Client",
                                font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 30))

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10, padx=20)  # Added horizontal padding

        ttk.Label(input_frame, text="First Binary Number:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=8)
        self.num1_entry = ttk.Entry(input_frame, width=40)  # Increased width
        self.num1_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=8, sticky=tk.EW)

        ttk.Label(input_frame, text="Operation:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=8)
        self.operator_var = tk.StringVar(value="+")
        operator_frame = ttk.Frame(input_frame)
        operator_frame.grid(row=1, column=1, columnspan=3, sticky=tk.W, padx=10, pady=8)

        operators = [("+ Add", "+"), ("- Subtract", "-"),
                     ("× Multiply", "*"), ("÷ Divide", "/"),
                     ("<< Shift Left", "<<"), (">> Shift Right", ">>")]

        for i, (text, op) in enumerate(operators[:3]):  # First row
            ttk.Radiobutton(operator_frame, text=text, variable=self.operator_var,
                            value=op).grid(row=0, column=i, padx=5, sticky=tk.W)

        for i, (text, op) in enumerate(operators[3:]):  # Second row
            ttk.Radiobutton(operator_frame, text=text, variable=self.operator_var,
                            value=op).grid(row=1, column=i, padx=5, pady=(5, 0), sticky=tk.W)

        ttk.Label(input_frame, text="Second Binary Number:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=8)
        self.num2_entry = ttk.Entry(input_frame, width=40)  # Increased width
        self.num2_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=8, sticky=tk.EW)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        calculate_btn = ttk.Button(button_frame,
                                   text="Calculate (Send to Server)",
                                   command=self.send_to_server,
                                   width=25)
        calculate_btn.pack()

        result_frame = ttk.Frame(main_frame)
        result_frame.pack(fill=tk.X, pady=10, padx=20)

        self.result_var = tk.StringVar(value="Waiting for calculation...")
        result_label = ttk.Label(result_frame,
                                 textvariable=self.result_var,
                                 font=("Courier New", 12),
                                 foreground="blue",
                                 wraplength=600)
        result_label.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Ready to connect to server")
        status_bar = ttk.Label(main_frame,
                               textvariable=self.status_var,
                               relief=tk.SUNKEN,
                               anchor=tk.W,
                               padding=(10, 5))
        status_bar.pack(fill=tk.X, pady=(20, 0), ipady=5)

        input_frame.columnconfigure(1, weight=1)

    def validate_inputs(self, num1, num2):
        """Validate all inputs before sending to server"""
        if not all(c in "01" for c in num1) or not all(c in "01" for c in num2):
            raise ValueError("Les nombres doivent être en binaire (0 ou 1).")
        return True

    def send_to_server(self):
        num1 = self.num1_entry.get().strip()
        num2 = self.num2_entry.get().strip()
        operator = self.operator_var.get()

        try:
            self.validate_inputs(num1, num2)

            equation = [checksum_encode(num1), checksum_encode(num2), operator]
            print(checksum_encode(num1))
            print(checksum_encode(num2))
            message = json.dumps(equation)

            self.status_var.set("Sending to server...")
            self.root.update()

            # Send to server
            print(f"[>] Sending to {self.SERVER_IP}:{self.SERVER_PORT}: {message}")
            self.client_socket.sendto(message.encode(), (self.SERVER_IP, self.SERVER_PORT))

            # Receive response
            response, _ = self.client_socket.recvfrom(1024)
            decoded_response = response.decode()

            # Update UI
            print(f"[<] Received from server: {decoded_response}")
            self.result_var.set(f"Server response: {decoded_response[:decoded_response.find("= ")]} \n {decoded_response[decoded_response.find("= "):]}")
            self.status_var.set("Response received successfully")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            self.status_var.set(f"Error: {str(e)}")
        except socket.timeout:
            messagebox.showerror("Error", "No response from server (timeout)")
            self.status_var.set("Request timed out")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")

    def __del__(self):
        """Clean up socket when closing"""
        self.client_socket.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = UDPClientGUI(root)
    root.mainloop()