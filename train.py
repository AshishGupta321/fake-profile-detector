import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("data/dataset.csv")

# Preprocessing (same as before)
df["Created At"] = pd.to_datetime(df["Created At"], errors='coerce')
df["account_age_days"] = (pd.to_datetime("today") - df["Created At"]).dt.days
df["engagement_score"] = df["Retweet Count"] + df["Mention Count"]
df["retweet_per_follower"] = df["Retweet Count"] / (df["Follower Count"] + 1)
df["Verified"] = df["Verified"].astype(int)

# Drop unused columns
df = df.drop([
    "User ID", "Username", "Tweet", "Location", "Hashtags", "Created At"
], axis=1, errors='ignore')

# Features & target
X = df.drop("Bot Label", axis=1)
y = df["Bot Label"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/model.pkl")

print("Model trained and saved!")