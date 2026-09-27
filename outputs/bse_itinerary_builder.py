#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from pathlib import Path

OUTPUT = Path(__file__).parent / "BSE_Trip_Itinerary_2026.pdf"

W, H = A4

# Colour palette
NAVY    = colors.HexColor("#1a2744")
GOLD    = colors.HexColor("#c9a84c")
LIGHT   = colors.HexColor("#f5f5f0")
MUTED   = colors.HexColor("#666666")
WHITE   = colors.white

def styles():
    return {
        "title": ParagraphStyle("title",
            fontName="Helvetica-Bold", fontSize=28, textColor=WHITE,
            alignment=TA_CENTER, spaceAfter=4),
        "subtitle": ParagraphStyle("subtitle",
            fontName="Helvetica", fontSize=13, textColor=GOLD,
            alignment=TA_CENTER, spaceAfter=2),
        "dates": ParagraphStyle("dates",
            fontName="Helvetica", fontSize=10, textColor=WHITE,
            alignment=TA_CENTER, spaceAfter=0),
        "day_header": ParagraphStyle("day_header",
            fontName="Helvetica-Bold", fontSize=14, textColor=WHITE,
            alignment=TA_LEFT, spaceAfter=0),
        "event_title": ParagraphStyle("event_title",
            fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
            spaceAfter=2),
        "event_body": ParagraphStyle("event_body",
            fontName="Helvetica", fontSize=9.5, textColor=colors.HexColor("#333333"),
            leading=14, spaceAfter=2),
        "ref": ParagraphStyle("ref",
            fontName="Helvetica-Oblique", fontSize=8.5, textColor=MUTED,
            spaceAfter=0),
        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=8, textColor=MUTED,
            alignment=TA_CENTER),
    }

def header_table(s):
    inner = Table([[
        Paragraph("BAYSIDE ELITE", s["title"]),
        Paragraph("BSE 2026", s["subtitle"]),
        Paragraph("Gold Coast  ·  5 – 8 June 2026", s["dates"]),
    ]], colWidths=[W - 40*mm])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 18),
        ("BOTTOMPADDING", (0,0), (-1,-1), 18),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("LINEBELOW", (0,2), (-1,2), 3, GOLD),
    ]))
    return inner

def day_banner(label, date_str, s):
    t = Table([[Paragraph(f"{label}  ·  {date_str}", s["day_header"])]], colWidths=[W - 40*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 10),
        ("LINEAFTER", (0,0), (-1,-1), 4, GOLD),
    ]))
    return t

def event_card(time, icon, title, details, ref, s, bg=None):
    bg = bg or LIGHT
    time_cell  = Paragraph(f"<b>{time}</b>", ParagraphStyle("tc",
        fontName="Helvetica-Bold", fontSize=9, textColor=NAVY,
        alignment=TA_RIGHT))
    icon_cell  = Paragraph(icon, ParagraphStyle("ic",
        fontName="Helvetica-Bold", fontSize=14, textColor=GOLD,
        alignment=TA_CENTER))
    body_lines = [Paragraph(f"<b>{title}</b>", s["event_title"])]
    for line in details:
        body_lines.append(Paragraph(line, s["event_body"]))
    if ref:
        body_lines.append(Paragraph(f"Ref: {ref}", s["ref"]))
    body_cell = body_lines

    t = Table([[time_cell, icon_cell, body_cell]],
              colWidths=[22*mm, 10*mm, (W - 40*mm - 32*mm)])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("LINEBELOW",     (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
    ]))
    return t

def build():
    s = styles()
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=18*mm, bottomMargin=18*mm)
    story = []

    # ── Header ──────────────────────────────────────────────
    story.append(header_table(s))
    story.append(Spacer(1, 8*mm))

    # ── FRIDAY 5 JUNE ───────────────────────────────────────
    story.append(day_banner("FRIDAY", "5 June 2026", s))
    story.append(Spacer(1, 2*mm))

    story.append(event_card(
        "3:00 PM", "👥",
        "Member Arrivals",
        ["Hugo, Joe, Mitchell, Ryan M — arriving at check-in (3:00 PM)",
         "Ryan G — flying up (VA529), arriving approx. 5:10 PM after travel from airport",
         "Troy — arriving late Friday evening, approx. 10:00 PM"],
        None, s))

    story.append(event_card(
        "3:20 PM", "✈",
        "Depart Sydney — VA 529  (Ryan G)",
        ["Sydney Airport Terminal 2  →  Gold Coast Airport Terminal 1",
         "Arrives 4:40 PM  ·  Non-stop  ·  Boeing 737-800  ·  ~30 min travel to apartment",
         "Check in early — Lite fare, seats not pre-assigned"],
        "EUYLIE", s, bg=WHITE))

    story.append(event_card(
        "3:00 PM", "🏨",
        "Check In — OCEAN Luxury Skyhome at Oracle",
        ["Level 36, 21 Elizabeth Avenue, Gold Coast QLD 4218",
         "Check-in window: 3:00 PM – 9:00 PM  (call ahead to arrange time)",
         "3-bedroom ocean-view apartment  ·  6 adults",
         "Host contact: +61 0433 608 900  ·  Bring government ID + security deposit"],
        "5326296631", s))

    story.append(event_card(
        "6:00 PM", "🃏",
        "Poker & Pizza Night",
        ["Ryan M's accommodation  (location TBC)",
         "Grab a slice, shuffle up and deal — running late into the night"],
        None, s, bg=WHITE))

    story.append(event_card(
        "10:00 PM", "🚖",
        "Troy Arrives",
        ["Late arrival — welcome to Gold Coast, Troy!"],
        None, s))

    story.append(Spacer(1, 5*mm))

    # ── SATURDAY 6 JUNE ─────────────────────────────────────
    story.append(day_banner("SATURDAY", "6 June 2026", s))
    story.append(Spacer(1, 2*mm))

    story.append(event_card(
        "Morning", "☕",
        "Breakfast at Local Cafe & Free Time",
        ["Head to a local cafe for breakfast — plenty of options around Broadbeach & Oracle",
         "Free time until golf  ·  relax, explore, or hit the beach"],
        None, s, bg=WHITE))

    story.append(event_card(
        "1:08 PM", "⛳",
        "Tee Time — Group 1 (3 players)",
        ["The Glades Golf Club  ·  18 Holes",
         "Dress code: collared shirt required, no denim",
         "All tee times from 3 PM onwards are walking only",
         "Carts must be returned by 5:30 PM"],
        "422609726", s))

    story.append(event_card(
        "1:16 PM", "⛳",
        "Tee Time — Group 2 (3 players)",
        ["The Glades Golf Club  ·  18 Holes",
         "Same course, 8-minute stagger",
         "GolfNow contact: 1800 942 929"],
        "422609773", s, bg=WHITE))

    story.append(event_card(
        "5:30 PM", "🏌",
        "Post-Round Drinks",
        ["Carts returned  ·  Gather at the clubhouse for a drink",
         "Allow time to freshen up before dinner"],
        None, s))

    story.append(event_card(
        "7:30 PM", "🍷",
        "Dinner — Kost Restaurant",
        ["Shop 135S/3 Oracle Boulevard, Broadbeach QLD 4218",
         "Main Dining Room  ·  6 guests  ·  Until 9:30 PM",
         "Package: Kost Experience — $155 per person",
         "BSE Awards Presentation — best bettor of the year crowned at dinner",
         "No-show/late cancellation fee: $25 per person  ·  Cancel 24 hrs prior if needed"],
        "39LFSW4254PH", s, bg=WHITE))

    story.append(event_card(
        "9:30 PM", "🎰",
        "Star Casino",
        ["The Star Gold Coast  ·  1 Casino Drive, Broadbeach QLD 4218",
         "Running late into the night — good luck, gents"],
        None, s))

    story.append(Spacer(1, 5*mm))

    # ── SUNDAY 7 JUNE ───────────────────────────────────────
    story.append(day_banner("SUNDAY", "7 June 2026", s))
    story.append(Spacer(1, 2*mm))

    story.append(event_card(
        "Morning", "☕",
        "Breakfast & Farewell",
        ["Group breakfast before everyone heads off",
         "All guests depart Sunday — safe travels!"],
        None, s, bg=WHITE))

    story.append(event_card(
        "By 11:00 AM", "🔑",
        "Check Out — OCEAN Luxury Skyhome",
        ["Return keys to host  ·  Vacate by 11:00 AM sharp",
         "Damage policy: up to AUD 500 may be charged for damage"],
        "5326296631", s))

    story.append(Spacer(1, 5*mm))

    # ── Quick Reference ─────────────────────────────────────
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    story.append(Spacer(1, 3*mm))

    ref_data = [
        [Paragraph("<b>BOOKING REFERENCES</b>", ParagraphStyle("rh",
            fontName="Helvetica-Bold", fontSize=10, textColor=NAVY)), "", "", ""],
        [Paragraph("<b>Item</b>", s["ref"]),
         Paragraph("<b>Details</b>", s["ref"]),
         Paragraph("<b>Ref / Confirmation</b>", s["ref"]),
         Paragraph("<b>Contact</b>", s["ref"])],
        ["Virgin Australia (both flights)",
         "VA529 Fri 3:20PM / VA518 Mon 11:20AM",
         "EUYLIE",
         "virginaustralia.com"],
        ["Accommodation",
         "OCEAN Skyhome, 21 Elizabeth Ave GC",
         "5326296631  PIN: 8625",
         "+61 0433 608 900"],
        ["Golf — Group 1",
         "The Glades, Sat 1:08 PM, 3 players",
         "422609726",
         "1800 942 929"],
        ["Golf — Group 2",
         "The Glades, Sat 1:16 PM, 3 players",
         "422609773",
         "1800 942 929"],
        ["Dinner — Kost",
         "Oracle Blvd, Sat 7:30 PM, 6 guests",
         "39LFSW4254PH",
         "kostrestaurant.com.au"],
    ]

    ref_table = Table(ref_data, colWidths=[45*mm, 58*mm, 42*mm, 25*mm])
    ref_table.setStyle(TableStyle([
        ("SPAN",          (0,0), (3,0)),
        ("BACKGROUND",    (0,0), (3,0), LIGHT),
        ("BACKGROUND",    (0,1), (3,1), NAVY),
        ("TEXTCOLOR",     (0,1), (3,1), WHITE),
        ("FONTNAME",      (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 8),
        ("FONTNAME",      (0,1), (-1,1), "Helvetica-Bold"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS", (0,2), (-1,-1), [WHITE, LIGHT]),
        ("GRID",          (0,1), (-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("LINEBELOW",     (0,0), (-1,0), 1, GOLD),
    ]))
    story.append(ref_table)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("Generated for Ryan Gillis  ·  Bayside Elite 2026", s["footer"]))

    doc.build(story)
    print(f"PDF saved: {OUTPUT}")

if __name__ == "__main__":
    build()
