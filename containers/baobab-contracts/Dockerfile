# ==============================================================================
# Baobab Platform Contracts — OCI Distribution Image
#
# This is NOT an application/runtime container.
#
# It is an immutable, language-neutral distribution artifact containing the
# canonical Baobab platform contracts.
#
# Runtime engines should normally consume generated language-specific packages.
# CI/CD, contract testing, SDK generation, conformance verification and
# infrastructure tooling may consume this OCI bundle directly.
# ==============================================================================

FROM scratch

ARG VERSION
ARG REVISION

LABEL org.opencontainers.image.title="Baobab Platform Contracts"
LABEL org.opencontainers.image.description="Canonical language-neutral contracts for the Baobab Platform"
LABEL org.opencontainers.image.source="https://github.com/nabhold/shared"
LABEL org.opencontainers.image.version="${VERSION}"
LABEL org.opencontainers.image.revision="${REVISION}"
LABEL org.opencontainers.image.vendor="Nabhold Group Africa"

# ---------------------------------------------------------------------------
# Canonical Baobab platform contracts
# ---------------------------------------------------------------------------

COPY contracts/ /baobab/contracts/

# Contract catalogue / lock manifest
COPY contracts.lock.yaml /baobab/contracts.lock.yaml

# ---------------------------------------------------------------------------
# Interface definitions used for language-specific generation
# ---------------------------------------------------------------------------

COPY packages/contracts/proto/ /baobab/interfaces/proto/
COPY packages/contracts/graphql/ /baobab/interfaces/graphql/
COPY packages/contracts/buf.yaml /baobab/interfaces/buf.yaml
COPY packages/contracts/buf.gen.yaml /baobab/interfaces/buf.gen.yaml

# ---------------------------------------------------------------------------
# Distribution documentation
# ---------------------------------------------------------------------------

COPY README.md /baobab/README.md
COPY LICENSE /baobab/LICENSE