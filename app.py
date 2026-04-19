import streamlit as st
import requests

st.title("🤖 Fake Profile Detector")

followers = st.number_input("Followers", min_value=0)
following = st.number_input("Following", min_value=0)
tweets = st.number_input("Total Tweets", min_value=0)
account_age = st.number_input("Account Age (days)", min_value=1)

if st.button("Check"):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json={
                "followers": followers,
                "following": following,
                "tweets": tweets,
                "account_age": account_age
            }
        )

        # 🔥 IMPORTANT CHECK
        if response.status_code != 200:
            st.error("Backend error. Check API.")
            st.write(response.text)
        else:
            result = response.json()

            # ✅ Styled Output
            if result["prediction"] == "Bot":
                st.error(f"⚠️ Bot Detected\nConfidence: {result['confidence']}")
            else:
                st.success(f"✅ Real User\nConfidence: {result['confidence']}")

            # 📊 Graph
            st.subheader("📊 Profile Stats")
            data = {
                "Followers": followers,
                "Following": following,
                "Tweets": tweets
            }
            st.bar_chart(data)

            # 🧠 Explanation
            if result["prediction"] == "Bot":
                st.subheader("🧠 Why this might be a bot:")
                
                if followers < 50:
                    st.write("- Low number of followers")
                if tweets > 100:
                    st.write("- High activity level")
                if following > followers:
                    st.write("- Unusual follower/following ratio")

    except Exception as e:
        st.error(f"Error: {e}")