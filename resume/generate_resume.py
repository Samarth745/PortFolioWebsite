import json
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).parent
source = ROOT / "Samarth_Prabhu_CV.json"
output = ROOT / "Samarth_Prabhu_Resume.pdf"

with source.open(encoding="utf-8") as file:
    resume = json.load(file)

ink = colors.HexColor("#17211f")
coral = colors.HexColor("#e4572e")
muted = colors.HexColor("#626964")
line = colors.HexColor("#d6d1c5")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Name", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=ink, alignment=TA_LEFT, spaceAfter=3))
styles.add(ParagraphStyle(name="Role", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=14, textColor=coral, spaceAfter=4))
styles.add(ParagraphStyle(name="Contact", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=11, textColor=muted, spaceAfter=10))
styles.add(ParagraphStyle(name="Heading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=12, textColor=coral, spaceBefore=8, spaceAfter=5, uppercase=True))
styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=ink, spaceAfter=3))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=10, textColor=muted))
styles.add(ParagraphStyle(name="Job", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=8.5, leading=11, textColor=ink, spaceAfter=2))


def markdown(text):
    return re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)


def section(title):
    return [Paragraph(title, styles["Heading"]), Table([['']], colWidths=[174 * mm], rowHeights=[0.5], style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), line)]))]

story = [Paragraph(resume["name"], styles["Name"]), Paragraph(f'{resume["title"]} · {resume["subtitle"]}', styles["Role"])]
story.append(Paragraph(f'{resume["location"]} · {resume["email"]} · {resume["linkedin"]}', styles["Contact"]))
story.extend(section("Profile"))
story.append(Paragraph(markdown(resume["summary"]), styles["Body"]))
story.extend(section("Experience"))

for job in resume["work_experience"]:
    title = job["title"].replace("--", "—")
    dates = f'{job["start_date"]} — {job["end_date"]}'
    story.append(Paragraph(f'<b>{title}</b> <font color="#626964">· {dates}</font>', styles["Job"]))
    company = job["company"]
    if job.get("client"):
        company += f' · {job["client"]}'
    story.append(Paragraph(company, styles["Small"]))
    for achievement in job["achievements"]:
        story.append(Paragraph(f'• {markdown(achievement)}', styles["Body"]))
    story.append(Spacer(1, 2))

story.extend(section("Skills"))
skill_rows = []
for category, skills in resume["skills"].items():
    skill_rows.append([Paragraph(f'<b>{category}</b>', styles["Small"]), Paragraph(skills, styles["Body"])])
skill_table = Table(skill_rows, colWidths=[45 * mm, 129 * mm], hAlign="LEFT")
skill_table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LINEBELOW', (0, 0), (-1, -2), 0.3, line), ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 8), ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
story.append(skill_table)
story.extend(section("Education & Recognition"))
for item in resume["education"]:
    story.append(Paragraph(f'<b>{item["degree"]}</b> · {item["institution"]} · {item["start_year"]}—{item["end_year"]}', styles["Body"]))
story.append(Paragraph("Certificate of Appreciation and Outstanding Performance Rating — Infosys", styles["Body"]))

doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=14 * mm, bottomMargin=14 * mm, title="Samarth Prabhu Resume", author="Samarth Prabhu")
doc.build(story)
print(output)
