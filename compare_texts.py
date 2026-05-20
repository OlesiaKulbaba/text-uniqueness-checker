import pandas as pd

# Функція для створення тришарових відрізків (три слова підряд)
def create_trigrams(text):
    words = text.split()  # Розбиваємо текст на слова
    trigrams = []
    for i in range(len(words) - 2):  # Шукаємо три слова підряд
        trigrams.append(" ".join(words[i:i+3]))
    return trigrams

# Функція для підсвічування неунікальних фрагментів
def highlight_non_unique_fragments(texts):
    highlighted_texts = []
    non_unique_percentages = []

    # Зберігаємо всі тришарові відрізки
    all_trigrams = []
    for text in texts:
        all_trigrams.append(set(create_trigrams(text)))  # Множина тришарових відрізків для кожного тексту

    for i in range(len(texts)):
        text1 = texts[i]
        trigrams1 = create_trigrams(text1)  # Тришарові відрізки для першого тексту
        highlighted_text = text1  # Початковий текст (без змін)
        total_length = len(text1)
        non_unique_length = 0  # Сума довжин неунікальних фрагментів
        used_trigrams = set()  # Множина для зберігання вже доданих неунікальних тришарових відрізків

        # Порівнюємо з іншими текстами
        for j in range(len(texts)):
            if i != j:  # Порівнюємо лише різні тексти
                trigrams2 = create_trigrams(texts[j])  # Тришарові відрізки для другого тексту
                common_trigrams = set(trigrams1).intersection(trigrams2)  # Знаходимо спільні тришарові відрізки

                # Якщо є спільні тришарові відрізки, то ці частини є неунікальними
                for trigram in common_trigrams:
                    if trigram not in used_trigrams:  # Додаємо лише ті, що ще не були додані
                        highlighted_text = highlighted_text.replace(trigram, f'<span style="background-color: yellow;">{trigram}</span>')
                        non_unique_length += len(trigram.split())  # Додаємо довжину неунікальних фрагментів
                        used_trigrams.add(trigram)  # Додаємо триграму до множини використаних

        # Обчислюємо відсоток неунікальності
        if total_length > 0:
            non_unique_percentage = (non_unique_length / total_length) * 100
        else:
            non_unique_percentage = 0  # У випадку, якщо текст порожній

        non_unique_percentages.append(non_unique_percentage)
        highlighted_texts.append(highlighted_text)

    return highlighted_texts, non_unique_percentages

# Завантажуємо дані з Excel файлу
data = pd.read_excel("texts.xlsx")

# Викликаємо функцію для порівняння текстів
highlighted_texts, non_unique_percentages = highlight_non_unique_fragments(data['Text'].tolist())

# Створення HTML файлу
html_content = """
<html>
<head><title>Текстове порівняння</title></head>
<body>
"""

# Додаємо результати в HTML файл
for i, highlighted_text in enumerate(highlighted_texts):
    html_content += f"""
    <h1>Текст {i+1}</h1>
    <p>Процент не унікальних фрагментів: {non_unique_percentages[i]:.2f}%</p>
    <p>{highlighted_text}</p>
    """

html_content += "</body></html>"

# Записуємо результат в HTML файл
with open("comparison_result.html", "w", encoding="utf-8") as file:
    file.write(html_content)
