#!/bin/bash

echo "=== Compilando extensión Rust con maturin ==="
cd src
maturin build --release

echo "=== Instalando extensión compilada ==="
pip install target/wheels/rust_extension-0.1.0-cp311-cp311-manylinux_2_34_aarch64.whl

echo "=== Ejecutando ejemplo Python ==="
cd ../performance-python
python main.py
