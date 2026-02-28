import os
import sqlite3
import re
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# .envの読み込み
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 全発言をカウントする対象ロールのID (オプション)
TARGET_ROLE_ID_STR = os.getenv('TARGET_ROLE_ID')
TARGET_ROLE_ID = int(TARGET_ROLE_ID_STR) if TARGET_ROLE_ID_STR and TARGET_ROLE_ID_STR.isdigit() else None

# データベースファイル名
DB_FILE = 'cynical.db'

# Lv.2 冷笑判定用正規表現 (お好みでキーワードを増やしてください)
# r'...' の中に検知したい単語を | で区切って記述します
CYNICAL_PATTERN = re.compile(r'(どうせ|はいはい|意味あんの|意味ない|必死|草|（笑）|冷める|冷笑|うお|どわー|どわ～|偽善|真面目か|嘲笑|寒い|おつ|乙|勘違い|😏|🥶|🥱)')

class CynicalBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # メッセージ内容の取得を許可
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # データベースの初期化
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS cynical_counts
                     (guild_id INTEGER, user_id INTEGER, count INTEGER DEFAULT 0,
                     PRIMARY KEY(guild_id, user_id))''')
        conn.commit()
        conn.close()
        # スラッシュコマンドを同期
        await self.tree.sync()
        print("Slash commands synced.")

bot = CynicalBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author.bot:
        return

    # 対象のロールを持っているかどうか確認
    has_target_role = False
    if TARGET_ROLE_ID and isinstance(message.author, discord.Member):
        if any(role.id == TARGET_ROLE_ID for role in message.author.roles):
            has_target_role = True

    # メッセージが冷笑パターンにマッチするか、特定のロールを持っているユーザーか判定
    if has_target_role or CYNICAL_PATTERN.search(message.content):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # カウントをアップサート (存在しなければ作成、あれば+1)
        c.execute('''INSERT INTO cynical_counts (guild_id, user_id, count)
                     VALUES (?, ?, 1)
                     ON CONFLICT(guild_id, user_id) 
                     DO UPDATE SET count = count + 1''', 
                  (message.guild.id, message.author.id))
        conn.commit()
        conn.close()

        # 検知した合図としてリアクションを付与
        try:
            await message.add_reaction('🥶')
        except discord.Forbidden:
            print("リアクション権限がありません。")

    # 通常のコマンドも動くようにする
    await bot.process_commands(message)

# --- スラッシュコマンド ---

@bot.tree.command(name="count", description="冷笑カウントを確認します")
@app_commands.describe(user="確認したいユーザー（省略すると自分）")
async def count(interaction: discord.Interaction, user: discord.Member = None):
    target_user = user or interaction.user
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT count FROM cynical_counts WHERE guild_id = ? AND user_id = ?', 
              (interaction.guild.id, target_user.id))
    result = c.fetchone()
    conn.close()

    count_val = result[0] if result else 0
    await interaction.response.send_message(
        f'{target_user.display_name} さんの通算冷笑回数: **{count_val}回** です。',
        ephemeral=False # みんなに見えるように設定
    )

@bot.tree.command(name="ranking", description="冷笑家ランキングを表示します")
async def ranking(interaction: discord.Interaction):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT user_id, count FROM cynical_counts 
                 WHERE guild_id = ? AND count > 0 
                 ORDER BY count DESC LIMIT 10''', 
              (interaction.guild.id,))
    results = c.fetchall()
    conn.close()

    if not results:
        await interaction.response.send_message("まだ冷笑家はいません。")
        return

    embed = discord.Embed(title="🏆 冷笑家ランキング", color=0x2ecc71)
    description = ""
    for i, (u_id, val) in enumerate(results, 1):
        description += f"**{i}位:** <@{u_id}> — `{val}回` \n"
    
    embed.description = description
    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    if not TOKEN:
        print("エラー: .envファイルに DISCORD_TOKEN が設定されていません。")
    else:
        bot.run(TOKEN)