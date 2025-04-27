import streamlit as st
import pandas as pd
import os
import base64

# Define the base directory where images are stored
BASE_DIR = "D:/Data Science Project/game platform"

# Load dataset with correct encoding
df = pd.read_csv(os.path.join(BASE_DIR, "game_dataset.csv"), encoding="ISO-8859-1")

# Function to get local image path
def get_image_path(image_filename):
    image_path = os.path.join(BASE_DIR, os.path.basename(image_filename))
    return image_path if os.path.exists(image_path) else None

# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set Background Image
BACKGROUND_IMAGE = "back.jpg"
background_path = os.path.join(BASE_DIR, BACKGROUND_IMAGE)
if os.path.exists(background_path):
    base64_bg = get_base64_image(background_path)
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{base64_bg}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar background image styling
SIDEBAR_IMAGE = "4.jpg"
sidebar_path = os.path.join(BASE_DIR, SIDEBAR_IMAGE)
if os.path.exists(sidebar_path):
    base64_sidebar = get_base64_image(sidebar_path)
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/jpg;base64,{base64_sidebar}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar content
st.sidebar.title("🎮 Gaming Platform")

st.sidebar.markdown("""
<div style='color:white; font-size:16px; line-height:1.6; text-align:justify;'>
Welcome to the ultimate <b>Retro & Modern Game Hub</b> – your one-stop destination to discover, download, and enjoy legendary games right on your device!

Whether you're a nostalgic gamer or a modern arcade fan, we've got something epic for you. 🎉
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### ✨ Key Features")
st.sidebar.markdown("""
- 🔍 **Explore** a curated collection of classic and trending games  
- ⚡ **Quick Download** and easy install process  
- 🤖 **Smart Suggestions** based on your game interest  
""")

st.sidebar.markdown("### 🎮 How to Play")
st.sidebar.markdown("""
1. 📥 **Download** the game zip file from the button below the game description  
2. 📂 **Extract** the zip file into a folder named after the game  
3. 📱 **Install PPSSPP App** to run the game [Download here](https://www.ppsspp.org/)  
4. 📤 **Import the extracted game** into the PPSSPP application  
5. 🎉 **Start Playing and Enjoy!**
""")

st.sidebar.markdown("### 💡 Pro Tips")
st.sidebar.markdown("""
- 🕹️ Use a above 4GB Ram Device for smoother gameplay  
- 🌐 Ensure internet for downloading and updates  
- 💬 Download Multiple Game And Run at a Time!  
""")

# Custom Styling
st.markdown(
    """
    <style>
        .main-header {
            background-color: white;
            padding: 20px;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: black;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .main-footer {
            background-color: white;
            padding: 15px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            color: black;
            border-radius: 10px;
            position: fixed;
            bottom: 0;
            width: 100%;
            left: 0;
        }
        .stButton > button {
            width: 100%;
        }
        .download-button {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        .game-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        .game-description-title {
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin-top: 20px;
        }
        .game-title {
            text-align: center;
            font-size: 26px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("<div class='main-header'>Gaming Platform</div>", unsafe_allow_html=True)

# Initialize session state
if "selected_game" not in st.session_state:
    st.session_state.selected_game = df["Game Name"].tolist()[0]

# Game selection
game_names = df["Game Name"].tolist()
selected_game = st.selectbox("Select a Game", game_names, index=game_names.index(st.session_state.selected_game), key="game_select")
st.session_state.selected_game = selected_game

# Display game details
def display_game_details(game_name):
    game_info = df[df["Game Name"] == game_name].iloc[0]

    st.markdown(f"<div class='game-title'>{game_info['Game Name']}</div>", unsafe_allow_html=True)

    image_path = get_image_path(game_info["Profile Image URL"])
    if image_path:
        st.image(image_path, caption=game_info["Game Name"], use_container_width=True)
    else:
        st.warning("Image not found!")

    st.markdown("<div class='game-description-title'>Description</div>", unsafe_allow_html=True)
    st.write(game_info["Description"])

    st.markdown(
        f"""
        <div class='download-button'>
            <a href='{game_info['Download Link']}' target='_blank'>
                <button style='background-color:#4CAF50;color:white;padding:10px 20px;border:none;border-radius:5px;font-size:16px;'>
                    Download Here
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display selected game details
display_game_details(st.session_state.selected_game)

# Suggest similar games
st.subheader("You May Also Like")
similar_games = df[df["Genre"] == df[df["Game Name"] == st.session_state.selected_game].iloc[0]["Genre"]]
similar_games = similar_games.sample(n=min(4, len(similar_games)), replace=False)

cols = st.columns(4)
for idx, (_, row) in enumerate(similar_games.iterrows()):
    with cols[idx]:
        image_path = get_image_path(row["Profile Image URL"])
        if st.button(row['Game Name'], key=f"btn_{row['Game Name']}"):
            st.session_state.selected_game = row['Game Name']
            st.rerun()
        if image_path:
            st.image(image_path, caption=row["Game Name"], width=150)

# Additional row for random game suggestions
st.subheader("Explore More Games")
random_games = df.sample(n=min(8, len(df)), replace=False)
random_rows = [random_games.iloc[i:i+4] for i in range(0, len(random_games), 4)]

for row_games in random_rows:
    cols = st.columns(len(row_games))
    for idx, (_, row) in enumerate(row_games.iterrows()):
        with cols[idx]:
            image_path = get_image_path(row["Profile Image URL"])
            if st.button(row['Game Name'], key=f"rand_btn_{row['Game Name']}"):
                st.session_state.selected_game = row['Game Name']
                st.rerun()
            if image_path:
                st.image(image_path, caption=row["Game Name"], width=150)

# Footer
st.markdown("<div class='main-footer' style='text-align: center; width: 100%;'>© 2025 Gaming Platform. Explore, Play, Enjoy!</div>", unsafe_allow_html=True)