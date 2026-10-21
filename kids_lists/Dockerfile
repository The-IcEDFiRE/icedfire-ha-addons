FROM python:3.12-alpine
ARG BUILD_VERSION=0.1.0
ARG BUILD_ARCH=amd64
LABEL io.hass.version="${BUILD_VERSION}" io.hass.type="app" io.hass.arch="${BUILD_ARCH}"
WORKDIR /opt/kids-lists
COPY app.py run.sh ./
RUN chmod +x run.sh && mkdir -p /data
EXPOSE 8099
CMD ["./run.sh"]
