# Stage 1 — build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /build
COPY frontend/package*.json frontend/vite.config.js frontend/tailwind.config.js ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2 — final image
ARG BUILD_FROM
FROM $BUILD_FROM

ARG BUILD_ARCH BUILD_DATE BUILD_DESCRIPTION BUILD_NAME BUILD_REF BUILD_REPOSITORY BUILD_VERSION

# Python deps
COPY backend/requirements.txt /app/backend/
RUN pip3 install --no-cache-dir -r /app/backend/requirements.txt

# App code
COPY backend/ /app/backend/
COPY --from=frontend-builder /build/dist/ /app/static/

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
