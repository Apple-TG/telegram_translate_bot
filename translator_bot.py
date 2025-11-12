import asyncio

# ✅ 解决 Python 3.14 无默认事件循环的问题
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from googletrans import Translator

# 初始化翻译器
translator = Translator()

# 🚨 请换成你自己的 BotFather Token
TOKEN = "8508810484:AAFG2h8EV8wWI6wLSoy8V_jRLHr4BQf8HxM"

# 🔁 双向翻译函数
async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text:
        return  # 忽略空白讯息

    # 🔍 自动检测语言
    detected = translator.detect(text)
    src_lang = detected.lang

    # 🧠 根据语言决定翻译目标
    if src_lang.startswith("zh"):  # 中文发言 -> 英文
        target_lang = "en"
    else:  # 外语发言 -> 简体中文
        target_lang = "zh-cn"

    # 🌐 执行翻译
    result = translator.translate(text, dest=target_lang)

    # 💬 回复结果
    await update.message.reply_text(
        f"🌏 检测语言：{src_lang}\n🎯 翻译为：{target_lang}\n💬 结果：{result.text}"
    )

# 🚀 启动机器人
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_message))

print("✅ 双向自动翻译机器人已启动中…")
app.run_polling()
