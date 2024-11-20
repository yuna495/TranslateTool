import threading
import time
from tkinter import LEFT, RIGHT, VERTICAL, Frame, Scrollbar, Text, Tk, Y

import keyboard
import pyperclip
from deep_translator import GoogleTranslator
from PIL import Image
from pystray import Icon, Menu, MenuItem


# 翻訳ウインドウの設定
def show_translation_window(original, translated):
    window = Tk()
    window.title("Translation Result")
    window.geometry("500x200")  # サイズを調整
    window.resizable(True, True)

    # 背景色を黒に設定
    window.configure(bg="black")

    # 最前面に表示
    window.attributes("-topmost", True)

    # メインフレーム
    frame = Frame(window, bg="black")
    frame.pack(fill="both", expand=True)

    # スクロールバー
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # 翻訳結果を表示するテキストボックス
    text_area = Text(
        frame,
        wrap="word",
        yscrollcommand=scrollbar.set,
        bg="black",
        fg="white",
        font=(None, 14),  # フォントサイズを調整
        padx=10,
        pady=10,
        highlightthickness=0,
    )
    text_area.pack(side=LEFT, fill="both", expand=True)
    scrollbar.config(command=text_area.yview)

    # 翻訳前と翻訳後のテキストを表示
    text_area.insert("1.0", f"Original:\n{original}\n\nTranslated:\n{translated}")
    text_area.config(state="disabled")  # ユーザーが編集できないようにする

    # Escキーでウインドウを閉じる処理
    def close_window(event=None):
        window.destroy()

    # Escキーにバインド
    window.bind("<Escape>", close_window)

    window.mainloop()


# タスクバーアイコンの設定
def create_image():
    # 外部アイコン画像を利用
    return Image.open("D:\\Games\\Python\\translateTool\\icon\\icon.png")


def quit_application(icon, item):
    icon.stop()


# タスクバーアイコンとメニューの初期化
icon = Icon("Translator", create_image(), menu=Menu(MenuItem("Quit", quit_application)))


# 英語以外かどうかを判定する関数
def is_non_english(text):
    # 英字以外の文字が含まれているかを判定
    return any(not char.isascii() for char in text)


# 翻訳処理を実行
def translate_clipboard():
    try:
        current_clipboard = pyperclip.paste()

        # 翻訳処理
        print(f"Target Text: {current_clipboard}")
        try:
            # 英語以外は全て英語に翻訳
            if is_non_english(current_clipboard):
                translated = GoogleTranslator(source="auto", target="en").translate(
                    current_clipboard
                )
            else:
                # 英語の場合は日本語に翻訳
                translated = GoogleTranslator(source="auto", target="ja").translate(
                    current_clipboard
                )

            # 翻訳結果をウインドウに表示
            show_translation_window(current_clipboard, translated)
        except Exception as translate_error:
            print(f"Translation Error: {translate_error}")
    except Exception as clipboard_error:
        print(f"Clipboard Error: {clipboard_error}")


# クリップボード監視と翻訳処理
def clipboard_monitor():
    while True:
        try:
            # `Ctrl` が押しっぱなしで `C` が2回押されたかを監視
            if keyboard.is_pressed("ctrl"):
                if keyboard.read_event().name == "c":
                    # 1回目の `C`
                    time.sleep(0.1)  # タイミング調整
                    if keyboard.read_event().name == "c":
                        # 2回目の `C`
                        translate_clipboard()
        except Exception as clipboard_error:
            print(f"Clipboard Error: {clipboard_error}")

        time.sleep(0.1)  # チェック間隔を短めに設定


# スレッドでクリップボード監視を実行
clipboard_thread = threading.Thread(target=clipboard_monitor, daemon=True)
clipboard_thread.start()

# タスクバーアイコンを実行
icon.run()
