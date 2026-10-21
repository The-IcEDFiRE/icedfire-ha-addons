ARG BUILD_FROM=node:22-bookworm-slim
FROM ${BUILD_FROM}
ARG UPSTREAM_SHA=unknown
ARG WRANGLER_VERSION=4.45.0
LABEL org.opencontainers.image.source="https://github.com/Br0ck25/My-Lists" \
      org.opencontainers.image.revision="${UPSTREAM_SHA}"
# Keep a current trusted CA bundle available to Node, Wrangler and workerd.
# Do not disable TLS certificate verification.
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
WORKDIR /srv/my-lists
RUN npm install --no-save --ignore-scripts --no-audit --no-fund "wrangler@${WRANGLER_VERSION}" && npm cache clean --force
COPY upstream/ /srv/my-lists/upstream/
COPY private_gateway.js /srv/my-lists/private_gateway.js
COPY run.sh /usr/local/bin/my-lists-run
RUN chmod 755 /usr/local/bin/my-lists-run && mkdir -p /data
EXPOSE 8787
CMD ["/usr/local/bin/my-lists-run"]
