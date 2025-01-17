import os
from sys import platform

import database

PROGRAM_NAME = "Trans Ren"
VERSION = "1.7"
DESCRIPTION = "TransRen: Translate your Renpy game into any language"
EPILOG = "For more information, visit https://github.com/duc010298-1/translate-renpy"

LANGUAGE_SUPPORT = ["af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", "zh-CN", "zh-TW", "co", "hr", "cs",
                    "da", "nl", "en", "eo", "et", "fi", "fr", "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "he", "hi", "hmn",
                    "hu", "is", "ig", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", "ko", "ku", "ky", "lo", "la", "lv", "lt",
                    "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "my", "ne", "no", "ny", "or", "ps", "fa", "pl", "pt", "pa",
                    "ro", "ru", "sm", "gd", "sr", "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tl", "tg", "ta",
                    "tt", "te", "th", "tr", "tk", "uk", "ur", "ug", "uz", "vi", "cy", "xh", "yi", "yo", "zu"]
ISO_SUPPORT = 'ISO-639-1'

TXT_01 = "Please drag and drop target folder: "
TXT_02 = f"Enter the game\'s original language ({ISO_SUPPORT}): "
TXT_03 = f"Enter the language you want to translate into ({ISO_SUPPORT}): "
TXT_04 = "Enter the number of threads you want to run: "
TXT_05 = "Do you want to display the browser window? [y/n]: "
TXT_06 = "Do you want to continue the current process? [y/n]: "

def clear_console():
    return os.system('clear') if platform in ["linux", "linux2", "darwin"] else os.system('cls')


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def print_header():
    print(f"{PROGRAM_NAME}\nVersion: {VERSION}\n{DESCRIPTION}\n{EPILOG}\n{'#'*90}")


def process_input_info(folder_dir='', original_language='', into_language='', number_of_thread='', is_continue=False):
    clear_console()
    print_header()

    if folder_dir:
        print(f'{TXT_01}{folder_dir}')
    else:
        folder_dir = input(TXT_01)
        if not os.path.exists(folder_dir):
            process_input_info(is_continue=is_continue)
            return

    if original_language:
        print(f"{TXT_02}{original_language}")
    else:
        original_language = input(TXT_02)
        if original_language not in LANGUAGE_SUPPORT:
            process_input_info(folder_dir=folder_dir, is_continue=is_continue)
            return

    if into_language:
        print(f'{TXT_03}{into_language}')
    else:
        into_language = input(TXT_03)
        if into_language not in LANGUAGE_SUPPORT:
            process_input_info(
                folder_dir=folder_dir,
                original_language=original_language,
                is_continue=is_continue
            )
            return

    if number_of_thread:
        print(f'{TXT_04}{number_of_thread}')
    else:
        number_of_thread = input(TXT_04)
        if not represents_int(number_of_thread) or int(number_of_thread) < 1:
            process_input_info(
                folder_dir=folder_dir,
                original_language=original_language,
                into_language=into_language,
                is_continue=is_continue
            )
            return

    show_browser = input(TXT_05).strip().lower()
    if show_browser not in ['y', 'n']:
        process_input_info(
            folder_dir=folder_dir,
            original_language=original_language,
            into_language=into_language,
            number_of_thread=number_of_thread,
            is_continue=is_continue
        )
        return

    database.add_info(folder_dir, original_language, into_language)
    return {
        'folder_dir': folder_dir,
        'original_language': original_language,
        'into_language': into_language,
        'number_of_thread': number_of_thread,
        'show_browser': show_browser,
        'is_continue': is_continue
    }


def input_info():
    clear_console()
    info = database.get_info()
    print_header()
    if info:
        database.reset_phrase_status()
        total_phrase = database.count_phrase()
        total_done_done = database.count_phrase_done()
        percent = 100
        if total_phrase != 0:
            percent = round(float(total_done_done) /
                            float(total_phrase) * 100, 2)
        print(f"Looks like the previous translation wasn't complete\nFolder target: {info.path}\nCurrent process: {total_done_done}/{total_phrase} ({percent}%)")
        is_continue = input(TXT_06).strip().lower()
        if is_continue not in ['y', 'n']:
            input_info()
            return
        if is_continue == 'n':
            info = None
            database.reset_database()
    else:
        database.reset_database()
    if info:
        return process_input_info(
            folder_dir=info.path,
            original_language=info.original_language,
            into_language=info.into_language,
            is_continue=True
        )
    else:
        return process_input_info()
