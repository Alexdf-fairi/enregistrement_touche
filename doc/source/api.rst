API
===================

Cette section présente les fonctions et variables disponibles dans le code. Les fonctions principales sont listées avec leurs descriptions, leurs paramètres, et leurs retours.
 
touches_appuyees
 
   Liste globale pour stocker les touches enregistrées lors de l'exécution.
 
enregistrement
 
   Booléen global pour savoir si l'enregistrement des touches est actif.
 
esc_press_count
 
   Compteur global pour suivre le nombre d'appuis sur la touche Échap.
 
keyboard_layout
 
   Représente la disposition simplifiée d'un clavier AZERTY sous forme de liste de listes.
 
on_press(key)
 
   Gère les événements liés à l'appui des touches sur le clavier.
 
   **Paramètres**:
      - **key** (*pynput.keyboard.Key*) : La touche qui a été pressée.
 
   **Retour**:
      - `bool` : Retourne `False` si l'écoute du clavier doit s'arrêter, sinon rien.
 
   **Exceptions**:
      - Affiche une erreur en cas de problème lors de l'enregistrement des touches.
 
analyser_touches(touches)
 
   Analyse la liste des touches enregistrées pour générer des statistiques, un histogramme et une heatmap.
 
   **Paramètres**:
      - **touches** (*list[str]*) : Liste des touches enregistrées.
 
   **Retour**:
      - Aucun.
 
generer_histogramme(stats)
 
   Génère un histogramme représentant le nombre d'appuis pour chaque touche enregistrée.
 
   **Paramètres**:
      - **stats** (*collections.Counter*) : Un objet `Counter` contenant les statistiques des appuis de touches.
 
   **Retour**:
      - Aucun.
 
creer_clavier(stats)
 
   Crée une heatmap interactive représentant la disposition du clavier avec des niveaux de couleur basés sur le nombre d'appuis des touches.
 
   **Paramètres**:
      - **stats** (*collections.Counter*) : Un objet `Counter` contenant les statistiques des appuis de touches.
 
   **Retour**: aucun