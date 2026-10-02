from mcp.server.fastmcp import FastMCP

from mcp_server.tools.adverse_events import search_adverse_events
from mcp_server.tools.drug_information import get_drug_information
from mcp_server.tools.safety_database import query_safety_database
from mcp_server.tools.safety_analytics import safety_analytics
from mcp_server.tools.literature_search import search_clinical_literature


# Create MCP server
mcp = FastMCP("PharmaSafety MCP Server")


@mcp.tool()
def search_adverse_events_tool(
    drug_name: str,
    adverse_event: str
):
    """
    Search pharmacovigilance cases for a drug and adverse event.
    """

    return search_adverse_events(
        drug_name,
        adverse_event
    )


@mcp.tool()
def get_drug_information_tool(
    drug_name: str
):
    """
    Retrieve information about a drug.
    """

    return get_drug_information(
        drug_name
    )


@mcp.tool()
def query_safety_database_tool(
    drug_name: str | None = None,
    seriousness: str | None = None
):
    """
    Query safety cases using optional filters.
    """

    return query_safety_database(
        drug_name=drug_name,
        seriousness=seriousness
    )


@mcp.tool()
def safety_analytics_tool(
    drug_name: str
):
    """
    Generate safety statistics for a drug.
    """

    return safety_analytics(
        drug_name
    )


@mcp.tool()
def search_clinical_literature_tool(
    drug_name: str,
    safety_topic: str | None = None
):
    """
    Search clinical literature related to a drug.
    """

    return search_clinical_literature(
        drug_name,
        safety_topic
    )


if __name__ == "__main__":
    mcp.run()