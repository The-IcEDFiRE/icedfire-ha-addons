ARG UPSTREAM_IMAGE=ghcr.io/cedya77/aiometadata:latest
FROM ${UPSTREAM_IMAGE}
ARG BUILD_VERSION=0.0.0
ARG BUILD_ARCH=amd64
LABEL io.hass.version="${BUILD_VERSION}" io.hass.type="app" io.hass.arch="${BUILD_ARCH}"
COPY startup.mjs launcher.json /app/ha-launcher/
ENTRYPOINT ["node", "/app/ha-launcher/startup.mjs"]
CMD []
