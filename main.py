#############################################################
###################### Gerenciador de IPS.###################
# Aplicação desenvolvida para listar Ips descritos em um    #
# arquivo e possibilitar conexão remota via TS Windows      #
# --------------------------------------------------------- #
# Desenvolvido em: 08/01/2025                               #
# por: Marcos Vilela Alves                                  #
# Versão: 1.0                                               #
#############################################################

import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import subprocess

# Função para carregar a configuração do arquivo INI
def CarregaLista(arquivo_path):
    config = configparser.ConfigParser()
    with open(arquivo_path, "r", encoding="utf-8") as f:
        config.read_file(f)
    servers = []
    if "Servers" in config:
        for ip, description in config["Servers"].items():
            servers.append((ip, description))
    return servers
# Função para conectar ao IP selecionado
def connect_to_server(ip):
    try:
        # Comando para abrir a Conexão de Área de Trabalho Remota do Windows
        subprocess.run(["mstsc", "/v:" + ip], check=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível conectar ao servidor {ip}.\nErro: {e}")

# Interface gráfica
def main():
    arquivo_config = "config.ini"
    servers = CarregaLista(arquivo_config)

    if not servers:
        messagebox.showerror("Erro", f"O arquivo {arquivo_config} não contém servidores configurados.")
        return

    root = tk.Tk()
    root.title("Gerenciador de Conexões RDP")

    # Lista de servidores
    label = tk.Label(root, text="Selecione um servidor para conectar:")
    label.pack(pady=5)

    server_list = ttk.Treeview(root, columns=("IP", "Description"), show="headings", height=10)
    server_list.heading("IP", text="IP")
    server_list.heading("Description", text="Descrição")
    server_list.column("IP", width=150)
    server_list.column("Description", width=250)

    # Adiciona servidores à lista
    for ip, description in servers:
        server_list.insert("", "end", values=(ip, description))
    server_list.pack(padx=10, pady=10)

    # Botão para conectar
    def on_connect():
        selected_item = server_list.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Nenhum servidor selecionado!")
            return
        ip = server_list.item(selected_item, "values")[0]
        connect_to_server(ip)

    connect_button = tk.Button(root, text="Conectar", command=on_connect)
    connect_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
