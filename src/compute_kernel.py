import numpy as np

def generate_ndvi_tile_features(n_tiles=5000, seed=42):
    rng = np.random.default_rng(seed)
    ndvi_m, ndvi_s, therm, soil = [], [], [], []
    for _ in range(n_tiles):
        u = rng.random()
        if u < 0.084:
            ndvi_m.append(0.65 + rng.random() * 0.15)
            ndvi_s.append(0.1 + rng.random() * 0.1)
        elif u < 0.14:
            ndvi_m.append(0.1 + rng.random() * 0.15)
            ndvi_s.append(0.01 + rng.random() * 0.05)
        elif u < 0.17:
            ndvi_m.append(0.25 + rng.random() * 0.15)
            ndvi_s.append(0.05 + rng.random() * 0.1)
        else:
            ndvi_m.append(0.1 + rng.random() * 0.7)
            ndvi_s.append(0.01 + rng.random() * 0.19)
        therm.append(rng.random() * 0.5)
        soil.append(0.2 + rng.random() * 0.6)
    return np.array(ndvi_m), np.array(ndvi_s), np.array(therm), np.array(soil)
