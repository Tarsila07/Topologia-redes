import time
import random
import heapq

ip_table = {}
graph = {}
rede_carregada = False

# --- CONFIGURAÇÃO DA REDE ---
def carregar_topologia():
    global ip_table, graph, rede_carregada
    print("\n[Sistema] Carregando definições de topologia...")
    time.sleep(1)
    
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
        # Hosts
        "192.168.10.2": "h1",  "192.168.10.3": "h2",
        "192.168.10.18": "h3", "192.168.10.19": "h4",
        "192.168.10.66": "h5", "192.168.10.67": "h6",
        "192.168.10.98": "h7", "192.168.10.99": "h8"
    }

    # 2. Grafo
    graph = {
        "c1": {"a1": 1, "a2": 1},
        "a1": {"c1": 1, "e1": 2, "e2": 2},
        "a2": {"c1": 1, "e3": 2, "e4": 2},
        "e1": {"a1": 2, "h1": 4, "h2": 4},
        "e2": {"a1": 2, "h3": 4, "h4": 4},
        "e3": {"a2": 2, "h5": 4, "h6": 4},
        "e4": {"a2": 2, "h7": 4, "h8": 4},
        "h1": {"e1": 4}, "h2": {"e1": 4},
        "h3": {"e2": 4}, "h4": {"e2": 4},
        "h5": {"e3": 4}, "h6": {"e3": 4},
        "h7": {"e4": 4}, "h8": {"e4": 4}
    }
    
    rede_carregada = True
    print("[Sucesso] Topologia carregada. Hosts disponíveis: h1 a h8.")

def resolver_input(entrada):
    """
    Tenta descobrir se o usuário digitou um NOME (h1) ou um IP.
    Retorna uma tupla: (IP_do_Dispositivo, Nome_do_Nó)
    """
    entrada = entrada.strip() 
    
    if entrada in ip_table:
        return entrada, ip_table[entrada]

    for ip, nome in ip_table.items():
        if nome == entrada:
            return ip, nome
            
    return None, None

def listar_dispositivos():
    if not rede_carregada:
        print("[Erro] Carregue a rede primeiro (Opção 1).")
        return

    print("\n--- Tabela de Dispositivos (Nomes & IPs) ---")
    
    mapa = {}
    for ip, nome in ip_table.items():
        if nome not in mapa: mapa[nome] = []
        mapa[nome].append(ip)
    
    
    print("HOSTS:")
    for i in range(1, 9):
        nome = f"h{i}"
        if nome in mapa: print(f"  {nome:<3} -> {mapa[nome][0]}")
        
    print("\nROTEADORES:")
    for nome in sorted(mapa.keys()):
        if not nome.startswith('h'):
            print(f"  {nome:<3} -> {', '.join(mapa[nome])}")
    print("-" * 40)

# --- ALGORITMOS ---

def find_path(start_node, end_node):
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

def xprobe(origem_input, destino_input):
    if not rede_carregada:
        print("[Erro] Carregue a rede primeiro.")
        return

    
    ip_orig, nome_orig = resolver_input(origem_input)
    ip_dest, nome_dest = resolver_input(destino_input)

    if not nome_orig or not nome_dest:
        print(f"ERRO: Dispositivo '{origem_input}' ou '{destino_input}' não encontrado.")
        return

    print(f"\n--- XProbe: {nome_orig} ({ip_orig}) -> {nome_dest} ({ip_dest}) ---")
    
    latencia_ida, path = find_path(nome_orig, nome_dest)
    
    if not path:
        print("Destino inalcançável.")
        return

    print(f"Rota Lógica: {' -> '.join(path)}")
    print("\nColetando amostras RTT...")
    amostras = []
    for i in range(1, 4):
        rtt = (latencia_ida * 2) + random.uniform(0.1, 1.5)
        amostras.append(rtt)
        print(f"  Seq={i} | RTT={rtt:.2f} ms")
        time.sleep(0.3)

    media = sum(amostras) / len(amostras)
    print(f"\n[ Resultado ] Status: UP | RTT Médio: {media:.2f} ms")

def mostrar_rota(origem_input, destino_input):
    if not rede_carregada:
        print("[Erro] Carregue a rede primeiro.")
        return

   
    ip_orig, nome_orig = resolver_input(origem_input)
    ip_dest, nome_dest = resolver_input(destino_input)

    if not nome_orig or not nome_dest:
        print("ERRO: Dispositivos não encontrados.")
        return

    print(f"\n--- Rota Otimizada: {nome_orig} para {nome_dest} ---")
    custo, path = find_path(nome_orig, nome_dest)

    if not path:
        print("Sem rota disponível.")
        return

    visual = " -> ".join([f"[{no}]" for no in path])
    print(f"\n{visual}")
    print(f"\nSaltos: {len(path)-1} | Custo Total: {custo} ms")

# --- MENU ---
def main():
    while True:
        print("\n=== SIMULADOR DE REDE (PROJETO 2) ===")
        print("1. Configurar Rede (Start)")
        print("2. Listar Nomes e IPs")
        print("3. Executar XProbe (Ping)")
        print("4. Mostrar Rota (Trace)")
        print("5. Sair")
        
        opcao = input("\nOpção: ")

        if opcao == '1':
            carregar_topologia()
        elif opcao == '2':
            listar_dispositivos()
        elif opcao == '3':
            orig = input("Origem (ex: h1 ou IP): ")
            dest = input("Destino (ex: h7 ou IP): ")
            xprobe(orig, dest)
        elif opcao == '4':
            orig = input("Origem (ex: h1): ")
            dest = input("Destino (ex: h7): ")
            mostrar_rota(orig, dest)
        elif opcao == '5':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()