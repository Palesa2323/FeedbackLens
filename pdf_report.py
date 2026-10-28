
from io import BytesIO
from xml.sax.saxutils import escape

import matplotlib.pyplot as plt
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as PDFImage,
    LongTable,
    KeepTogether,
)

from report_analysis import (
    generate_report_insights,
    generate_recommendations,
    find_common_words,
)

from visualizations import (
    create_sentiment_donut,
    create_sentiment_comparison,
    create_score_distribution,
)


def build_feedback_pdf(summary, results_df):
    """Create a downloadable PDF report from existing analysis results."""

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="FeedbackLens AI Feedback Report",
        author="FeedbackLens AI",
    )

    # Soft feminine tech palette
    lavender = colors.HexColor("#80649B")
    pale_lavender = colors.HexColor("#F1EAF9")
    blush = colors.HexColor("#FCEBF1")
    cream = colors.HexColor("#FFFDF7")
    muted = colors.HexColor("#766A80")
    dark = colors.HexColor("#453851")
    grid = colors.HexColor("#E5D8EF")

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        alignment=TA_CENTER,
        textColor=lavender,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        alignment=TA_CENTER,
        textColor=muted,
        spaceAfter=18,
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontSize=16,
        leading=20,
        textColor=lavender,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True,
    ))

    styles.add(ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        textColor=dark,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="SmallCell",
        parent=styles["BodyText"],
        fontSize=7.5,
        leading=10,
        textColor=dark,
        wordWrap="CJK",
    ))

    styles.add(ParagraphStyle(
        name="TableHeader",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=dark,
    ))

    story = []

    def add_paragraph(text, style="ReportBody"):
        story.append(Paragraph(str(text), styles[style]))

    def add_heading(text):
        story.append(Paragraph(escape(text), styles["SectionHeading"]))

    def add_table(data, widths, header=True):
        table = LongTable(
            data,
            colWidths=widths,
            repeatRows=1 if header else 0,
            hAlign="LEFT",
        )

        commands = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.4, grid),
        ]

        if header:
            commands.extend([
                ("BACKGROUND", (0, 0), (-1, 0), pale_lavender),
                ("TEXTCOLOR", (0, 0), (-1, 0), dark),
            ])

        if len(data) > 1:
            commands.append(
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, cream])
            )

        table.setStyle(TableStyle(commands))
        story.append(table)
        story.append(Spacer(1, 8))

    def chart_to_pdf_image(fig, width=165 * mm):
        image_buffer = BytesIO()
        fig.savefig(
            image_buffer,
            format="png",
            dpi=160,
            bbox_inches="tight",
            facecolor="#FFFCFF",
        )
        plt.close(fig)
        image_buffer.seek(0)

        image = PDFImage(image_buffer)
        image.drawWidth = width
        image.drawHeight = width * 0.57
        return image

    # ---------- COVER AND EXECUTIVE SUMMARY ----------
    story.append(Spacer(1, 12 * mm))
    add_paragraph("FeedbackLens AI", "ReportTitle")
    add_paragraph(
        "Feedback Analysis Report | Sentiment, patterns and recommendations",
        "ReportSubtitle",
    )

    add_heading("1. Executive summary")

    total = int(summary.get("total_reviews", len(results_df)))

    summary_rows = [
        [
            Paragraph("Metric", styles["TableHeader"]),
            Paragraph("Responses", styles["TableHeader"]),
            Paragraph("Percentage", styles["TableHeader"]),
        ],
        [
            Paragraph("Total feedback", styles["SmallCell"]),
            str(total),
            "100.0%" if total else "0.0%",
        ],
        [
            Paragraph("Positive", styles["SmallCell"]),
            str(summary.get("positive_count", 0)),
            f'{summary.get("positive_percentage", 0):.1f}%',
        ],
        [
            Paragraph("Negative", styles["SmallCell"]),
            str(summary.get("negative_count", 0)),
            f'{summary.get("negative_percentage", 0):.1f}%',
        ],
        [
            Paragraph("Neutral", styles["SmallCell"]),
            str(summary.get("neutral_count", 0)),
            f'{summary.get("neutral_percentage", 0):.1f}%',
        ],
    ]

    add_table(summary_rows, [65 * mm, 45 * mm, 45 * mm])

    add_paragraph(
        "This report summarises the sentiment classifications, recurring "
        "language, notable patterns and suggested areas for review in the "
        "uploaded feedback. Recommendations are indicators for investigation, "
        "not proof of the underlying causes."
    )

    # ---------- SENTIMENT CHARTS ----------
    add_heading("2. Sentiment visualisations")

    try:
        story.append(
            chart_to_pdf_image(
                create_sentiment_donut(results_df)
            )
        )
        story.append(Spacer(1, 8))
    except Exception:
        add_paragraph("The sentiment donut chart could not be generated.")

    try:
        story.append(
            chart_to_pdf_image(
                create_sentiment_comparison(results_df)
            )
        )
        story.append(Spacer(1, 8))
    except Exception:
        add_paragraph("The sentiment comparison chart could not be generated.")

    if "compound" in results_df.columns:
        try:
            add_heading("Sentiment score distribution")
            story.append(
                chart_to_pdf_image(
                    create_score_distribution(results_df)
                )
            )
            story.append(Spacer(1, 8))
        except Exception:
            add_paragraph("The score distribution chart could not be generated.")
    else:
        add_paragraph(
            "A sentiment score distribution chart was not included because "
            "individual compound scores are not available in the results."
        )

    # ---------- KEY INSIGHTS ----------
    add_heading("3. Key findings")

    report_insights = generate_report_insights(summary, results_df)

    if report_insights:
        for insight in report_insights:
            add_paragraph("• " + escape(str(insight)))
    else:
        add_paragraph("No additional report insights were generated.")

    # ---------- COMMON WORDS ----------
    add_heading("4. Descriptive word analysis")

    for sentiment in ["Positive", "Negative", "Neutral"]:
        words = find_common_words(
            results_df,
            sentiment=sentiment,
            top_n=10,
        )

        add_paragraph(f"<b>{sentiment} feedback</b>")

        if words:
            word_rows = [
                [
                    Paragraph("Word", styles["TableHeader"]),
                    Paragraph("Mentions", styles["TableHeader"]),
                ]
            ]

            for word, count in words:
                word_rows.append([
                    Paragraph(escape(str(word)), styles["SmallCell"]),
                    str(count),
                ])

            add_table(word_rows, [90 * mm, 40 * mm])
        else:
            add_paragraph("No frequent descriptive words were identified.")

    add_paragraph(
        "Word mentions count occurrences in the feedback, not unique "
        "respondents. Frequent terms should be interpreted in context."
    )

    # ---------- RECOMMENDATIONS ----------
    add_heading("5. Recommendations")

    recommendations = generate_recommendations(summary, results_df)

    if recommendations:
        recommendation_rows = [[
            Paragraph("Area", styles["TableHeader"]),
            Paragraph("Priority", styles["TableHeader"]),
            Paragraph("Evidence", styles["TableHeader"]),
            Paragraph("Suggested action", styles["TableHeader"]),
        ]]


        for recommendation in recommendations:
            recommendation_rows.append([
                Paragraph(
                    escape(str(recommendation.get("area", ""))),
                    styles["SmallCell"],
                ),
                Paragraph(
                    escape(str(recommendation.get("priority", ""))),
                    styles["SmallCell"],
                ),
                Paragraph(
                    escape(str(recommendation.get("evidence", ""))),
                    styles["SmallCell"],
                ),
                Paragraph(
                    escape(str(recommendation.get("action", ""))),
                    styles["SmallCell"],
                ),
            ])


        add_table(
            recommendation_rows,
            [32 * mm, 22 * mm, 55 * mm, 55 * mm],
        )
    else:
        add_paragraph("No recommendations were generated for this dataset.")

    # ---------- ORIGINAL FEEDBACK APPENDIX ----------
    add_heading("6. Original feedback appendix")

    if "Feedback" in results_df.columns:
        feedback_rows = [[
            Paragraph("Feedback", styles["TableHeader"]),
            Paragraph("Sentiment", styles["TableHeader"]),
        ]]

        for _, row in results_df.iterrows():
            feedback_text = (
                ""
                if pd.isna(row.get("Feedback"))
                else str(row.get("Feedback"))
            )

            sentiment_text = (
                ""
                if pd.isna(row.get("Sentiment"))
                else str(row.get("Sentiment"))
            )

            feedback_rows.append([
                Paragraph(
                    escape(feedback_text).replace("\n", "<br/>"),
                    styles["SmallCell"],
                ),
                Paragraph(
                    escape(sentiment_text),
                    styles["SmallCell"],
                ),
            ])

        add_table(
            feedback_rows,
            [130 * mm, 35 * mm],
        )
    else:
        add_paragraph(
            "The original feedback column was not available for the appendix."
        )

    def add_page_number(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(muted)
        canvas.drawString(
            18 * mm,
            10 * mm,
            "FeedbackLens AI | Feedback Analysis Report",
        )
        canvas.drawRightString(
            landscape(A4)[0] - 18 * mm
            if document.pagesize == landscape(A4)
            else A4[0] - 18 * mm,
            10 * mm,
            f"Page {document.page}",
        )
        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
