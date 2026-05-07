from pathlib import Path
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Union
import json
import tempfile

from celerpy.settings import settings
from celerpy.model.input import (
    ModelSetup,
    OrangeStats,
    OrangeConversionOptions,
)
from celerpy.model.output import (
    OrangeParamsOutput,
)
from celerpy.process import communicate_model
from celerpy.visualize import CelerGeo

# Since we're not raytracing with Geant4...
settings.g4_geo_optimize = False


def start_celer_geo(
    filename: Path,
    celer_prefix: Path,
    orange_options: Optional[OrangeConversionOptions] = None,
):
    assert celer_prefix.is_dir()

    settings.prefix_path = celer_prefix
    if orange_options is not None:
        tmpfile = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        tmpfile.write(orange_options.model_dump_json())
        tmpfile.close()
        settings.g4org_options = Path(tmpfile.name)
    else:
        settings.g4org_options = None

    setup = ModelSetup(geometry_file=filename)
    assert setup.geometry_file.is_file()

    if settings.profiling:
        setup.perfetto_file = Path(filename.stem + ".perfetto")

    return CelerGeo(setup=setup)


def run_and_load(
    filename: Path,
    celer_prefix: Path,
    orange_options: Optional[OrangeConversionOptions] = None,
):
    # Create temporary files for orange conversion outputs
    output_files = {}
    for key in ["csg", "org"]:  # "objects",
        tmpfile = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        tmpfile.close()
        output_files[key] = tmpfile.name

    if orange_options is None:
        orange_options = OrangeConversionOptions()
    else:
        orange_options = orange_options.model_copy()

    for key, filepath in output_files.items():
        setattr(orange_options, f"{key}_output_file", filepath)

    # Run, convert to ORANGE, save statistics, exit
    with start_celer_geo(
        filename, celer_prefix, orange_options=orange_options
    ) as celer_geo:
        stats = communicate_model(celer_geo.process, OrangeStats(), OrangeParamsOutput)
        results: dict = celer_geo.close()

    for key, filepath in output_files.items():
        with open(filepath, "r") as f:
            results[key] = json.load(f)
    results["orange_stats"] = stats.model_dump()
    results["orange_opts"] = orange_options.model_dump()

    return results


## PROCESSING


def _as_list(x: Any) -> List[Any]:
    if x is None:
        return []
    assert isinstance(x, list)
    return x


def summarize_csg(csg: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for item in _as_list(csg):
        name = item.get("label")
        item_stats = {
            "tree_size": len(item["tree"]),
        }
        for key in ["volumes", "surfaces", "remapped_surfaces"]:
            item_stats[key] = len(item[key])
        out[name] = item_stats

    return out


def summarize_orange_stats(stats: Dict[str, Any]) -> Dict[str, Any]:
    scalars = stats["scalars"]
    sizes = stats["sizes"]
    bih = sizes["bih"]
    result = {
        k: v for k, v in scalars.items() if k.startswith("max_") or k.startswith("num_")
    }
    for key in [
        "reals",
        "transforms",
        "volume_records",
        "logic_ints",
        "surface_types",
    ]:
        result[key] = sizes[key]
    for key in ["inner_nodes", "leaf_nodes"]:
        result["bih_" + key] = bih[key]
    return result


def _count_surfaces_by_type(surfaces: Dict[str, Any]) -> Dict[str, int]:
    types = _as_list(surfaces.get("types"))
    # Some files encode per-surface sizes; we only need counts by type.
    return dict(Counter(types))


def _count_transforms(transforms: Any) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for t in _as_list(transforms):
        # ORANGE encodes transforms as flat lists: len=3 (translation) or len=12 (3x3 + translation).
        n = len(t)
        if n == 3:
            key = "translation"
        elif n == 12:
            key = "transformation"
        elif n == 0:
            key = "none"
        else:
            print("unexpected transform:", t)
            key = "invalid"
        counts[key] += 1
    return dict(counts)


def _logic_word_counts(volumes: List[Dict[str, Any]]) -> Dict[int, int]:
    counts: Dict[int, int] = defaultdict(int)
    for v in volumes:
        length = len(v["logic"].split())
        counts[length] += 1
    return dict(counts)


def summarize_org_universe(uni):
    surfaces = uni.get("surfaces", {})
    uni_entry = {
        "surface_counts": _count_surfaces_by_type(surfaces),
        "transform_counts": _count_transforms(uni.get("transforms")),
        "logic_sizes": _logic_word_counts(_as_list(uni.get("volumes"))),
    }
    return uni_entry


def summarize_org_universes(org: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for uni in _as_list(org.get("universes")):
        name = uni["md"]["name"]
        out[name] = summarize_org_universe(uni)
    return out


DEFAULT_ORG = {
    "surface_counts": [],
    "transform_counts": [],
    "logic_sizes": [],
}


def summarize(data: dict):
    csg = summarize_csg(data["csg"])
    org = summarize_org_universes(data["org"])

    for k, csg_item in csg.items():
        try:
            org_item = org[k]
        except KeyError:
            org_item = DEFAULT_ORG.copy()
        csg_item.update(org_item)

    result = summarize_orange_stats(data["orange_stats"])
    result["csg"] = csg
    result.update(data["timers"])
    result["g4opt"] = data["runtime"]["environment"]["G4_GEO_OPTIMIZE"].lower() in (
        "true",
        "1",
        "yes",
    )

    return result


results = run_and_load("/Users/veb/cel_profiling/dune/geometry/dune-celeritas-rice.gdml",
                       Path("/Users/veb/opt/celeritas/build/"))

with open("out.json","w") as f:
    json.dump(results["orange_stats"], f)

