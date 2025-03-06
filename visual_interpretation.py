# Scatter plot with predictions colored by risk level
plt.figure(figsize=(12, 8))
scatter = plt.scatter(test['household_income'], test['net_debt'], 
                     c=pred_test, cmap='RdYlGn_r', alpha=0.7)
plt.colorbar(scatter, label='Frugal Fatigue Index')
plt.xlabel('Household Income')
plt.ylabel('Net Debt')
plt.title('Frugal Fatigue Risk Map')
plt.savefig('Frugal Fatigue Risk Map.png')
plt.close()

# Heatmap of correlation between original and transformed variables
variables_importantes = list(significant_features.drop('const'))[:2]  # First 2 variables
corr_matrix = X_train_enhanced[variables_importantes].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation between Important Variables')
plt.tight_layout()
plt.savefig('Correlation Variables.png')
plt.close()

print("\nHybrid Model for Completed Frugal Fatigue Index.")
