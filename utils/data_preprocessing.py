import pandas as pd

df = pd.read_csv("data/dataset.csv")

# Drop useless columns
df = df.drop([
    "User ID",
    "Username",
    "Tweet",
    "Location",
    "Hashtags"
], axis=1)
# Convert date → account age
df["Created At"] = pd.to_datetime(df["Created At"], errors='coerce')
df["account_age_days"] = (pd.to_datetime("today") - df["Created At"]).dt.days

# Engagement
df["engagement_score"] = df["Retweet Count"] + df["Mention Count"]

# Ratio
df["retweet_per_follower"] = df["Retweet Count"] / (df["Follower Count"] + 1)
df["Verified"] = df["Verified"].astype(int)
df = df.drop(["Created At"], axis=1)


print(df.columns)