# Usar imagen base oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar Rust y Python
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar Rust (necesario para maturin)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Instalar herramientas de desarrollo útiles
RUN apt-get update && apt-get install -y \
    git \
    vim \
    nano \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de configuración primero (para aprovechar la caché de Docker)
COPY requirements.txt ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Construir la extensión de Python con maturin (si existe Cargo.toml)
RUN if [ -f Cargo.toml ]; then maturin develop --release; fi

# Exponer puerto (ajusta según tu aplicación)
EXPOSE 8000

# Comando por defecto
CMD ["python", "-m", "http.server", "8000"]
