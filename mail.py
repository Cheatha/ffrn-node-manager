# -*- coding: utf-8 -*-
from flask_mail import Message

def getMail(node):
    msg = Message("Dein Freifunk Knoten", sender=("FFRN Node Registration", "info@freifunk-rhein-neckar.de"), recipients = [node['email']])
    msg.body = '''
Hey {nickname},

Du hast gerade einen neuen Knoten für das Netz von Freifunk Rhein Neckar registriert - cool!

Die Daten deines Knotens lauten:

    Hostname:       {hostname}
    MAC:            {mac}
    VPN Key:        {key}
    Koordinaten:    {coords}
    Nick:           {nickname}
    Mail:           {email}
    Token:          {token}

Bitte halte diese Daten aktuell. Du kannst Sie unter [1] pflegen.

Wir hoffen, dass Du gut zurecht gekommen bist und würden uns freuen, wenn Du dich auch persönlich in die Community einbringen würdest. Vielleicht kannst Du ja sogar noch weitere Leute von unserem Projekt überzeugen.

Solltest du Probleme oder Anregungen haben, kannst Du entweder auf diese Email antworten oder uns mittels einer der Kontaktmöglichkeiten im Wiki [2] erreichen.

Viele Grüße,
Freifunk Rhein Neckar

[1] https://register.freifunk-rhein-neckar.de/
[2] https://w.ffrn.de/kontakt
'''.format(**node)
    return msg
