import pyautogui
import time
from colorama import init, Fore, Style
from PIL import Image, ImageChops
import os
import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk
import keyboard
import random
#from banque import *

# Initialiser colorama
init()

def clear_screen():
    os.system('cls')  # Pour Windows

clear_screen()

print(f"Demarrage du Bot...")

def bring_window_to_front(window_title):
    import ctypes
    user32 = ctypes.windll.user32
    hwnd = user32.FindWindowW(None, window_title)
    if hwnd:
        user32.SetForegroundWindow(hwnd)

bring_window_to_front('Fils - Abrak v1.44.13')

time.sleep(0.3)

def action_pour_seek():
    print(Fore.YELLOW + "Seek en cours..." + Style.RESET_ALL)
    chemin_sauvegarde = r"C:\Users\CRNL29P-19-302\Documents\Bot\Farm"

    if not os.path.exists(chemin_sauvegarde):
        os.makedirs(chemin_sauvegarde)

    def capture_ecran_avec_touche():
        pyautogui.keyDown('e')
        time.sleep(0.2)
        screenshot = pyautogui.screenshot()
        pyautogui.keyUp('e')
        return screenshot

    screenshot = capture_ecran_avec_touche()
    chemin_fichier = os.path.join(chemin_sauvegarde, "Original.png")
    screenshot.save(chemin_fichier)

    def capture_ecran():
        screenshot = pyautogui.screenshot()
        return screenshot

    screenshot = capture_ecran()
    chemin_fichier = os.path.join(chemin_sauvegarde, "Screenshot.png")
    screenshot.save(chemin_fichier)

    print(f"Capture d'écran sauvegardée")

    pyautogui.FAILSAFE = False

    chemin_originale = os.path.join(chemin_sauvegarde, "Original.png")
    originale = Image.open(chemin_originale)

    zone_x1, zone_y1 = 287, 17
    zone_x2, zone_y2 = 1629, 801

    seuil_diff = 75
    perimetre_abstraction = 50

    zones_evitees = []

    time.sleep(0.3)

    def detect_clusters(diff_image, threshold=5):
        diff_array = np.array(diff_image)
        diff_gray = cv2.cvtColor(diff_array, cv2.COLOR_RGB2GRAY)
        _, binary_diff = cv2.threshold(diff_gray, threshold, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    ecran = pyautogui.screenshot(region=(zone_x1, zone_y1, zone_x2 - zone_x1, zone_y2 - zone_y1))

    originale_rgb = originale.crop((zone_x1, zone_y1, zone_x2, zone_y2)).convert("RGB")
    ecran_rgb = ecran.convert("RGB")

    diff = ImageChops.difference(originale_rgb, ecran_rgb)

    contours = detect_clusters(diff, seuil_diff)

    diff_coords_filtrees = []
    largest_contour = None
    largest_area = 0

    contourCount = 0
    for contour in contours:
        contourCount += 1

    if contourCount > 0:
        x, y, w, h = cv2.boundingRect(contours[random.randint(0,contourCount-1)])
        center_x, center_y = x + w // 2 + zone_x1, y + h // 2 + zone_y1

        if not any(x1 <= center_x <= x2 and y1 <= center_y <= y2 for (x1, y1, x2, y2) in zones_evitees):
            pyautogui.keyDown('shift')
            offset_x = 5
            pyautogui.click(center_x + offset_x, center_y)
            pyautogui.keyUp('shift')
            time.sleep(2) 
            #pyautogui.click(x=1610, y=789)
            pyautogui.click(x=50, y=50)

            x1 = max(center_x - perimetre_abstraction, zone_x1)
            y1 = max(center_y - perimetre_abstraction, zone_y1)
            x2 = min(center_x + perimetre_abstraction, zone_x2)
            y2 = min(center_y + perimetre_abstraction, zone_y2)
            zones_evitees.append((x1, y1, x2, y2))
        else:
            print("Changement détecté mais dans une zone évitée.")
    else:
        print("Pas de gros changement détecté dans la zone spécifiée.")   
    time.sleep(0.2)
    print(Fore.YELLOW + "Action pour seek.png terminée." + Style.RESET_ALL)

def action_pour_cbt(x, y):
    """
    Action à exécuter lorsque l'image cbt.png est trouvée.
    """
    print(Fore.YELLOW + "Combat en cours..." + Style.RESET_ALL)
    global sort_location
    if sort_location:
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        # Clique aux coordonnées spécifiées
        pyautogui.click(x=x, y=y)
        pyautogui.moveTo(50,50)        
        print(f"Click effectué aux coordonnées ({x}, {y}).")
        time.sleep(0.4)
    else:
        print("Image 'sort.png' non trouvée.")
    time.sleep(0.2)
    print(Fore.YELLOW + "Action pour sort.png terminée." + Style.RESET_ALL)

def recherche_image(image_path, x_var, y_var):
    """
    Cherche l'image sur l'écran et exécute une action si elle est trouvée.
    """
    global sort_location
    try:
        position = pyautogui.locateOnScreen(image_path)
        if position:
            print(Fore.GREEN + f"L'image {image_path} a été trouvée !" + Style.RESET_ALL)
            if image_path == 'seek.png':
                action_pour_seek()
                #banque()
            elif image_path == 'sort.png':
                sort_location = pyautogui.locateOnScreen('sort.png')
                action_pour_cbt(x_var.get(), y_var.get())
            return True
        else:
            print(Fore.RED + f"L'image {image_path} n'a pas été trouvée." + Style.RESET_ALL)
            return False
    except pyautogui.ImageNotFoundException:
        print(Fore.RED + f"L'image {image_path} n'a pas été trouvée sur l'écran." + Style.RESET_ALL)
        return False

def recherche_en_continue(images, x_var, y_var, max_loops=4, deplacement_x=50, deplacement_y=50):
    """
    Fonction qui recherche les images en continue et déplace la souris si aucune image n'est trouvée après max_loops boucles.
    """
    boucle_count = 0
    while True:
        image_trouvee = False
        for image in images:
            if recherche_image(image, x_var, y_var):
                image_trouvee = True
                boucle_count = 0  # Réinitialiser le compteur si une image est trouvée
                break
        
        if not image_trouvee:
            boucle_count += 1
            if boucle_count >= max_loops:
                print(Fore.CYAN + "Aucune image trouvée après 10 boucles. Déplacement de la souris." + Style.RESET_ALL)
                current_x, current_y = pyautogui.position()
                new_x = current_x + deplacement_x
                new_y = current_y + deplacement_y
                pyautogui.moveTo(new_x, new_y)
                boucle_count = 0  # Réinitialiser le compteur après déplacement
        else:
            boucle_count = 0  # Réinitialiser le compteur si une image est trouvée
        
        time.sleep(1)  # Attendre un peu avant la prochaine recherche

# Liste des images à rechercher
images_a_rechercher = ['seek.png', 'sort.png']

# Configuration des coordonnées prédéfinies
predefined_coords = {
    "Forgerons": (1494, 738),
    "Gobelins": (1350, 515),
    "Piou": (954, 515),
    "Sanglier [4/8]": (671, 660)
}

# Création de l'interface graphique
def start_gui():
    global x_var, y_var  # Déclarer les variables comme globales

    root = tk.Tk()
    root.title("Configuration des Coordonnées")

    tk.Label(root, text="Choisissez les coordonnées:").pack(pady=5)

    def on_select(event):
        selected_option = coord_combobox.get()
        if selected_option in predefined_coords:
            x, y = predefined_coords[selected_option]
            x_var.set(x)
            y_var.set(y)

    coord_combobox = ttk.Combobox(root, values=list(predefined_coords.keys()))
    coord_combobox.bind("<<ComboboxSelected>>", on_select)
    coord_combobox.pack(pady=5)

    tk.Label(root, text="Coordonnée X:").pack(pady=5)
    x_var = tk.IntVar(value=predefined_coords["Forgerons"][0])
    tk.Entry(root, textvariable=x_var).pack(pady=5)

    tk.Label(root, text="Coordonnée Y:").pack(pady=5)
    y_var = tk.IntVar(value=predefined_coords["Forgerons"][1])
    tk.Entry(root, textvariable=y_var).pack(pady=5)

    tk.Button(root, text="Démarrer", command=lambda: recherche_en_continue(images_a_rechercher, x_var, y_var)).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    
    try:
        start_gui()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nInterruption détectée avec Ctrl+C. Arrêt du script..." + Style.RESET_ALL)
