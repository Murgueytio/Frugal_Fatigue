# Frugal_Fatigue
I propose a simultaneous equations econometric model that captures the multidimensional nature of this phenomenon at the micro and macroeconomic levels.

**1. DATA SIMULATION**

We simulate data to illustrate the model

**2. ESTIMATION OF THE MODELS**

**3. EVALUATION AND PREDICTION**

**4. EARLY WARNING SYSTEM**

![image](https://github.com/user-attachments/assets/da2d0123-1fcc-41a5-baaf-a6629837c689)

**5. NONLINEAR COMPLEXITY AND INTERPRETABILITY**

**5.1. Transformaciones No Lineales con Diagnóstico Visual**

Implementación

**5.2. Generalized Additive Models (GAM)**

Implementation with interpretation

![image](https://github.com/user-attachments/assets/fd03d8dd-b88c-4273-96dd-231cdb7dae34)

![image](https://github.com/user-attachments/assets/f62ee504-4dcb-491e-8379-cf0a0c71076d)

**5.3. IV3SLS**

**Considerations on the Proposed IV3SLS Model** 

**A) Structure of Equations:**

  A.1) Each composite index (changes_expense, job_search, changes_consumption) is modelled as a function of its component variables and the exogenous variables.

  A.2) The target variable (frugal_fatigue) is modelled as a function of the composite indices, which are treated as endogenous and instrumentalised with all exogenous and component variables.

**B) Instrumentalisation:**

  B.1) In the frugal_fatigue equation, the composite indices are treated as endogenous (enclosed in brackets).

  B.2) All component and exogenous variables are used as instruments for these indices.

**C) Prediction Function:**

  C.1) The predict_with_iv3sls() function allows the application of the estimated model to new data.

  C.2) It sequentially predicts the composite indices and then the target variable.

  C.3) It includes the classification of fatigue levels using your original function.

**D) Model Evaluation:**

  D.1) A function is included to evaluate the model on test data.

  D.2) It calculates common metrics such as MSE, RMSE, MAE, and R².

This approach adequately captures the hierarchical structure of the model, where the sub-indices are first calculated and then used to predict frugal fatigue, considering the potential interdependencies between the variables.

![image](https://github.com/user-attachments/assets/4fd7e31a-5028-4763-b0eb-fd55f53c1329)

![image](https://github.com/user-attachments/assets/878d1105-148b-4779-a07b-9b6811724acc)

![image](https://github.com/user-attachments/assets/e3fe1a9b-6935-42d8-9b03-a510cd05c087)

![image](https://github.com/user-attachments/assets/29fc1444-f5e0-4471-a094-cbc00217ff1a)




**6. HYBRIDIZATION INDEX FRUGAL FATIGUE**

**6.1. Non-Parametric Exploratory Phase**

![image](https://github.com/user-attachments/assets/3064a7ba-7ba1-40a5-84a7-a020fe4869ef)

![image](https://github.com/user-attachments/assets/88a86a07-4a3e-4988-b5b8-ceecc973917e)

![image](https://github.com/user-attachments/assets/eb89ec4a-84ef-4898-8d40-9baaa3089656)

![image](https://github.com/user-attachments/assets/52f4c186-d16a-41a6-801c-816b0aa8ab96)

**6.2. Improved Modeling Phase**

![image](https://github.com/user-attachments/assets/c281efe1-bedd-4d31-80ae-f1121432c700)

![image](https://github.com/user-attachments/assets/a87a0d09-e767-4800-94e4-3a07b53af387)

**6.3. Improved Alert System**

![image](https://github.com/user-attachments/assets/e3466e2e-afe2-4531-8252-d672007883fe)

**6.4. Visualization of Results for Interpretation**

![image](https://github.com/user-attachments/assets/691edfb2-1154-4631-8e90-47ac72731af2)

![image](https://github.com/user-attachments/assets/e6eb2e8a-a251-4c6b-a5fb-dc245ea74c30)

**7. ADVANCED VISUALIZATIONS FOR THE FRUGAL FATIGUE MODEL**

**7.1. Relationships Between Variables**

![image](https://github.com/user-attachments/assets/66002d42-2f25-4cb8-9b9d-77d5bb9e7590)

![image](https://github.com/user-attachments/assets/b573fd9e-5022-44d5-b55e-4fadc290237b)

![image](https://github.com/user-attachments/assets/fdab3abe-56e0-4e55-9ca5-7e4c92a8b1d6)

**7.2. Interpretation of the Model



