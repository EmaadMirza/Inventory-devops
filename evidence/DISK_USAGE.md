# Disk usage snapshot - 3 November 2026

Decimal GB (1 GB = 1,000,000,000 bytes). Docker sizes are rounded estimates; host file totals are logical lengths.

| Assignment-specific category | GB |
|---|---:|
| Source, Git, tests, reports and evidence | 0.0023 |
| Downloaded Kind executable | 0.0108 |
| Exported image archive and other temporary/QA files | 0.0990 |
| Docker images, deduplicated incremental image-store usage | 3.997 |
| Container writable layers, excluding mounts | 0.481 |
| Assignment volumes: Maven, Jenkins, Kind node /var | 1.821 |
| Assignment build cache with Shared=false only | 1.176 |
| **Assignment logical total estimate** | **7.59** |

Pre-existing Docker logical data is separate: images 1.018 GB; existing volumes 0.048 GB; exclusive existing build cache 0.275 GB. Total approximately 1.34 GB.

Free space at measurement: C: 8.26 GB; D: 84.61 GB. No assignment data was written to D:.

The image number is the engine's deduplicated image-store total (5.015 GB) minus the observed initial image-store total (1.018 GB). It is not the sum of all image virtual sizes. Layers shared between the Ansible images are counted once. Cache layers marked Shared=true are excluded from the cache addition because their storage is already represented by images. The Kind /var volume holds an independent nested Kubernetes image/runtime store, so its actual stored copy is a separate volume cost.

C: free space decreased by approximately 10.43 GB since the initial check (18.68 GB free). This is a drive-wide observation, not exact attribution. The two Docker VHDX files have a combined current logical file length of approximately 11.00 GB; do not add that on top of Docker categories. Their pre-task lengths were not measured. Dynamic VHDX allocation, filesystem metadata, compression, temporary files and unrelated host activity prevent exact physical attribution.

Snapshot precedes final source ZIP and any later Jenkins UI capture. Raw measurements and calculation inputs are retained in ignored .lab; evidence/disk-usage.json contains the calculated results. Nothing was deleted.
