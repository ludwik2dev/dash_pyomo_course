import pyomo.environ as pyo
import pathlib


# Data
fruits = {
    'Apple': {'price': 4, 'size': 3},
    'Pear': {'price': 7, 'size': 5},
}
MAX_BASKET_SIZE = 60

# Initialize model
model = pyo.ConcreteModel()

# Add set
model.fruits = pyo.Set(initialize=fruits.keys())

# Add variable - this we want to calculate / find
model.quantity = pyo.Var(model.fruits, domain=pyo.NonNegativeIntegers)

# Add objective - we want to maximize income in our basket
model.income = pyo.Objective(expr = sum( fruits[fruit]['price'] * model.quantity[fruit] for fruit in model.fruits ), sense=pyo.maximize)

# Add constraint - max size of our basket
model.basket = pyo.Constraint(expr = sum( fruits[fruit]['size'] * model.quantity[fruit] for fruit in model.fruits ) <= MAX_BASKET_SIZE )

# Solve model
solver_name = 'cbc'
solver_path = pathlib.Path(__file__).parent.resolve() / f'{solver_name}.exe'
solver = pyo.SolverFactory(solver_name, executable=solver_path)
results = solver.solve(model)

# Print results
print( f'Total income: {pyo.value(model.income)}' )
for fruit in model.fruits:
    print( f'{fruit} quantity: {model.quantity[fruit]()}' )