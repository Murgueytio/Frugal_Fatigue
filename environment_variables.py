np.random.seed(123)
n = 1000 # number of consumers

# Exogenous variables
household_income = np.random.normal(3000, 1000, n)
net_debt = np.random.normal(10000, 5000, n)

# Variables for changes in spending patterns
discretionary_expenses = -0.15 * household_income + 0.03 * net_debt + np.random.normal(0, 500, n)
basic_expenses = -0.05 * household_income + 0.01 * net_debt + np.random.normal(0, 200, n)
frec_offers = -0.0002 * household_income + 0.00003 * net_debt + np.random.normal(0, 1, n)

# Variables for job search
jobs_wanted = -0.001 * household_income + 0.0002 * net_debt + np.random.normal(0, 2, n)
lost_expectation = -0.0003 * household_income + 0.00004 * net_debt + np.random.normal(0, 0.5, n)
jobs_lower_status = -0.0002 * household_income + 0.00003 * net_debt + np.random.normal(0, 0.5, n)

# Variables for changes in consumption
change_brands = -0.0002 * household_income + 0.00005 * net_debt + np.random.normal(0, 0.5, n)
deferred_purchases = -0.0003 * household_income + 0.00006 * net_debt + np.random.normal(0, 0.7, n)
change_preferences = -0.0001 * household_income + 0.00003 * net_debt + np.random.normal(0, 0.4, n)

# Calculate the subscripts
changes_expense = 0.4 * discretionary_expenses + 0.3 * basic_expenses + 0.3 * frec_offers
job_search = 0.5 * jobs_wanted + 0.3 * lost_expectation + 0.2 * jobs_lower_status
changes_consumption = 0.4 * change_brands + 0.4 * deferred_purchases + 0.2 * change_preferences

# Calculate the Frugal Fatigue Index
frugal_fatigue = 0.4 * changes_expense + 0.3 * job_search + 0.3 * changes_consumption + np.random.normal(0, 50, n)

# Dataframe
data = pd.DataFrame({
    # Control variables
    'household_income': household_income,
    'net_debt': net_debt,
    
    # Expenditure variables
    'discretionary_expenses': discretionary_expenses,
    'basic_expenses': basic_expenses,
    'frec_offers': frec_offers,
    
    # Employment variables
    'jobs_wanted': jobs_wanted,
    'lost_expectation': lost_expectation,
    'jobs_lower_status': jobs_lower_status,
    
    # Consumption variables
    'change_brands': change_brands,
    'deferred_purchases': deferred_purchases,
    'change_preferences': change_preferences,
    
    # Subscripts
    'changes_expense': changes_expense,
    'job_search': job_search,
    'changes_consumption': changes_consumption,
    
    # Main index
    'frugal_fatigue': frugal_fatigue
})
