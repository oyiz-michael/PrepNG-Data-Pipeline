import pymssql, os

def lambda_handler(event, _):
    conn = pymssql.connect(
        server   = os.getenv("DB_HOST"),
        user     = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        database = os.getenv("DB_NAME"),
        port     = 1433,
        as_dict  = True
    )
    cur = conn.cursor()
    cur.execute("SELECT @@VERSION AS version")
    row = cur.fetchone()
    conn.close()
    return row