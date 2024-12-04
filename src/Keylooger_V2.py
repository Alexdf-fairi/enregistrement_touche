from pynput import keyboard
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors

# Variable globale pour stocker les touches enregistrées
touches_appuyees = []
enregistrement = False
esc_press_count = 0  # Compteur d'appuis sur la touche Échap

# Disposition du clavier (clavier AZERTY simplifié)
keyboard_layout = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "←"],
    ["Tab", "A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "^", "$"],
    ["Caps", "Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "ù", "Enter"],
    ["Shift", "W", "X", "C", "V", "B", "N", ",", ";", ":", "!", "Shift"],
    ["Ctrl", "Alt", "Espace", "AltGr", "Ctrl"]
]

# Fonction pour démarrer/arrêter l'enregistrement des touches
def on_press(key):
    global enregistrement, touches_appuyees, esc_press_count

    try:
        # Si 'Échap' est pressé
        if key == keyboard.Key.esc:
            esc_press_count += 1
            if esc_press_count == 2:  # Quitter si Échap est appuyé deux fois
                print("Programme terminé.")
                return False  # Arrête l'écoute du clavier
            
            # Alterner le mode enregistrement
            enregistrement = not enregistrement
            if enregistrement:
                print("Enregistrement démarré...")
                touches_appuyees = []  # Réinitialiser les touches
            else:
                print("Enregistrement arrêté.")
        
        elif enregistrement:
            esc_press_count = 0  # Réinitialiser le compteur Échap
            # Ajouter la touche appuyée à touches_appuyees
            if hasattr(key, 'char') and key.char is not None:
                touches_appuyees.append(key.char.lower())  # Caractères imprimables
            elif hasattr(key, 'name') and key.name is not None:
                touches_appuyees.append(key.name.lower())  # Touches spéciales comme "shift"
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des touches : {e}")

# Fonction pour analyser les touches enregistrées
def analyser_touches(touches):
    stats = Counter(touches)

    print("\nStatistiques des touches pressées :")
    for touche, count in stats.items():
        print(f"Touche '{touche}': {count} fois")

    # Générer un histogramme des touches appuyées
    generer_histogramme(stats)

    # Générer le clavier heatmap
    creer_clavier(stats)

# Fonction pour générer un histogramme
def generer_histogramme(stats):
    plt.figure(figsize=(10, 6))
    plt.bar(stats.keys(), stats.values(), color='skyblue')
    plt.xlabel("Touches")
    plt.ylabel("Nombre d'appuis")
    plt.title("Histogramme des touches appuyées")
    plt.show()

# Fonction pour créer un clavier dynamique avec opacité
def creer_clavier(stats):
    max_count = max(stats.values(), default=1)  # Pour normaliser les couleurs

    # Définir la colormap
    cmap = plt.cm.plasma
    norm = mcolors.Normalize(vmin=0, vmax=max_count)

    # Créer la figure
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set_xlim(0, 15)
    ax.set_ylim(-7, 0)
    ax.axis('off')

    # Dessiner chaque ligne du clavier
    key_width = 1
    key_height = 1
    horizontal_spacing = 0.2
    vertical_spacing = 0.2
    y_offset = 0
    for row in keyboard_layout:
        x_offset = 0
        for key in row:
            # Couleur de la touche en fonction des statistiques
            count = stats.get(key.lower(), 0)  # Statistiques en minuscules pour correspondance
            base_color = cmap(norm(count))

            # Ajouter un canal alpha (opacité)
            rgba_color = mcolors.to_rgba(base_color, alpha=0.7)  # Alpha = 70%

            # Dessiner la touche comme un rectangle
            rect = patches.Rectangle(
                (x_offset, y_offset), key_width, key_height,
                linewidth=1, edgecolor="black", facecolor=rgba_color
            )
            ax.add_patch(rect)

            # Afficher le texte de la touche
            ax.text(
                x_offset + key_width / 2, y_offset + key_height / 2,
                f"{key}\n{count}",  # Inclure le nombre d'appuis
                ha="center", va="center", fontsize=8, color="white" if count > 0 else "black"
            )

            # Ajuster la position pour la prochaine touche
            x_offset += key_width + horizontal_spacing

        # Ajuster la position pour la prochaine ligne
        y_offset -= key_height + vertical_spacing

    # Ajouter une barre de couleur pour la légende
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation="vertical", pad=0.02)
    cbar.set_label("Nombre d'appuis")

    # Afficher le clavier
    plt.title("Heatmap du clavier")
    plt.show()

# Démarrer le listener pour enregistrer les touches
if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press) as listener:
        print("Appuyez sur 'Échap' pour commencer/arrêter l'enregistrement.")
        print("Appuyez deux fois sur 'Échap' pour terminer le programme.")
        listener.join()

    # Après l'arrêt du listener, analyser les touches dans le thread principal
    analyser_touches(touches_appuyees)
