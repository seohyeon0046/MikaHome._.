# Cross-platform option: docker build -t falx-deck . && docker run --rm -p 5050:5050 falx-deck
FROM python:3.8-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends git r-base-core \
      r-cran-tidyr r-cran-dplyr r-cran-ggplot2 r-cran-svglite \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY server/requirements.txt server/requirements.txt
RUN pip install --no-cache-dir -r server/requirements.txt
RUN git clone --quiet https://github.com/Mestway/falx.git vendor/falx \
    && git -C vendor/falx checkout --quiet fcae5e536f44c19780ae9f00b94e397723924757
COPY . .
EXPOSE 5050
CMD ["python", "server/app.py", "--host", "0.0.0.0", "--port", "5050"]
