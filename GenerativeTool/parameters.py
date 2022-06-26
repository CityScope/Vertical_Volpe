#IMPORT THIRD PARTY LIBRARIES
import numpy as np
import multiprocessing

city_length = 12
nodes_per_floor = city_length * city_length
city_height = 50
n_var_p = city_length * city_length * city_length * 2
n_obj_p = 3
n_constr_p = 3
xl_p = np.array([1] * city_length * city_length * city_length * 2)
xu_land_uses = [5] * city_length * city_length * city_length
xu_volumes = [625] * city_length * city_length * city_length
xu_p = xu_land_uses.copy()
xu_p.extend(xu_volumes)
xu_p = np.array(xu_p)
type_var_p = int
n_gen_p = 600 # Number of generations to compute
#NUMBERS FOR LANDUSES
park = 1
amenity = 2
office = 3
residence = 4
air = 5
land_uses_p = {1:"park",2:"amenity",3:"office",4:"residence",5:"air"}
i_land_uses_p = {land_uses_p[n]:n for n in land_uses_p.keys()}
#GRAVITY FOR LANDUSES
gravity = {"park":0,"air":0,"residence":1,"office":10,"amenity":18}
#COLORS FOR LANDUSES
colors_p = {"park":'lightgreen',"air":'lightblue',"residence":'orange',"office":'dodgerblue',"amenity":'magenta'}
color_scale_p = [colors_p[n[1]] for n in sorted(land_uses_p.items(), key=lambda kv: kv[0])]
#CONSTRAINTS OF POPULATION
nbr_of_residences = 300
nbr_of_amenities = 300
nbr_of_offices = 300
#PARAMETERS FOR PARALLELIZATION
n_threads_p = multiprocessing.cpu_count()
#SaveOrNotCSV
saveCSV = True
path_to_code = "C:/Users/adminlocal/Documents/WorkspacesPython/VerticalCity"