#IMPORT THIRD PARTY LIBRARIES
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.rnsga3 import RNSGA3
from pymoo.optimize import minimize
from pymoo.factory import get_algorithm, get_crossover, get_mutation, get_sampling
import numpy as np
from pymoo.core.problem import starmap_parallelized_eval # Library for parallelization
from multiprocessing.pool import ThreadPool # Library for parallelization
import pandas as pd # Library to save CSV files


#IMPORT OTHER FILES
from parameters import *
from evaluationFunctions import *
from savefiles import *

class ElementwiseSphereWithConstraint(ElementwiseProblem):

    def __init__(self, **kwargs):
        super().__init__(n_var=n_var_p, n_obj=n_obj_p, n_constr=n_constr_p, xl=xl_p, xu=xu_p, type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        #Get land uses from variables x
        landUses = x[0:city_length*city_length*city_length]
        #Count the times each land use appears in the solution
        counter_landUses = count_landUses(landUses)
        #For F, both sum the number of parks and the volume of those parks
        f1 = f_greenspace(landUses)
        f2 = 0#-np.sum(x[city_length*city_length*city_length::])
        f3 = f_gravity(landUses)
        out["F"] = [f1,f2,f3]
        #G is not needed as there are no constraints for now
        g1 = g_nbr_residences(counter_landUses[i_land_uses_p["residence"]])
        g2 = g_nbr_offices(counter_landUses[i_land_uses_p["office"]])
        g3 = g_nbr_amenities(counter_landUses[i_land_uses_p["amenity"]])
        out["G"] = [g1,g2,g3]

class geneticMachine():
    def __init__(self):
        #Initialise the pool for parallelization
        self.pool = ThreadPool(n_threads_p)
        # define the problem by passing the starmap interface of the thread pool
        self.geneticVertical = ElementwiseSphereWithConstraint(runner=self.pool.starmap, func_eval=starmap_parallelized_eval)
        # Define reference points
        self.ref_points = np.array([[0,0,0]])
        # Get Algorithm
        self.algorithm = RNSGA3(
            ref_points=self.ref_points,
            pop_per_ref_point=105,
            mu=0.1,
            sampling=get_sampling("int_random"),
            crossover=get_crossover("int_sbx", prob=1.0, eta=3.0),
            mutation=get_mutation("int_pm", eta=3.0),
            eliminate_duplicates=True,)
        #Minimise towards objectives
        self.res = minimize(self.geneticVertical, 
                    algorithm=self.algorithm,
                    termination=('n_gen', n_gen_p),
                    seed=1,
                    verbose=True,
                    save_history=True)
        #We close the pool responsible for parallelization
        self.pool.close()
        #Save data to CSV
        #Save in CSV
        if(saveCSV):
            save_generations(self)
            '''landUse_labels = self.res.history[0].pop.get("X")[0][0:city_length*city_length*city_length]
            size_labels = self.res.history[0].pop.get("X")[0][city_length*city_length*city_length::]
            d1 = {str(0): landUse_labels}
            df1 = pd.DataFrame(data=d1)
            d2 = {str(0): size_labels}
            df2 = pd.DataFrame(data=d2)
            counter_column = 1
            for generation in range(1,n_gen_p,n_gen_p//20):
                landUse_labels = self.res.history[generation].pop.get("X")[0][0:city_length*city_length*city_length]
                size_labels = self.res.history[generation].pop.get("X")[0][city_length*city_length*city_length::]
                df1.insert(counter_column,str(generation), landUse_labels, True)
                df2.insert(counter_column,str(generation), size_labels, True)
                counter_column += 1
            df1.to_csv(path_to_data+'/landUse_labels.csv')
            df2.to_csv(path_to_data+'/size_labels.csv')'''
