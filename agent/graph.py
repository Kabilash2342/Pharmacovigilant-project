import asyncio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

load_dotenv()


# ============================================
# 1. MCP CLIENT
# ============================================

mcp_client = MultiServerMCPClient(
    {
        "pharma_safety": {
            "transport": "stdio",
            "command": "python",
            "args": ["-m", "mcp_server.server"],
        }
    }
)


# ============================================
# 2. LLM
# ============================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# ============================================
# 3. SYSTEM PROMPT
# ============================================

SYSTEM_PROMPT = """
You are a Pharmacovigilance Safety Investigation Assistant.

Your job is to investigate drug safety questions using ONLY information
returned by the available tools.

IMPORTANT RULES:

1. Never invent patient information, adverse events, outcomes,
   drug properties, clinical details, or literature findings.

2. Do not assume information that is not present in the tool results.

3. Every factual claim about a safety case must be supported by
   retrieved data.

4. If the available data does not contain enough information to answer
   a question, explicitly say that the available data is insufficient.

5. Clearly distinguish:
   - Retrieved facts
   - Calculated statistics
   - Interpretation

6. You may calculate simple statistics from retrieved records.

7. Do not claim causality from spontaneous adverse-event reports.

8. Do not provide patient-specific medical advice.

9. Mention important limitations of the available dataset.

10. Prioritize evidence and accuracy over completeness.
"""
# ============================================
# CREATE LANGGRAPH AGENT
# ============================================



# ============================================
# 4. CREATE AGENT
# ============================================
async def generate_safety_report(messages):
    """
    Generate a structured Safety Investigation Report
    from the evidence collected by the agent.
    """

    report_prompt = """
You are a Pharmacovigilance Safety Report Generator.

Create a structured Safety Investigation Report using ONLY
the evidence contained in the conversation and tool results.

Do not invent facts.

Do not provide patient-specific medical advice.

Do not claim that a drug causes an adverse event based only
on spontaneous reports.

Clearly distinguish retrieved facts, calculated statistics,
literature findings, and interpretation.

Use exactly this structure:

# SAFETY INVESTIGATION REPORT

## 1. Investigation Overview
- Drug
- Safety concern
- Investigation objective

## 2. Drug Information
Summarize only information retrieved from the database.

## 3. Adverse Event Case Evidence
Include:
- Number of cases
- Case IDs
- Seriousness
- Severity
- Patient demographics
- Countries
- Outcomes
- Relevant dates

## 4. Safety Analytics
Include calculated statistics such as:
- Total cases
- Serious cases
- Fatal cases
- Outcome distribution
- Age statistics

## 5. Clinical Literature Evidence
Summarize the relevant literature retrieved by the literature tool.

## 6. Safety Signal Interpretation
Explain what the retrieved evidence suggests.
Do not claim causality.

## 7. Data Limitations
Mention limitations such as:
- Small sample size
- Missing denominator
- Under-reporting
- Missing clinical information
- Lack of causal evidence

## 8. Investigation Summary
Provide a concise evidence-based summary.

Important:
Do not add clinical recommendations unless they are explicitly
supported by retrieved evidence.
"""

    messages_for_report = [
        {
            "role": "system",
            "content": report_prompt
        }
    ]

    for message in messages:
        if hasattr(message, "content"):
            messages_for_report.append(
                {
                    "role": "user",
                    "content": str(message.content)
                }
            )

    report = await llm.ainvoke(messages_for_report)

    return report.content

def save_report(report):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"safety_investigation_{timestamp}.md"

    filepath = reports_dir / filename

    filepath.write_text(
        report,
        encoding="utf-8"
    )

    return filepath
def generate_pdf_report(report, markdown_path):
    """
    Convert the safety investigation Markdown report
    into a formatted PDF.
    """

    pdf_path = markdown_path.with_suffix(".pdf")

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    body_style = styles["BodyText"]
    body_style.leading = 14

    table_header_style = styles["BodyText"]
    table_header_style.fontName = "Helvetica-Bold"

    story = []

    lines = report.splitlines()

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        # Empty line
        if not line:
            story.append(
                Spacer(1, 8)
            )

            i += 1
            continue

        # Main title
        if line.startswith("# "):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    text,
                    title_style
                )
            )

            story.append(
                Spacer(1, 15)
            )

            i += 1
            continue

        # Section heading
        if line.startswith("## "):

            text = line[3:].strip()

            story.append(
                Paragraph(
                    text,
                    heading_style
                )
            )

            story.append(
                Spacer(1, 6)
            )

            i += 1
            continue

        # Markdown table
        if line.startswith("|"):

            table_data = []

            # Read all table rows
            while i < len(lines):

                current = lines[i].strip()

                if not current.startswith("|"):
                    break

                # Ignore markdown separator row
                if set(
                    current.replace("|", "").replace("-", "").replace(":", "").replace(" ", "")
                ) == set():

                    i += 1
                    continue

                cells = [
                    cell.strip()
                    for cell in current.strip("|").split("|")
                ]

                table_data.append(cells)

                i += 1

            if table_data:

                # Convert cells into Paragraphs
                formatted_data = []

                for row_index, row in enumerate(table_data):

                    formatted_row = []

                    for cell in row:

                        style = (
                            table_header_style
                            if row_index == 0
                            else body_style
                        )

                        formatted_row.append(
                            Paragraph(cell, style)
                        )

                    formatted_data.append(formatted_row)

                table = Table(
                    formatted_data,
                    repeatRows=1,
                    hAlign="LEFT"
                )

                table.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, 0),
                                colors.lightgrey
                            ),
                            (
                                "TEXTCOLOR",
                                (0, 0),
                                (-1, 0),
                                colors.black
                            ),
                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.5,
                                colors.grey
                            ),
                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "TOP"
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                6
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                5
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                5
                            ),
                        ]
                    )
                )

                story.append(table)

                story.append(
                    Spacer(1, 12)
                )

                continue

        # Bullet point
        if line.startswith("- "):

            text = line[2:].strip()

            story.append(
                Paragraph(
                    "• " + text,
                    body_style
                )
            )

            i += 1
            continue

        # Normal paragraph
        story.append(
            Paragraph(
                line,
                body_style
            )
        )

        i += 1

    doc.build(story)

    return pdf_path
async def investigate(
    agent,
    user_input,
    thread_id="streamlit-session"
):
    """
    Run one conversational turn.
    """

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config=config
    )

    response = result["messages"][-1].content

    return response
async def create_pharma_agent():

    tools = await mcp_client.get_tools()

    memory = InMemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=memory
    )

    return agent


async def create_agent():
    tools = await mcp_client.get_tools()

    memory = InMemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=memory
    )

    return agent
async def create_pharma_agent():

    tools = await mcp_client.get_tools()

    memory = InMemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=memory
    )

    return agent
async def main():

    # Create MCP tools
    tools = await mcp_client.get_tools()

    # Create memory
    memory = InMemorySaver()

    # Create agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=memory
    )

    config = {
        "configurable": {
            "thread_id": "pharma-investigation-1"
        }
    }

    print("\n--------------------------------")
    print("PharmaSafety Conversational Agent")
    print("--------------------------------")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("\nAgent: Goodbye!")
            break

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            },
            config=config
        )

        response = result["messages"][-1].content

        print("\nAgent:", response)
 

if __name__ == "__main__":
    asyncio.run(main())