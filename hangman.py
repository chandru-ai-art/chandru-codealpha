import random

words = ["python", "hangman", "programming", "computer", "algorithm"]
word = random.choice(words)

used = []
wrong = 0
limit = 6
show = []

for _ in word:
    show.append("_")

print("Hangman game")
print("Guess letters")
print()

while wrong < limit:
    print("Word:", end=" ")
    for c in show:
        print(c, end=" ")
    print()

    print("Used:", used)
    print("Wrong left:", limit - wrong)

    g = input("Letter: ").lower()

    if len(g) != 1:
        print("one letter only\n")
        continue

    if g in used:
        print("already used\n")
        continue

    used.append(g)

    if g in word:
        i = 0
        for ch in word:
            if ch == g:
                show[i] = g
            i += 1
        print("correct\n")
    else:
        wrong += 1
        print("wrong\n")

    if "_" not in show:
        print("You win")
        print("Word was:", word)
        break

if wrong == limit:
    print("You lose")
    print("Word was:", word)
