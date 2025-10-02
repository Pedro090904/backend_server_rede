# Documentação Backend

# 1. Frameworks importados relacionadas as API's

from flask import Flask, jsonify 
from flask_cors import CORS # Para permitir que o frontend acesse a API

1. Flask é a Api que cria o servidor web
2. jsonify converte os dados em python para JSON
3. flask_cors integra as API's com o frontend sem bloqueio do navegador e evitando erros de CORS

# 2. Bibliotecas importadas

from scapy.all import sniff, IP, TCP, UDP # <-- MUDANÇA AQUI
import sys
import threading
import time
from collections import defaultdict, Counter

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
SERVER_IP = "192.168.1.201" # Verifique se este ainda é seu IP
JANELA_DE_TEMPO = 5 # Segundos

- A variável SERVER_IP define o endereço IP do servidor que o script vai monitorar ou usar como origem, caso o ip seja diferente do verificado, é preciso atualizar a variável
- A variável JANELA_DE_TEMPO define o intervalo para coletar as estatísticas e agrupar pacotes  

# 4. Estrutura de dados 

traffic_data = defaultdict(lambda: {'in': 0, 'out': 0, 'protocols': {'in': Counter(), 'out': Counter()}}) # <-- MUDANÇA AQUI
data_lock = threading.Lock()

1. A variável traffic_data cria um dicionário com um valor pré-definido pela função lambda, ela se refere ao ip monitorado
   1.1  A chave "in" do dicionário se refere aos dados de entrada
   1.2  A chave "out" do dicionário se refere aos dados de saída
2. A variável data_lock faz com que o tráfego sendo atualizado muitas vezes, garante que apenas uma thread por vez mexa na estrutura, evitando inconsistências.

# 5. Dicionário para armazenar os dados

last_window_data = {}
last_window_lock = threading.Lock()

1. A variável last_window_data = {} é um dicionário global que armazena os dados de tráfego processados da última janela completa e é o **endponit da API que serve para o frontend**
2. A variável last_window_lock = threading.Lock()
   2.1 O **threading.Lock()** garante que apenas uma thread por vez pode acessar ou modificar o last


# 6. Lógica de captura atualiza com direção e portas


# 7. Lógica do processador de janela (modificada para a nova estrutura)


# 8. Configuração da API com Flask (sem alterações)


# 9. Início da Execução (sem alterações)
