# Importações novas para a API
from flask import Flask, jsonify
from flask_cors import CORS # Para permitir que o frontend acesse a API

# Importações que já tínhamos, com TCP e UDP adicionados
from scapy.all import sniff, IP, TCP, UDP # <-- MUDANÇA AQUI
import sys
import threading
import time
from collections import defaultdict, Counter

# --- Variáveis de Configuração ---
SERVER_IP = "192.168.0.16" # Verifique se este ainda é seu IP
JANELA_DE_TEMPO = 5 # Segundos

# --- ESTRUTURA DE DADOS MODIFICADA ---
# A lambda agora cria uma estrutura aninhada para os protocolos
traffic_data = defaultdict(lambda: {'in': 0, 'out': 0, 'protocols': {'in': Counter(), 'out': Counter()}}) # <-- MUDANÇA AQUI
data_lock = threading.Lock()

# Dicionário para armazenar os dados da ÚLTIMA janela completa, para a API servir
last_window_data = {}
last_window_lock = threading.Lock()

# --- LÓGICA DE CAPTURA ATUALIZADA COM DIREÇÃO E PORTAS ---
def process_packet(packet):
    global traffic_data
    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        source_ip = ip_layer.src
        destination_ip = ip_layer.dst
        packet_size = len(packet)
        
        if source_ip == SERVER_IP or destination_ip == SERVER_IP:
            with data_lock:
                direction = 'in' if destination_ip == SERVER_IP else 'out'
                client_ip = source_ip if direction == 'in' else destination_ip
                
                # --- INÍCIO DA NOVA LÓGICA DE PROTOCOLO ---
                protocol_key = "OUTRO" # Valor padrão
                
                if packet.haslayer(TCP):
                    # A porta do servidor é a de destino (dport) na entrada e a de origem (sport) na saída
                    server_port = packet[TCP].dport if direction == 'in' else packet[TCP].sport
                    protocol_key = f"TCP:{server_port}"
                elif packet.haslayer(UDP):
                    server_port = packet[UDP].dport if direction == 'in' else packet[UDP].sport
                    protocol_key = f"UDP:{server_port}"
                elif ip_layer.proto == 1:
                    protocol_key = "ICMP"
                # --- FIM DA NOVA LÓGICA DE PROTOCOLO ---

                # Atualiza o tráfego total de entrada/saída (esta linha não muda)
                traffic_data[client_ip][direction] += packet_size
                # Atualiza a contagem do protocolo específico para a direção específica
                traffic_data[client_ip]['protocols'][direction][protocol_key] += packet_size # <-- MUDANÇA AQUI

# --- LÓGICA DO PROCESSADOR DE JANELA (MODIFICADA para nova estrutura) ---
def process_and_reset_window():
    global traffic_data, last_window_data
    while True:
        time.sleep(JANELA_DE_TEMPO)
        
        data_to_process = {}
        with data_lock:
            if traffic_data:
                data_to_process = dict(traffic_data)
                traffic_data.clear()

        with last_window_lock:
            # --- MUDANÇA AQUI para converter os contadores aninhados ---
            for client, data in data_to_process.items():
                data['protocols']['in'] = dict(data['protocols']['in'])
                data['protocols']['out'] = dict(data['protocols']['out'])
            last_window_data = data_to_process

        # Opcional: imprimir no console para depuração
        print(f"[{time.strftime('%H:%M:%S')}] Janela de dados atualizada com {len(last_window_data)} clientes.")
        sys.stdout.flush()

# --- Configuração da API com Flask (sem alterações) ---
app = Flask(__name__)
CORS(app) 

@app.route('/api/traffic')
def get_traffic_data():
    """Este é o endpoint da nossa API."""
    with last_window_lock:
        # Retorna uma cópia dos dados da última janela como resposta JSON
        return jsonify(last_window_data)

# --- Início da Execução (sem alterações) ---
if __name__ == "__main__":
    print("Iniciando o servidor de captura e API (v3 - com portas)...")
    
    processor_thread = threading.Thread(target=process_and_reset_window, daemon=True)
    processor_thread.start()
    
    capture_thread = threading.Thread(target=lambda: sniff(prn=process_packet, filter="ip", store=0), daemon=True)
    capture_thread.start()

    print(f"Servidor API rodando! Acesse http://127.0.0.1:5000/api/traffic")
    print("-----------------------------------------")
    
    app.run(host="0.0.0.0", port=5000)