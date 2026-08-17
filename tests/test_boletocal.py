"""Testes do BoletoCal (oracle do create-mvp)."""
from boletocal.parser import extract
from boletocal.calendar import to_ics

SAMPLE = """Beneficiario: Energisa Sul-SC\nVencimento: 15/08/2025\nValor: R$ 287,43\nLinha digitavel: 23793.30426.00000.0.000000000000000\n"""

def test_extract_due():
    d = extract(SAMPLE)
    assert d["due"] == "2025-08-15"

def test_extract_value():
    d = extract(SAMPLE)
    assert d["value"] == 287.43
    assert d["raw_value"] == "287,43"

def test_extract_payee():
    d = extract(SAMPLE)
    assert "Energisa" in d["payee"]

def test_extract_linha_digitavel():
    d = extract(SAMPLE)
    assert d["linha_digitavel"] is not None

def test_to_ics_contains_due_and_value():
    d = extract(SAMPLE)
    ics = to_ics(d)
    assert "20250815" in ics
    assert "Energisa" in ics
    assert "BEGIN:VEVENT" in ics and "END:VEVENT" in ics
