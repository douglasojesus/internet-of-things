import tkinter as tk
from tkinter import messagebox
import requests
import json

class Dispositivo():
    def __init__(self, id, tipo_medicao, medicao_atual, esta_ativo, porta, ip, nome):
        self.id = id
        self.tipo_medicao = tipo_medicao
        self.medicao_atual = medicao_atual
        self.esta_ativo = esta_ativo
        self.porta = porta
        self.ip = ip
        self.nome = nome

class Application(tk.Tk):
    def __init__(self, url):
        super().__init__()
        self.title("Controle de Dispositivos")
        self.geometry("700x500")
        self.create_widgets()
        self.url = url

    def create_widgets(self):
        self.menu_label = tk.Label(self, text="Selecione uma opção:")
        self.menu_label.pack()

        self.menu_options = tk.StringVar(self)
        self.menu_options.set("Ver dispositivos disponíveis")
        self.menu = tk.OptionMenu(self, self.menu_options,
                                  "Ver dispositivos disponíveis",
                                  "Ligar sensor",
                                  "Desligar sensor",
                                  "Solicitar medição atual do sensor",
                                  "Ver IP do servidor (broker)")
        self.menu.pack()

        self.device_id_label = tk.Label(self, text="ID do dispositivo:")
        self.device_id_label.pack()
        self.device_id_entry = tk.Entry(self)
        self.device_id_entry.pack()

        self.submit_button = tk.Button(self, text="Enviar", command=self.handle_option)
        self.submit_button.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

    def handle_option(self):
        try:
            option = self.menu_options.get()
            device_id = self.device_id_entry.get()
            if option == "Ver dispositivos disponíveis":
                self.show_devices()
            elif option == "Ligar sensor":
                if device_id.isdigit():
                    self.turn_on_sensor(device_id)
                else:
                    messagebox.showerror("Erro", "O ID do dispositivo deve ser um número.")
            elif option == "Desligar sensor":
                if device_id.isdigit():
                    self.turn_off_sensor(device_id)
                else:
                    messagebox.showerror("Erro", "O ID do dispositivo deve ser um número.")
            elif option == "Solicitar medição atual do sensor":
                if device_id.isdigit():
                    self.request_sensor_measurement(device_id)
                else:
                    messagebox.showerror("Erro", "O ID do dispositivo deve ser um número.")
            elif option == "Ver IP do servidor (broker)":
                self.show_server_ip()
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erro", "Verifique se o servidor está conectado!")

    def desserializacao(self, lista_json):
        dispositivos = []
        for objeto in lista_json:
            id = objeto["pk"]
            tipo_medicao = objeto["fields"]["tipo_medicao"]
            medicao_atual = objeto["fields"]["medicao_atual"]
            esta_ativo = objeto["fields"]["esta_ativo"]
            ip = objeto["fields"]["ip"]
            porta = objeto["fields"]["porta"]
            nome = objeto["fields"]["nome"]
            dispositivo = Dispositivo(id, tipo_medicao, medicao_atual, esta_ativo, porta, ip, nome)
            dispositivos.append(dispositivo)
        return dispositivos

    def show_devices(self):
        response = requests.get(self.url)
        try:
            devices = eval(json.loads(response.text).replace("true", "True").replace("null", "None").replace("false", "False"))
            if isinstance(devices, list):
                device_list = "\n".join([f"ID: {d['pk']}, Nome: {d['fields']['nome']}, Medição: {d['fields']['tipo_medicao']}, Está ativo: {d['fields']['esta_ativo']}, Porta: {d['fields']['porta']}, IP: {d['fields']['ip']}" for d in devices])
                self.result_label.config(text="Dispositivos disponíveis:\n" + device_list)
            else:
                self.result_label.config(text="Erro: Resposta inválida da API.")
        except json.JSONDecodeError:
            self.result_label.config(text="Erro: Resposta inválida da API.")

    def turn_on_sensor(self, device_id):
        response = requests.post(self.url, data={"id": device_id, "comando": "ligar"})
        self.handle_response(response, "ligado")

    def turn_off_sensor(self, device_id):
        response = requests.post(self.url, data={"id": device_id, "comando": "desligar"})
        self.handle_response(response, "desligado")

    def request_sensor_measurement(self, device_id):
        response = requests.post(self.url, data={"id": device_id, "comando": "dados"})
        try:
            if 'value' in response.json():
                self.result_label.config(text=f"Medição atual: {response.json()['value']}")
            else:
                self.result_label.config(text=f"Erro: {response.json()}")
        except json.JSONDecodeError:
            self.result_label.config(text="Erro: Resposta inválida da API.")

    def show_server_ip(self):
        response = requests.post(self.url, data={"comando": "ver_ip_server"})
        try:
            if 'value' in response.json():
                self.result_label.config(text=f"IP do servidor: {response.json()['value']}")
            else:
                self.result_label.config(text=f"Erro: {response.json()}")
        except json.JSONDecodeError:
            self.result_label.config(text="Erro: Resposta inválida da API.")

    def handle_response(self, response, success_message):
        try:
            if 'value' in response.json() and response.json()['value'] == success_message:
                self.result_label.config(text=f"Dispositivo {success_message}!")
            else:
                self.result_label.config(text=f"Erro: {response.json()}")
        except json.JSONDecodeError:
            self.result_label.config(text="Erro: Resposta inválida da API.")


if __name__ == "__main__":
    ip = input("Informe o endereço (IP) do servidor: ")
    # URL da API onde os dados serão enviados
    url = f'http://{ip}:1026/api/'

    app = Application(url)
    app.mainloop()
