# python-maturin
Examples with python and rust using maturin


# Ejecución
```bash
docker run -v $(pwd):/app python-maturin bash -c "cd src && maturin build --release && pip install target/wheels/rust_extension-0.1.0-cp311-cp311-manylinux_2_34_aarch64.whl && cd ../performance-python && python main.py"
```
