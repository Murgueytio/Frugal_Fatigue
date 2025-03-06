# Split data for training (70%) and testing (30%)
train, test = train_test_split(data, test_size=0.3, random_state=42)

# Model for changes in expenditure
X_spent = sm.add_constant(train[['discretionary_expenses', 'basic_expenses', 'frec_offers', 
                                'household_income', 'net_debt']])
expense_model = sm.OLS(train['changes_expense'], X_spent).fit()

# Job search model
X_job = sm.add_constant(train[['jobs_wanted', 'lost_expectation', 'jobs_lower_status', 
                                'household_income', 'net_debt']])
employment_model = sm.OLS(train['job_search'], X_job).fit()

# Model for changes in consumption
X_consumption = sm.add_constant(train[['change_brands', 'deferred_purchases', 'change_preferences', 
                                  'household_income', 'net_debt']])
consumption_model = sm.OLS(train['changes_consumption'], X_consumption).fit()

# Main model of frugal fatigue
X_fatigue = sm.add_constant(train[['changes_expense', 'job_search', 'changes_consumption', 
                                 'household_income', 'net_debt']])
fatigue_model = sm.OLS(train['frugal_fatigue'], X_fatigue).fit()
