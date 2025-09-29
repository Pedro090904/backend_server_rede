# Importações necessárias:
# - sniff, IP: da Scapy, como antes
# - threading: para executar nosso "relógio" de 5 segundos em paralelo
# - time: para fazer o relógio esperar 5 segundos
# - defaultdict, Counter: para facilitar a criação e contagem no nosso dicionário
from scapy.all import sniff, IP
import sys
import threading
import time
from collections import defaultdict, Counter

# --- Variáveis de Configuração ---
SERVER_IP = "192.168.0.14" # Verifique se este ainda é seu IP
JANELA_DE_TEMPO = 5 # Segundos

# --- Estrutura de Dados Global ---
# Este dicionário guardará os dados da janela atual.
# Usamos um Lock para evitar que a captura e o processamento mexam nos dados ao mesmo tempo.
traffic_data = defaultdict(lambda: {'in': 0, 'out': 0, 'protocols': Counter()})
data_lock = threading.Lock()

# Função que será chamada para cada pacote capturado (LÓGICA MODIFICADA)
def process_packet(packet):
    global traffic_data
    if packet.haslayer(IP):
        ip_layer = packet.getlayer(IP)
        source_ip = ip_layer.src
        destination_ip = ip_layer.dst
        packet_size = len(packet)

        # Mapeia o número do protocolo para um nome
        PROTOCOLS = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
        protocol_name = PROTOCOLS.get(ip_layer.proto, f"Protocolo #{ip_layer.proto}")
        
        # Lógica para identificar tráfego de entrada e saída
        if source_ip == SERVER_IP or destination_ip == SERVER_IP:
            
            # Adquire o "cadeado" para modificar o dicionário com segurança
            with data_lock:
                if destination_ip == SERVER_IP:
                    direction = 'in'
                    client_ip = source_ip
                else: # source_ip == SERVER_IP
                    direction = 'out'
                    client_ip = destination_ip
                
                # ATUALIZA A ESTRUTURA DE DADOS (em vez de imprimir)
                traffic_data[client_ip][direction] += packet_size
                traffic_data[client_ip]['protocols'][protocol_name] += packet_size

# NOVA FUNÇÃO: O "Despachante" que processa a janela de tempo
def process_and_reset_window():
    global traffic_data
    while True:
        # 1. Espera a janela de tempo passar
        time.sleep(JANELA_DE_TEMPO)
        
        # 2. Adquire o "cadeado" para pegar os dados coletados
        with data_lock:
            # Faz uma cópia dos dados para processar e já limpa o original
            data_to_process = dict(traffic_data)
            traffic_data.clear()
        
        # 3. Processa e exibe os dados da janela que acabou de fechar
        if not data_to_process:
            print(f"\n--- Janela de {JANELA_DE_TEMPO}s ({time.strftime('%H:%M:%S')}) --- Sem tráfego ---")
        else:
            print(f"\n--- Resumo da Janela de {JANELA_DE_TEMPO}s ({time.strftime('%H:%M:%S')}) ---")
            for client, data in data_to_process.items():
                print(f"Cliente: {client} | Entrada: {data['in']} bytes | Saída: {data['out']} bytes")
                # Opcional: mostrar detalhes dos protocolos
                # for proto, size in data['protocols'].items():
                #     print(f"  -> {proto}: {size} bytes")
        
        sys.stdout.flush()


# --- Início da Execução ---
if __name__ == "__main__":
    print("Iniciando a captura e agregação de pacotes...")
    print(f"Monitorando o servidor no IP: {SERVER_IP}")
    print(f"Agregando dados em janelas de {JANELA_DE_TEMPO} segundos.")
    print("-----------------------------------------")
    sys.stdout.flush()

    # Cria e inicia a thread do nosso "despachante"
    # O 'daemon=True' faz com que a thread feche junto com o programa principal
    processor_thread = threading.Thread(target=process_and_reset_window, daemon=True)
    processor_thread.start()

    # Inicia a captura (esta função bloqueia a execução, por isso a thread é necessária)
    try:
        sniff(prn=process_packet, filter="ip", store=0)
    except Exception as e:
        print(f"Erro ao iniciar a captura: {e}")
        print("Certifique-se de executar como administrador.")