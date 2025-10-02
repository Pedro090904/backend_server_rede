
# Backend - Dashboard de Análise de Tráfego

Este diretório contém o código-fonte do backend para o projeto "Dashboard de Análise de Tráfego de Servidor em Tempo Real".

O objetivo deste backend é capturar pacotes de rede de um servidor-alvo, agregar os dados de tráfego em janelas de tempo configuráveis e expor essas informações através de uma API RESTful para ser consumida por um frontend. Este documento fornece as instruções detalhadas de configuração e execução.

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

O script `captura.py` possui duas variáveis principais no topo do arquivo que podem ser ajustadas conforme a necessidade.

1.  **Atualize o Endereço IP do Servidor-Alvo:**

      * Abra o Prompt de Comando (`cmd`) e digite `ipconfig` para descobrir o seu endereço IPv4 atual (ex: `192.168.0.14`).
      * Abra o arquivo `captura.py` e altere a variável `SERVER_IP` para o seu endereço IP.

    <!-- end list -->

    ```python
    # Define o endereço IP da máquina que será monitorada.
    SERVER_IP = "SEU_IP_AQUI" 
    ```

2.  **(Opcional) Ajuste a Janela de Tempo:**

      * A variável `JANELA_DE_TEMPO` define o intervalo em segundos para a agregação dos dados. O padrão é 5 segundos, conforme solicitado no trabalho.

    <!-- end list -->

    ```python
    # Define o intervalo de agregação dos dados em segundos.
    JANELA_DE_TEMPO = 5
    ```

## 3\. Instalação

Antes da primeira execução, é necessário instalar as bibliotecas Python que o projeto utiliza.

1.  **Abra o Prompt de Comando como Administrador.**
2.  Use o comando `cd` para **navegar até a pasta do projeto backend**.
      * *Exemplo:* `cd C:\Users\SeuUsuario\Documentos\GitHub\meu_dashboard\backend`
3.  Execute o seguinte comando para instalar todas as dependências:
    ```cmd
    pip install Flask Flask-Cors scapy
    ```

## 4\. Execução

O script deve ser executado com privilégios de administrador para que possa capturar o tráfego de rede. Ele possui dois modos de operação: um modo padrão que monitora todo o tráfego e um modo com filtro para monitorar portas específicas.

### 4.1. Passo a Passo para Executar

1.  **Abra o Prompt de Comando como Administrador:**

      * Clique no Menu Iniciar do Windows, digite `cmd`, clique com o botão direito sobre o "Prompt de Comando" e selecione "Executar como administrador".

2.  **Navegue até a Pasta do Projeto:**

      * Use o comando `cd` para entrar na pasta onde o arquivo `captura.py` está localizado, como no passo de instalação.

### 4.2. Modos de Execução

#### Modo 1: Monitoramento Completo (Sem Filtro)

Neste modo, o script captura **todo** o tráfego de rede de e para o `SERVER_IP` configurado. É útil para uma análise geral ou para descobrir quais serviços estão ativos.

  * **Comando:**
    ```cmd
    python captura.py
    ```

#### Modo 2: Monitoramento com Filtro de Portas

Neste modo, você pode especificar exatamente quais portas de serviço deseja monitorar, isolando o tráfego de aplicações específicas e ignorando todo o "ruído" restante.

  * **Comando:**
    ```cmd
    python captura.py --ports PORTA1,PORTA2,PORTA3
    ```
  * **Como usar:**
      * Use o argumento `--ports` seguido de uma lista de números de porta, separados por vírgula, **sem espaços**.
      * **Exemplo Prático:** Para monitorar apenas seus servidores de teste HTTP (porta 80 do IIS) e FTP (portas 21 e 20), o comando seria:
        ```cmd
        python captura.py --ports 80,21,20
        ```

Ao iniciar, o script informará qual filtro está ativo. Se nenhum filtro for especificado, ele monitorará o `host` como um todo.

## 5\. Verificação

Para confirmar que o backend está funcionando:

1.  O terminal onde o script está rodando deve exibir mensagens como `[HH:MM:SS] Janela de dados atualizada com X clientes.` a cada 5 segundos.
2.  Abra um navegador de internet e acesse a URL da API: **`http://127.0.0.1:5000/api/traffic`**.
3.  Você deverá ver os dados de tráfego em formato JSON, que serão consumidos pelo frontend.