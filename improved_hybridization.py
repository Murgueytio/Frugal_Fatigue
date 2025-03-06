# Prepare variables to include identified nonlinearities
X_train = train[variables].copy()
X_test = test[variables].copy()
y_train = train['frugal_fatigue']
y_test = test['frugal_fatigue']

# Create polynomial terms to capture specific nonlinearities
# Based on the identified thresholds, we add quadratic terms
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

poly_feature_names = poly.get_feature_names_out(X_train.columns)

# GAM model for identified nonlinear components
# s() for splines, l() for linear terms
gam_model = LinearGAM(s(0, n_splines=8) +  # changes_expense (spline)
                      s(1, n_splines=8) +  # job_search (spline)
                      s(2, n_splines=8) +  # changes_consumption (spline)
                      s(3, n_splines=10) + # household_income (spline)
                      s(4, n_splines=10))  # net_debt (spline)

gam_model.fit(X_train, y_train)
gam_pred_train = gam_model.predict(X_train)
gam_pred_test = gam_model.predict(X_test)

print("\nGAM Model Summary")
print(f"R² in training: {r2_score(y_train, gam_pred_train):.4f}")
print(f"R² in test: {r2_score(y_test, gam_pred_test):.4f}")
print(f"MSE in test: {mean_squared_error(y_test, gam_pred_test):.4f}")

# Visualize partial effects of GAM
plt.figure(figsize=(15, 12))
for i, term in enumerate(gam_model.terms):
    if term.isintercept:
        continue
    
    plt.subplot(2, 3, i+1)
    XX = gam_model.generate_X_grid(term=i)
    plt.plot(XX[:, i], gam_model.partial_dependence(term=i, X=XX))
    plt.title(f'Partial Effect: {variables[i]}')
    plt.xlabel(variables[i])
    plt.ylabel('Effect on Frugal Fatigue')

plt.tight_layout()
plt.savefig('Partial Effects GAM.png')
plt.close()

# Apply scikit-learn for interpretable parametric model incorporating GAM features
X_train_enhanced = pd.DataFrame(X_train).copy()
X_test_enhanced = pd.DataFrame(X_test).copy()

# For each variable, add terms for the identified inflection points
for var in umbrales:
    idx = variables.index(var)
    for threshold in umbrales[var]:
        # Binary variables for each threshold
        X_train_enhanced[f"{var}_major_{threshold:.0f}"] = (X_train_enhanced[var] > threshold).astype(int)
        X_test_enhanced[f"{var}_major_{threshold:.0f}"] = (X_test_enhanced[var] > threshold).astype(int)
        
        # Interaction with other key variables
        for other_var in variables:
            if other_var != var:
                X_train_enhanced[f"{var}_major_{threshold:.0f}_{other_var}"] = X_train_enhanced[f"{var}_major_{threshold:.0f}"] * X_train_enhanced[other_var]
                X_test_enhanced[f"{var}_major_{threshold:.0f}_{other_var}"] = X_test_enhanced[f"{var}_major_{threshold:.0f}"] * X_test_enhanced[other_var]

# Add cluster as categorical variable
X_train_enhanced['cluster'] = train['cluster'] if 'cluster' in train.columns else kmeans.predict(scaler.transform(X_train))
X_test_enhanced['cluster'] = test['cluster'] if 'cluster' in test.columns else kmeans.predict(scaler.transform(X_test))

# Adding cluster interactions with main variables
for i in range(n_clusters):
    for var in variables:
        X_train_enhanced[f'cluster_{i}_{var}'] = (X_train_enhanced['cluster'] == i).astype(int) * X_train_enhanced[var]
        X_test_enhanced[f'cluster_{i}_{var}'] = (X_test_enhanced['cluster'] == i).astype(int) * X_test_enhanced[var]

# Compare models
# Linear Model. Ordinary Least Squares (OLS)
X_train_sm = sm.add_constant(X_train_enhanced)
X_test_sm = sm.add_constant(X_test_enhanced)
linear_model = sm.OLS(y_train, X_train_sm).fit()

# Selection of significant variables
pvalues = linear_model.pvalues
significant_features = pvalues[pvalues < 0.05].index
print(f"\nSignificant variables ({len(significant_features)}):")
print(significant_features.tolist())

# OLS model with significant variables
X_train_sig = sm.add_constant(X_train_enhanced[significant_features.drop('const')])
X_test_sig = sm.add_constant(X_test_enhanced[significant_features.drop('const')])
final_model = sm.OLS(y_train, X_train_sig).fit()

# Evaluate the final model
pred_train = final_model.predict(X_train_sig)
pred_test = final_model.predict(X_test_sig)

print("\nSummary of the final parametric model:")
print(f"R² in training: {r2_score(y_train, pred_train):.4f}")
print(f"R² in test: {r2_score(y_test, pred_test):.4f}")
print(f"MSE in test: {mean_squared_error(y_test, pred_test):.4f}")

print("\nFinal Model Coefficients:")
print(final_model.summary().tables[1])

# Comparing both models: GAM versus improved OLS
print("\nModel Comparison:")
print(f"GAM - R² test: {r2_score(y_test, gam_pred_test):.4f}, MSE test: {mean_squared_error(y_test, gam_pred_test):.4f}")
print(f"OLS - R² test: {r2_score(y_test, pred_test):.4f}, MSE test: {mean_squared_error(y_test, pred_test):.4f}")
