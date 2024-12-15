# Keylogger Heatmap

Ce projet est un keylogger qui enregistre les appuis de touche et génère :
- Un histogramme du nombre d'appuis sur chaque touche.
- Une heatmap affichant les zones les plus utilisées du clavier.

## Fonctionnalités

- **Enregistrement des touches :** Les frappes sont enregistrées avec `pynput` dès qu'on appuie sur `Échap` pour démarrer et arrêtées en appuyant à nouveau sur `Échap`.
- **Affichage graphique :** L'affichage graphique se fait en appuyant sur `Échap` après avoir stopper l'enregistrement. Il va alors s'afficher :
  - Histogramme : Visualisation du nombre d'appuis par touche.
  - Heatmap : Affiche une carte à gradient de couleur pour une représentation visuelle du clavier.
- **Interactivité :** L'application utilise `matplotlib`  pour générer des graphiques et des heatmaps interactifs.

## Installation

### Prérequis

- Python 3.13
- Les bibliothèques nécessaires sont listées dans `requirements.txt`.

### Installation des dépendances

Pour installer les dépendances, exécutez :

```bash
pip install -r requirements.txt
