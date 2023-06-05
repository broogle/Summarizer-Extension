from googletrans import Translator


def g_translate(text, lang):

    translate = Translator()

    text_parts = text.split('. ')
    translated_text = []

    for parts in text_parts:
        translated_text.append(translate.translate(
            parts, src='en', dest=lang).text)

    return ' '.join(translated_text) + '.'
