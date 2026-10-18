# Optional data services

Install Redis and/or PostgreSQL only when the AIO app actually uses that backend.

**Redis:** [Installation and connection guide](redis/DOCS.md).

**PostgreSQL 17:** [Installation, connection, backup and major-upgrade guide](postgresql/DOCS.md).

Both apps default to **no host port exposure**. Retrieve the internal DNS hostname from the installed app information and put the correct connection URL into the consuming AIO app's Configuration tab. Neither service is automatically configured as a dependency.
