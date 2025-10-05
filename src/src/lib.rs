use pyo3::prelude::*;
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// Almacenamiento en memoria global para Rust
type MemoryStore = Arc<Mutex<HashMap<String, String>>>;

lazy_static::lazy_static! {
    static ref MEMORY_STORE: MemoryStore = Arc::new(Mutex::new(HashMap::new()));
}

/// Almacena un valor en memoria
#[pyfunction]
fn memory_store(key: String, value: String) -> PyResult<bool> {
    let mut store = MEMORY_STORE.lock().unwrap();
    store.insert(key, value);
    Ok(true)
}

/// Recupera un valor de memoria
#[pyfunction]
fn memory_get(key: String) -> PyResult<Option<String>> {
    let store = MEMORY_STORE.lock().unwrap();
    Ok(store.get(&key).cloned())
}

/// Actualiza un valor en memoria
#[pyfunction]
fn memory_update(key: String, value: String) -> PyResult<bool> {
    let mut store = MEMORY_STORE.lock().unwrap();
    if store.contains_key(&key) {
        store.insert(key, value);
        Ok(true)
    } else {
        Ok(false)
    }
}

/// Elimina un valor de memoria
#[pyfunction]
fn memory_delete(key: String) -> PyResult<bool> {
    let mut store = MEMORY_STORE.lock().unwrap();
    Ok(store.remove(&key).is_some())
}

/// Obtiene todas las claves almacenadas
#[pyfunction]
fn memory_keys() -> PyResult<Vec<String>> {
    let store = MEMORY_STORE.lock().unwrap();
    Ok(store.keys().cloned().collect())
}

/// Obtiene el número de elementos almacenados
#[pyfunction]
fn memory_size() -> PyResult<usize> {
    let store = MEMORY_STORE.lock().unwrap();
    Ok(store.len())
}

/// Limpia toda la memoria
#[pyfunction]
fn memory_clear() -> PyResult<bool> {
    let mut store = MEMORY_STORE.lock().unwrap();
    store.clear();
    Ok(true)
}

/// Almacena múltiples valores de una vez
#[pyfunction]
fn memory_store_batch(items: Vec<(String, String)>) -> PyResult<usize> {
    let mut store = MEMORY_STORE.lock().unwrap();
    let count = items.len();
    for (key, value) in items {
        store.insert(key, value);
    }
    Ok(count)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rust_extension(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(memory_store, m)?)?;
    m.add_function(wrap_pyfunction!(memory_get, m)?)?;
    m.add_function(wrap_pyfunction!(memory_update, m)?)?;
    m.add_function(wrap_pyfunction!(memory_delete, m)?)?;
    m.add_function(wrap_pyfunction!(memory_keys, m)?)?;
    m.add_function(wrap_pyfunction!(memory_size, m)?)?;
    m.add_function(wrap_pyfunction!(memory_clear, m)?)?;
    m.add_function(wrap_pyfunction!(memory_store_batch, m)?)?;
    Ok(())
}
