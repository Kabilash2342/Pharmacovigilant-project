from database.connection import get_connection


def safety_analytics(drug_name: str):
    """
    Generate safety statistics for a specific drug.
    """

    query = """
        SELECT
            COUNT(DISTINCT sc.case_id) AS total_cases,

            COUNT(
                DISTINCT CASE
                    WHEN sc.seriousness = 'Serious'
                    THEN sc.case_id
                END
            ) AS serious_cases,

            COUNT(
                DISTINCT CASE
                    WHEN sc.outcome = 'Fatal'
                    THEN sc.case_id
                END
            ) AS fatal_cases,

            COUNT(ae.event_id) AS total_adverse_events

        FROM safety_cases sc

        JOIN drugs d
            ON sc.drug_id = d.drug_id

        LEFT JOIN adverse_events ae
            ON sc.case_id = ae.case_id

        WHERE d.drug_name = ?;
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, (drug_name,))

    row = cursor.fetchone()

    result = {
        "drug_name": drug_name,
        "total_cases": row.total_cases,
        "serious_cases": row.serious_cases,
        "fatal_cases": row.fatal_cases,
        "total_adverse_events": row.total_adverse_events
    }

    cursor.close()
    connection.close()

    return result


if __name__ == "__main__":

    result = safety_analytics("Drug X")

    print(result)