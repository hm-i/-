import streamlit as st
import re

# ログイン情報
USERNAME = "Syny.jpd"
PASSWORD = "dance2025syny"

# 認証チェック
def check_login():
    st.title("🔐 ログイン")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    if st.button("ログイン"):
        if username == USERNAME and password == PASSWORD:
            st.session_state["authenticated"] = True
        else:
            st.error("ユーザー名またはパスワードが違います")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    check_login()
    st.stop()

# アプリ本体
st.title("🎵 ダンス練習チェッカー（20曲・人数表示つき）")

# 曲とメンバー定義（順番を保持）
songs = {
    "カチューシャ": {"こゆ", "まこ", "ちさと","ゆう","しおん","そら","なるみ","ありさ","ひな",""},
    "君好き": {"ありさ", "ひじり", "ゆう","まあや","こゆ","ひな","しおん"},
    "怪盗少女": {"こゆ", "ともか", "ちさと","ありさ","ひな"},
    "サイクロン": {"しおん", "ちさと","ともか","はるか","ひじり","ゆう","そら","なるみ"},
    "After like": {"ひまり", "ちさと", "まこ","こゆき","まい","はる"},
    "come again": {"しおん", "まこ", "こゆき"},
    "裸足でsummer": {"まこ", "ちさと","あんな","ゆう","なるみ","そら","ありさ"},
    "ドリアン少年": {"しおん","ちさと","なるみ","ゆう","ひな"},
    "グリズリー": {"ともか","ありさ","そら","ひな"},
    "ハロハロミライ": {"はる","ひじり","あんな","ひまり","そら","なるみ","ゆー","まい"},
    "かがみ": {"はるか","こゆき","まい","ゆー","しおん","そら","ひまり"},
    "夏祭り": {"はるか","ひじり","ゆう","あんな","ゆー","そら","なるみ","ちさと","まあや"},
}

# 今日の参加者入力
names = st.text_input("🧍‍♀️ 今日の参加者をカンマまたは『、』で入力（例: あかり,けん、さゆ）")

if names:
    name_list = re.split(r'[、,]+', names)
    present = set(n.strip() for n in name_list if n.strip())

    st.markdown("---")
    st.markdown("## 🧑‍🤝‍🧑 本日の参加者")
    st.write("、".join(sorted(present)) or "（なし）")

    # 出席率ランキング用
    ranking = []
    for song, members in songs.items():
        attending = members & present
        total = len(members)
        attending_count = len(attending)
        rate = attending_count / total if total > 0 else 0
        ranking.append((song, rate, attending_count, total))

    # 出席率の高い順にソートしてランキングだけ先に表示
    st.markdown("## 📊 出席率ランキング")
    for song, rate, attend_num, total_num in sorted(ranking, key=lambda x: x[1], reverse=True):
        st.markdown(f"**🎵 {song}**： {attend_num}/{total_num}人（{rate:.0%}）")

    # 詳細表示は元の順番通り
    st.markdown("---")
    st.markdown("## 📋 各曲の詳細")
    for song, members in songs.items():
        attending = members & present
        absent = members - present
        total = len(members)
        attending_count = len(attending)

        st.subheader(f"{song}")
        st.write(f"👥 全体人数：{total}")
        st.write(f"🙋‍♀️ 本日の参加可能人数：{attending_count}")
        st.write(f"✅ 出席: {'、'.join(sorted(attending)) or 'なし'}")
        st.write(f"❌ 不在: {'、'.join(sorted(absent)) or 'なし'}")
