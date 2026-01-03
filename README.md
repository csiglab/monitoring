# Monitoring Sample System

> ...

## Fluent Bit

```bash
# docker run -it --rm \
#   -v $(pwd)/fluent-bit:/fluent-bit/etc \
#   -v /home/dbremont/Code/local-experiments/py-monitoring:/logs:ro \
#   -v fluentbit-state:/fluent-bit/state \
#   fluent/fluent-bit:3.0.4 \
#   -c /fluent-bit/etc/fluent-bit.conf
```

`docker compose up -d`

`docker exec -it clickhouse clickhouse-client`

`docker exec -it clickhouse clickhouse-client --user=admin --password=admi`

`docker compose logs -f fluent-bit`

`docker compose logs -f clickhouse`

docker compose down

docker compose up -d

docker compose logs -f fluent-bit

Table:

```bash
CREATE DATABASE IF NOT EXISTS logs;

```

```sql
CREATE TABLE IF NOT EXISTS logs.app_logs
(
    ts        DateTime DEFAULT now(),
    log_tag   String,
    message   String
)
ENGINE = MergeTree
ORDER BY ts;
```

```sql

SHOW DATABASES;

SELECT *
FROM logs.app_logs
ORDER BY ts DESC
LIMIT 10;
```


```bash
curl -sS -X POST 'http://localhost:8123/?query=INSERT%20INTO%20logs.app_logs%20FORMAT%20JSONEachRow' \                                      [16:26:04]
--data-binary '{"ts":"2026-01-01 21:00:00","log_tag":"test","message":"hello world"}'

```



```sql
CREATE USER IF NOT EXISTS fluentbit IDENTIFIED WITH plaintext_password BY 'fluentbitpass';
GRANT ALL ON logs.* TO fluentbit;
```