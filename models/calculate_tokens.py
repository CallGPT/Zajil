def calculate_tokens(text):
    arabic_chars = set(' اب ت ث ج ح خ دذرزس ش ص ض ط ظ ع غ ف ق ك ل م ن ه وى')
    english_chars = set('abcdefghijklmnopqrstuvwxyz')
    
    arabic_count = sum(char in arabic_chars for char in text)
    english_count = sum(char in english_chars for char in text)

    if arabic_count > english_count:
        tokens = [text[i:i+4] for i in range(0, len(text), 4)]
    else:
        tokens = [text[i:i+10] for i in range(0, len(text), 10)]

    return len(tokens)
