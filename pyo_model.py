import pyomo.environ as pyo
import pathlib
import math
import time

import input


def uc_model(units):

    # ## Auxiliary functions

    def power_bounds(_m, plant, _hour):
        '''Max power for each plant'''
        return ( 0, plants[plant]['power'] )
    
    def power_pos_bounds(_m, plant, _hour):
        return ( 0, plants[plant]['power'] * ( 1 - OPT_POWER ) )
    
    def power_neg_bounds(_m, plant, _hour):
        return ( -plants[plant]['power'] * ( OPT_POWER - MIN_POWER ), 0 )
    
    def vc(m, plant, hour):

        '''Additional vc cost related to deviation from optimal point'''

        BASE_COST = plants[plant]['vc']
        max_power = plants[plant]['power']
        opt_power = plants[plant]['power'] * OPT_POWER 

        # Cost related to negative power / deviation in minus from optimal power
        a = BASE_COST * ( DEVIATION_COST - 1 ) / ( max_power * ( MIN_POWER - OPT_POWER ) ) 
        b = -a * OPT_POWER * max_power
        x = opt_power + (opt_power + m.power_neg[plant, hour])
        y = neg_cost = a * x + b

        # Cost related to positive power / deviation in plus from optimal power
        a = BASE_COST * ( DEVIATION_COST - 1 ) / ( max_power * ( 1 - OPT_POWER ) )
        b = -a * OPT_POWER * max_power
        x = opt_power + (opt_power + m.power_pos[plant, hour])
        y = pos_cost = a * x + b

        return neg_cost + BASE_COST + pos_cost

    # ### Data
    
    # ## Constants
    HOURS = [t for t in range(1, 25)]
    MIN_POWER = 0.4
    START_UP_COST = 10
    OPT_POWER = 0.7
    DEVIATION_COST = 1.25

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
    model.plants = pyo.Set(initialize=list(plants.keys()))
    model.demand_sources = pyo.Set(initialize=list(demand_sources.keys()))

    # ## Variables
    model.power = pyo.Var(model.plants, model.hours, domain=pyo.NonNegativeReals, bounds=power_bounds)
    model.power_pos = pyo.Var(model.plants, model.hours, domain=pyo.NonNegativeReals, bounds=power_pos_bounds)
    model.power_neg = pyo.Var(model.plants, model.hours, domain=pyo.NonPositiveReals, bounds=power_neg_bounds)
    model.on = pyo.Var(model.plants, model.hours, domain=pyo.Binary)
    model.change_state = pyo.Var(model.plants, model.hours, domain=pyo.Integers, bounds=(-1, 1))  # switch-on = 1, switch-off = -1, else 0
    model.switch_on = pyo.Var(model.plants, model.hours, domain=pyo.NonNegativeIntegers, bounds=(-1, 1))
    model.switch_off = pyo.Var(model.plants, model.hours, domain=pyo.NonPositiveIntegers, bounds=(-1, 1))

    # ## Objective - minimize cost of the power system
    model.system_costs = pyo.Objective(
        expr = 
        
        # Plants variable cost
        + sum( model.power[plant, hour] * vc(model, plant, hour) for hour in model.hours for plant in model.plants )

        # Plants start-up cost
        + sum( START_UP_COST * plants[plant]['vc'] * plants[plant]['power'] * model.switch_on[plant, hour] for hour in model.hours for plant in model.plants )
        
        , sense=pyo.minimize)

    # ## Constraints

    # Demand has to be fullfilled in each hour (not less not more)
    model.demand = pyo.Constraint(model.hours, rule=lambda m, hour:
        + sum( m.power[plant, hour] for plant in m.plants )
        ==
        + sum( demand_sources[ele]['power'] * demand_profile[hour] for ele in m.demand_sources )
        )

    # Max plant power
    model.ct_plant_max_power = pyo.Constraint( model.plants, model.hours, rule=lambda m, plant, hour: m.power[plant, hour] <= plants[plant]['power'] * m.on[plant, hour] )
    model.ct_plant_min_power = pyo.Constraint( model.plants, model.hours, rule=lambda m, plant, hour: m.power[plant, hour] >= MIN_POWER * plants[plant]['power'] * m.on[plant, hour] )
    model.ct_plant_opt_power = pyo.Constraint( model.plants, model.hours, rule=lambda m, plant, hour: m.power[plant, hour] == m.power_neg[plant, hour] + OPT_POWER * plants[plant]['power'] * m.on[plant, hour] + m.power_pos[plant, hour] )

    # Plant start up
    model.ct_change_state = pyo.Constraint( model.plants, model.hours, rule=lambda m, plant, hour: m.change_state[plant, hour] == m.on[plant, hour] - m.on[plant, hour-1] if hour > 1 else m.change_state[plant, hour] == m.on[plant, hour] )
    model.ct_switch = pyo.Constraint( model.plants, model.hours, rule=lambda m, plant, hour: m.change_state[plant, hour] == m.switch_on[plant, hour] + m.switch_off[plant, hour] )

    # Plant ramp
    model.ramp_up = pyo.Constraint(   
        model.plants, model.hours, rule=lambda m, plant, hour: 
        m.power[plant, hour] - m.power[plant, hour-1] 
        <= 
        + plants[plant]['ramp'] * model.on[plant, hour-1] 
        + MIN_POWER * plants[plant]['power'] * (1 - model.on[plant, hour-1])
        if hour > 1 else pyo.Constraint.Skip )
    model.ramp_down = pyo.Constraint( 
        model.plants, model.hours, rule=lambda m, plant, hour: 
        m.power[plant, hour] - m.power[plant, hour-1] 
        >= 
        - plants[plant]['ramp'] * model.on[plant, hour] 
        - plants[plant]['power'] * (1 - model.on[plant, hour])
        if hour > 1 else pyo.Constraint.Skip )

    # ## Solve the model
    mip_solver = 'cbc'
    # solver_path = pathlib.Path(__file__).parent.resolve() / f'{solver_name}.exe'
    nlp_solver = 'ipopt'
    solver = pyo.SolverFactory('mindtpy')
    start_time = time.time()
    results = solver.solve(model, mip_solver=mip_solver, nlp_solver=nlp_solver)  # absolute_bound_tolerance=0.01, relative_bound_tolerance=0.01, small_dual_tolerance=0.01, integer_tolerance=0.01

    # ## Optimalization results 
    if (results.solver.status == pyo.SolverStatus.ok) and (results.solver.termination_condition in [pyo.TerminationCondition.optimal, pyo.TerminationCondition.feasible]):

        print(f'Model is {results.solver.termination_condition}')

        # # Printing m.on
        # print('\t\t', [ str(hour).rjust(2, ' ') for hour in model.hours ], end='\n\n')
        # for unit in model.plants:
        #     print(unit.ljust(8, ' ') , '\t', [ str(int(pyo.value(model.on[unit, hour]))).rjust(2, ' ') for hour in model.hours ])

        # # Printing start-up related variables
        # print('\t\t\t', [ str(hour).rjust(2, ' ') for hour in model.hours ], end='\n\n')
        # for unit in model.plants:
        #     print('On:', unit.ljust(15, ' ') , '\t', [ str(int(pyo.value(model.on[unit, hour]))).rjust(2, ' ') for hour in model.hours ])
        #     print('State:', unit.ljust(8, ' ') , '\t', [ str(int(pyo.value(model.change_state[unit, hour]))).rjust(2, ' ') for hour in model.hours ])
        #     print('Switch on:', unit.ljust(8, ' ') , '\t', [ str(int(pyo.value(model.switch_on[unit, hour]))).rjust(2, ' ') for hour in model.hours ])
        #     print('Switch off:', unit.ljust(8, ' ') , '\t', [ str(int(pyo.value(-model.switch_off[unit, hour]))).rjust(2, ' ') for hour in model.hours ])
        #     print(end='\n')

        # # Power variance
        # total = 0
        # n = 0
        # for plant in model.plants:
        #     for hour in model.hours:
        #         power = model.power[plant, hour]()
        #         opt_power = plants[plant]['power'] * OPT_POWER 
        #         on = model.on[plant, hour]()
                
        #         if on:
        #             total = total + math.pow( power / opt_power - 1 , 2 )
        #         n = n + on
        # print(f'\nPower variance: {round( total / n , 2)}\n')
        # print(f'Execution time: {round( time.time() - start_time, 2 )}\n')

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