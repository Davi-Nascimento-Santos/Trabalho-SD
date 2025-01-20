import time
import random
from threading import Thread, Lock

class Pod:
    def __init__(self, name):
        self.name = name
        self.requests = []
        self.processing = []
        self.capacity = 5  # Número máximo de processos para rodar
        self.status = 'Rodando'
        self.lock = Lock()  # Controle de concorrência

    def add_request(self, request):
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                return True
        return False

    def process_requests(self):
        while True:
            with self.lock:
                if self.requests and len(self.processing) < self.capacity:
                    request = self.requests.pop(0)
                    self.processing.append(request)
                    print(f">>> {self.name} processando a requisicao {request}")

            if request:
                time.sleep(random.randint(5, 7))  # Simula o tempo de processamento
                with self.lock:
                    self.processing.remove(request)
                print(f"--- {self.name} completou a requisicao {request}")
            time.sleep(1)  # Evita loop excessivo

class MasterNode:
    def __init__(self):
        self.pods = []
        self.deployment_active = True
        self.current_pod_index = 0  # Índice para balanceamento round-robin
        self.lock = Lock()  # Controle de concorrência

    def add_pod(self, pod):
        self.pods.append(pod)
        thread = Thread(target=pod.process_requests)
        thread.start()

    def remove_pod(self, pod_name):
        with self.lock:
            self.pods = [pod for pod in self.pods if pod.name != pod_name]

    def balance_requests(self, request):
        with self.lock:
            if not self.pods:
                print(f"Nenhum pod disponível para processar a requisicao {request}")
                return

            pod = self.pods[self.current_pod_index]
            if pod.add_request(request):
                print(f"+++ Requisicao {request} atribuida ao {pod.name}")
                self.current_pod_index = (self.current_pod_index + 1) % len(self.pods)
            else:
                print(f"Pod {pod.name} sem capacidade para aceitar a requisicao {request}")

    def scale_pods(self, num_pods):
        with self.lock:
            current_count = len(self.pods)
            if num_pods > current_count:
                for i in range(num_pods - current_count):
                    new_pod = Pod(f"pod-{current_count + i + 1}")
                    self.add_pod(new_pod)
                    print(f"Adicionado {new_pod.name}")
            elif num_pods < current_count:
                for i in range(current_count - num_pods):
                    pod_name = self.pods[-1].name
                    self.remove_pod(pod_name)
                    print(f"Removido {pod_name}")

    def monitor_pods(self):
        while self.deployment_active:
            with self.lock:
                for pod in self.pods:
                    if len(pod.requests) + len(pod.processing) >= pod.capacity:
                        print(f"Pod {pod.name} sobrecarregado. Escalando...")
                        self.scale_pods(len(self.pods) + 1)
            time.sleep(5)

class LoadGenerator:
    def __init__(self, master):
        self.master = master

    def send_requests(self):
        request_id = 0
        while True:
            self.master.balance_requests(request_id)
            request_id += 1
            time.sleep(random.randint(1, 2))

if __name__ == "__main__":
    master = MasterNode()
    master.scale_pods(2)

    load_generator = LoadGenerator(master)

    monitor_thread = Thread(target=master.monitor_pods)
    monitor_thread.start()

    load_thread = Thread(target=load_generator.send_requests)
    load_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        master.deployment_active = False
        print("Desligando...")
