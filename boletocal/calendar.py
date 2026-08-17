"""BoletoCal — gera um .ics (evento + alarme) a partir dos dados do boleto."""
from __future__ import annotations
from datetime import datetime, timedelta

ICS_HEAD = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//BoletoCal//PT-BR//\nCALSCALE:GREGORIAN\n"
ICS_TAIL = "END:VCALENDAR"

def _fmt(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S")

def to_ics(data: dict, reminder_days: int = 2) -> str:
    due = datetime.strptime(data["due"], "%Y-%m-%d")
    payee = data.get("payee") or "Boleto"
    value = data.get("raw_value") or (f'{data["value"]:.2f}' if data.get("value") else "")
    summary = f"Boleto: {payee} {('R$ '+value) if value else ''}".strip()
    alarm = (due - timedelta(days=reminder_days))
    lines = [
        ICS_HEAD,
        "BEGIN:VEVENT",
        f"UID:boletocal-{due.strftime('%Y%m%d')}-{abs(hash(payee))}",
        f"DTSTAMP:{_fmt(datetime.now())}",
        f"DTSTART;VALUE=DATE:{data['due'].replace('-','')}",
        f"SUMMARY:{summary}",
        f"DESCRIPTION:Pagar até o vencimento. Linha digitável: {data.get('linha_digitavel') or 'n/a'}",
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"TRIGGER:-P{reminder_days}D",
        f"DESCRIPTION:Lembrete: {summary}",
        "END:VALARM",
        "END:VEVENT",
        ICS_TAIL,
    ]
    return "\n".join(lines)
