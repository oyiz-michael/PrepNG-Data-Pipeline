python layers: https://github.com/keithrozario/Klayers/tree/master?tab=readme-ov-file


# SQL-to-S3 Dump Lambda

Runs a SQL query against our SQL Server, writes the results to a CSV in `/tmp`, and uploads the file to S3 for downstream processing.

---

## How it works
1. Lambda connects to the database with **pymssql** (layer: `Klayers-p312-pymssql`).
2. Executes the query you provide in `SQL_QUERY`.
3. Streams rows into a CSV file (`results_<UTC-timestamp>.csv`).
4. Uploads the file to **s3://$S3_BUCKET/$S3_KEY_PREFIX/**.

---

## Environment variables

| Var | Example | Purpose |
|-----|---------|---------|
| `DB_HOST` | `mydb.cluster-xyz.us-east-1.rds.amazonaws.com` | SQL Server host |
| `DB_USER` | `svc_reader` | DB login |
| `DB_PASS` | *secret* | DB password (store in console) |
| `DB_NAME` | `AdventureWorks2012` | Database name |
| `SQL_QUERY` | `SELECT TOP 100 * FROM dbo.Appointments` | Query to dump |
| `S3_BUCKET` | `preps-data-pipeline-s3` | Destination bucket |
| `S3_KEY_PREFIX` | `staging-daily` | Folder/prefix in S3 |

---

## IAM & networking
* **IAM** – execution role needs  
  `s3:PutObject` on `arn:aws:s3:::<bucket>/<prefix>/*`
* **VPC** – Lambda subnets must reach S3:  
  * NAT Gateway **or** S3 Gateway VPC Endpoint (recommended).
* Port **1433** open from Lambda SG to SQL Server SG.

---