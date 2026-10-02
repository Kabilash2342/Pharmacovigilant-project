from mcp_server.tools.adverse_events import search_adverse_events
from mcp_server.tools.drug_information import get_drug_information
from mcp_server.tools.safety_database import query_safety_database
from mcp_server.tools.safety_analytics import safety_analytics
from mcp_server.tools.literature_search import search_clinical_literature


print("\n--- 1. ADVERSE EVENTS ---")

result = search_adverse_events(
    "Drug X",
    "Liver Injury"
)

print(result)


print("\n--- 2. DRUG INFORMATION ---")

result = get_drug_information(
    "Drug X"
)

print(result)


print("\n--- 3. SAFETY DATABASE ---")

result = query_safety_database(
    drug_name="Drug X",
    seriousness="Serious"
)

print(result)


print("\n--- 4. SAFETY ANALYTICS ---")

result = safety_analytics(
    "Drug X"
)

print(result)


print("\n--- 5. CLINICAL LITERATURE ---")

result = search_clinical_literature(
    "Drug X",
    "Liver Injury"
)

print(result)