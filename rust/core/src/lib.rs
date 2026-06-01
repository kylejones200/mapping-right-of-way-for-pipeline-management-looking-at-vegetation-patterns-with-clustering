//! Synthetic NDVI tile features for ROW vegetation clustering.

struct Lcg(u64);

impl Lcg {
    fn new(seed: u64) -> Self {
        Self(seed)
    }

    fn next_u32(&mut self) -> u32 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1);
        (self.0 >> 33) as u32
    }

    fn uniform(&mut self) -> f64 {
        self.next_u32() as f64 / u32::MAX as f64
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct NdviTileFeatures {
    pub ndvi_mean: Vec<f64>,
    pub ndvi_std: Vec<f64>,
    pub thermal_anomaly: Vec<f64>,
    pub soil_moisture: Vec<f64>,
}

pub fn generate_ndvi_tile_features(n_tiles: usize, seed: u64) -> NdviTileFeatures {
    let mut rng = Lcg::new(seed);
    let mut ndvi_mean = Vec::with_capacity(n_tiles);
    let mut ndvi_std = Vec::with_capacity(n_tiles);
    let mut thermal_anomaly = Vec::with_capacity(n_tiles);
    let mut soil_moisture = Vec::with_capacity(n_tiles);

    for _ in 0..n_tiles {
        let u = rng.uniform();
        if u < 0.084 {
            ndvi_mean.push(0.65 + rng.uniform() * 0.15);
            ndvi_std.push(0.1 + rng.uniform() * 0.1);
            thermal_anomaly.push(rng.uniform() * 0.3);
            soil_moisture.push(0.2 + rng.uniform() * 0.6);
        } else if u < 0.14 {
            ndvi_mean.push(0.1 + rng.uniform() * 0.15);
            ndvi_std.push(0.01 + rng.uniform() * 0.05);
            thermal_anomaly.push(rng.uniform() * 0.2);
            soil_moisture.push(0.1 + rng.uniform() * 0.3);
        } else if u < 0.17 {
            ndvi_mean.push(0.25 + rng.uniform() * 0.15);
            ndvi_std.push(0.05 + rng.uniform() * 0.1);
            thermal_anomaly.push(0.5 + rng.uniform() * 0.5);
            soil_moisture.push(0.3 + rng.uniform() * 0.2);
        } else {
            ndvi_mean.push(0.1 + rng.uniform() * 0.7);
            ndvi_std.push(0.01 + rng.uniform() * 0.19);
            thermal_anomaly.push(rng.uniform() * 0.3);
            soil_moisture.push(0.2 + rng.uniform() * 0.6);
        }
    }

    NdviTileFeatures {
        ndvi_mean,
        ndvi_std,
        thermal_anomaly,
        soil_moisture,
    }
}
