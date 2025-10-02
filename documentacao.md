# Documentação Backend

# 1. Frameworks importados relacionadas as API's

```from flask import Flask, jsonify```

```from flask_cors import CORS``` # Para permitir que o frontend acesse a API

1. Flask é a Api que cria o servidor web
2. jsonify converte os dados em python para JSON
3. flask_cors integra as API's com o frontend sem bloqueio do navegador e evitando erros de CORS

# 2. Bibliotecas importadas

```from scapy.all import sniff, IP, TCP, UDP``` # <-- MUDANÇA AQUI

```import sys```

```import threading```

```import time```

```from collections import defaultdict, Counter```

1. Scapy analisa e manipula pacotes de redes.
   1.1 Sniff captura pacotes em tempo real
   1.2 IP, TCP, UDP são protocolos scapy que manipulam pacotes de IP, TCP e UDP
2. Sys permite acessar funções e variáveis do interpretador Python
3. threading é a biblioteca importada para executar tarefas em paralelo usando threads.
4. time é a biblioteca por definir funções de tempo
5. collections são estruturas de dados complexas
   5.1 dafaultdict é um dicionário que já cria valores padrão se a chave não existe
   5.2 Counter conta e armazena os elementos

# 3. Variáveis de configuração 
```SERVER_IP = "192.168.1.201"``` # Verifique se este ainda é seu IP

```JANELA_DE_TEMPO = 5 # Segundos```

- A variável SERVER_IP define o endereço IP do servidor que o script vai monitorar ou usar como origem, caso o ip seja diferente do verificado, é preciso atualizar a variável
- A variável JANELA_DE_TEMPO define o intervalo para coletar as estatísticas e agrupar pacotes  

# 4. Estrutura de dados 

```traffic_data = defaultdict(lambda: {'in': 0, 'out': 0, 'protocols': {'in': Counter(), 'out': Counter()}})``` # <-- MUDANÇA AQUI

```data_lock = threading.Lock()```

1. A variável traffic_data cria um dicionário com um valor pré-definido pela função lambda, ela se refere ao ip monitorado
   1.1  A chave "in" do dicionário se refere aos dados de entrada
   1.2  A chave "out" do dicionário se refere aos dados de saída
2. A variável data_lock faz com que o tráfego sendo atualizado muitas vezes, garante que apenas uma thread por vez mexa na estrutura, evitando inconsistências.

# 5. Dicionário para armazenar os dados

```last_window_data = {}```

```last_window_lock = threading.Lock()```

1. A variável last_window_data = {} é um dicionário global que armazena os dados de tráfego processados da última janela completa e é o **endponit da API que serve para o frontend**
2. A variável last_window_lock = threading.Lock() 
   2.1 O **threading.Lock()** garante que o apenas uma thread por vez pode acessar ou modificar o dicionário **last_window_data = {}**
   2.2 **last_window_data = {}** Está previnindo condições de corrida e garante a integridade dos dados em um ambiente multithread.

# 6. Lógica de captura atualiza com direção e portas

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

1. a linha de codigo ``` def process_packet(packet): ``` define a função que processa individualmente cada pacote capturado.
2. A linha de código ``` global traffic_data ``` interaje com a variável global para armazenar os dados de tráfego de forma agregada.
3. A linha de código``` global  if packet.haslayer(IP): ``` garante que o pacote capturado possui uma camada IP, ignorando outros tipos de pacote.
   3.1 As variáveis ``` ip_layer, source_ip, destination_ip, packet_size ``` vão receber respectivamente os dados referentes a camada de IP, os endereços de origem e destino, e o tamanho total do pacote em bytes.
4. A linha de código ``` if source_ip == SERVER_IP or destination_ip == SERVER_IP: ``` filtra os pacotes por relevância onde ó ira permitir o processamento de pacotes que têm o servidor como origem ou destino.
5. A linha de código ``` direction = 'in' if destination_ip == SERVER_IP else 'out' ``` define a direção do pacote, *in* se entrar *out* se sair.
6. A linha de código ``` client_ip = source_ip if direction == 'in' else destination_ip ``` Identifica o endereço IP do cliente com base na direção do tráfego.
7. A variável ``` protocol_key = "OUTRO" ``` define um valor padrão para tráfego que não se encaixa nos critérios seguintes.
8. Agora são defindos filtros que definem o tipo  do pacote capturado, onde se o pacote cair no filtro indentifica-se a porta (dport ou sport) e cria-se a chave, vejamos:

               if packet.haslayer(TCP):
                  # A porta do servidor é a de destino (dport) na entrada e a de origem (sport) na saída
                  server_port = packet[TCP].dport if direction == 'in' else packet[TCP].sport
                  protocol_key = f"TCP:{server_port}"
               elif packet.haslayer(UDP):
                  server_port = packet[UDP].dport if direction == 'in' else packet[UDP].sport
                  protocol_key = f"UDP:{server_port}"
               elif ip_layer.proto == 1:
                  protocol_key = "ICMP"

No caso apenas o ultimo filtro (``` elif ip_layer.proto == 1: ```) se comparta de maneira diferente indentificando os pacotes ICMP através do seu número de protocolo na camada IP.
9. A linha de código ``` traffic_data[client_ip][direction] += packet_size ``` Atualiza a contagem geral de bytes para aquele cliente, naquela direção.
10. A linha de código  ``` traffic_data[client_ip]['protocols'][direction][protocol_key] += packet_size ``` faz a mesma que o de cima só que para um para o protocolo específico identificado.

# 7. Lógica do processador de janela (modificada para a nova estrutura)

def process_and_reset_window():
    global traffic_data, last_window_data
    while True:
        time.sleep(JANELA_DE_TEMPO)

1. A função process_and_reset_window() é executada em um thread separada e é responsável por processar e resetar os dados de tráfego em intervalos regulares, definido pela varável **time.sleep(JANELA_DE_TEMPO)**

        data_to_process = {}
        with data_lock:
            if traffic_data:
                data_to_process = dict(traffic_data)
                traffic_data.clear()

2. O diciónario global **last_window_data = {}** que foi citado acima, ele é atualizado com os novos dados processados, com a proteção do **with last_window_lock:**

           with last_window_lock:
            # --- MUDANÇA AQUI para converter os contadores aninhados ---
            for client, data in data_to_process.items():
                data['protocols']['in'] = dict(data['protocols']['in'])
                data['protocols']['out'] = dict(data['protocols']['out'])
            last_window_data = data_to_process

3. Usando o **with data_lock:**, os dados acumulados em **if traffic_data:** são copiados para o **data_to_process = dict(traffic_data)** e em seguinda o traffic_data é limpo para a próxima janela.
   3.1 Os dados acumulados são convertidos de objetos **Counter** para o dicionário padrão do Python. É necessário para serem serializados e servidos pela API de forma correta.
4. A variável with last_window_lock:
   4.1 **in** ou **out** A direção do tráfego é determinada.
   4.2 in: entrada e out: saída, o IP do cliente é indentificado com base nessa direção.

        print(f"[{time.strftime('%H:%M:%S')}] Janela de dados atualizada com {len(last_window_data)} clientes.")
        sys.stdout.flush()
        
5. Apartir da linha **print(f"[{time.strftime('%H:%M:%S')}]...)** até a **sys.stdout.flush()**, são usadas para fins de depuração. Exibindo no console a quantidade de clientes encontrados na janela de tempo processada, permitindo que o desenvolvedor monitore o funcionamento do sistema em tempo real.

# 8. Configuração da API com Flask (sem alterações)

@app.route('/api/traffic')
def get_traffic_data():
    """Este é o endpoint da nossa API."""
    with last_window_lock:
        # Retorna uma cópia dos dados da última janela como resposta JSON
        return jsonify(last_window_data)

1. A função get_traffic_data() é o endpoint da API responsável por fornecer os dados de tráfego de rede para o frontend do dashboard.
2. A variável **with last_window_lock:** evita que a função de processamento de janela tente escrever na variável enquanto esta função a está lendo, prevenindo erros ou dados inconsistentes.

# 9. Início da Execução (sem alterações)
    
    ports_to_monitor = []
    # sys.argv é a lista de argumentos passados na linha de comando
    if "--ports" in sys.argv:
        try:
            # Pega o valor que vem depois de "--ports"
            ports_arg_index = sys.argv.index("--ports") + 1
            ports_str = sys.argv[ports_arg_index]
            
            if ports_str.lower() != "all":
                # Converte a string "80,21,20" em uma lista ['80', '21', '20']
                ports_to_monitor = ports_str.split(',')
        except (ValueError, IndexError):
            print("AVISO: Argumento --ports usado incorretamente. Monitorando todas as portas.")
            ports_to_monitor = []

1. if "--ports" in sys.argv é o script qu verifica o argumento **--ports**




    if ports_to_monitor:
        # Se temos portas, cria o filtro específico
        port_filter_part = " or ".join([f"port {p.strip()}" for p in ports_to_monitor])
        bpf_filter = f"host {SERVER_IP} and ({port_filter_part})"
    else:
        # Se não temos portas, cria o filtro geral (apenas pelo IP)
        bpf_filter = f"host {SERVER_IP}"
    # --- FIM DA LÓGICA CORINGA ---

    print("Iniciando o servidor de captura e API (v5 - filtro dinâmico)...")
    
    processor_thread = threading.Thread(target=process_and_reset_window, daemon=True)
    processor_thread.start()
    
    # Usa o filtro que acabamos de criar dinamicamente
    capture_thread = threading.Thread(target=lambda: sniff(prn=process_packet, filter=bpf_filter, store=0), daemon=True)
    capture_thread.start()

    print(f"Servidor API rodando! Filtro de captura ativo: [{bpf_filter}]")
    print("-----------------------------------------")
    print(f"Servidor API rodando! Acesse http://127.0.0.1:5000/api/traffic")
    print("-----------------------------------------")
    app.run(host="0.0.0.0", port=5000)