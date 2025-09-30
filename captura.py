# Importações novas para a API
from flask import Flask, jsonify
from flask_cors import CORS # Para permitir que o frontend acesse a API

# Importações que já tínhamos
from scapy.all import sniff, IP
import sys
import threading
import time
from collections import defaultdict, Counter

# --- Variáveis de Configuração ---
SERVER_IP = "172.27.6.48" # Verifique se este ainda é seu IP
JANELA_DE_TEMPO = 5 # Segundos

# --- Estruturas de Dados Globais ---
# Dicionário para coletar o tráfego da janela ATUAL
traffic_data = defaultdict(lambda: {'in': 0, 'out': 0, 'protocols': Counter()})
data_lock = threading.Lock()

# NOVO: Dicionário para armazenar os dados da ÚLTIMA janela completa, para a API servir
last_window_data = {}
last_window_lock = threading.Lock()

# --- Lógica de Captura e Agregação (sem alterações) ---
def process_packet(packet):
    global traffic_data
    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        source_ip = ip_layer.src
        destination_ip = ip_layer.dst
        packet_size = len(packet)
        PROTOCOLS = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
        protocol_name = PROTOCOLS.get(ip_layer.proto, f"Protocolo #{ip_layer.proto}")
        
        if source_ip == SERVER_IP or destination_ip == SERVER_IP:
            with data_lock:
                direction = 'in' if destination_ip == SERVER_IP else 'out'
                client_ip = source_ip if direction == 'in' else destination_ip
                traffic_data[client_ip][direction] += packet_size
                traffic_data[client_ip]['protocols'][protocol_name] += packet_size

# --- Lógica do Processador de Janela---
def process_and_reset_window():
    global traffic_data, last_window_data
    while True:
        time.sleep(JANELA_DE_TEMPO)
        
        data_to_process = {}
        with data_lock:
            if traffic_data:
                # Copia os dados para processar e limpa a estrutura de coleta
                data_to_process = dict(traffic_data)
                traffic_data.clear()

        # ATUALIZA A VARIÁVEL QUE A API VAI USAR
        with last_window_lock:
            # Converte os objetos Counter para dicionários normais para o JSON
            for client, data in data_to_process.items():
                data['protocols'] = dict(data['protocols'])
            last_window_data = data_to_process

        # Opcional: imprimir no console para depuração
        print(f"[{time.strftime('%H:%M:%S')}] Janela de dados atualizada com {len(last_window_data)} clientes.")
        sys.stdout.flush()

# --- Configuração da API com Flask ---
app = Flask(__name__)
CORS(app) # Habilita o CORS para a aplicação

@app.route('/api/traffic')
def get_traffic_data():
    """Este é o endpoint da nossa API."""
    with last_window_lock:
        # Retorna uma cópia dos dados da última janela como resposta JSON
        return jsonify(last_window_data)

# --- Início da Execução ---
if __name__ == "__main__":
    print("Iniciando o servidor de captura e API...")
    
    # Inicia o processador de janela em uma thread
    processor_thread = threading.Thread(target=process_and_reset_window, daemon=True)
    processor_thread.start()
    
    # NOVO: Inicia a captura de pacotes em sua própria thread
    capture_thread = threading.Thread(target=lambda: sniff(prn=process_packet, filter="ip", store=0), daemon=True)
    capture_thread.start()

    print(f"Servidor API rodando! Acesse http://127.0.0.1:5000/api/traffic")
    print("-----------------------------------------")
    
    # Inicia o servidor Flask. O 'host="0.0.0.0"' permite que outras máquinas na rede acessem sua API
    app.run(host="0.0.0.0", port=5000)