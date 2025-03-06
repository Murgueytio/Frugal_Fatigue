import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.inspection import permutation_importance
import shap
from lime import lime_tabular

def exploratory_visualizations(data, variables, save_path=None):
    """
    Create exploratory visualizations to better understand the relationships between the variables of the frugal fatigue model.
    """

    main_variables = variables + ['frugal_fatigue']
    g = sns.pairplot(data[main_variables], 
                    diag_kind="kde", 
                    plot_kws={'alpha': 0.6, 's': 30, 'edgecolor': 'k'},
                    height=2.5)
    g.fig.suptitle('Relationships between Variables and Frugal Fatigue', y=1.02, fontsize=16)
    if save_path:
        plt.savefig(f"{save_path}/pairplot_variables.png", bbox_inches='tight')
    plt.close()

main_variables = variables + ['frugal_fatigue'] 

plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(data[main_variables].corr(), dtype=bool))
custom_cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(data[main_variables].corr(), 
           mask=mask, 
           cmap=custom_cmap, 
           vmax=1, 
           vmin=-1, 
           center=0,
           square=True, 
           linewidths=.5, 
           cbar_kws={"shrink": .5}, 
           annot=True, 
           fmt='.2f')
plt.title('Correlation Matrix between Variables', fontsize=16)

plt.show()

# Boxplots of frugal fatigue by income and debt quartiles
fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# Income quartiles
data['income_quartiles'] = pd.qcut(data['household_income'], 4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'])
sns.boxplot(x='income_quartiles', y='frugal_fatigue', data=data, ax=axes[0], palette='Blues')
axes[0].set_title('Frugal Fatigue by Income Quartile', fontsize=14)
axes[0].set_xlabel('Income Quartiles')  
axes[0].set_ylabel('Frugal Fatigue Index')

# Debt Quartiles
data['debt_quartiles'] = pd.qcut(data['net_debt'], 4, labels=['Q1 (Low)', 'Q2', 'Q3', 'Q4 (High)'])
sns.boxplot(x='debt_quartiles', y='frugal_fatigue', data=data, ax=axes[1], palette='Reds')
axes[1].set_title('Frugal Fatigue by Debt Quartile', fontsize=14)
axes[1].set_xlabel('Debt Quartiles')
axes[1].set_ylabel('Frugal Fatigue Index')
    
plt.tight_layout()

plt.show()

# 3D visualization of the 3 most important variables
correlations = data[variables].corrwith(data['frugal_fatigue']).abs().sort_values(ascending=False)
top3_vars = correlations.index[:3].tolist()
    
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')
    
scatter = ax.scatter(data[top3_vars[0]], 
                    data[top3_vars[1]], 
                    data[top3_vars[2]],
                    c=data['frugal_fatigue'], 
                    cmap='plasma', 
                    s=40, 
                    alpha=0.7)
    
ax.set_xlabel(top3_vars[0])
ax.set_ylabel(top3_vars[1])
ax.set_zlabel(top3_vars[2])
plt.colorbar(scatter, label='Frugal Fatigue', pad=0.1)
plt.title(f'3D Relationship between the Most Important Variables', fontsize=16)
    
plt.show()

def visualizations_interpretation(model, X_train, X_test, y_train, y_test, variables, save_path=None):
    """
    Visualizations that help interpret the frugal fatigue model.
    """
    # Standardized coefficients
    if hasattr(model, 'params'):
        # Statsmodels Model
        coefs = model.params[1:] # Exclude constant
        std_coefs = coefs * X_train.std()[coefs.index]
        importances = pd.Series(std_coefs.abs(), index=coefs.index).sort_values(ascending=False)
        
        plt.figure(figsize=(12, 8))
        importances.head(15).plot(kind='barh', color='skyblue')
        plt.title('Importance of Variables (Standardized Coefficients)', fontsize=16)
        plt.xlabel('Importance')
        plt.tight_layout()
        if save_path:
            plt.savefig(f"{save_path}/Importance Variables.png", bbox_inches='tight')
        plt.close()
    else:
        # Scikit-learn Model with feature importances
        if hasattr(model, 'feature_importances_'):
            importances = pd.Series(model.feature_importances_, index=variables).sort_values(ascending=False)
            
            plt.figure(figsize=(12, 8))
            importances.plot(kind='barh', color='skyblue')
            plt.title('Importance Variables', fontsize=16)
            plt.xlabel('Importance')
            plt.tight_layout()
            if save_path:
                plt.savefig(f"{save_path}/Importance Variables.png", bbox_inches='tight')
            plt.close()
        else:
        # Permutation 
            result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
            importances = pd.Series(result.importances_mean, index=variables).sort_values(ascending=False)
            
            plt.figure(figsize=(12, 8))
            importances.plot(kind='barh', color='skyblue')
            plt.title('Importance of Variables (Permutation Importance)', fontsize=16)
            plt.xlabel('Importance')
            plt.tight_layout()
            if save_path:
                plt.savefig(f"{save_path}/Importance Variables.png", bbox_inches='tight')
            plt.close()
    
    # Model Residuals
    if hasattr(model, 'predict'):
        y_pred = model.predict(X_test)
        residuals = y_test - y_pred
        
        plt.figure(figsize=(12, 8))
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='-')
        plt.title('Residuals vs Predicted Values', fontsize=16)
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        if save_path:
            plt.savefig(f"{save_path}/Residuals vs Predicted Values.png", bbox_inches='tight')
        plt.close()
        
        # QQ-Plot Residuals
        plt.figure(figsize=(12, 8))
        sm.qqplot(residuals, line='45', fit=True)
        plt.title('QQ-Plot Residuals', fontsize=16)
        plt.tight_layout()
        if save_path:
            plt.savefig(f"{save_path}/QQ-Plot Residuals.png", bbox_inches='tight')
        plt.close()
        
        # Histogram of Residuals
        plt.figure(figsize=(12, 8))
        sns.histplot(residuals, kde=True, bins=30)
        plt.axvline(x=0, color='r', linestyle='--')
        plt.title('Residuals Distribution', fontsize=16)
        plt.xlabel('Residuals')
        plt.ylabel('Frecuencia')
        if save_path:
            plt.savefig(f"{save_path}/Histogram of Residuals.png", bbox_inches='tight')
        plt.close()
    
    return importances
