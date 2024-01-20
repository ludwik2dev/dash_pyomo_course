import pyomo.environ as pyo
import pathlib

import input


def uc_model(units):

    # ## Auxiliary functions

    def power_bounds(_m, plant, _hour):
        '''Max power for each plant'''
        return ( 0, plants[plant]['power'] )

    # ### Data
    
    # ## Constants
    HOURS = [t for t in range(1, 25)]

    # ## Profiles
    demand_profile = { hour+1: value for hour, value in enumerate(input.profiles['demand']) }

    # ## Units
    plants = { key: val for key, val in units.items() if units[key]['type'] in ['coal', 'gas', 'nuclear'] }
    demand_sources = { key: val for key, val in units.items() if units[key]['type'] in ['demand'] }
    
    # ### Pyomo model

    # ## Model initialization
    model = pyo.ConcreteModel()

    # ## Sets
    model.hours = pyo.Set(initialize=HOURS)
    model.plants = pyo.Set(initialize=plants.keys())
    model.demand_sources = pyo.Set(initialize=demand_sources.keys())

    # ## Variables
    model.power = pyo.Var(model.plants, model.hours, domain=pyo.NonNegativeReals, bounds=power_bounds)

    # ## Objective - minimize cost of the power system
    model.system_costs = pyo.Objective(
        expr = 
        
        # Plants variable cost
        + sum( model.power[plant, hour] * plants[plant]['vc'] for hour in model.hours for plant in model.plants ),
        
        sense=pyo.minimize)

    # ## Constraints

    # Demand has to be fullfilled in each hour (not less not more)
    model.demand = pyo.Constraint(model.hours, rule=lambda m, hour:
        + sum( m.power[plant, hour] for plant in m.plants )
        ==
        + sum( demand_sources[ele]['power'] * demand_profile[hour] for ele in m.demand_sources )
        )

    # Max plant power
    model.ct_plant_power = pyo.Constraint( model.plants, model.hours, rule=lambda m, plant, hour: m.power[plant, hour] <= plants[plant]['power'] )

    # ## Solve the model
    solver_name = 'cbc'
    solver_path = pathlib.Path(__file__).parent.resolve() / f'{solver_name}.exe'
    solver = pyo.SolverFactory(solver_name, executable=solver_path)
    results = solver.solve(model)

    # ## Optimalization results 
    if (results.solver.status == pyo.SolverStatus.ok) and (results.solver.termination_condition in [pyo.TerminationCondition.optimal, pyo.TerminationCondition.feasible]):

        print(f'Model is {results.solver.termination_condition}')

        # System cost
        sys_cost = round(pyo.value(model.system_costs), 0)
        sys_cost = f'{sys_cost} $'
        
        # Summarize results - power of each plant at each hour
        model.results = {}
        for unit in model.plants:
            model.results[unit] = {}
            for hour in model.hours:
                power = round(pyo.value(model.power[unit, hour]), 2)
                model.results[unit][hour] = power
        
        return model.results, sys_cost

    elif (results.solver.termination_condition == pyo.TerminationCondition.infeasible):
        print('Model is infeasible') 
        model, sys_cost = False, 0
        return False, 0

    elif (results.solver.termination_condition == pyo.TerminationCondition.unbounded):
        print('Model is unbounded')
        model, sys_cost = False, 0
        return False, 0 

    else:
        print('Unhandled error. Solver Status: ',  results.solver.status)
        model, sys_cost = False, 0
        return False, 0
    

if __name__ == '__main__':
    uc_model(input.units)