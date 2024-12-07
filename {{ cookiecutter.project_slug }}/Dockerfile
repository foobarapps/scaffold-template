FROM ghcr.io/astral-sh/uv:0.5.5-python3.12-bookworm-slim AS base

RUN apt update && \
    apt install -y curl git && \
    apt clean

ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.11/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=a2e2d47078a8dafc5949491e5ea7267cc721d67c

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

ARG USER_ID=10000
ARG GROUP_ID=10001
ARG USERNAME=user

RUN getent group $GROUP_ID || addgroup --gid $GROUP_ID $USERNAME
RUN id $USER_ID >/dev/null 2>&1 || adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID $USERNAME

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV UV_PROJECT_ENVIRONMENT=/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY --chown=$USER_ID:$GROUP_ID . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/venv/bin:$PATH"

RUN chown -R $USER_ID:$GROUP_ID /app /venv
USER $USER_ID:$GROUP_ID

FROM base AS dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM base
