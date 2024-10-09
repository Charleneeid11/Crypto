import pandas as pd 
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import shap

# Read the CSV file, skipping the first row with numbers
df = pd.read_csv('res.csv', skiprows=1)

# Define categorical columns explicitly
categorical_columns = ['Primitive', 'Implementation', 'Compiler']

# Convert numeric columns explicitly
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
df['Relative time'] = pd.to_numeric(df['Relative time'], errors='coerce')

# Handle missing values for numeric columns only
df.fillna(df.select_dtypes(include=['float64', 'int64']).mean(), inplace=True)

# Initialize LabelEncoders for categorical columns
label_encoders = {}

# Apply Label Encoding to categorical columns if they exist in the DataFrame
for column in categorical_columns:
    if column in df.columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le  # Store the encoder for potential inverse transformation later
    else:
        print(f"Column '{column}' does not exist in the DataFrame.")

# Scenario 1: Time as the target, excluding Relative time as a feature
print("Scenario 1: 'Time' as the target, excluding 'Relative time' as a feature.")
target_column = 'Time'
X = df.drop(['Time', 'Relative time'], axis=1)
y = df[target_column]

# Use regression model for continuous target 'Time'
model = RandomForestRegressor(n_estimators=50, n_jobs=-1)

# Fit the model
model.fit(X, y)

# Get feature importances
importances = model.feature_importances_
feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
feature_importances = feature_importances.sort_values(by='Importance', ascending=False)

# Print the top 10 features for 'Time'
print(f"Top features for {target_column}:")
print(feature_importances.head(10))

# Perform SHAP analysis for interpretability
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X, plot_type="bar")


# Scenario 2: Relative time as the target, excluding Time as a feature
print("\nScenario 2: 'Relative time' as the target, excluding 'Time' as a feature.")
target_column = 'Relative time'
X = df.drop(['Time', 'Relative time'], axis=1)
y = df[target_column]

# Use regression model for continuous target 'Relative time'
model = RandomForestRegressor(n_estimators=50, n_jobs=-1)

# Fit the model
model.fit(X, y)

# Get feature importances
importances = model.feature_importances_
feature_importances = pd.DataFrame({'Feature': X.columns, 'Importance': importances})
feature_importances = feature_importances.sort_values(by='Importance', ascending=False)

# Print the top 10 features for 'Relative time'
print(f"Top features for {target_column}:")
print(feature_importances.head(10))

# Perform SHAP analysis for interpretability
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X, plot_type="bar")
