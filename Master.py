import time
from threading import Thread
from Pod import Pod

class MasterNode:
    def __init__(self):
        self.pods = []
        self.deployment_active = True
        self.resources = {"cpu": 100, "ram": 100, "rom": 100}
        self.current_pod_index = 0  # Índice para balanceamento round-robin

    def manage_pod(self, pod):
        """Gerencia a execução de um pod."""
        while self.deployment_active:
            if self._has_sufficient_resources():
                self._allocate_resources()
                pod.process_requests()
                self._release_resources()
            else:
                print(f"Pod {pod.name} aguardando por recursos.")
            time.sleep(10)

    def _has_sufficient_resources(self):
        return all(value >= 1 for value in self.resources.values())

    def _allocate_resources(self):
        for key in self.resources:
            self.resources[key] -= 1

    def _release_resources(self):
        for key in self.resources:
            self.resources[key] += 1

    def add_pod(self, pod):
        """Adiciona um pod à lista de pods gerenciados."""
        self.pods.append(pod)
        for _ in range(5):
            thread = Thread(target=self.manage_pod, args=(pod,), daemon=True)
            pod.threads.append(thread)
            thread.start()

    def remove_pod(self, pod_name):
        """Remove um pod pelo nome."""
        self.pods = [pod for pod in self.pods if pod.name != pod_name]

    def balance_requests(self, request):
        """Distribui requisições de forma round-robin."""
        if not self.pods:
            print("Nenhum pod disponível para balancear as requisições.")
            return

        pod = self.pods[self.current_pod_index]
        if pod.add_request(request):
            print(f"Requisição {request} atribuída ao {pod.name}.")
            self.current_pod_index = (self.current_pod_index + 1) % len(self.pods)
        else:
            print(f"Pod {pod.name} não pôde processar a requisição {request}.")
            self.monitor_pods()

    def scale_pods(self, num_pods):
        """Escala o número de pods conforme necessário."""
        if num_pods > len(self.pods):
            for _ in range(num_pods - len(self.pods)):
                new_pod = Pod(f"pod-{len(self.pods) + 1}")
                self.add_pod(new_pod)
                print(f"Adicionado {new_pod.name}.")
        elif num_pods < len(self.pods):
            for _ in range(len(self.pods) - num_pods):
                pod_name = self.pods[-1].name
                self.remove_pod(pod_name)
                print(f"Removido {pod_name}.")

    def monitor_pods(self):
        """Monitora os pods e realiza escala automática conforme necessário."""
        while self.deployment_active:
            for pod in self.pods:
                if pod.is_overloaded():
                    print(f"Pod {pod.name} sobrecarregado. Escalando...")
                    self.scale_pods(len(self.pods) + 1)
            time.sleep(5)
