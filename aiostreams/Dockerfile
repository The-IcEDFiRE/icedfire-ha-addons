# GitHub Actions pins this to the upstream image digest, not mutable latest.
ARG UPSTREAM_IMAGE=ghcr.io/viren070/aiostreams:latest
FROM ${UPSTREAM_IMAGE}

ARG BUILD_VERSION=1.0.0
ARG BUILD_ARCH=amd64
LABEL io.hass.version="${BUILD_VERSION}" \
      io.hass.type="app" \
      io.hass.arch="${BUILD_ARCH}"

COPY startup.mjs /app/startup.mjs
# Preserve upstream distroless Node entrypoint. This is interpreted by Node.
CMD ["/app/startup.mjs"]
