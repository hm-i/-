import streamlit as st

# ログイン設定（省略可）
USERNAME = "Syny.jpd"
PASSWORD = "dance2025syny"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_login():
    st.title("🔐 ログイン")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
        else:
            st.error("ユーザー名またはパスワードが違います")

if not st.session_state["authenticated"]:
    check_login()
    st.stop()

# メンバーと曲データ
all_members = ["ゆう", "まこ", "ちさと", "こゆ", "ひな", "しおん", "そら", "なるみ", "ありさ", "ひまり",
               "ひじり", "まあや", "ともか", "はるか", "こゆき", "まい", "ゆー", "あんな", "はる"]

songs = {
    "カチューシャ": {"こゆ", "まこ", "ちさと", "ゆう", "しおん", "そら", "なるみ", "ありさ", "ひな", "ひじり"},
    "君好き": {"ひな", "しおん", "ゆう", "まあや", "こゆ"},
    # ...以下省略
}

st.title("🎵 出席チェッカー（色付き）")

# 出席状態
if "selected_members" not in st.session_state:
    st.session_state["selected_members"] = set()

st.markdown("## ✅ 出席者をタップ")

cols = st.columns(4)
for i, name in enumerate(all_members):
    col = cols[i % 4]
    selected = name in st.session_state["selected_members"]
    style = """
        background-color:#d0f0ff;
        padding:8px;
        border-radius:10px;
        text-align:center;
        cursor:pointer;
        font-weight:bold;
    """ if selected else """
        background-color:#f0f0f0;
        padding:8px;
        border-radius:10px;
        text-align:center;
        cursor:pointer;
    """
    if col.button(f"{'✅' if selected else '⬜'} {name}", key=name):
        if selected:
            st.session_state["selected_members"].remove(name)
        else:
            st.session_state["selected_members"].add(name)
    # 色付き表示
    col.markdown(f"<div style='{style}'>{'✅' if selected else '⬜'} {name}</div>", unsafe_allow_html=True)

# 出席メンバー表示
selected_members = st.session_state["selected_members"]

if selected_members:
    st.markdown("---")
    st.markdown("## 🧑‍🤝‍🧑 出席メンバー")
    st.write("、".join(sorted(selected_members)))

    st.markdown("## 🏆 出席ランキング")
    ranking = []
    for song, members in songs.items():
        attend = members & selected_members
        total = len(members)
        ranking.append((song, len(attend), total, len(attend) / total if total else 0))
    ranking.sort(key=lambda x: x[1], reverse=True)
    for song, count, total, rate in ranking:
        st.write(f"🎵 {song}: {count}/{total}人（{rate:.0%}）")

    st.markdown("## 📋 曲ごとの出席")
    for song, members in songs.items():
        attending = members & selected_members
        absent = members - selected_members
        st.subheader(f"{song}")
        st.write(f"👥 全体: {len(members)}人")
        st.write(f"✅ 出席: {'、'.join(sorted(attending)) or 'なし'}")
        st.write(f"❌ 不在: {'、'.join(sorted(absent)) or 'なし'}")
