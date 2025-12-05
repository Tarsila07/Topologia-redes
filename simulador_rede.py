import time
import random
import heapq

# --- VARIÁVEIS GLOBAIS (ESTADO DA REDE) ---
ip_table = {}
graph = {}
rede_carregada = False

# --- FUNÇÃO DA ETAPA 2: DEFINIR A CONFIGURAÇÃO ---
def carregar_topologia():
    """
    Simula a importação/definição da rede conforme a Fase 1.
    No mundo real, isso poderia ler um arquivo .json. 
    Aqui, carregamos o dicionário diretamente.
    """
    global ip_table, graph, rede_carregada
    
    print("\n[Sistema] Carregando definições de topologia...")
    time.sleep(1) # Simula tempo de carregamento
    
    # 1. Definição dos Dispositivos (IP -> Nome)
    ip_table = {
        # Core
        "192.168.10.201": "c1", "192.168.10.205": "c1",
        # Aggregation
        "192.168.10.202": "a1", "192.168.10.209": "a1", "192.168.10.213": "a1",
        "192.168.10.206": "a2", "192.168.10.217": "a2", "192.168.10.221": "a2",
        # Edge
        "192.168.10.210": "e1", "192.168.10.1": "e1",
        "192.168.10.214": "e2", "192.168.10.17": "e2",
        "192.168.10.218": "e3", "192.168.10.65": "e3",
        "192.168.10.222": "e4", "192.168.10.97": "e4",
        # Hosts (Seus IPs Válidos)
        "192.168.10.2": "h1",  "192.168.10.3": "h2",
        "192.168.10.18": "h3", "192.168.10.19": "h4",
        "192.168.10.66": "h5", "192.168.10.67": "h6",
        "192.168.10.98": "h7", "192.168.10.99": "h8"
    }

    # 2. Definição das Conexões (Grafo e Pesos/Latência)
    graph = {
        "c1": {"a1": 1, "a2": 1},
        "a1": {"c1": 1, "e1": 2, "e2": 2},
        "a2": {"c1": 1, "e3": 2, "e4": 2},
        "e1": {"a1": 2, "h1": 4, "h2": 4},
        "e2": {"a1": 2, "h3": 4, "h4": 4},
        "e3": {"a2": 2, "h5": 4, "h6": 4},
        "e4": {"a2": 2, "h7": 4, "h8": 4},
        # Voltas dos Hosts
        "h1": {"e1": 4}, "h2": {"e1": 4},
        "h3": {"e2": 4}, "h4": {"e2": 4},
        "h5": {"e3": 4}, "h6": {"e3": 4},
        "h7": {"e4": 4}, "h8": {"e4": 4}
    }
    
    rede_carregada = True
    print("[Sucesso] Topologia Tree-Tier carregada. 8 Hosts, 7 Roteadores.")

# --- FUNÇÕES AUXILIARES (Listar, Buscar) ---

def listar_dispositivos():
    if not rede_carregada:
        print("[Erro] Defina a configuração da rede primeiro (Opção 1).")
        return

    print("\n--- Dispositivos na Rede ---")
    print(f"{'DISPOSITIVO':<12} | {'IPs ATRIBUÍDOS'}")
    print("-" * 40)
    
    # Agrupa IPs por dispositivo para exibir bonito
    dispositivos = {}
    for ip, nome in ip_table.items():
        if nome not in dispositivos:
            dispositivos[nome] = []
        dispositivos[nome].append(ip)
        
    for nome in sorted(dispositivos.keys()):
        ips = ", ".join(dispositivos[nome])
        print(f"{nome:<12} | {ips}")
    print("-" * 40)

def get_node_from_ip(ip):
    return ip_table.get(ip)

# --- ALGORITMOS (XProbe e Dijkstra) ---

def find_path(start_node, end_node):
    # Dijkstra Simples
    queue = [(0, start_node, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited: continue
        visited.add(node)
        path = path + [node]
        if node == end_node: return cost, path
        if node in graph:
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path))
    return float("inf"), []

def xprobe(ip_origem, ip_destino):
    if not rede_carregada:
        print("[Erro] Carregue a rede primeiro.")
        return

    print(f"\n--- Executando XProbe ---")
    node_origem = get_node_from_ip(ip_origem)
    node_destino = get_node_from_ip(ip_destino)

    if not node_origem or not node_destino:
        print("ERRO: IP não encontrado na tabela de roteamento.")
        return

    # Etapa 4: Calcular rota e latência
    latencia_ida, path = find_path(node_origem, node_destino)
    
    if not path:
        print("Destino inalcançável.")
        return

    print(f"Rota Lógica: {' -> '.join(path)}")
    
    # Etapa 5: Estatísticas
    print("\nColetando amostras RTT...")
    amostras = []
    for i in range(1, 4):
        # Simula variação de rede (Jitter)
        rtt = (latencia_ida * 2) + random.uniform(0.1, 1.5)
        amostras.append(rtt)
        print(f"  Seq={i} | RTT={rtt:.2f} ms")
        time.sleep(0.3)

    media = sum(amostras) / len(amostras)
    print(f"\n[XProbe Result] Status: UP | RTT Médio: {media:.2f} ms")

# --- MENU PRINCIPAL (CLI) ---
def main():
    while True:
        print("\n=== SIMULADOR DE REDE (PROJETO 2) ===")
        print("1. Importar/Definir Configuração da Rede")
        print("2. Listar Dispositivos e IPs")
        print("3. Executar XProbe (Ping/RTT)")
        print("4. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            carregar_topologia()
        elif opcao == '2':
            listar_dispositivos()
        elif opcao == '3':
            origem = input("IP Origem: ")
            destino = input("IP Destino: ")
            xprobe(origem, destino)
        elif opcao == '4':
            print("Encerrando simulador.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()