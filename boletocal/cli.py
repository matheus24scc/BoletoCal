"""BoletoCal CLI — extrai boleto de um arquivo e gera o .ics."""
from __future__ import annotations
import argparse, json, pathlib, sys
from .parser import extract
from .calendar import to_ics

def main(argv=None):
    ap = argparse.ArgumentParser(prog="boletocal", description="Boleto -> evento de calendario (.ics)")
    ap.add_argument("path", help="arquivo de texto/boleto (.txt)")
    ap.add_argument("--reminder-days", type=int, default=2)
    args = ap.parse_args(argv)
    text = pathlib.Path(args.path).read_text(encoding="utf-8", errors="replace")
    data = extract(text)
    if not data["due"]:
        print("ERRO: nao foi possivel extrair o vencimento.", file=sys.stderr); return 1
    print(json.dumps(data, ensure_ascii=False, indent=2))
    ics = to_ics(data, args.reminder_days)
    out = pathlib.Path(args.path).with_suffix(".ics")
    out.write_text(ics, encoding="utf-8")
    print(f"\n.ics gerado: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
