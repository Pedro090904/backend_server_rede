# Documentação Backend

## Frameworks importados relacionadas as API's

from flask import Flask, jsonify 
from flask_cors import CORS # Para permitir que o frontend acesse a API

1. Flask é a Api que cria o servidor web
2. jsonify converte os dados em python para JSON
3. flask_cors integra as API's com o frontend sem bloqueio do navegador e evitando erros de CORS

# Bibliotecas importadas

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

# Variáveis de configuração 

# --- Variáveis de Configuração ---
SERVER_IP = "192.168.1.201" # Verifique se este ainda é seu IP
JANELA_DE_TEMPO = 5 # Segundos

- A variável SERVER_IP define o endereço IP do servidor que o script vai monitorar ou usar como origem, caso o ip seja diferente do verificado, é preciso atualizar a variável
- A variável JANELA_DE_TEMPO define o intervalo para coletar as estatísticas e agrupar pacotes  

#

