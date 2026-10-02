from database.connection import get_connection


def query_safety_database(
    drug_name: str | None = None,
    seriousness: str | None = None
):
    """
    Query safety cases using optional drug and seriousness filters.
    """

    query = """
        SELECT
            sc.case_id,
            d.drug_name,
            p.age,
            p.sex,
            p.country,
            sc.report_date,
            sc.seriousness,
            sc.outcome
        FROM safety_cases sc
        JOIN drugs d
            ON sc.drug_id = d.drug_id
        JOIN patients p
            ON sc.patient_id = p.patient_id
        WHERE 1 = 1
    """

    parameters = []

    if drug_name:
        query += """
            AND d.drug_name = ?
        """
        parameters.append(drug_name)

    if seriousness:
        query += """
            AND sc.seriousness = ?
        """
        parameters.append(seriousness)

    query += """
        ORDER BY sc.report_date DESC;
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, parameters)

    rows = cursor.fetchall()

    results = []

    for row in rows:
        results.append({
            "case_id": row.case_id,
            "drug_name": row.drug_name,
            "age": row.age,
            "sex": row.sex,
            "country": row.country,
            "report_date": row.report_date,
            "seriousness": row.seriousness,
            "outcome": row.outcome
        })

    cursor.close()
    connection.close()

    return results


if __name__ == "__main__":

    results = query_safety_database(
        drug_name="Drug X",
        seriousness="Serious"
    )

    for result in results:
        print(result)