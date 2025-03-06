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

# Identify thresholds using simple decision trees to find inflection points
dt = DecisionTreeRegressor(max_depth=3, min_samples_leaf=50)
dt.fit(data[variables], data['frugal_fatigue'])

plt.figure(figsize=(20, 10))
plot_tree(dt, feature_names=variables, filled=True, rounded=True, fontsize=10)
plt.savefig('Tree Thresholds.png')
plt.close()

# Extracting thresholds from trees
def extract_thresholds(tree, feature_names):
    thresholds = {name: [] for name in feature_names}
    
    def extract_recursive(node_id=0):
        if tree.children_left[node_id] != -1:  # No es una hoja
            feature = feature_names[tree.feature[node_id]]
            threshold = tree.threshold[node_id]
            thresholds[feature].append(threshold)
            
            extract_recursive(tree.children_left[node_id])
            extract_recursive(tree.children_right[node_id])
    
    extract_recursive()
    return {k: sorted(set(v)) for k, v in thresholds.items() if v}

umbrales = extract_thresholds(dt.tree_, variables)
print("Thresholds identified in key variables:")
for var, thresholds in umbrales.items():
    print(f"{var}: {thresholds}")

# Segmentation by clustering for different fatigue profiles with normalized variables
X_cluster = data[variables].copy()
scaler = StandardScaler()
X_cluster_scaled = scaler.fit_transform(X_cluster)

# Finding the optimal number of clusters using the 'Elbow Method'
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_cluster_scaled)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertias, 'bx-')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.title('Elbow Method for determining optimal k')
plt.savefig('K-Means Elbow Method.png')
plt.close()

# Apply K-Means with k=3 (or the optimum according to the graph)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
data['cluster'] = kmeans.fit_predict(X_cluster_scaled)

# Characterize each cluster
cluster_stats = data.groupby('cluster')[variables + ['frugal_fatigue']].mean()
print("\nCustomer profiles by cluster:")
print(cluster_stats)

# Visualize the distribution of frugal fatigue by cluster
plt.figure(figsize=(12, 6))
for i in range(n_clusters):
    sns.kdeplot(data[data['cluster'] == i]['frugal_fatigue'], 
                label=f'Cluster {i}')
plt.xlabel('Frugal Fatigue Index')
plt.ylabel('Density')
plt.title('Distribution of Frugal Fatigue by Cluster')
plt.legend()
plt.savefig('Distribution Fatigue Clusters.png')
plt.close()
