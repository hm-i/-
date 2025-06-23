import streamlit as st
import re

# ログイン情報
USERNAME = "Syny.jpd"
PASSWORD = "dance2025syny"

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
st.title("🎵 ダンス練習チェッカー（20曲・詳細出席情報つき）")

# 曲データ（順番保持）
songs = {
    "カチューシャ": {"こゆ", "まこ", "ちさと","ゆう","しおん","そら","なるみ","ありさ","ひな","ひじり"},
    "君好き": {"ひな", "しおん", "ゆう","まあや","こゆ"},
    "怪盗少女": {"こゆ", "ともか", "ちさと","ありさ","ひな"},
    "サイクロン": {"しおん", "ちさと","ともか","はるか","ひじり","ゆう","そら","なるみ"},
    "After like": {"ひまり", "ちさと", "まこ","こゆき","まい","はる"},
    "come again": {"しおん", "まこ", "こゆき"},
    "裸足でsummer": {"まこ", "ちさと","あんな","ゆう","なるみ","ひな","ありさ"},
    "ドリアン少年": {"まあや","ちさと","なるみ","ゆう","ひな"},
    "グリズリー": {"まあや","ともか","ありさ","そら","ひな"},
    "ハロハロミライ": {"はる","ひじり","あんな","ひまり","そら","なるみ","ゆー","まい"},
    "かがみ": {"はるか","こゆき","まい","ゆー","しおん","そら","ひまり"},
    "夏祭り": {"はるか","ひじり","ゆう","あんな","ゆー","そら","なるみ","ひな","まあや"},
}

# --- 入力欄 ---
def parse_names(raw_input):
    return set(n.strip() for n in re.split(r"[、,]+", raw_input) if n.strip())

names_present = st.text_input("✅ 本日の参加者（例: まこ,しおん）")
names_late = st.text_input("⏰ 遅れてくる人（例: ひまり、まこ）")
names_leave_early = st.text_input("🚪 途中で帰る人（例: まあや,ゆう）")

present = parse_names(names_present)
late = parse_names(names_late)
early = parse_names(names_leave_early)

if present or late or early:
    st.markdown("---")
    st.markdown("## 👥 入力情報の確認")
    st.write(f"✅ 参加者：{'、'.join(sorted(present)) or '（なし）'}")
    st.write(f"⏰ 遅れてくる人：{'、'.join(sorted(late)) or '（なし）'}")
    st.write(f"🚪 途中で帰る人：{'、'.join(sorted(early)) or '（なし）'}")

    # 出席率ランキング準備
    ranking = []
    for song, members in songs.items():
        attending = members & present
        late_attending = members & late
        early_leaving = members & early
        total = len(members)
        attending_count = len(attending)
        rate = attending_count / total if total else 0
        ranking.append((song, rate, attending_count, total))

    st.markdown("## 📊 出席率ランキング")
    for song, rate, attending_count, total in sorted(ranking, key=lambda x: x[1], reverse=True):
        st.markdown(f"**🎵 {song}**： {attending_count}/{total}人（{rate:.0%}）")

    st.markdown("---")
    st.markdown("## 📋 各曲の詳細")

    for song, members in songs.items():
        attending = members & present
        late_attending = members & late
        early_leaving = members & early
        absent = members - present - late - early

        total = len(members)
        attending_count = len(attending)

        st.subheader(f"{song}")
        st.write(f"👥 全体人数：{total}")
        st.write(f"🙋‍♀️ 本日の参加可能人数（通常）：{attending_count}")
        st.write(f"✅ 出席: {'、'.join(sorted(attending)) or 'なし'}")
        
        if late_attending:
            st.write(f"⏰ 遅れてくる: {'、'.join(sorted(late_attending))}")
        
        if early_leaving:
            st.write(f"🚪 途中で帰る: {'、'.join(sorted(early_leaving))}")
        
        st.write(f"❌ 不在: {'、'.join(sorted(absent)) or 'なし'}")
