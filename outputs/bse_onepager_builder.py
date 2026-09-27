#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from pathlib import Path

OUTPUT = Path(__file__).parent / "BSE_2026_One_Pager.pdf"

W, H = A4

NAVY  = colors.HexColor("#1a2744")
GOLD  = colors.HexColor("#c9a84c")
LIGHT = colors.HexColor("#f5f5f0")
MUTED = colors.HexColor("#888888")
WHITE = colors.white

S = {
    "title":    ParagraphStyle("t",  fontName="Helvetica-Bold", fontSize=22, textColor=WHITE, alignment=TA_CENTER),
    "sub":      ParagraphStyle("s",  fontName="Helvetica",      fontSize=11, textColor=GOLD,  alignment=TA_CENTER),
    "dates":    ParagraphStyle("d",  fontName="Helvetica",      fontSize=9,  textColor=WHITE, alignment=TA_CENTER),
    "day":      ParagraphStyle("dy", fontName="Helvetica-Bold", fontSize=9,  textColor=WHITE),
    "time":     ParagraphStyle("tm", fontName="Helvetica-Bold", fontSize=8,  textColor=NAVY,  alignment=TA_RIGHT),
    "event":    ParagraphStyle("ev", fontName="Helvetica-Bold", fontSize=8.5,textColor=NAVY),
    "detail":   ParagraphStyle("dt", fontName="Helvetica",      fontSize=7.5,textColor=colors.HexColor("#444444"), leading=11),
    "ref_head": ParagraphStyle("rh", fontName="Helvetica-Bold", fontSize=7.5,textColor=WHITE),
    "ref_body": ParagraphStyle("rb", fontName="Helvetica",      fontSize=7,  textColor=colors.HexColor("#333333")),
    "footer":   ParagraphStyle("ft", fontName="Helvetica",      fontSize=7,  textColor=MUTED, alignment=TA_CENTER),
    "members":  ParagraphStyle("mb", fontName="Helvetica",      fontSize=8,  textColor=colors.HexColor("#333333"), alignment=TA_CENTER),
}

CW = W - 36*mm  # content width

def header():
    t = Table([[
        Paragraph("BAYSIDE ELITE", S["title"]),
        Paragraph("BSE 2026", S["sub"]),
        Paragraph("Gold Coast  ·  5 – 8 June 2026", S["dates"]),
    ]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("LINEBELOW",     (0,2), (-1,2), 2.5, GOLD),
    ]))
    return t

def members_bar():
    t = Table([[Paragraph(
        "Hugo  ·  Joe  ·  Mitchell  ·  Ryan G  ·  Ryan M  ·  Troy",
        S["members"])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), LIGHT),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW",     (0,0), (-1,0), 1, GOLD),
    ]))
    return t

def day_row(label, date):
    t = Table([[Paragraph(f"{label}  ·  {date}", S["day"])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    return t

def row(time, event, detail, bg=WHITE):
    t = Table([[
        Paragraph(time, S["time"]),
        [Paragraph(event, S["event"]), Paragraph(detail, S["detail"])],
    ]], colWidths=[18*mm, CW - 18*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), bg),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("LINEBELOW",     (0,0), (-1,-1), 0.3, colors.HexColor("#dddddd")),
    ]))
    return t

def refs_table():
    data = [
        [Paragraph("BOOKING REFS", S["ref_head"]),
         Paragraph("REF / CONFIRMATION", S["ref_head"]),
         Paragraph("CONTACT", S["ref_head"])],
        ["Virgin Australia (VA529 Fri / VA518 Mon)",  "EUYLIE",               "virginaustralia.com"],
        ["Accommodation — OCEAN Skyhome, Level 36",  "5326296631  PIN: 8625", "+61 0433 608 900"],
        ["Golf Group 1 — The Glades, Sat 1:08 PM",   "422609726",             "1800 942 929"],
        ["Golf Group 2 — The Glades, Sat 1:16 PM",   "422609773",             "1800 942 929"],
        ["Dinner — Kost, Sat 7:30 PM",               "39LFSW4254PH",         "kostrestaurant.com.au"],
    ]
    t = Table(data, colWidths=[75*mm, 52*mm, CW - 127*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), NAVY),
        ("FONTNAME",      (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",      (0,0), (-1,-1), 7),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, LIGHT]),
        ("GRID",          (0,0), (-1,-1), 0.3, colors.HexColor("#cccccc")),
        ("LINEBELOW",     (0,0), (-1,0), 1, GOLD),
    ]))
    return t

def build():
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4,
                            leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=14*mm, bottomMargin=12*mm)
    sp = lambda n=2: Spacer(1, n*mm)
    story = [
        header(), sp(2),
        members_bar(), sp(3),

        # FRIDAY
        day_row("FRIDAY", "5 June 2026"), sp(1),
        row("3:00 PM",  "Arrivals — Hugo, Joe, Mitchell, Ryan M",
                        "Check in at OCEAN Luxury Skyhome · Level 36, 21 Elizabeth Ave, Gold Coast"),
        row("3:20 PM",  "Ryan G — Departs Sydney (VA529)",
                        "Arrives Gold Coast 4:40 PM · ~5:10 PM at apartment", LIGHT),
        row("6:00 PM",  "Poker & Pizza Night",
                        "Ryan M's accommodation (TBC)"),
        row("10:00 PM", "Troy Arrives",
                        "Late arrival — welcome aboard!", LIGHT),
        sp(3),

        # SATURDAY
        day_row("SATURDAY", "6 June 2026"), sp(1),
        row("Morning",  "Breakfast at Local Cafe & Free Time",
                        "Explore Broadbeach before heading to the course"),
        row("1:08 PM",  "Golf — Group 1 (3 players)",
                        "The Glades Golf Club · 1 Glades Drive, Robina · 18 holes · Collared shirt, no denim", LIGHT),
        row("1:16 PM",  "Golf — Group 2 (3 players)",
                        "The Glades Golf Club · same course, 8-min stagger · Carts back by 5:30 PM"),
        row("7:30 PM",  "Dinner & BSE Awards — Kost Restaurant",
                        "3 Oracle Blvd, Broadbeach · 6 guests · Kost Experience $155pp · Awards presentation", LIGHT),
        row("9:30 PM",  "Star Casino",
                        "The Star Gold Coast · 1 Casino Drive, Broadbeach · running late"),
        sp(3),

        # SUNDAY
        day_row("SUNDAY", "7 June 2026"), sp(1),
        row("Morning",  "Breakfast & Farewell",
                        "Group breakfast · all guests depart Sunday"),
        row("By 11 AM", "Check Out — OCEAN Luxury Skyhome",
                        "Return keys · bring ID · vacate by 11:00 AM sharp", LIGHT),
        sp(3),

        HRFlowable(width="100%", thickness=0.8, color=GOLD), sp(2),
        refs_table(), sp(3),
        Paragraph("BSE 2026  ·  Gold Coast  ·  Ryan Gillis", S["footer"]),
    ]

    doc.build(story)
    print(f"PDF saved: {OUTPUT}")

if __name__ == "__main__":
    build()
