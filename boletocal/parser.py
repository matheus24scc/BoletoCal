"""BoletoCal — extrai vencimento, valor e beneficiário de boletos (texto/linha digitável)."""
from __future__ import annotations
import re
from datetime import datetime

_DUE = re.compile(r"(?:vencimento|venc\.?|data\s*de\s*vencimento|data\s*venc\.?)[\s:]*(\d{2}[/-]\d{2}[/-]\d{4})", re.I)
_VALUE = re.compile(r"(?:valor(?:\s*documento|\s*a\s*pagar|\s*cobrado)?)[\s:]*R\$\s*([\d]{1,3}(?:\.\d{3})*(?:,\d{2})?)", re.I)
_PAYEE = re.compile(r"(?:benefici\w*\s*rio|cedente|empresa|sacado)[\s:]*([^\n]+)", re.I)
_LINHA = re.compile(r"(?:linha\s*digit[\wà-ú]*\s*:?\s*)?(\d{5}[.\s]?\d{5}[.\s]?\d{5}[.\s]?\d[.\s]?\d{5,15})|(\d{47})", re.I)

def _to_float(br: str) -> float:
    s = br.strip().replace(".", "").replace(",", ".")
    return float(s)

def _to_iso(d: str) -> str:
    return datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m-%d")

def extract(text: str) -> dict:
    due_m = _DUE.search(text)
    val_m = _VALUE.search(text)
    pay_m = _PAYEE.search(text)
    lin_m = _LINHA.search(text)
    return {
        "payee": pay_m.group(1).strip() if pay_m else None,
        "due": _to_iso(due_m.group(1)) if due_m else None,
        "value": _to_float(val_m.group(1)) if val_m else None,
        "raw_value": val_m.group(1) if val_m else None,
        "linha_digitavel": (lin_m.group(1) or lin_m.group(2)) if lin_m else None,
    }
