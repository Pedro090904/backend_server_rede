// Passo 1: Importar as classes necessárias da biblioteca 'cap'
const { Cap, decoders } = require('cap');

// --- Variáveis de Configuração ---
// Lembre-se de alterar estes valores para os da sua máquina
const SERVER_IP = "192.168.0.14"; // IMPORTANTE: Troque pelo IP do seu computador!

// --- Início do Script ---

// Encontra o primeiro dispositivo de rede disponível com um endereço IP
const device = Cap.findDevice(SERVER_IP);
if (!device) {
    console.error(`Erro: Nenhum dispositivo de rede encontrado para o IP ${SERVER_IP}`);
    console.error("Verifique se o IP está correto e se você está executando o script com privilégios de administrador.");
    process.exit(1);
}

console.log("Iniciando a captura de pacotes...");
console.log(`Monitorando o servidor no IP: ${SERVER_IP}`);
console.log(`Escutando no dispositivo: ${device.name} (${device.addresses[0].addr})`);
console.log("-----------------------------------------");

// Cria uma instância do capturador
const c = new Cap();

// Define o tamanho do buffer que armazenará os pacotes capturados
const bufSize = 10 * 1024 * 1024; // 10 MB
const buffer = Buffer.alloc(bufSize);

// Abre o dispositivo para captura em modo promíscuo
// O filtro 'ip' garante que só pegaremos pacotes IPv4
c.open(device.name, 'ip', bufSize, buffer);

// Define um listener que será chamado toda vez que um novo pacote chegar
c.on('packet', (nbytes, trunc) => {
    // Apenas processa pacotes Ethernet (a camada mais comum)
    if (decoders.Ethernet.prototype.decode(buffer, 0)) {
        // A 'cap' nos dá os dados decodificados do cabeçalho IP
        const ipHeader = decoders.IPV4.prototype.decode(buffer, 14); // O cabeçalho IP começa no byte 14 do frame Ethernet

        // Extrai as informações que precisamos
        const sourceIp = ipHeader.saddr;
        const destinationIp = ipHeader.daddr;
        const packetSize = ipHeader.length; // Tamanho total do pacote IP
        
        // O protocolo é um número (ex: 6 para TCP, 17 para UDP). Vamos mapeá-lo para um nome.
        const PROTOCOLS = {
            1: 'ICMP',
            6: 'TCP',
            17: 'UDP',
        };
        const protocolName = PROTOCOLS[ipHeader.protocol] || `Protocolo #${ipHeader.protocol}`;

        // Lógica para identificar tráfego de entrada e saída (idêntica à anterior)
        if (sourceIp === SERVER_IP || destinationIp === SERVER_IP) {
            let direction = "";
            let clientIp = "";

            if (destinationIp === SERVER_IP) {
                direction = "Entrada (IN)";
                clientIp = sourceIp;
            } else {
                direction = "Saída (OUT)";
                clientIp = destinationIp;
            }

            // Exibir no console as informações extraídas
            console.log(
                `[${direction}] Cliente: ${clientIp} | Protocolo: ${protocolName} | Tamanho: ${packetSize} bytes`
            );
        }
    }
});