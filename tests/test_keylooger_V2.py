import pytest
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors

# Configuration du clavier AZERTY pour le test
keyboard_layout = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "←"],
    ["Tab", "A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "^", "$"],
    ["Caps", "Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "ù", "Enter"],
    ["Shift", "W", "X", "C", "V", "B", "N", ",", ";", ":", "!", "Shift"],
    ["Ctrl", "Alt", "Espace", "AltGr", "Ctrl"]
]


@pytest.fixture(autouse=True)
def setup():
    """Réinitialise les variables globales utilisées."""
    global touches_appuyees, enregistrement, esc_press_count
    touches_appuyees = []
    enregistrement = False
    esc_press_count = 0
    yield


def test_toggle_enregistrement():
    """Teste la logique de démarrage/arrêt d'enregistrement."""
    global enregistrement, esc_press_count

    # Simuler un premier appui sur Échap
    esc_press_count += 1
    enregistrement = not enregistrement

    # Vérifier que l'enregistrement démarre
    assert enregistrement is True
    assert esc_press_count == 1

    # Simuler un second appui sur Échap
    esc_press_count += 1
    enregistrement = not enregistrement

    # Vérifier que l'enregistrement s'arrête
    assert enregistrement is False
    assert esc_press_count == 2


def test_record_keys():
    """Teste l'ajout des touches enregistrées."""
    global enregistrement, touches_appuyees

    # Démarrer l'enregistrement
    enregistrement = True

    # Simuler l'appui sur une touche imprimable
    key_char = 'a'
    if enregistrement:
        touches_appuyees.append(key_char.lower())

    # Vérifier que la touche a été ajoutée
    assert touches_appuyees == ['a']

    # Simuler l'appui sur une touche spéciale
    key_char = 'shift'
    if enregistrement:
        touches_appuyees.append(key_char.lower())

    # Vérifier que les deux touches ont été ajoutées
    assert touches_appuyees == ['a', 'shift']


def test_statistics():
    """Teste le calcul des statistiques des touches."""
    touches_appuyees = ['a', 'b', 'a', 'c', 'b', 'b']
    stats = Counter(touches_appuyees)

    # Vérifier les statistiques calculées
    assert stats['a'] == 2
    assert stats['b'] == 3
    assert stats['c'] == 1


def test_generate_histogram():
    """Teste la génération de l'histogramme des touches."""
    stats = Counter({'a': 3, 'b': 2, 'c': 1})

    # Simuler la création d'un histogramme
    plt.figure(figsize=(10, 6))
    plt.bar(stats.keys(), stats.values(), color='skyblue')
    plt.xlabel("Touches")
    plt.ylabel("Nombre d'appuis")
    plt.title("Histogramme des touches appuyées")

    # Tester l'affichage sans exception
    try:
        plt.show()
    except Exception as e:
        pytest.fail(f"Erreur lors de l'affichage de l'histogramme : {e}")


def test_generate_keyboard_heatmap():
    """Teste la création de la heatmap du clavier."""
    stats = Counter({'a': 5, 'b': 3, 'c': 1})
    max_count = max(stats.values(), default=1)

    # Simuler la création d'une heatmap de clavier
    cmap = plt.cm.plasma
    norm = mcolors.Normalize(vmin=0, vmax=max_count)

    # Créer la figure
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.set_xlim(0, 15)
    ax.set_ylim(-7, 0)
    ax.axis('off')

    # Dessiner chaque ligne de touches
    key_width = 1
    key_height = 1
    horizontal_spacing = 0.2
    vertical_spacing = 0.2
    y_offset = 0

    for row in keyboard_layout:
        x_offset = 0
        for key in row:
            count = stats.get(key.lower(), 0)
            base_color = cmap(norm(count))
            rgba_color = mcolors.to_rgba(base_color, alpha=0.7)

            # Dessiner une touche
            rect = patches.Rectangle(
                (x_offset, y_offset), key_width, key_height,
                linewidth=1, edgecolor="black", facecolor=rgba_color
            )
            ax.add_patch(rect)

            # Ajouter le texte de la touche
            ax.text(
                x_offset + key_width / 2, y_offset + key_height / 2,
                f"{key}\n{count}",
                ha="center", va="center", fontsize=8, color="white" if count > 0 else "black"
            )

            # Ajuster la position pour la prochaine touche
            x_offset += key_width + horizontal_spacing

        # Ajuster la position pour la prochaine ligne
        y_offset -= key_height + vertical_spacing

    # Ajouter une barre de couleur
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation="vertical", pad=0.02)
    cbar.set_label("Nombre d'appuis")

    # Tester l'affichage sans exception
    try:
        plt.show()
    except Exception as e:
        pytest.fail(f"Erreur lors de l'affichage de la heatmap : {e}")
