

# Backend - Dashboard de Análise de Tráfego

Este diretório contém o código-fonte do backend para o projeto "Dashboard de Análise de Tráfego de Servidor em Tempo Real".

O objetivo deste backend é capturar pacotes de rede de um servidor-alvo, agregar os dados de tráfego em janelas de 5 segundos e expor essas informações através de uma API RESTful para ser consumida por um frontend. [cite\_start]Este documento fornece as instruções detalhadas de configuração e execução, conforme solicitado nos entregáveis do projeto[cite: 23].

## 1\. Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados no seu sistema (Windows):

  * **Python (versão 3.7 ou superior):**

      * Faça o download no [site oficial do Python](https://www.python.org/downloads/windows/).
      * **IMPORTANTE:** Durante a instalação, marque a caixa de seleção que diz **"Add Python to PATH"**.

  * **Npcap:**

      * Esta ferramenta é o driver que permite a captura de pacotes no Windows.
      * Faça o download no [site oficial do Npcap](https://www.google.com/search?q=https://npcap.com/%23download).
      * Durante a instalação, certifique-se de que a opção **"Install Npcap in WinPcap API-compatible Mode"** esteja marcada.

## 2\. Configuração

Antes de rodar o servidor, você precisa configurar o script para monitorar a interface de rede correta.

1.  **Descubra o seu Endereço IP Local:**

      * Abra o Prompt de Comando (`cmd`).
      * Digite o comando `ipconfig` e pressione Enter.
      * Procure pelo seu adaptador de rede ativo (ex: "Adaptador de LAN sem Fio Wi-Fi") e anote o valor do **"Endereço IPv4"** (ex: `192.168.0.14`).

2.  **Atualize o Script:**

      * Abra o arquivo `captura.py` em um editor de texto como o VS Code.
      * Localize a linha que define a variável `SERVER_IP`.
      * Substitua o valor existente pelo endereço IP que você anotou no passo anterior.

    <!-- end list -->

    ```python
    # Linha a ser alterada no arquivo captura.py
    SERVER_IP = "SEU_IP_AQUI" 
    ```

## 3\. Instalação das Dependências

Com os pré-requisitos instalados e o script configurado, o próximo passo é instalar as bibliotecas Python necessárias para o projeto.

1.  **Abra o Prompt de Comando como Administrador:**

      * Clique no Menu Iniciar do Windows.
      * Digite `cmd`.
      * Clique com o botão direito sobre o "Prompt de Comando" e selecione **"Executar como administrador"**.

2.  **Navegue até a Pasta do Projeto:**

      * Use o comando `cd` (change directory) para entrar na pasta onde o arquivo `captura.py` está localizado.
      * *Exemplo:* `cd C:\Users\SeuUsuario\Documentos\GitHub\meu_dashboard\backend`

3.  **Instale as Bibliotecas:**

      * Com o terminal na pasta correta, execute o seguinte comando para instalar Flask, Flask-Cors e Scapy:

    <!-- end list -->

    ```cmd
    pip install Flask Flask-Cors scapy
    ```

## 4\. Execução

Depois de instalar as dependências, o backend está pronto para ser executado.

1.  Certifique-se de que você ainda está no **Prompt de Comando como Administrador** e dentro da pasta do projeto.
2.  Execute o script com o seguinte comando:
    ```cmd
    python captura.py
    ```
3.  Se tudo ocorrer bem, você verá mensagens indicando que o servidor foi iniciado e está rodando. O terminal ficará ativo, executando o servidor.
    ```
    Iniciando o servidor de captura e API...
    Servidor API rodando! Acesse http://127.0.0.1:5000/api/traffic
    -----------------------------------------
    [23:55:10] Janela de dados atualizada com 2 clientes.
    [23:55:15] Janela de dados atualizada com 3 clientes.
    ```

## 5\. Verificação

Para confirmar que a API está funcionando e servindo os dados corretamente:

1.  Mantenha o terminal do passo anterior rodando.
2.  Abra um navegador de internet (Chrome, Firefox, etc.).
3.  Acesse a seguinte URL: **`http://127.0.0.1:5000/api/traffic`**

Você deverá ver os dados de tráfego agregados, formatados em JSON, aparecendo na página. A cada 5 segundos que você atualizar a página, os dados devem mudar, refletindo a última janela de tempo capturada.