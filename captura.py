# Importa as funções necessárias da biblioteca Scapy
from scapy.all import sniff, IP
import sys

# --- Variáveis de Configuração ---
SERVER_IP = "192.168.0.14" # Verifique se este ainda é seu IP

print("Iniciando a captura de pacotes com Python/Scapy...")
print(f"Monitorando o servidor no IP: {SERVER_IP}")
print("-----------------------------------------")
sys.stdout.flush() # Força a exibição imediata do print

# Função que será chamada para cada pacote capturado
def process_packet(packet):
    # Verifica se o pacote é do tipo IP para evitar erros
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
            direction = "Entrada (IN)" if destination_ip == SERVER_IP else "Saída (OUT)"
            client_ip = source_ip if destination_ip == SERVER_IP else destination_ip
            
            print(f"[{direction}] Cliente: {client_ip} | Protocolo: {protocol_name} | Tamanho: {packet_size} bytes")
            sys.stdout.flush()

# Inicia a captura. A função sniff vai rodar para sempre.
# prn=process_packet -> chama a nossa função para cada pacote
# filter="ip" -> captura apenas pacotes IP
# store=0 -> não guarda os pacotes na memória para economizar recursos
sniff(prn=process_packet, filter="ip", store=0)