#!/usr/bin/env python3
"""
Ejemplo de uso de funciones Rust compiladas con maturin
Incluye funciones de almacenamiento en memoria y benchmarks
"""

import time
from typing import Dict, List, Optional, Tuple

# Importar el módulo Rust compilado
import rust_extension


class PythonMemoryStore:
    """Almacenamiento en memoria implementado en Python"""

    def __init__(self):
        self._store: Dict[str, str] = {}

    def store(self, key: str, value: str) -> bool:
        """Almacena un valor en memoria"""
        self._store[key] = value
        return True

    def get(self, key: str) -> Optional[str]:
        """Recupera un valor de memoria"""
        return self._store.get(key)

    def update(self, key: str, value: str) -> bool:
        """Actualiza un valor en memoria"""
        if key in self._store:
            self._store[key] = value
            return True
        return False

    def delete(self, key: str) -> bool:
        """Elimina un valor de memoria"""
        if key in self._store:
            del self._store[key]
            return True
        return False

    def keys(self) -> List[str]:
        """Obtiene todas las claves almacenadas"""
        return list(self._store.keys())

    def size(self) -> int:
        """Obtiene el número de elementos almacenados"""
        return len(self._store)

    def clear(self) -> bool:
        """Limpia toda la memoria"""
        self._store.clear()
        return True

    def store_batch(self, items: List[Tuple[str, str]]) -> int:
        """Almacena múltiples valores de una vez"""
        for key, value in items:
            self._store[key] = value
        return len(items)


def benchmark_memory_operations():
    """Benchmark de operaciones de memoria entre Rust y Python"""
    print("\n" + "=" * 60)
    print("BENCHMARK DE OPERACIONES DE MEMORIA")
    print("=" * 60)

    # Inicializar almacenamientos
    python_store = PythonMemoryStore()

    # Limpiar almacenamiento Rust
    rust_extension.memory_clear()

    # Datos de prueba
    test_data = [(f"key_{i}", f"value_{i}") for i in range(1000)]

    # Benchmark: Almacenamiento individual
    print("\n--- Almacenamiento Individual (1000 operaciones) ---")

    # Python
    start_time = time.time()
    for key, value in test_data:
        python_store.store(key, value)
    python_store_time = time.time() - start_time

    # Rust
    start_time = time.time()
    for key, value in test_data:
        rust_extension.memory_store(key, value)
    rust_store_time = time.time() - start_time

    print(f"Python: {python_store_time:.4f} segundos")
    print(f"Rust:   {rust_store_time:.4f} segundos")
    print(f"Rust es {python_store_time / rust_store_time:.2f}x más rápido")

    # Benchmark: Lectura
    print("\n--- Lectura (1000 operaciones) ---")

    # Python
    start_time = time.time()
    for key, _ in test_data:
        python_store.get(key)
    python_get_time = time.time() - start_time

    # Rust
    start_time = time.time()
    for key, _ in test_data:
        rust_extension.memory_get(key)
    rust_get_time = time.time() - start_time

    print(f"Python: {python_get_time:.4f} segundos")
    print(f"Rust:   {rust_get_time:.4f} segundos")
    print(f"Rust es {python_get_time / rust_get_time:.2f}x más rápido")

    # Benchmark: Almacenamiento en lote
    print("\n--- Almacenamiento en Lote (1000 elementos) ---")

    # Python
    start_time = time.time()
    python_store.store_batch(test_data)
    python_batch_time = time.time() - start_time

    # Rust
    rust_extension.memory_clear()  # Limpiar antes del test
    start_time = time.time()
    rust_extension.memory_store_batch(test_data)
    rust_batch_time = time.time() - start_time

    print(f"Python: {python_batch_time:.4f} segundos")
    print(f"Rust:   {rust_batch_time:.4f} segundos")
    print(f"Rust es {python_batch_time / rust_batch_time:.2f}x más rápido")

    # Verificar tamaños
    print(f"\nElementos en Python: {python_store.size()}")
    print(f"Elementos en Rust: {rust_extension.memory_size()}")


def demo_memory_functions():
    """Demostración de las funciones de memoria"""
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN DE FUNCIONES DE MEMORIA")
    print("=" * 60)

    # Limpiar memoria Rust
    rust_extension.memory_clear()

    print("\n--- Operaciones básicas ---")

    # Almacenar
    rust_extension.memory_store("nombre", "Juan")
    rust_extension.memory_store("edad", "25")
    rust_extension.memory_store("ciudad", "Madrid")

    print(f"Elementos almacenados: {rust_extension.memory_size()}")
    print(f"Claves: {rust_extension.memory_keys()}")

    # Leer
    nombre = rust_extension.memory_get("nombre")
    edad = rust_extension.memory_get("edad")
    print(f"Nombre: {nombre}")
    print(f"Edad: {edad}")

    # Actualizar
    rust_extension.memory_update("edad", "26")
    nueva_edad = rust_extension.memory_get("edad")
    print(f"Edad actualizada: {nueva_edad}")

    # Eliminar
    rust_extension.memory_delete("ciudad")
    print(f"Elementos después de eliminar ciudad: {rust_extension.memory_size()}")

    print("\n--- Almacenamiento en lote ---")
    datos_lote = [
        ("producto1", "laptop"),
        ("producto2", "mouse"),
        ("producto3", "teclado"),
        ("producto4", "monitor"),
    ]

    elementos_insertados = rust_extension.memory_store_batch(datos_lote)
    print(f"Elementos insertados en lote: {elementos_insertados}")
    print(f"Total de elementos: {rust_extension.memory_size()}")


def benchmark_sum_function():
    """Benchmark de la función sum original"""
    print("\n" + "=" * 60)
    print("BENCHMARK DE FUNCIÓN SUM")
    print("=" * 60)

    def sum_as_string_python(a: int, b: int) -> str:
        return str(a + b)

    # Test de rendimiento
    a, b = 1000, 2000

    # Medir tiempo Rust
    start_time = time.time()
    for _ in range(10000000):
        rust_extension.sum_as_string(a, b)
    rust_time = time.time() - start_time

    # Medir tiempo Python
    start_time = time.time()
    for _ in range(10000000):
        sum_as_string_python(a, b)
    python_time = time.time() - start_time

    print(f"Rust (10,000,000 iteraciones): {rust_time:.4f} segundos")
    print(f"Python (10,000,000 iteraciones): {python_time:.4f} segundos")
    print(f"Rust es {python_time / rust_time:.2f}x más rápido")


def main():
    """Función principal que demuestra todas las funcionalidades"""

    print("🚀 EJEMPLO DE USO DE FUNCIONES RUST DESDE PYTHON")
    print("=" * 60)

    # Función original
    resultado = rust_extension.sum_as_string(5, 10)
    print(f"sum_as_string(5, 10) = {resultado}")

    # Demostración de funciones de memoria
    demo_memory_functions()

    # Benchmarks
    benchmark_sum_function()
    benchmark_memory_operations()

    print("\n" + "=" * 60)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 60)


if __name__ == "__main__":
    main()
