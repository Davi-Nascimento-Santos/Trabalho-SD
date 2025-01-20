import time
import random

class Pod:
    def __init__(self, name):
        self.name = name
        self.requests = []
        self.processing = []
        self.capacity = 10  # número máximo de processos para rodar
        self.status = 'Rodando'
        self.threads = []

    # Pod recebe um request e se possuir capacidade aceita
    def add_request(self, request):
        if len(self.requests) < self.capacity:
            self.requests.append(request)
            return True
        else:
            return False

    def process_requests(self):
        while True:
            if (self.requests) and (len(self.processing) < self.capacity):
                request = self.requests.pop(0)
                self.processing.append(request)
                print(f">>> {self.name} processando a requisicao {request}")
                time.sleep(random.randint(5, 7))  # Simula o tempo de processamento
                self.processing.remove(request)
                print(f"--- {self.name} completou a requisicao {request}")
            time.sleep(5)