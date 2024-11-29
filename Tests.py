import pytest
from collections import Counter
import sys

# Inclure le répertoire courant dans le chemin de recherche
sys.path.append(".")

from Keylooger_V2 import analyser_touches, generer_histogramme, creer_clavier

# Test pour analyser_touches
def test_analyser_touches(capsys):
    touches = ["a", "b", "a", "c", "a", "b"]
    analyser_touches(touches)
    captured = capsys.readouterr()
    assert "Touche 'a': 3 fois" in captured.out
    assert "Touche 'b': 2 fois" in captured.out
    assert "Touche 'c': 1 fois" in captured.out

# Test pour générer_histogramme
def test_generer_histogramme():
    stats = Counter({"a": 3, "b": 2, "c": 1})
    try:
        generer_histogramme(stats)
    except Exception as e:
        pytest.fail(f"generer_histogramme a levé une exception : {e}")

# Test pour creer_clavier
def test_creer_clavier():
    stats = Counter({"a": 3, "b": 2, "c": 1})
    try:
        creer_clavier(stats)
    except Exception as e:
        pytest.fail(f"creer_clavier a levé une exception : {e}")
