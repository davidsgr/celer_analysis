import sys
import matplotlib.pyplot as plt

sys.path[:0] = ["/Users/veb/opt/celeritas/celerpy/"]
import celerpy
from celerpy.settings import settings
settings.prefix_path = "/Users/veb/opt/celeritas/build/"
from celerpy import model, visualize

gdml = "/Users/veb/cel_profiling/atlas/geometry/atlas-full-run4_LArEndcapNeg0x6cd79ea0.gdml"
celer_geo = visualize.CelerGeo.from_filename(gdml)

celer_geo.reset_id_map()
imager = visualize.Imager(
    celer_geo,
    model.ImageInput(
        lower_left=[-379.5, 0.1, -318.9],
        upper_right=[379.5, 0.1, 4.6],
        rightward=[0.0, 0.0, 1.0],
        vertical_pixels=512,
    )
    )
(fig, ax) = plt.subplots()
imager(ax, colorbar=False);

ax.set_title("")
plt.savefig("atlas-full-run4_LArEndcapNeg0x6cd79ea0_slice.pdf")

