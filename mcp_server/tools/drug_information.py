from database.connection import get_connection


def get_drug_information(drug_name: str):
    """
    Retrieve information about a drug from the database.
    """

    query = """
        SELECT
            drug_id,
            drug_name,
            generic_name,
            drug_class,
            indication,
            manufacturer,
            approval_date
        FROM drugs
        WHERE drug_name = ?;
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, (drug_name,))

    row = cursor.fetchone()

    if row is None:
        cursor.close()
        connection.close()

        return {
            "message": f"No information found for drug: {drug_name}"
        }

    result = {
        "drug_id": row.drug_id,
        "drug_name": row.drug_name,
        "generic_name": row.generic_name,
        "drug_class": row.drug_class,
        "indication": row.indication,
        "manufacturer": row.manufacturer,
        "approval_date": row.approval_date
    }

    cursor.close()
    connection.close()

    return result


if __name__ == "__main__":

    result = get_drug_information("Drug X")

    print(result)