# Frugal_Fatigue
I propose a simultaneous equations econometric model that captures the multidimensional nature of this phenomenon at the micro and macroeconomic levels.

**1. DATA SIMULATION**

We simulate data to illustrate the model

**2. ESTIMATION OF THE MODELS**

**3. EVALUATION AND PREDICTION**

**4. EARLY WARNING SYSTEM**

Summary of the Frugal Fatigue Model

Main model coefficients:
=======================================================================================
                          coef    std err          t      P>|t|      [0.025      0.975]
---------------------------------------------------------------------------------------
const                   5.1259      7.123      0.720      0.472      -8.859      19.111
changes_expense         0.3925      0.009     43.968      0.000       0.375       0.410
job_search              1.1368      1.828      0.622      0.534      -2.453       4.727
changes_consumption     6.9290      5.372      1.290      0.198      -3.618      17.476
household_income        0.0008      0.003      0.301      0.763      -0.004       0.006
net_debt               -0.0005      0.001     -0.877      0.381      -0.002       0.001
=======================================================================================

Predictions for New Consumers:
   household_income      net_debt  pred_fatigue fatigue_levels
0       1636.148343   8593.787590    -72.108837            LOW
1       2405.237184   6361.701450    147.209468           MEAN
2       4143.790523   7244.988869    139.784640           MEAN
3       1902.466907  13049.298415   -168.200393            LOW
4       2537.904779   8506.633288     44.952208            LOW


