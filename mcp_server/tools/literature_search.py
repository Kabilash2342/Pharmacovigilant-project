from database.connection import get_connection


def search_clinical_literature(
    drug_name: str,
    safety_topic: str | None = None
):
    """
    Search clinical literature related to a drug
    and optionally a safety topic.
    """

    query = """
        SELECT
            literature_id,
            title,
            authors,
            journal,
            publication_year,
            doi,
            abstract_text,
            drug_name,
            safety_topic
        FROM literature
        WHERE drug_name = ?
    """

    parameters = [drug_name]

    if safety_topic:
        query += """
            AND safety_topic = ?
        """
        parameters.append(safety_topic)

    query += """
        ORDER BY publication_year DESC;
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, parameters)

    rows = cursor.fetchall()

    results = []

    for row in rows:
        results.append({
            "literature_id": row.literature_id,
            "title": row.title,
            "authors": row.authors,
            "journal": row.journal,
            "publication_year": row.publication_year,
            "doi": row.doi,
            "abstract": row.abstract_text,
            "drug_name": row.drug_name,
            "safety_topic": row.safety_topic
        })

    cursor.close()
    connection.close()

    return results


if __name__ == "__main__":

    results = search_clinical_literature(
        "Drug X",
        "Liver Injury"
    )

    for result in results:
        print(result)