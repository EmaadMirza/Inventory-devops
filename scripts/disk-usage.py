"""Read-only attribution using saved Docker snapshots; sizes use decimal GB."""
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
def read(path):
    data = (root / path).read_bytes()
    return data.decode("utf-16" if data.startswith(b"\xff\xfe") else "utf-8-sig")
def size(value):
    number, unit = re.fullmatch(r"([0-9.]+)([a-zA-Z]+)", value).groups()
    return float(number) * {"B":1,"kB":1e3,"MB":1e6,"GB":1e9}[unit]

project = json.loads(read(".lab/project-disk.json"))
builder = [json.loads(line) for line in read(".lab/builder-usage.json").splitlines() if line.strip()]
images = [json.loads(line) for line in read(".lab/image-layer-data.jsonl").splitlines() if line.strip()]
drives = json.loads(read(".lab/drive-space.json"))
host = sum(x["Bytes"] for x in project)
tool = (root / ".lab/kind.exe").stat().st_size
archive = (root / ".lab/mini-inventory-image.tar").stat().st_size
lab = next(x["Bytes"] for x in project if x["Group"] == ".lab")
assigned_cache = sum(size(x["Size"]) for x in builder if not x["Shared"] and x["CreatedAt"].startswith("2026-11-03"))
existing_cache = sum(size(x["Size"]) for x in builder if not x["Shared"] and not x["CreatedAt"].startswith("2026-11-03"))
old_layers = set(l for image in images[:4] for l in image["RootFS"]["Layers"])
new_layers = set(l for image in images[4:] for l in image["RootFS"]["Layers"])
summary = {
    "units": "decimal GB = 1,000,000,000 bytes; Docker CLI rounded estimates",
    "host_project_without_lab_GB": (host-lab)/1e9,
    "downloaded_kind_tool_GB": tool/1e9,
    "exported_image_archive_GB": archive/1e9,
    "other_lab_temporary_and_QA_GB": (lab-tool-archive)/1e9,
    "host_total_GB": host/1e9,
    "assignment_images_deduplicated_GB_estimate": 5.015-1.018,
    "assignment_container_writable_layers_GB_estimate": 0.4814,
    "assignment_volumes_GB_estimate": 1.526+0.2676+0.02773,
    "assignment_cache_exclusive_GB_estimate": assigned_cache/1e9,
    "preexisting_images_GB_estimate": 1.018,
    "preexisting_volumes_GB_estimate": 0.04816,
    "preexisting_cache_exclusive_GB_estimate": existing_cache/1e9,
    "cross_assignment_existing_shared_layer_count": len(old_layers & new_layers),
    "initial_C_free_GB": 18.683834368,
    "free_GB": {d["Name"]: d["Free"]/1e9 for d in drives},
    "caveat": "Images use engine-wide deduplicated image total minus observed pre-assignment baseline. Cache counts only Shared=false. VHDX expansion, metadata, compression and other host activity prevent exact physical attribution; do not add VHDX length to these categories. Snapshot precedes final source ZIP."
}
summary["assignment_total_GB_estimate"] = sum(summary[k] for k in ["host_total_GB","assignment_images_deduplicated_GB_estimate","assignment_container_writable_layers_GB_estimate","assignment_volumes_GB_estimate","assignment_cache_exclusive_GB_estimate"])
summary["observed_C_free_reduction_GB_not_exact_attribution"] = summary["initial_C_free_GB"]-summary["free_GB"]["C"]
(root / "evidence/disk-usage.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))
