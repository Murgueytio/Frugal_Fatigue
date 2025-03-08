# FIRST VERSION

from linearmodels.system import IV3SLS
import pandas as pd
import numpy as np
import statsmodels.api as sm

# Define equations for the system
# Level 1: Equations for composite indices
# Level 2: Equation for frugal_fatigue

formulas = {
    'changes_expense': 'changes_expense ~ 1 + discretionary_expenses + basic_expenses + frec_offers + household_income + net_debt',
    
    'job_search': 'job_search ~ 1 + jobs_wanted + lost_expectation + jobs_lower_status + household_income + net_debt',
    
    'changes_consumption': 'changes_consumption ~ 1 + change_brands + deferred_purchases + change_preferences + household_income + net_debt',
    
    # Composite indices are treated as endogenous and instrumentalized with the exogenous variables
    'frugal_fatigue': 'frugal_fatigue ~ 1 + [changes_expense + job_search + changes_consumption ~ discretionary_expenses + basic_expenses + frec_offers + jobs_wanted + lost_expectation + jobs_lower_status + change_brands + deferred_purchases + change_preferences + household_income + net_debt]'
}

# Create and adjust the model
model = IV3SLS.from_formula(formulas, data=data)
results = model.fit(cov_type='robust')

print(results.summary)

# Function to save the results to a file
def save_results_to_file(results, filename='iv3sls_results.txt'):
    with open(filename, 'w') as f:
        f.write(str(results.summary))
    print(f"Results saved in {filename}")

# Save results
save_results_to_file(results)

# Function to predict using the IV3SLS model
def predict_with_iv3sls(new_data, results):
    """
    Make predictions using the estimated IV3SLS model

    Args:
    new_data: DataFrame with the new consumer data
    results: Results of the IV3SLS model

    Returns:
    DataFrame with predictions and fatigue levels
    """
    # Create copy to store results
    predictions = new_data.copy()
    
    # Extract coefficients from each equation
    coefs_expense = results.params['changes_expense']
    coefs_job = results.params['job_search']
    coefs_consumption = results.params['changes_consumption']
    coefs_fatigue = results.params['frugal_fatigue']
    
    # Predict changes_expense
    X_expense = sm.add_constant(new_data[['discretionary_expenses', 'basic_expenses', 'frec_offers', 
                                         'household_income', 'net_debt']])
    predictions['changes_expense'] = X_expense @ coefs_expense
    
    # Predict job_search
    X_job = sm.add_constant(new_data[['jobs_wanted', 'lost_expectation', 'jobs_lower_status', 
                                     'household_income', 'net_debt']])
    predictions['job_search'] = X_job @ coefs_job
    
    # Predict changes_consumption
    X_consumption = sm.add_constant(new_data[['change_brands', 'deferred_purchases', 'change_preferences', 
                                            'household_income', 'net_debt']])
    predictions['changes_consumption'] = X_consumption @ coefs_consumption
    
    # Predict frugal_fatigue using the predicted values
    X_fatigue = sm.add_constant(predictions[['changes_expense', 'job_search', 'changes_consumption']])
    predictions['pred_fatigue'] = X_fatigue @ coefs_fatigue
    
    # Classify fatigue levels using your classify_fatigue function
    predictions['fatigue_levels'] = [classify_fatigue(valor) for valor in predictions['pred_fatigue']]
    
    return predictions

# Example of use with new data and with new_consumers already defined
predicted_results = predict_with_iv3sls(new_consumers, results)

print("\nPredicciones para nuevos consumidores:")
print(predicted_results[['pred_fatigue', 'fatigue_levels']].head())

# Función para evaluar la calidad del modelo en datos de prueba
def evaluate_model(test_data, results):
    """
    Evalúa el modelo en los datos de prueba
    
    Args:
        test_data: DataFrame con datos de prueba
        results: Resultados del modelo IV3SLS
        
    Returns:
        DataFrame con métricas de evaluación
    """
    # Realizar predicciones en datos de prueba
    predictions = predict_with_iv3sls(test_data, results)
    
    # Calcular métricas de error
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    
    mse = mean_squared_error(test_data['frugal_fatigue'], predictions['pred_fatigue'])
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(test_data['frugal_fatigue'], predictions['pred_fatigue'])
    r2 = r2_score(test_data['frugal_fatigue'], predictions['pred_fatigue'])
    
    # Mostrar métricas
    print("\nMétricas de evaluación:")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R²: {r2:.4f}")
    
    return predictions

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

# SECOND VERSION

from linearmodels.system import IV3SLS
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

if data.isnull().sum().sum() > 0:
    raise ValueError("The dataset contains null values, please check before continuing.")

# Define equations for the system

formulas = {
    'changes_expense': 'changes_expense ~ 1 + discretionary_expenses + basic_expenses + frec_offers + household_income + net_debt',
    'job_search': 'job_search ~ 1 + jobs_wanted + lost_expectation + jobs_lower_status + household_income + net_debt',
    'changes_consumption': 'changes_consumption ~ 1 + change_brands + deferred_purchases + change_preferences + household_income + net_debt',
    'frugal_fatigue': 'frugal_fatigue ~ 1 + [changes_expense + job_search + changes_consumption ~ '
                      'discretionary_expenses + basic_expenses + frec_offers + jobs_wanted + '
                      'lost_expectation + jobs_lower_status + change_brands + deferred_purchases + '
                      'change_preferences + household_income + net_debt]'
}

# Create and adjust the model
model = IV3SLS.from_formula(formulas, data=data)
results = model.fit(cov_type='robust')

print(results.summary)

# Save results
def save_results_to_file(results, filename='iv3sls_results.txt'):
    with open(filename, 'w') as f:
        f.write(str(results.summary))
    print(f"Results saved in  {filename}")

save_results_to_file(results)

# Function to predict using the IV3SLS model
def predict_with_iv3sls(new_data, results):
    """
    Make predictions using the estimated IV3SLS model

    Args:
    new_data: DataFrame with the new consumer data
    results: Results of the IV3SLS model

    Returns:
    DataFrame with predictions and fatigue levels
    """
    predictions = new_data.copy()
    
    # Extract coefficients correctly using `LOC`
    coefs_expense = results.params.loc['changes_expense']
    coefs_job = results.params.loc['job_search']
    coefs_consumption = results.params.loc['changes_consumption']
    coefs_fatigue = results.params.loc['frugal_fatigue']

    # Ensure that matrices include a constant
    X_expense = sm.add_constant(new_data[['discretionary_expenses', 'basic_expenses', 'frec_offers', 'household_income', 'net_debt']], has_constant='add')
    predictions['changes_expense'] = X_expense @ coefs_expense

    X_job = sm.add_constant(new_data[['jobs_wanted', 'lost_expectation', 'jobs_lower_status', 'household_income', 'net_debt']], has_constant='add')
    predictions['job_search'] = X_job @ coefs_job

    X_consumption = sm.add_constant(new_data[['change_brands', 'deferred_purchases', 'change_preferences', 'household_income', 'net_debt']], has_constant='add')
    predictions['changes_consumption'] = X_consumption @ coefs_consumption

    # Predict frugal_fatigue
    X_fatigue = sm.add_constant(predictions[['changes_expense', 'job_search', 'changes_consumption']], has_constant='add')
    predictions['pred_fatigue'] = X_fatigue @ coefs_fatigue

    # Classify fatigue levels using the `classify_fatigue` function
    predictions['fatigue_levels'] = predictions['pred_fatigue'].apply(classify_fatigue)

    return predictions

# Example of use with new data
predicted_results = predict_with_iv3sls(new_consumers, results)

print("\nPredictions for new consumers:")
print(predicted_results[['pred_fatigue', 'fatigue_levels']].head())

# Function to evaluate model quality on test data
def evaluate_model(test_data, results):
    """
    Evaluate the model on test data.

    Args:
    test_data: DataFrame with test data.
    results: Results of the IV3SLS model.

    Returns:
    DataFrame with evaluation metrics.
    """
    predictions = predict_with_iv3sls(test_data, results)

    mse = mean_squared_error(test_data['frugal_fatigue'], predictions['pred_fatigue'])
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(test_data['frugal_fatigue'], predictions['pred_fatigue'])
    r2 = r2_score(test_data['frugal_fatigue'], predictions['pred_fatigue'])

    print("\nMétricas de evaluación:")
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R²: {r2:.4f}")

    return predictions

predicted_test = evaluate_model(test_data, results)
