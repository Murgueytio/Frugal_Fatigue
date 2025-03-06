def classify_fatigue(fatigue_value, high_threshold=150, mean_threshold=80):
    """Classify the level of financial fatigue"""
    if fatigue_value > high_threshold:
        return "HIGH"
    elif fatigue_value > mean_threshold:
        return "MEAN"
    else:
        return "LOW"

# Sort the predictions
fatigue_levels = [classify_fatigue(valor) for valor in pred_fatigue]
test_with_pred = test.copy()
test_with_pred['pred_fatigue'] = pred_fatigue
test_with_pred['fatigue_levels'] = fatigue_levels

# Function to apply on new data
def predict_frugal_fatigue(new_data, spent_model, job_model, consumption_model, fatigue_model):
    """Predicts the level of financial fatigue for new consumers.
       The 'new_data' parameter uses the DataFrame with all the necessary variables.
       And return the DataFrame with predictions and fatigue levels.
    """
    # Preparing data for submodels
    X_new_spent = sm.add_constant(new_data[['discretionary_expenses', 'basic_expenses', 'frec_offers', 
                                    'household_income', 'net_debt']])
    X_new_job = sm.add_constant(new_data[['jobs_wanted', 'lost_expectation', 'jobs_lower_status', 
                                    'household_income', 'net_debt']])
    X_new_consumption = sm.add_constant(new_data[['change_brands', 'deferred_purchases', 'change_preferences', 
                                    'household_income', 'net_debt']])
    
    # Subscript Predictions
    pred_spent = spent_model.predict(X_new_spent)
    pred_job = job_model.predict(X_new_job)
    pred_consumption = consumption_model.predict(X_new_consumption)
    
    # Prepare data for the main model
    X_new_fatigue = sm.add_constant(pd.DataFrame({
        'changes_expense': pred_spent,
        'job_search': pred_job,
        'changes_consumption': pred_consumption,
        'household_income': new_data['household_income'].values,
        'net_debt': new_data['net_debt'].values
    }))
    
    # Predicting Frugal Fatigue
    pred_fatigue = fatigue_model.predict(X_new_fatigue)
    
    # Create the results dataframe
    results = new_data.copy()
    results['pred_fatigue'] = pred_fatigue
    results['fatigue_levels'] = [classify_fatigue(valor) for valor in pred_fatigue]
    
    return results

# Use case with new simulated data
new_consumers = pd.DataFrame({
    'household_income': np.random.normal(3000, 1000, 5),
    'net_debt': np.random.normal(10000, 5000, 5),
    'discretionary_expenses': np.random.normal(-300, 500, 5),
    'basic_expenses': np.random.normal(-100, 200, 5),
    'frec_offers': np.random.normal(3, 1, 5),
    'jobs_wanted': np.random.normal(2, 2, 5),
    'lost_expectation': np.random.normal(0.5, 0.5, 5),
    'jobs_lower_status': np.random.normal(0.7, 0.5, 5),
    'change_brands': np.random.normal(0.6, 0.5, 5),
    'deferred_purchases': np.random.normal(0.8, 0.7, 5),
    'change_preferences': np.random.normal(0.5, 0.4, 5)
})

# Get predictions
new_predictions = predict_frugal_fatigue(new_consumers, 
                                                spent_model, 
                                                job_model, 
                                                consumption_model, 
                                                fatigue_model)

# Show results
print("Summary of the Frugal Fatigue Model")
print("\nMain model coefficients:")
print(fatigue_model.summary().tables[1])

print("\nPredictions for new consumers:")
print(new_predictions[['household_income', 'net_debt', 'pred_fatigue', 'fatigue_levels']])
