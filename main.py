import threading
from screenshot import main, task_queue
from translate import translate_main
from demonstrate import show_translation


def process_screenshot() -> None:
    """
    Извлекает изображение из очереди, переводит текст с изображения и демонстрирует перевод.
    """
    while True:
        filename = task_queue.get()
        translate_text = translate_main(filename, 'ru')
        show_translation(translate_text)
        task_queue.task_done()

if __name__ == "__main__":
    # Запуск процесса создания скриншотов в отдельном потоке
    main_thread = threading.Thread(target=main)
    main_thread.start()

    # Запуск потока для обработки скриншотов
    process_thread = threading.Thread(target=process_screenshot)
    process_thread.daemon = True
    process_thread.start()

    # Блокировка основного потока, чтобы программа не завершалась
    main_thread.join()
