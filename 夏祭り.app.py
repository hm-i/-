import streamlit as st

# ログイン情報（例：ユーザー名とパスワードのペア）
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

# 初期状態なら未認証
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 認証されていなければログイン画面
if not st.session_state["authenticated"]:
    check_login()
    st.stop()

import streamlit as st
import re

st.title("🎵 ダンス練習チェッカー（20曲・人数表示つき）")

# 20曲の曲名と固定メンバー
songs = {
    "カチューシャ": {"あかり", "けん", "さゆ"},
    "君好き": {"けん", "なお", "ゆう"},
    "怪盗少女": {"さゆ", "みな", "あや"},
    "サイクロン": {"れい", "なお"},
    "After like": {"ひまり", "ちさと", "まこ","こゆき","まい","はる"},
    "": {"あかり", "さゆ", "なお"},
    "": {"ゆう", "あかり"},
    "": {"けん", "れい"},
    "曲9": {"れい", "なお", "みな"},
    "曲10": {"さゆ", "ゆう"},
    "曲11": {"けん", "みお", "れい"},
    "曲12": {"なお", "あかり", "ゆう"},
    "曲13": {"れい", "さゆ", "みな"},
    "曲14": {"あや", "けん", "みお"},
    "曲15": {"あかり", "なお", "あや"},
    "曲16": {"さゆ", "ゆう", "みお"},
    "曲17": {"みな", "れい", "けん"},
    "曲18": {"あや", "なお", "ゆう"},
    "曲19": {"あかり", "けん", "れい"},
    "": {"みお", "さゆ", "あかり"},
}

# 今日の参加者入力
names = st.text_input("🧍‍♀️ 今日の参加者をカンマまたは『、』で入力（例: あかり,けん、さゆ）")

if names:
    # 「,」または「、」で分割して正規化
    name_list = re.split(r'[、,]+', names)
    present = set(n.strip() for n in name_list if n.strip())

    st.markdown("---")
    st.markdown("## 🧑‍🤝‍🧑 本日の参加者")
    st.write("、".join(sorted(present)) or "（なし）")

    st.markdown("## 📋 結果")

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
