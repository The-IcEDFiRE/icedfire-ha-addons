ARG UPSTREAM_IMAGE=redis:7.4-bookworm
FROM ${UPSTREAM_IMAGE}
ARG BUILD_VERSION=0.0.0
ARG BUILD_ARCH=amd64
USER root
RUN apt-get update && apt-get install -y --no-install-recommends jq && rm -rf /var/lib/apt/lists/*
COPY run.sh /usr/local/bin/ha-service-start
RUN chmod 755 /usr/local/bin/ha-service-start
LABEL io.hass.version="${BUILD_VERSION}" io.hass.type="app" io.hass.arch="${BUILD_ARCH}"
ENTRYPOINT ["/usr/local/bin/ha-service-start"]
