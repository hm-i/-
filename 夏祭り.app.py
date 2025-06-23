import streamlit as st

# ログイン情報（省略可）
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

# メンバーリスト
all_members = ["ゆう", "まこ", "ちさと", "こゆ", "ひな", "しおん", "そら", "なるみ", "ありさ", "ひまり",
               "ひじり", "まあや", "ともか", "はるか", "こゆき", "まい", "ゆー", "あんな", "はる"]

# 曲ごとの出演者
songs = {
    "カチューシャ": {"こゆ", "まこ", "ちさと", "ゆう", "しおん", "そら", "なるみ", "ありさ", "ひな", "ひじり"},
    "君好き": {"ひな", "しおん", "ゆう", "まあや", "こゆ"},
    "怪盗少女": {"こゆ", "ともか", "ちさと", "ありさ", "ひな"},
    "サイクロン": {"しおん", "ちさと", "ともか", "はるか", "ひじり", "ゆう", "そら", "なるみ"},
    "After like": {"ひまり", "ちさと", "まこ", "こゆき", "まい", "はる"},
    "come again": {"しおん", "まこ", "こゆき"},
    "裸足でsummer": {"まこ", "ちさと", "あんな", "ゆう", "なるみ", "ひな", "ありさ"},
    "ドリアン少年": {"まあや", "ちさと", "なるみ", "ゆう", "ひな"},
    "グリズリー": {"まあや", "ともか", "ありさ", "そら", "ひな"},
    "ハロハロミライ": {"はる", "ひじり", "あんな", "ひまり", "そら", "なるみ", "ゆー", "まい"},
    "かがみ": {"はるか", "こゆき", "まい", "ゆー", "しおん", "そら", "ひまり"},
    "夏祭り": {"はるか", "ひじり", "ゆう", "あんな", "ゆー", "そら", "なるみ", "ひな", "まあや"},
}

st.title("🎵 タップで出席チェック")

st.markdown("## ✅ 出席者をタップして選択")

# 選択状態を記憶
if "selected_members" not in st.session_state:
    st.session_state.selected_members = set()

# 表示：4列ずつでタップボタン
cols = st.columns(4)
for idx, member in enumerate(all_members):
    col = cols[idx % 4]
    if member in st.session_state.selected_members:
        if col.button(f"✅ {member}", key=member):
            st.session_state.selected_members.remove(member)
    else:
        if col.button(f"⬜ {member}", key=member):
            st.session_state.selected_members.add(member)

selected_members = st.session_state.selected_members

if selected_members:
    st.markdown("---")
    st.markdown("## 🏆 出席人数ランキング（多い順）")

    ranking = []
    for song, members in songs.items():
        attending = members & selected_members
        rate = len(attending) / len(members) if members else 0
        ranking.append((song, len(attending), len(members), rate))
    ranking.sort(key=lambda x: x[1], reverse=True)

    for song, count, total, rate in ranking:
        st.write(f"🎵 **{song}**：{count} / {total}人 出席（{rate:.0%}）")

    st.markdown("---")
    st.markdown("## 📋 曲ごとの出席状況")
    for song, members in songs.items():
        attending = members & selected_members
        absent = members - selected_members

        st.subheader(f"🎵 {song}")
        st.write(f"👥 全体人数: {len(members)}")
        st.write(f"🙋‍♀️ 出席人数: {len(attending)}")
        st.write(f"✅ 出席: {'、'.join(sorted(attending)) or 'なし'}")
        st.write(f"❌ 不在: {'、'.join(sorted(absent)) or 'なし'}")
else:
    st.info("メンバーをタップして選択してください。")
