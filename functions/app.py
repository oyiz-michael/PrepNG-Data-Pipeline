import os, csv
from datetime import datetime, timezone
import pymssql
import boto3

def lambda_handler(event, context):
    print("Starting handler")
    db_host = os.environ.get("DB_HOST")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")

    print(f"Connecting to {db_host}/{db_name}")
    conn = pymssql.connect(
        server=db_host,
        user=db_user,
        password=db_pass,
        database=db_name,
        port=1433,
        as_dict=True
    )
    print("Connected successfully")

    cur = conn.cursor()
    cur.execute("""
    SELECT TOP 50 
        p.BusinessEntityID,
        p.FirstName,
        p.LastName,
        ea.EmailAddress,
        ea.ModifiedDate
    FROM [Person].[Person] p
    INNER JOIN [Person].[EmailAddress] ea
        ON p.BusinessEntityID = ea.BusinessEntityID
    WHERE ea.ModifiedDate >= '2010-01-01'
    ORDER BY ea.ModifiedDate DESC;
    """)
    
    print("Query executed")
    rows = cur.fetchall()
    print(f"Fetched {len(rows)} rows")
    columns = [col[0] for col in cur.description]
    conn.close()

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"results_{timestamp}.csv"
    local_path = f"/tmp/{filename}"
    print(f"Writing CSV to {local_path}")

    with open(local_path, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print("Uploading file...")
    s3 = boto3.client('s3')
    bucket = os.environ.get('S3_BUCKET')
    prefix = os.environ.get('S3_KEY_PREFIX', 'query_results')
    s3.upload_file(local_path, bucket, f"{prefix}/{filename}")
    print("Upload successful")

    return {
        "statusCode": 200,
        "body": f"Uploaded {filename}"
    }
