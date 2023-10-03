import os

import translatepy
from flask import after_this_request

def read_srt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                return file.read()
        except Exception as e:
            print(f"Could not read the file due to: {e}")
            return ""


def write_srt(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def translate_srt(content, dest_language):
    if not dest_language:
        raise ValueError("Destination language is not provided")

    translator = translatepy.Translator()
    blocks = content.split('\n\n')
    translated_content = ""

    for i, block in enumerate(blocks):
        lines = block.split('\n')
        timecodes = lines[1] if len(lines) > 1 else ""
        text = ' '.join(lines[2:])
        translated_text = translator.translate(text, dest_language)
        translated_text = translated_text or ""

        # Ensure the translated text is formatted with the correct timecodes
        translated_block = f"{lines[0]}\n{timecodes}\n{translated_text}\n\n"

        translated_content += translated_block

    return translated_content

def remove_file(response, file_path):
    @after_this_request
    def remove(response):
        os.remove(file_path)
        return response

    return response