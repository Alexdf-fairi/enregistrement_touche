Tests
=====

``tests/test_keylooger_V2.py`` : Ces tests permettent de tester toutes les fonctionnalités importantes du code.
 
Pour exécuter les tests, on peut utiliser la commande suivante :
``pytest tests/``
 
- Black & Ruff
 
Le code source du projet à été formater à l'aide de Black via la commande suivante et à été analyser par Ruff:
``black src/``
``ruff check src/``
 
- Coverage
 
On peut vérifier le coverage à l'aide des commandes suivantes :
 
``coverage run --source src/ -m pytest``
puis
``coverage report`` 

 
Pour analyser le code on peut utiliser la commande pylint qui attribue un score global de qualité au code :
``pylint .\src\Keylooger_V2.py``