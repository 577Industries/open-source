FROM python:3.12-slim

LABEL org.opencontainers.image.title="Forge Evolve Reference Engine" \
      org.opencontainers.image.vendor="577 Industries Inc." \
      org.opencontainers.image.authors="Thomas G. Waweru <info@577industries.com>" \
      org.opencontainers.image.url="https://www.577industries.com/evolve" \
      org.opencontainers.image.source="https://github.com/577Industries/forge-evolve-reference"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg

WORKDIR /app

COPY requirements.txt pyproject.toml README.md ./
COPY forge_evolve_engine.py run_adversarial_benchmarks.py ./
COPY forge_evolve/ ./forge_evolve/
COPY schemas/ ./schemas/
COPY benchmarks/ ./benchmarks/
COPY figures/ ./figures/
COPY tests/ ./tests/

RUN pip install --no-cache-dir -e . && \
    pytest -v

ENTRYPOINT ["forge-evolve"]
CMD ["benchmark", "--suite", "nist-mbe"]
