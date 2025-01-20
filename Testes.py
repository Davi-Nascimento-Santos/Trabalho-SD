import time
import random
from threading import Thread

class MasterNode:
    def __init__(self):
        self.pods = []
        self.deployment_active = True
        self.cpu = 100
        self.ram = 100
        self.rom = 100
        self.current_pod_index = 0  # Índice para balanceamento round-robin
    

    def manage_pod(self, pod):
        while self.deployment_active:
            if self.cpu >= 1 and self.ram >= 1 and self.rom >= 1:
                self.cpu -= 1; self.ram -= 1; self.rom -= 1;
                pod.process_requests()
                self.cpu += 1; self.ram += 1; self.rom += 1;
            else:
                print(f"Pod {pod.name} esperando por recursos")
            time.sleep(10)


    def add_pod(self, pod):
        self.pods.append(pod)
        for i in range(5):
            thread = Thread(target=self.manage_pod, args=(pod,))
            pod.threads.append(thread)
            thread.start()


    def remove_pod(self, pod_name):
        self.pods = [pod for pod in self.pods if pod.name != pod_name]


    def balance_requests(self, request):
        try:
            pod = self.pods[self.current_pod_index]
        except:
            self.current_pod_index = 0
            pod = self.pods[self.current_pod_index]

        if pod.add_request(request):
            print(f"+++ Requisicao {request} atribuda a {pod.name}")
            self.current_pod_index += 1
            return
        else:
            print(f"Nenhum container pôde aceitar a requisicao {request}")
            self.monitor_pods()


    def scale_pods(self, num_pods):
        if num_pods > len(self.pods):
            for i in range(num_pods - len(self.pods)):
                new_pod = Pod(f"pod-{len(self.pods) + 1}")
                self.add_pod(new_pod)
                print(f"Adicionado {new_pod.name}")
        else:
            for i in range(len(self.pods) - num_pods):
                pod_name = self.pods[-1].name
                self.remove_pod(pod_name)
                print(f"Removido {pod_name}")


    def monitor_pods(self):
        while self.deployment_active:
            for pod in self.pods:
                if len(pod.requests) + len(pod.processing) >= 8:
                    print(f"Pod {pod.name} sobrecarregado. Escalando...")
                    self.scale_pods(len(self.pods) + 1)
            time.sleep(5)


class Pod:
    def __init__(self, name):
        self.name = name
        self.requests = []
        self.processing = []
        self.capacity = 5  # número máximo de processos para rodar
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


class LoadGenerator:
    def __init__(self, master):
        self.master = master

    def send_requests(self):
        request_id = 0
        while True:
            self.master.balance_requests(request_id)
            request_id += 1
            time.sleep(random.randint(1,2))



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