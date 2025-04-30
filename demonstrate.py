import tkinter as tk
from tkinter import ttk
import pyperclip

def show_translation(translated_text: list) -> None:
    """
    Создаёт окно для отображения переведённого текста с возможностью его копирования.

    :param translated_text: Список с оригинальным и переведённым текстом.
    """
    root = tk.Tk()
    root.title("RedFox TRANSLATE")
    root.geometry("620x180")
    root.minsize(320, 180)
    root.configure(bg="#2c2c2c")

    style = ttk.Style()
    style.theme_use('default')

    # Конфигурация стилей для элементов
    style.configure("TFrame", background="#2c2c2c")
    style.configure("TLabel", background="#2c2c2c", foreground="#ffffff")
    style.configure("TButton", 
                    background="#444444", 
                    foreground="#ffffff", 
                    font=("Arial", 12, "bold"),
                    relief="raised", 
                    borderwidth=2,
                    activebackground="#333333", 
                    padding=5)

    frame = ttk.Frame(root, padding=(20, 10))
    frame.pack(fill=tk.BOTH, expand=True)

    frame_left = ttk.Frame(frame)
    frame_left.grid(row=0, column=0, sticky="nsew")

    frame_right = ttk.Frame(frame)
    frame_right.grid(row=0, column=1, sticky="nsew")

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    label_title1 = ttk.Label(frame_left, text="UNTRANSLATED", font=("Arial", 12, "bold"))
    label_title1.pack(pady=(5, 0))

    text1 = tk.Text(frame_left, wrap=tk.WORD, bg="#3c3c3c", fg="#ffffff", font=("Arial", 12), height=4)
    text1.insert(tk.END, translated_text[0])
    text1.config(state=tk.DISABLED)
    text1.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    label_title2 = ttk.Label(frame_right, text="TRANSLATED", font=("Arial", 12, "bold"))
    label_title2.pack(pady=(5, 0))

    text2 = tk.Text(frame_right, wrap=tk.WORD, bg="#3c3c3c", fg="#ffffff", font=("Arial", 12), height=4)
    text2.insert(tk.END, translated_text[1])
    text2.config(state=tk.DISABLED)
    text2.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

    button_frame = ttk.Frame(frame)
    button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")

    def copy_text():
        pyperclip.copy(translated_text[0])
        root.destroy()

    def copy_text2():
        pyperclip.copy(translated_text[1])
        root.destroy()

    button_copy = ttk.Button(button_frame, text="Копировать", command=copy_text)
    button_copy.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))

    button_close = ttk.Button(button_frame, text="Копировать", command=copy_text2)
    button_close.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))

    root.mainloop()

if __name__ == "__main__":
    # Пример вызова функции
    show_translation(["Текст без перевода. Это пример текста, который будет занимать несколько строк.", 
                      "Translated text. This is an example of text that will take multiple lines."])
