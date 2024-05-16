mod channel;

use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
fn _lowlevel(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(channel::bounded, m)?)?;
    Ok(())
}
