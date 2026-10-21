ARG BUILD_FROM=node:22-bookworm-slim
FROM ${BUILD_FROM}
ARG UPSTREAM_SHA=unknown
ARG WRANGLER_VERSION=4.45.0
LABEL org.opencontainers.image.source="https://github.com/Br0ck25/My-Lists" \
      org.opencontainers.image.revision="${UPSTREAM_SHA}"
WORKDIR /srv/my-lists
RUN npm install --no-save --ignore-scripts --no-audit --no-fund "wrangler@${WRANGLER_VERSION}" && npm cache clean --force
COPY upstream/ /srv/my-lists/upstream/
COPY private_gateway.js /srv/my-lists/private_gateway.js
COPY run.sh /usr/local/bin/my-lists-run
RUN chmod 755 /usr/local/bin/my-lists-run && mkdir -p /data
EXPOSE 8787
CMD ["/usr/local/bin/my-lists-run"]
