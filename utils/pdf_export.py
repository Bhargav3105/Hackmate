from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import (
    getSampleStyleSheet, ParagraphStyle
)
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import io


def generate_project_plan_pdf(idea, team_name="Team"):
    """
    Generates a PDF document for a single AI
    project idea. Returns bytes for download.
    """
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#1a1a2e"),
        spaceAfter=6,
        alignment=TA_LEFT
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontSize=12,
        textColor=colors.HexColor("#6342f5"),
        spaceAfter=16,
        fontName="Helvetica-Oblique"
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#1a1a2e"),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontSize=10.5,
        textColor=colors.HexColor("#3a3a3a"),
        leading=16,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=styles["Normal"],
        fontSize=10.5,
        textColor=colors.HexColor("#3a3a3a"),
        leading=16,
        leftIndent=14,
        spaceAfter=4
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#888888"),
        spaceAfter=20
    )

    story = []

    # Header
    story.append(Paragraph("HackMate", meta_style))
    story.append(
        Paragraph(idea.get("title", "Project Plan"),
                  title_style)
    )
    story.append(
        Paragraph(idea.get("tagline", ""), subtitle_style)
    )
    story.append(
        Paragraph(
            f"Team: {team_name} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"Difficulty: {idea.get('difficulty', 'Medium')}",
            meta_style
        )
    )
    story.append(
        HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#e0e0e0")
        )
    )
    story.append(Spacer(1, 12))

    # Problem
    story.append(Paragraph("The Problem", heading_style))
    story.append(
        Paragraph(idea.get("problem", ""), body_style)
    )

    # Solution
    story.append(Paragraph("Our Solution", heading_style))
    story.append(
        Paragraph(idea.get("solution", ""), body_style)
    )

    # Key Features
    story.append(
        Paragraph("Key Features", heading_style)
    )
    for feature in idea.get("key_features", []):
        story.append(
            Paragraph(f"•&nbsp;&nbsp;{feature}",
                      bullet_style)
        )

    # Tech Stack
    story.append(Paragraph("Tech Stack", heading_style))
    tech_text = ", ".join(idea.get("tech_stack", []))
    story.append(Paragraph(tech_text, body_style))

    # Timeline Table
    story.append(
        Paragraph("3-Day MVP Timeline", heading_style)
    )
    timeline = idea.get("mvp_timeline", {})
    table_data = [["Day", "Tasks"]]
    for day, task in timeline.items():
        day_label = day.replace("day_", "Day ")
        table_data.append([day_label, task])

    timeline_table = Table(
        table_data,
        colWidths=[1.0 * inch, 5.2 * inch]
    )
    timeline_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#6342f5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#e0e0e0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f7f7fb")]),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(timeline_table)
    story.append(Spacer(1, 14))

    # Wow Factor
    story.append(Paragraph("Wow Factor", heading_style))
    story.append(
        Paragraph(idea.get("wow_factor", ""), body_style)
    )

    story.append(Spacer(1, 20))
    story.append(
        HRFlowable(
            width="100%", thickness=1,
            color=colors.HexColor("#e0e0e0")
        )
    )
    story.append(
        Paragraph(
            "Generated by HackMate — AI-powered "
            "hackathon collaboration platform",
            meta_style
        )
    )

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()