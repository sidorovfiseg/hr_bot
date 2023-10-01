# разделяем текст по 2000 символол, возвращаем список

def split_text(text: str, max_chars: int = 4096) -> list:
    result = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    return result