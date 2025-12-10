import random

def shuffle_word(word, mistake_chance):
    if len(word) > 1 and random.randint(1, mistake_chance) == 1:
        i = random.randint(0, len(word) - 2)
        swapped = list(word)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        return "".join(swapped)
    return word


num_ett, num_tva, mistake_chance = map(int, input(
    "Ange två nummer (num_ett num_tva) och odds för felstavning (1/n): ").split())


try:
    with open("convertion_file.txt", "r", encoding="utf-8") as infile:
        text = infile.read()
except FileNotFoundError:
    exit()


formatted_lines = []
words = text.split()

for word in words:
    delay_value = random.randint(num_ett, num_tva) 
    scrambled_word = shuffle_word(word, mistake_chance)


    char_pairs = [scrambled_word[i:i+2] for i in range(0, len(scrambled_word), 2)]

    for pair in char_pairs:
        formatted_lines.append(f"STRING {pair}")
        formatted_lines.append(f"DELAY {delay_value}")

    

    formatted_lines.append("SPACE")
    formatted_lines.append(f"DELAY {delay_value}")

    if word.endswith("."):
        formatted_lines.append("DELAY 4000")

    elif word.endswith(","):
        formatted_lines.append("DELAY 1000")

with open("payload.dd", "w", encoding="utf-8") as outfile:
    outfile.write("\n".join(formatted_lines))

