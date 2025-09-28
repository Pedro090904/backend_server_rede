// Usando a biblioteca 'raw-socket' que é 100% JavaScript e mais confiável
const raw = require('raw-socket');

// --- Variáveis de Configuração ---
// Lembre-se de colocar o IP que você encontrou com o ipconfig
const SERVER_IP = "192.168.0.14"; // IMPORTANTE: Verifique se este ainda é seu IP!

// --- Início do Script ---
console.log("Iniciando a captura de pacotes com raw-socket...");
console.log(`Monitorando o servidor no IP: ${SERVER_IP}`);
console.log("-----------------------------------------");

// Cria um socket de baixo nível para escutar todos os pacotes IP.
// Esta operação requer privilégios de administrador.
try {
    const socket = raw.createSocket({ protocol: raw.Protocol.IP });

    socket.on('message', (buffer, source) => {
        // O buffer contém o pacote IP completo.
        // Vamos extrair as informações diretamente dos bytes do buffer.
        
        // IP de origem: bytes 12 a 15
        const sourceIp = `${buffer[12]}.${buffer[13]}.${buffer[14]}.${buffer[15]}`;
        // IP de destino: bytes 16 a 19
        const destinationIp = `${buffer[16]}.${buffer[17]}.${buffer[18]}.${buffer[19]}`;
        // Protocolo: byte 9 (6=TCP, 17=UDP, 1=ICMP)
        const protocolNumber = buffer[9];
        // Tamanho total do pacote: bytes 2 e 3
        const packetSize = buffer.readUInt16BE(2);

        // Mapeia o número do protocolo para um nome legível
        const PROTOCOLS = { 1: 'ICMP', 6: 'TCP', 17: 'UDP' };
        const protocolName = PROTOCOLS[protocolNumber] || `Protocol #${protocolNumber}`;

        // Lógica para identificar tráfego de entrada e saída do nosso servidor
        if (sourceIp === SERVER_IP || destinationIp === SERVER_IP) {
            const direction = (destinationIp === SERVER_IP) ? "Entrada (IN)" : "Saída (OUT)";
            const clientIp = (destinationIp === SERVER_IP) ? sourceIp : destinationIp;

            console.log(
                `[${direction}] Cliente: ${clientIp} | Protocolo: ${protocolName} | Tamanho: ${packetSize} bytes`
            );
        }
    });

    // Listener para erros
    socket.on('error', (error) => {
        console.error("ERRO NO SOCKET:", error);
        console.error("--> Verifique se você executou o script como Administrador.");
        socket.close();
    });

} catch (e) {
    console.error("FALHA AO CRIAR O SOCKET:", e);
    console.error("--> Este erro geralmente acontece se o script não for executado como Administrador.");
}