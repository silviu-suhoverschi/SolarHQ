# Global ARG — must be before any FROM to be usable in FROM instructions
ARG BUILD_FROM

# Stage 1 — build frontend (forced amd64: rolldown has no armv7/musl native binding)
# hadolint ignore=DL3029
FROM --platform=linux/amd64 node:20-alpine AS frontend-builder
WORKDIR /build
COPY frontend/package.json frontend/vite.config.js ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2 — final image
# hadolint ignore=DL3006
FROM $BUILD_FROM

ARG BUILD_ARCH BUILD_DATE BUILD_DESCRIPTION BUILD_NAME BUILD_REF BUILD_REPOSITORY BUILD_VERSION

# Python deps
COPY backend/requirements.txt /app/backend/
# hadolint ignore=DL3018
RUN apk add --no-cache --virtual .build-deps build-base libffi-dev rust cargo \
    && pip3 install --no-cache-dir -r /app/backend/requirements.txt \
    && apk del .build-deps

# App code
COPY backend/ /app/backend/
COPY --from=frontend-builder /static/ /app/static/

# s6-overlay scripts
COPY rootfs /
RUN chmod a+x /usr/bin/solarhq-*

EXPOSE 8099

LABEL \
    maintainer="Silviu Suhoverschi <silviu.suhoverschi@gmail.com>" \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version="${BUILD_VERSION}" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.revision="${BUILD_REF}" \
    org.opencontainers.image.version="${BUILD_VERSION}"
