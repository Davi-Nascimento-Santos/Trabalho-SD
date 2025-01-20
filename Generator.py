import time
import random
from threading import Thread, Lock

class LoadGenerator:
    def __init__(self, master):
        """
        Inicializa o gerador de carga.
        :param master: Instância do MasterNode que gerencia os pods.
        """
        self.master = master
        self.running = True  # Controle para encerrar o gerador de carga com segurança
        self.lock = Lock()  # Lock para sincronização, caso necessário em futuras expansões

    def send_requests(self):
        """
        Envia requisições continuamente para o MasterNode, simulando carga de trabalho.
        """
        request_id = 0
        while self.running:
            with self.lock:  # Garante que futuras modificações sejam thread-safe
                self.master.balance_requests(request_id)
                print(f"Gerador de carga: Enviou a requisição {request_id}")
                request_id += 1

            time.sleep(random.uniform(1, 2))  # Tempo ajustado para melhor distribuição de carga

    def stop(self):
        """
        Encerra o envio de requisições de forma controlada.
        """
        with self.lock:
            self.running = False
        print("Gerador de carga encerrado.")
