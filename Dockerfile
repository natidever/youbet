
# Install system dependencies
FROM python:3.12-slim



#The following configurations are to install the UV

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY . /app 
RUN uv pip install --system -e .

# RUN uv sync --frozen --no-cache


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
























