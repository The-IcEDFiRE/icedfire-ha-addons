ARG UPSTREAM_IMAGE=ghcr.io/sonicx161/aiomanager:latest
FROM ${UPSTREAM_IMAGE}
ARG BUILD_VERSION=0.0.0
ARG BUILD_ARCH=amd64
LABEL io.hass.version="${BUILD_VERSION}" io.hass.type="app" io.hass.arch="${BUILD_ARCH}"
COPY startup.mjs launcher.json /app/ha-launcher/
CMD ["/app/ha-launcher/startup.mjs"]
