from Master import MasterNode
from Pod import Pod
from Generator import LoadGenerator
from threading import Thread
from Interface import SimulationMenu
import time

if __name__ == "__main__":
    # Inicializar a interface de simulação
    menu = SimulationMenu()

    # Criação do MasterNode
    master = MasterNode()

    # Escalar pods iniciais (ajustável com base na lógica de entrada da interface)
    initial_pods = 3  # Número padrão, pode ser substituído por entrada da interface
    master.scale_pods(initial_pods)

    # Inicializar o gerador de carga
    load_generator = LoadGenerator(master)

    # Thread para monitorar os pods
    monitor_thread = Thread(target=master.monitor_pods, daemon=True)
    monitor_thread.start()

    # Thread para enviar requisições simuladas
    load_thread = Thread(target=load_generator.send_requests, daemon=True)
    load_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Encerrar a simulação com segurança
        master.deployment_active = False
        print("Desligando...")
