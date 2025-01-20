from Master import MasterNode
from Pod import Pod
from Generator import LoadGenerator
from threading import Thread
from Interface import Menu
import time

if __name__ == "__main__":
    menu = Menu()
    menu.botoes_menu()

    master = MasterNode()
    master.scale_pods(3)

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
