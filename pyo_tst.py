import pyomo.environ as pyo
import pathlib


# Data
fruits = {
    'Apple': {'price': 4, 'size': 3, 'max_quantity': 20},
    'Pear': {'price': 7, 'size': 5, 'max_quantity': 10},
}
baskets = {
    'Basket 1': {'max_size': 45, 'storage_cost': 2},
    'Basket 2': {'max_size': 35, 'storage_cost': 3},
}

# Initialize model
model = pyo.ConcreteModel()

# Add set
model.fruits = pyo.Set(initialize=fruits.keys())
model.baskets = pyo.Set(initialize=baskets.keys())

# Add variable - this we want to calculate / find
def fruit_bounds(m, _basket, fruit):
    return ( 0, fruits[fruit]['max_quantity'] )

model.quantity = pyo.Var(model.baskets, model.fruits, domain=pyo.NonNegativeIntegers, bounds=fruit_bounds)

# Add objective - we want to maximize income in our basket
model.income = pyo.Objective(expr = sum( ( fruits[fruit]['price'] - baskets[basket]['storage_cost'] ) * model.quantity[basket, fruit] for fruit in model.fruits for basket in model.baskets ), sense=pyo.maximize)

# Add constraint - max size of our baskets
model.basket = pyo.Constraint(model.baskets, rule=lambda m, basket: sum( fruits[fruit]['size'] * m.quantity[basket, fruit] for fruit in model.fruits ) <= baskets[basket]['max_size'] )
model.sum_quantity = pyo.Constraint(model.fruits, rule=lambda m, fruit: sum( m.quantity[basket, fruit] for basket in model.baskets ) <= fruits[fruit]['max_quantity'] )

# Solve model
solver_name = 'cbc'
solver_path = pathlib.Path(__file__).parent.resolve() / f'{solver_name}.exe'
solver = pyo.SolverFactory(solver_name, executable=solver_path)
results = solver.solve(model)

# Print status 
if (results.solver.status == pyo.SolverStatus.ok) and (results.solver.termination_condition in [pyo.TerminationCondition.optimal, pyo.TerminationCondition.feasible]):
    # Print results
    print( f'Total income: {pyo.value(model.income)}' )
    for basket in model.baskets:
        for fruit in model.fruits:
            print( f'{fruit} quantity in {basket}: {model.quantity[basket, fruit]()}' )

elif (results.solver.termination_condition == pyo.TerminationCondition.infeasible):
    print('Model is infeasible') 

elif (results.solver.termination_condition == pyo.TerminationCondition.unbounded):
    print('Model is unbounded') 

else:
    print('Unhandled error. Solver Status: ',  results.solver.status)
