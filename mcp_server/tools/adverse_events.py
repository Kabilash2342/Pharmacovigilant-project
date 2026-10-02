from database.connection import get_connection


def search_adverse_events(drug_name: str, adverse_event: str):
    """
    Search adverse-event cases for a given drug and adverse event.
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
            sc.outcome,
            ae.event_name,
            ae.severity
        FROM safety_cases sc
        JOIN drugs d
            ON sc.drug_id = d.drug_id
        JOIN patients p
            ON sc.patient_id = p.patient_id
        JOIN adverse_events ae
            ON sc.case_id = ae.case_id
        WHERE d.drug_name = ?
        AND ae.event_name = ?
        ORDER BY sc.report_date DESC;
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        query,
        (drug_name, adverse_event)
    )

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
            "outcome": row.outcome,
            "event_name": row.event_name,
            "severity": row.severity
        })

    cursor.close()
    connection.close()

    return results


if __name__ == "__main__":

    results = search_adverse_events(
        "Drug X",
        "Liver Injury"
    )

    for result in results:
        print(result)