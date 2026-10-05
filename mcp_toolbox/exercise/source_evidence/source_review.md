# MCP Toolbox source review

Verified 2026-10-05 UTC. This review distinguishes current source, a released runtime, historical link mapping, and actual execution.

## Pins and provenance

- Official repository: https://github.com/googleapis/mcp-toolbox (README confirms rename from googleapis/genai-toolbox)
- Default-branch snapshot: a24e5e68567fa014a42fc6cc711faa82b964d4c0, commit dated 2026-10-02
- Runtime tag: v1.13.1 → e14cda6b4f483e6b5e5ec23e342f9f232a6ce60f
- Official binary URL is in the pinned README: https://storage.googleapis.com/mcp-toolbox-for-databases/v1.13.1/linux/amd64/toolbox
- Observed version: 1.13.1+binary.linux.amd64.e14cda6
- Measured SHA-256: d8e0df24b5ce9934c8f7ae8466f64ff5512857c5a7e47640301750ee82f92db3. This is a hash calculated from the downloaded official bytes, not an independently published checksum or signature
- Source_manifest.json verifies 23 release-file copies by Git blob identity and SHA-256, and compares each with the main pin. Of these selected files, go.mod and BigQuery execute implementation differ; relevant SQLite, common annotations, toolsets/groups and security documentation match exactly
- Apache-2.0 LICENSE is retained both with source copies and exercise

## Source-to-tool mechanism

1. A source establishes database connection details. SQLite config has name/type/database/sqlCommenter; it has no readOnly field
2. SQLite passes database directly into sql.Open("sqlite", dbPath), using modernc.org/sqlite. It fixes MaxOpenConns=1 and MaxIdleConns=1
3. sqlite-execute-sql accepts an arbitrary non-empty SQL string and invokes source.RunSQL. No SQL-keyword blacklist is present
4. sqlite-sql resolves templateParameters into SQL text, then passes ordinary parameters as driver arguments to QueryContext. Only the latter is value binding
5. Toolsets group tools; current release/main documentation loads legacy toolsets as tools-only groups. The default group includes all configured primitives. A selected client subset does not create database permissions
6. SQLite IsReadOnly() returns false regardless of URI. Its SQL tools default to destructive/readOnlyHint=false unless explicitly annotated

Pinned evidence paths:
- internal/sources/sqlite/sqlite.go
- internal/tools/sqlite/sqliteexecutesql/sqliteexecutesql.go
- internal/tools/sqlite/sqlitesql/sqlitesql.go
- internal/prebuiltconfigs/tools/sqlite.yaml
- internal/tools/tools.go
- docs/en/documentation/configuration/{toolsets,groups}/_index.md

## Three distinct boundaries

- Protocol hint: readOnlyHint describes expected behavior. MCP explicitly says ToolAnnotations are hints and can be unfaithful. A hint does not independently constrain DB permissions
- DB/driver boundary: an account's grants, a native session restriction, or an actual SQLite file URI mode=ro can reject writes to the object covered by that boundary. Different engines and privileges are not interchangeable
- Toolbox readOnly coordination: where implemented, source.IsReadOnly affects annotation calculation and suppresses tools that explicitly advertise readOnlyHint=false. In common ShouldSuppress, nil/unannotated tools are warned about rather than automatically suppressed

The official broad read-only guide's matrix currently lists Cloud SQL Postgres, AlloyDB Postgres, Cloud SQL MySQL and BigQuery. It does not list SQLite or generic Postgres. This experiment does not extrapolate support.

Static mechanisms, not exercised against managed databases:
- Cloud SQL Postgres: DSN option cloudsql_session_read_only=locked
- AlloyDB Postgres: DSN option alloydb_session_read_only=locked; unsupported server version causes an initialization error
- Cloud SQL MySQL: driver connectionAttributes includes read_only_connection:true
- BigQuery: source readOnly coordinates writeMode; execute-sql performs a server dry run and checks statement type. blocked permits SELECT, protected is a separate temporary-session-write mode

Important BigQuery nuance: the source docs state protected permits temporary writes, classifies the source as read-only at the Toolbox layer, and does not apply the same writeMode restrictions to every tool such as bigquery-sql/forecast/analyze-contribution. Therefore do not paraphrase readOnlyHint as a universal guarantee of zero side effects. The restricted exercise makes no BigQuery security or runtime claim.

## Prebuilt use and production limits

The prebuilt-configs page warns these generic tools are for trusted development exploration, not arbitrary untrusted production users. Dynamic SQL requires a dedicated least-privilege database identity and native controls; parameterized custom tools are preferable for fixed workflows. DB read-only and client hints also do not prevent confidentiality loss from excessive read access.

## Genuine runtime exercise

The official downloaded binary actually handled MCP stdio requests. Python is only the fixture/client, not a mock of Toolbox. The initial run completed 26/26 checks; reviewer has independently rerun it and run separate CLI checks. Runtime evidence is in exercise/evidence and reviewer-owned qa directories.

Observed: prebuilt tool discovery, successful reads, mode=ro denial of main-DB INSERT/UPDATE/DELETE/DDL and a query_only reset chain, unchanged main database hash, successful parameter binding, typed parameter error, unknown tool -32602, writable control mutation despite a false readOnlyHint=true, and startup rejection of SQLite readOnly:true.

All SQL and DB content are synthetic. No real accounts, credentials, paid APIs, cloud databases or global MCP settings were used. Commands use stdio, --disable-version-check, --disable-reload, no telemetry exporter and a minimal environment. This is not an OS network sandbox claim.

The unknown-tool case tests an unconfigured name. It does not demonstrate named HTTP endpoint membership enforcement or OAuth/user authorization. mode=ro constrains the opened main database, not every temporary/attached database or the whole process. This is a small targeted regression experiment, not exhaustive adversarial security certification.

## Exact X link

https://x.com/denziideng/status/2104867878055084282 was opened once with cloud web retrieval and returned Internal Error. No post body/outlinks were retrieved, and no alternate access or bypass route was used. Parent supplied a previously verified Windows outlink mapping; that historical mapping must not be presented as a successful new cloud reading. Original social claim is therefore not independently revalidated in this run.

## Additional official references

- https://mcp-toolbox.dev/documentation/configuration/prebuilt-configs/
- https://mcp-toolbox.dev/documentation/configuration/security/read-only/
- https://mcp-toolbox.dev/integrations/sqlite/source/
- https://www.sqlite.org/uri.html (file: URI and mode=ro)
- https://modelcontextprotocol.io/specification/2025-06-18/schema#toolannotations (hint semantics)
- https://pkg.go.dev/modernc.org/sqlite (driver URI documentation, current page; runtime behavior verified against pinned binary rather than inferred from an unpinned package page)
