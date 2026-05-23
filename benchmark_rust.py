#!/usr/bin/env python3
import time, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent; sys.path.insert(0,str(ROOT/"src"))
from compute_kernel import generate_ndvi_tile_features
def main():
    t0=time.perf_counter()
    for _ in range(200):
        generate_ndvi_tile_features(500,42)
    py_s=time.perf_counter()-t0
    try:
        import mapping_right_of_way_for_pipeline_management_looking_at_vegetation_patterns_with_clustering_rs as rs
    except ImportError:
        print("Build: cd rust && maturin develop --release -m py/Cargo.toml"); print(f"Python {py_s:.3f}s"); return
    rs_s=rs.bench_kernel_py(500,42,200)
    print(f"Python {py_s:.3f}s Rust {rs_s:.3f}s speedup {py_s/max(rs_s,1e-9):.1f}x")
    py=generate_ndvi_tile_features(500,42)
    rs_out=rs.generate_ndvi_tile_features_py(500,42)
    for a,b in zip(py, rs_out):
        assert np.asarray(a).shape == np.asarray(b).shape
    print("Correctness: OK (shapes match; stochastic generator)")
if __name__=="__main__": main()
