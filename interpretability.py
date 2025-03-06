import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess

# Example of a LOWESS chart for income and fatigue
plt.figure(figsize=(10, 6))
sns.scatterplot(x='household_income', y='frugal_fatigue', data=data, alpha=0.5)
lowess_line = lowess(data['frugal_fatigue'], data['household_income'], frac=0.3)
plt.plot(lowess_line[:, 0], lowess_line[:, 1], 'r-', linewidth=3)
plt.title('Income-Fatigue Ratio with LOWESS Smoothing')
plt.show()

# Define X and Y using the same variables as the original model
X_fatigue_train = sm.add_constant(train[['changes_expense', 'job_search', 'changes_consumption', 
                                      'household_income', 'net_debt']])
y_fatigue_train = train['frugal_fatigue']

X_fatigue_test = sm.add_constant(test[['changes_expense', 'job_search', 'changes_consumption', 
                                    'household_income', 'net_debt']])
y_fatigue_test = test['frugal_fatigue']

from pygam import LinearGAM, s, l   # s() for splines, l() for linear terms

# GAM model for the main index
gam_model = LinearGAM(s(0) + s(1) + s(2) + l(3) + l(4))
gam_model.fit(X_fatigue_train.drop(columns=['const']), y_fatigue_train)  # Remove constant from statsmodels

# Visualization of partial effects
plt.figure(figsize=(12, 8))
titles = ['Changes Expense', 'Job Search', 'Cchanges Consumption', 'Household Income', 'Net Debt']

for i, term in enumerate(gam_model.terms):
    if term.isintercept:
        continue
    
    XX = gam_model.generate_X_grid(term=i)
    plt.plot(XX[:, i], gam_model.partial_dependence(term=i, X=XX))
    plt.title(f'Nonlinear effect of {titles[i]}')
    plt.xlabel(titles[i])
    plt.ylabel('Effect on Frugal Fatigue')
    plt.show()

