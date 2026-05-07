import sys
import matplotlib.pyplot as plt

sys.path[:0] = ["/Users/veb/opt/celeritas/celerpy/"]
import celerpy
from celerpy.settings import settings
settings.prefix_path = "/Users/veb/opt/celeritas/build/"
from celerpy import model, visualize

from celerpy.model.input import *
from celerpy.model.output import *

gdml = "dune-celeritas-rice.gdml"
celer_geo = visualize.CelerGeo.from_filename(gdml)

celer_geo.reset_id_map()
draw_image = visualize.Imager(
    celer_geo,
    model.ImageInput(
        lower_left=[0, -788, -583],
        upper_right=[0, 1030, 1724],
        rightward=[0.0, 0.0, 1.0],
        vertical_pixels=512,
    ))
(fig, ax) = plt.subplots()
draw_image(ax);

plt.title("Slice at $x=0$")
plt.savefig("dune-celeritas-rice_x-slice.png", dpi=300, bbox_inches="tight")

