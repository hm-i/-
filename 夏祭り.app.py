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
all_members = ["ひまり", "まこ", "ちさと", "こゆ", "ゆう", "しおん", "そら", "なるみ", "ありさ", "ひな",
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

st.title("🎵 タップで出席チェック（ボタン色変わる）")

# 選択状態を記憶
if "selected_members" not in st.session_state:
    st.session_state.selected_members = set()

cols = st.columns(4)

for idx, member in enumerate(all_members):
    col = cols[idx % 4]
    selected = member in st.session_state.selected_members

    # 背景色付きのボタン風表示
    color = "#90ee90" if selected else "#eee"  # 緑かグレー
    button_html = f"""
    <div style="
        background-color: {color};
        border-radius: 8px;
        padding: 10px 0;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        user-select: none;
        ">
        {member}
    </div>
    """
    col.markdown(button_html, unsafe_allow_html=True)

    # 透明ボタンでクリック検知（キーはmemberで一意に）
    if col.button("", key=member):
        if selected:
            st.session_state.selected_members.remove(member)
        else:
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
