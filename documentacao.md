# Documentação Backend

## Frameworks importadas relacionadas as API's

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



