import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import partial_dependence, PartialDependenceDisplay
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeRegressor, plot_tree
from statsmodels.nonparametric.smoothers_lowess import lowess
from pygam import LinearGAM, s, l, f

# Visualizing non-linear relationships with LOWESS
plt.figure(figsize=(15, 10))

variables = ['changes_expense', 'job_search', 'changes_consumption', 'household_income', 'net_debt']

for i, var in enumerate(variables):
    plt.subplot(2, 3, i+1)
    sns.scatterplot(x=var, y='frugal_fatigue', data=data, alpha=0.4)
    
    # LOWESS adjustment for each variable
    lowess_result = lowess(data['frugal_fatigue'], data[var], frac=0.3)
    plt.plot(lowess_result[:, 0], lowess_result[:, 1], 'r-', linewidth=2)
    
    plt.title(f'Relation {var} and fatigue')
    plt.tight_layout()

plt.savefig('Nonlinear Relationship.png')
plt.close()
