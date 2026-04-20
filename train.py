import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load data
df = pd.read_csv("data/dataset.csv")

# Convert boolean to int
df["Verified"] = df["Verified"].astype(int)

# 🔥 Feature Engineering (IMPORTANT)

# Log transformations (better than raw counts)
df["log_followers"] = df["Follower Count"].apply(lambda x: 0 if x == 0 else math.log(x))
df["retweet_log"] = df["Retweet Count"].apply(lambda x: math.log(x + 1))
df["mention_log"] = df["Mention Count"].apply(lambda x: math.log(x + 1))

# Engagement feature
df["engagement"] = (df["Retweet Count"] + df["Mention Count"]) / (df["Follower Count"] + 1)

# Features & target
X = df[[
    "Verified",
    "log_followers",
    "retweet_log",
    "mention_log",
    "engagement"
]]

y = df["Bot Label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔥 Improved model
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
joblib.dump(model, "models/model.pkl")

print("Model trained and saved!")