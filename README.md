# 🥶 冷笑カウンター (Cynical Counter) Bot

Discordサーバー内での「冷笑」的な発言を検知し、ユーザーごとにカウント・ランキング化するお遊び用Discord Botです。

## ✨ 機能

- **自動検知＆カウント:** 「どうせ」「はいはい」「客観的に見て」「草（文末）」「（笑）」などの特定のキーワードを自動検知し、データベース（SQLite）にカウントを蓄積します。
- **リアクション付与:** 冷笑発言を検知した際、合図としてそのメッセージに「🥶」のリアクションを自動で付与します。
- **スラッシュコマンド対応:** 以下のコマンドでカウント数やランキングを確認できます。

### 📜 コマンド一覧

- `/count [ユーザー]`: 指定したユーザー（省略時は自分）の通算冷笑回数を確認します。
- `/ranking`: サーバー内の「冷笑家」トップ10ランキングを表示します。

## 🛠️ 必要要件

- Python 3.8 以上
- 以下のPythonパッケージ:
  - `discord.py`
  - `python-dotenv`
- Discord Bot トークン（※**Message Content Intent** の有効化が必須です）

## 🚀 インストールと起動手順

1. **リポジトリのクローン:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **依存パッケージのインストール:**
   ```bash
   pip install discord.py python-dotenv
   ```

4. **環境変数の設定:**
   `sample.env` をコピーして `.env` ファイルを作成し、ご自身のDiscord Botトークンを記入してください。
   ```bash
   cp sample.env .env
   ```
   `.env` ファイルの中身:
   ```env
   DISCORD_TOKEN=あなたの_bot_token_をここに入力
   # 特定のユーザーの全発言をカウントするためのロールID（オプション。設定しない場合は空で構いません）
   TARGET_ROLE_ID=
   ```

5. **Botの起動:**
   ```bash
   python main.py
   ```
   初回起動時に自動でデータベースファイル (`cynical.db`) が作成され、スラッシュコマンドがサーバーに同期されます。

## ⚙️ カスタマイズ（キーワードの追加・変更）

`main.py` 内の以下の正規表現リストを編集することで、検知する「冷笑キーワード」を自由に変更・追加できます。

```python
# main.py 18行目付近
```

## 📝 備考

- Botをサーバーに招待する際は、権限として「メッセージの送信」「メッセージ履歴を読む」「リアクションの追加」を付与してください。
- Developer Portalの「Privileged Gateway Intents」にて、**Message Content Intent** のトグルを必ずONにしてください（メッセージの内容を読み取ってキーワードに反応するため）。

---
※このBotはジョーク用です。サーバーの雰囲気に合わせて楽しくご利用ください！
