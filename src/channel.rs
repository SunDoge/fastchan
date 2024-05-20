use pyo3::prelude::*;

#[pyclass]
pub struct Sender(crossbeam_channel::Sender<PyObject>);

#[pymethods]
impl Sender {
    fn send(&self, py: Python<'_>, x: &Bound<'_, PyAny>) -> anyhow::Result<()> {
        let x_owned = x.to_object(py);
        py.allow_threads(|| self.0.send(x_owned))?;
        Ok(())
    }
}

#[pyclass]
pub struct Receiver(crossbeam_channel::Receiver<PyObject>);

#[pymethods]
impl Receiver {
    fn recv(&self, py: Python) -> anyhow::Result<PyObject> {
        let x = py.allow_threads(|| self.0.recv())?;
        Ok(x)
    }

    fn __iter__(slf: PyRef<'_, Self>) -> PyResult<Py<ReceiverIter>> {
        let iter = ReceiverIter(slf.0.clone());
        Py::new(slf.py(), iter)
    }
}

#[pyclass]
pub struct ReceiverIter(crossbeam_channel::Receiver<PyObject>);

#[pymethods]
impl ReceiverIter {
    fn __iter__(slf: PyRef<'_, Self>) -> PyRef<'_, Self> {
        slf
    }
    fn __next__(slf: PyRefMut<'_, Self>) -> Option<PyObject> {
        slf.0.recv().ok()
    }
}

#[pyfunction]
pub fn bounded(cap: usize) -> (Sender, Receiver) {
    let (tx, rx) = crossbeam_channel::bounded(cap);
    (Sender(tx), Receiver(rx))
}
