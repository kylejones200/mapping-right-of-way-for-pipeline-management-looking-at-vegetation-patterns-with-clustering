use mapping_right_of_way_for_pipeline_management_looking_at_vegetation_patterns_with_clustering_core::generate_ndvi_tile_features;
use numpy::{PyArray1, IntoPyArray};
use pyo3::prelude::*;

#[pyfunction]
#[pyo3(signature = (n_tiles, seed=42))]
fn generate_ndvi_tile_features_py<'py>(py: Python<'py>, n_tiles: usize, seed: u64) -> PyResult<(Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>, Bound<'py, PyArray1<f64>>)> {
    let f = generate_ndvi_tile_features(n_tiles, seed);
    Ok((f.ndvi_mean.into_pyarray(py), f.ndvi_std.into_pyarray(py), f.thermal_anomaly.into_pyarray(py), f.soil_moisture.into_pyarray(py)))
}

#[pyfunction]
#[pyo3(signature = (n_tiles=5000, seed=42, iterations=200))]
fn bench_kernel_py(n_tiles: usize, seed: u64, iterations: usize) -> PyResult<f64> {
    let start = std::time::Instant::now();
    for _ in 0..iterations { let _ = generate_ndvi_tile_features(n_tiles, seed); }
    Ok(start.elapsed().as_secs_f64())
}

#[pymodule]
fn mapping_right_of_way_for_pipeline_management_looking_at_vegetation_patterns_with_clustering_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate_ndvi_tile_features_py, m)?)?;
    m.add_function(wrap_pyfunction!(bench_kernel_py, m)?)?;
    Ok(())
}
