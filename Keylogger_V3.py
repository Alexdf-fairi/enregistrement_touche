from pynput import keyboard
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image
import numpy as np
from collections import Counter

# Variables globales pour gérer l'enregistrement des touches
enregistrement = False
touche_appuyees = []

# Positions des touches sur l'image
positions = {
    '1': (1710, 558), '2': (1553, 558), '3': (1403, 558), '4': (1253, 558),
    '5': (824, 558), '6': (394, 558), '7': (244, 558), '8': (88, 558),
    '9': (1641, 435), '0': (1430, 435), '-': (1307, 435), '=': (1185, 435),
    'a': (1062, 435), 'z': (939, 435), 'e': (817, 435), 'r': (694, 435),
    't': (571, 435), 'y': (449, 435), 'u': (326, 435), 'i': (203, 435),
    'o': (74, 435), 'p': (1621, 312), '^': (1498, 312), '$': (1376, 312),
    'q': (1253, 312), 's': (1130, 312), 'd': (1008, 312), 'f': (885, 312),
    'g': (762, 312), 'h': (640, 313), 'j': (517, 312), 'k': (394, 312),
    'l': (272, 313), 'm': (108, 313), 'ù': (1730, 244), 'w': (1594, 190),
    'x': (1471, 190), 'c': (1348, 190), 'v': (1226, 190), 'b': (1103, 190),
    'n': (980, 190), ',': (858, 190), ';': (735, 190), ':': (612, 190),
    '!': (490, 190), ' ': (367, 190)  # Barre d'espace
}

# Fonction pour afficher l'histogramme
def afficher_histogramme(stats):
    plt.figure(figsize=(10, 6))
    plt.bar(stats.keys(), stats.values(), color='skyblue')
    plt.xlabel("Touches")
    plt.ylabel("Nombre d'appuis")
    plt.title("Histogramme des touches appuyées")
    plt.show()

# Fonction pour créer une heatmap
def creer_heatmap(stats, image_path):
    rayon = 80
    # Charger l'image de fond
    try:
        base_image = Image.open(image_path)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image: {e}")
        return

    # Taille de l'image
    image_width, image_height = base_image.size

    # Création d'une matrice de chaleur
    heatmap = np.zeros((image_height, image_width))

    # Normalisation des statistiques
    max_count = max(stats.values(), default=1)

    for key, count in stats.items():
        if key in positions:
            x, y = positions[key]
            intensity = count / max_count

            # Ajouter la chaleur autour des coordonnées
            for dx in range(-rayon, rayon):  # Rayon d'effet sur la largeur
                for dy in range(-rayon, rayon):  # Rayon d'effet sur la hauteur
                    dist = np.sqrt(dx**2 + dy**2)  # Distance au centre
                    if dist <= rayon:  # Appliquer seulement dans un rayon donné
                        weight = 1 - (dist / rayon)  # Réduire l'intensité avec la distance
                        heatmap[min(image_height - 1, max(0, y + dy)), 
                                min(image_width - 1, max(0, x + dx))] += intensity * weight

    # Créer un colormap (rouge -> jaune -> bleu)
    cmap = plt.cm.plasma
    norm = mcolors.Normalize(vmin=0, vmax=1)

    # Afficher l'image de fond
    plt.figure(figsize=(12, 8))
    plt.imshow(base_image, extent=[0, image_width, 0, image_height])

    # Superposer la heatmap
    plt.imshow(heatmap, cmap=cmap, norm=norm, alpha=0.6, extent=[0, image_width, 0, image_height])

    # Ajouter une barre de couleur
    plt.colorbar(label="Intensité des frappes")

    plt.axis('off')
    plt.title("Heatmap des touches")
    plt.show()

# Gestionnaire d'événements pour le clavier
def on_press(key):
    global enregistrement, touche_appuyees

    try:
        # Arrêter/démarrer l'enregistrement avec Échap
        if key == keyboard.Key.esc:
            if enregistrement:
                print("Arrêt de l'enregistrement.")
                # Calcul des statistiques
                stats = Counter(touche_appuyees)
                print("Statistiques :", stats)

                # Afficher l'histogramme et la heatmap
                afficher_histogramme(stats)
                creer_heatmap(stats, "clavier.png")
            else:
                print("Démarrage de l'enregistrement.")
                touche_appuyees = []  # Réinitialiser les touches enregistrées
            enregistrement = not enregistrement
        elif enregistrement:
            # Enregistrer les frappes
            touche = key.char if hasattr(key, 'char') else str(key)
            touche_appuyees.append(touche)

    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la touche : {e}")

# Lancer l'écoute du clavier
with keyboard.Listener(on_press=on_press) as listener:
    print("Appuyez sur 'Échap' pour démarrer ou arrêter l'enregistrement.")
    listener.join()
