def evaluate_model(model, X, y):
    """Evaluate a model with basic metrics"""
    predictions = model.predict(X)
    mse = np.mean((predictions - y)**2)
    r2 = model.rsquared
    return {
        'MSE': mse,
        'R2': r2,
        'Parameters': model.params
    }

# Evaluate test set
X_spent_test = sm.add_constant(test[['discretionary_expenses', 'basic_expenses', 'frec_offers', 
                                    'household_income', 'net_debt']])
X_job_test = sm.add_constant(test[['jobs_wanted', 'lost_expectation', 'jobs_lower_status', 
                                    'household_income', 'net_debt']])
X_consumption_test = sm.add_constant(test[['change_brands', 'deferred_purchases', 'change_preferences', 
                                    'household_income', 'net_debt']])

# Subscript Predictions
pred_spent = spent_model.predict(X_spent_test)
pred_job = job_model.predict(X_job_test)
pred_consumption = consumption_model.predict(X_consumption_test)

# Creating a dataframe for frugal fatigue prediction
X_fatigue_test = sm.add_constant(pd.DataFrame({
    'changes_expense': pred_spent,
    'job_search': pred_job,
    'changes_consumption': pred_consumption,
    'household_income': test['household_income'].values,
    'net_debt': test['net_debt'].values
}))

# Predicting frugal fatigue
pred_fatigue = fatigue_model.predict(X_fatigue_test)

# Calculate the metrics
results_spent = evaluate_model(spent_model, X_spent_test, test['changes_expense'])
results_job = evaluate_model(job_model, X_job_test, test['job_search'])
results_consumption = evaluate_model(consumption_model, X_consumption_test, test['changes_consumption'])
results_fatigue = evaluate_model(fatigue_model, X_fatigue_test, test['frugal_fatigue'])
