from database.DB_connect import DBConnect
from model.rifugio import Rifugio


class DAO:
    @staticmethod
    def get_all_rifugi():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM rifugio"
        cursor.execute(query)

        for row in cursor:
            r = Rifugio(
                id=row["id"],
                nome=row["nome"],
                localita=row["localita"],
                altitudine=row["altitudine"],
                capienza=row["capienza"],
                aperto=row["aperto"]
            )
            result.append(r)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edges_by_year(year):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT id_rifugio1, id_rifugio2, distanza, difficolta
                FROM connessione
                WHERE anno <= %s
                """
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result