import time
import random
from threading import Lock

class Pod:
    def __init__(self, name):
        self.name = name
        self.requests = []
        self.processing = []
        self.capacity = 10  # Número máximo de processos simultâneos
        self.status = 'Rodando'
        self.lock = Lock()  # Lock para evitar condições de corrida

    def add_request(self, request):
        """
        Adiciona uma requisição à fila do pod se houver capacidade disponível.
        """
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                return True
            else:
                print(f"{self.name} está no limite de capacidade. Requisição recusada.")
                return False

    def process_requests(self):
        """
        Processa requisições da fila enquanto houver capacidade disponível.
        """
        while True:
            with self.lock:
                if self.requests and len(self.processing) < self.capacity:
                    request = self.requests.pop(0)
                    self.processing.append(request)
                    print(f">>> {self.name} processando a requisição {request}")

            if request:
                self._process_request(request)

            time.sleep(2)  # Tempo de espera entre verificações

    def _process_request(self, request):
        """
        Simula o tempo de processamento de uma requisição.
        """
        time.sleep(random.randint(5, 7))  # Simula o tempo de processamento
        with self.lock:
            if request in self.processing:
                self.processing.remove(request)
                print(f"--- {self.name} completou a requisição {request}")

    def is_overloaded(self):
        """
        Verifica se o pod está sobrecarregado.
        """
        with self.lock:
            return len(self.requests) + len(self.processing) >= self.capacity
