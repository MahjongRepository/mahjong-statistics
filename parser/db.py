import bz2
import sqlite3
from typing import Optional


def load_logs_from_db(db_path: str, limit: Optional[int] = None, offset: Optional[int] = None):
    """
    Load logs from db and decompress logs content.
    How to download games content you can learn there: https://github.com/MahjongRepository/phoenix-logs
    """
    connection = sqlite3.connect(db_path)

    if not offset:
        offset = 0

    with connection:
        cursor = connection.cursor()
        if limit is None:
            cursor.execute("SELECT log_id, log_content FROM logs where is_sanma = 0 ORDER BY date DESC;")
        else:
            cursor.execute(
                "SELECT log_id, log_content FROM logs where is_sanma = 0 ORDER BY date LIMIT ? OFFSET ?;",
                [limit, offset],
            )
            # cursor.execute('SELECT log_id, log_content FROM logs where log_id = "2018050310gm-00a9-0000-786296ec";')
        data = cursor.fetchall()

    results = []
    for x in data:
        log_id = x[0]
        try:
            results.append({"log_id": log_id, "log_content": bz2.decompress(x[1]).decode("utf-8")})
        except:
            print(log_id)

    return results
