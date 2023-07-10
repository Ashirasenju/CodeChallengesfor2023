import queue
import threading
import time
import random


class Buffer:
    def __init__(self, taille):
        self.taille = taille
        self.file = queue.Queue(maxsize=taille)

    def production(self, element):
        self.file.put(element)

    def consommation(self):
        element = self.file.get()
        return element


class Producteur(threading.Thread):
    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer

    def run(self):
        while True:
            element = f"jk {random.randint(1, 10)}"
            self.buffer.production(element)
            time.sleep(1)


class Consommateur(threading.Thread):
    def __init__(self, buffer):
        threading.Thread.__init__(self)
        self.buffer = buffer

    def run(self):
        while True:
            element = self.buffer.consommation()
            print(f"Élément consommé : {element}")
            time.sleep(2)


# Création du buffer
stock = Buffer(5)

# Création des producteurs et des consommateurs
usine1 = Producteur(stock)
usine2 = Producteur(stock)
supermarche1 = Consommateur(stock)
supermarche2 = Consommateur(stock)

# Démarrage des threads
ouvrier1 = threading.Thread(target=usine1.run)
ouvrier2 = threading.Thread(target=usine2.run)
client1 = threading.Thread(target=supermarche1.run)
client2 = threading.Thread(target=supermarche2.run)

ouvrier1.start()
ouvrier2.start()
client1.start()
client2.start()
