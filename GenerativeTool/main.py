#IMPORT THIRD PARTY LIBRARIES
import numpy as np
import matplotlib.pyplot as plt
from pymoo.visualization.scatter import Scatter
import plotly.graph_objects as go

#IMPORT OTHER FILES
from parameters import *
from genetic import *
from visualization import *

#Create object for algorithm
genMachine = geneticMachine()
#Create object for visualization
visualizator = Visualizer()
#Add traces from the genetic machine
visualizator.add_traces(genMachine)
#Save as CSV

#Visualise in browser
visualizator.visualize()

#SHOW HOW THE F1 VALUES HAVE IMPROVED THROUGH THE GENERATIONS
val = [e.opt.get("F")[0][2] for e in genMachine.res.history]
plt.plot(np.arange(len(val)), val)
plt.show()