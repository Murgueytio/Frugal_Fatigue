percentiles = [70, 90]  
percentile_thresholds = np.percentile(pred_train, percentiles)

def classify_fatigue_percentile(fatigue_value, thresholds):
    if fatigue_value > thresholds[1]:
        return "HIGH"
    elif fatigue_value > thresholds[0]:
        return "MEAN"
    else:
        return "LOW"

# Complementary risk analysis
dt_risk = DecisionTreeRegressor(max_depth=5, min_samples_leaf=30)
dt_risk.fit(X_train, y_train)

# Function to predict risk
def predict_risk_detailed(new_data, gam_model, linear_model, dt_risk, 
                             scaler, kmeans, poly, variables, percentile_thresholds):
    """
    Predicts the frugal fatigue level where the

    Parameter: 
    new_data: DataFrame with all the necessary variables

    Return:
    the DataFrame with predictions, risk levels and contributing factors
    """
    # Prepare data
    X_new = new_data[variables].copy()
    
    # Base predictions with the tree (for explanations)
    pred_tree = dt_risk.predict(X_new)
    
    # Assign cluster
    clusters = kmeans.predict(scaler.transform(X_new))
    
    # Improve data with transformations applied to the final model
    X_new_enhanced = pd.DataFrame(X_new).copy()
    X_new_enhanced['cluster'] = clusters
    
    # Add terms based on thresholds
    for var in umbrales:
        for threshold in umbrales[var]:
            X_new_enhanced[f"{var}_mayor_{threshold:.0f}"] = (X_new_enhanced[var] > threshold).astype(int)
            
            for other_var in variables:
                if other_var != var:
                    X_new_enhanced[f"{var}_mayor_{threshold:.0f}_{other_var}"] = X_new_enhanced[f"{var}_mayor_{threshold:.0f}"] * X_new_enhanced[other_var]
    
    # Adding cluster interactions
    for i in range(n_clusters):
        for var in variables:
            X_new_enhanced[f'cluster_{i}_{var}'] = (X_new_enhanced['cluster'] == i).astype(int) * X_new_enhanced[var]
    
    # Select significant variables
    X_new_sign = sm.add_constant(X_new_enhanced[significant_features.drop('const')])
    
    # Linear prediction
    pred_linear = final_model.predict(X_new_sign)
    
    # GAM Prediction
    pred_gam = gam_model.predict(X_nuevos)
    
    # Averaging predictions (simple ensemble)
    pred_final = (pred_linear + pred_gam) / 2
    
    # Classify the level
    levels = [classify_fatigue_percentile(valor, percentile_thresholds) for valor in pred_final]
    
    # Identify the main factors (using model coefficients)
    main_factors = []
    for i, row in X_new_enhanced.iterrows():
        # Calculate contribution of each variable
        contribution = {}
        for var in variables:
            contribution = final_model.params.get(var, 0) * row.get(var, 0)
            contributions[var] = contribution
            
            # Adding contributions from derived terms
            for col in X_new_sign.columns:
                if var in col and col != var:
                    contribution += final_model.params.get(col, 0) * row.get(col, 0)
                    contributions[var] = contribution
        
        # Sort by importance
        sorted_contrib = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
        factors = [f"{k} ({v:.2f})" for k, v in sorted_contrib[:3]]
        main_factors.append(", ".join(factors))
    
    # Create the results dataframe
    results = new_data.copy()
    results['fatiga_pred'] = pred_final
    results['nivel_fatiga'] = levels
    results['main_factors'] = main_factors
    results['cluster'] = clusters
    
    return results

# Example of use with new simulated data
new_consumers = pd.DataFrame({
    'household_income': np.random.normal(3000, 1000, 5),
    'net_debt': np.random.normal(10000, 5000, 5),
    'changes_expense': np.random.normal(0, 200, 5),
    'job_search': np.random.normal(0, 1, 5),
    'changes_consumption': np.random.normal(0, 1, 5),
})

detailed_predictions = predict_risk_detailed(new_data,
                                              gam_model,
                                              linear_model,
                                              dt_risk,
                                              scaler,
                                              kmeans,
                                              poly,
                                              variables,
                                              percentile_thresholds)

print("\nDetailed predictions for new consumers:")
print(detailed_predictions[['household_income', 'net_debt', 'fatiga_pred', 
                             'nivel_fatiga', 'cluster', 'main_factors']])
