import pytest
from app.division import Division
import logging


def test_division_succes():
    """Teste une division normale."""
    division = Division(10, 2)
    assert division.diviser() == 5.0


def test_division_zero():
    """Teste la division par zéro."""
    division = Division(10, 0)
    assert division.diviser() == float("inf")


def test_division_type_error():
    """Teste si une exception est levée pour des valeurs non numériques."""
    with pytest.raises(ValueError, match="Les valeurs doivent être des nombres."):
        Division("10", 2).diviser()


def test_logs_division():
    """Vérifie que les logs sont bien écrits lors d'une division."""
    division = Division(10, 2)
    result = division.diviser()
    assert result == 5.0  # Vérifie que la division est correcte

    # Forcer l'écriture des logs dans le fichier avant de lire
    logging.shutdown()

    # Ouvre le fichier de log et vérifie que le message de succès est bien présent
    with open("logs/debug.log", "r") as log_file:
        logs = log_file.read()
        assert "Division réussie" in logs
