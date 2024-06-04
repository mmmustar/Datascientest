import time
i = 0
while i < (60 * 20):
    fichier = open("data.txt", "a")
    fichier.write(str(i) + "\n")
    fichier.close()
    i += 1
    time.sleep(1)
    