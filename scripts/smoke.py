"""Smoke test end-to-end do BoletoCal (uso real, nao so unittest)."""
from __future__ import annotations
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from boletocal.parser import extract
from boletocal.calendar import to_ics


def chk(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    return bool(cond)


def main() -> int:
    sample = (
        "Beneficiario: Energisa S.A.\n"
        "Vencimento: 15/09/2025\n"
        "Valor: R$ 150,75\n"
        "Linha digitavel: 12345.67890 12345.67890 12345.67890 1 12345678901234\n"
    )
    data = extract(sample)
    ok = True
    ok &= chk("extract vencimento=2025-09-15", data["due"] == "2025-09-15")
    ok &= chk("extract valor=150.75", abs((data["value"] or 0) - 150.75) < 1e-6)
    ok &= chk("extract beneficiario", data["payee"] == "Energisa S.A.")
    ok &= chk("extract linha digitavel", bool(data["linha_digitavel"]))
    ics = to_ics(data)
    ok &= chk("ics estrutura valida", ics.startswith("BEGIN:VCALENDAR") and ics.strip().endswith("END:VCALENDAR"))
    ok &= chk("ics tem vencimento", "20250915" in ics)
    ok &= chk("ics tem beneficiario", "Energisa" in ics)
    ok &= chk("ics tem alarme/lembrete", "BEGIN:VALARM" in ics)
    # CLI real
    tf = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    tf.write(sample); tf.close()
    try:
        from boletocal.cli import main as cli_main
        rc = cli_main([tf.name])
        ics_path = Path(tf.name).with_suffix(".ics")
        ok &= chk("cli gera .ics", rc == 0 and ics_path.exists())
    finally:
        Path(tf.name).unlink(missing_ok=True)
        Path(tf.name).with_suffix(".ics").unlink(missing_ok=True)
    print("\nSMOKE BoletoCal:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
