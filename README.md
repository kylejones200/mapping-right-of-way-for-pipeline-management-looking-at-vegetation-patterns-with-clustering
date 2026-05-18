# Mapping Right of Way for Pipeline Management Looking at Vegetation Patterns with Clustering

Published: 2025-10-28
Medium: [https://medium.com/@kyle-t-jones/mapping-right-of-way-for-pipeline-management-looking-at-vegetation-patterns-with-clustering-bf4e2614b24a](https://medium.com/@kyle-t-jones/mapping-right-of-way-for-pipeline-management-looking-at-vegetation-patterns-with-clustering-bf4e2614b24a)

## Business context

A pipeline operator receives a vegetation management report for 150 km of right-of-way (ROW). The report lists 47 tiles where NDVI (vegetation index) exceeds 0.7. Management asks: "Which areas need trimming first?"

The NDVI threshold doesn't answer this. A tile with NDVI=0.75 could be stable forest that's been there for decades, or it could be recent overgrowth encroaching on the pipeline. A tile with NDVI=0.65 might be below the threshold but showing rapid vegetation increase --- a leading indicator of future problems.

Single-variable thresholds treat all high-NDVI tiles identically. They don't capture spatial context, temporal trends, or multivariate patterns (vegetation + thermal + soil disturbance).

## About

Place the code for this article in this repository.
The original article export is saved as `article.md`.

## Files

Add your `.ipynb`, `.py`, `.yaml`, `.js`, `.ts`, or other project files here.

## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).