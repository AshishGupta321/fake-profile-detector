import streamlit as st
import requests
import math

st.title("🤖 Fake Profile Detector")

# Inputs
verified = st.selectbox("Verified Account", [0, 1])
followers = st.number_input("Follower Count", min_value=0)
retweets = st.number_input("Retweet Count", min_value=0)
mentions = st.number_input("Mention Count", min_value=0)

# Feature engineering (same as train.py)
log_followers = 0 if followers == 0 else math.log(followers)
retweet_log = math.log(retweets + 1)
mention_log = math.log(mentions + 1)
engagement = (retweets + mentions) / (followers + 1)

if st.button("Check"):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json={
                "Verified": verified,
                "log_followers": log_followers,
                "retweet_log": retweet_log,
                "mention_log": mention_log,
                "engagement": engagement
            }
        )

        if response.status_code != 200:
            st.error("Backend error")
            st.write(response.text)
        else:
            result = response.json()

            # Output
            if result["prediction"] == 1:
                st.error("🚨 Bot Detected")
            else:
                st.success("✅ Real User")

            # 📊 Graph
            st.subheader("📊 Activity Stats")
            st.bar_chart({
                "Followers": followers,
                "Retweets": retweets,
                "Mentions": mentions
            })

            # 🧠 Explanation
            if result["prediction"] == 1:
                st.subheader("🧠 Possible reasons:")
                if followers < 50:
                    st.write("- Low followers")
                if retweets > 100:
                    st.write("- High retweet activity")
                if mentions > 50:
                    st.write("- High mention activity")

    except Exception as e:
        st.error(f"Error: {e}")