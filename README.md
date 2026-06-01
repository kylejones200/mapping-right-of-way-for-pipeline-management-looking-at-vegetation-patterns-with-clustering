# Mapping Right of Way for Pipeline Management Looking at Vegetation Patterns with Clustering

Published: 2025-10-28
Medium: [https://medium.com/@kyle-t-jones/mapping-right-of-way-for-pipeline-management-looking-at-vegetation-patterns-with-clustering-bf4e2614b24a](https://medium.com/@kyle-t-jones/mapping-right-of-way-for-pipeline-management-looking-at-vegetation-patterns-with-clustering-bf4e2614b24a)

## Business context

A pipeline operator receives a vegetation management report for 150 km of right-of-way (ROW). The report lists 47 tiles where NDVI (vegetation index) exceeds 0.7. Management asks: "Which areas need trimming first?"

The NDVI threshold doesn't answer this. A tile with NDVI=0.75 could be stable forest that's been there for decades, or it could be recent overgrowth encroaching on the pipeline. A tile with NDVI=0.65 might be below the threshold but showing rapid vegetation increase --- a leading indicator of future problems.

Single-variable thresholds treat all high-NDVI tiles identically. They don't capture spatial context, temporal trends, or multivariate patterns (vegetation + thermal + soil disturbance).



## Rust performance port

Side-by-side **Python vs Rust** implementation of the numeric hot loop — NDVI tile feature generation. Reference PyO3 benchmark: **~250×** on a release build (local machine; run `benchmark_rust.py` to reproduce).

| Path | Role |
|------|------|
| `src/compute_kernel.py` | Python/numpy reference kernel |
| `rust/core/` | Pure Rust library |
| `rust/py/` | PyO3 bindings |
| `rust/bench/` | Standalone CLI benchmark |
| `benchmark_rust.py` | Python vs Rust timing + correctness check |

```bash
# Rust-only CLI benchmark
cd rust && cargo run --release -p mapping_right_of_way_for_pipeline_management_looking_at_vegetation_patterns_with_clustering_bench

# Python vs Rust (PyO3)
pip install maturin numpy
maturin develop --release -m rust/py/Cargo.toml
python benchmark_rust.py
```

Python ML training, solvers, and orchestration stay in Python; Rust targets the numeric hot loops. Stochastic generators validate output shapes; deterministic kernels match at tight floating-point tolerance.


## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).