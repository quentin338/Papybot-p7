from stop_words import STOP_WORDS

examples = ["Salut ! Je ne sais pas vous mais je veux tout connaître du Stade de France à Paris !",
            "1, avenue du Général Leclerc à Bordeaux",
            "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?",
            "Bonjour je veux savoir l'adresse du 13 rue des Bisounours à Paris, merci Papybot."]


def user_input_in_lowercase(user_input: str) -> str:
    return user_input.lower()


def removing_non_alnum(user_input: str) -> str:
    new_string = ""
    for word in user_input:
        for letter in word:
            if letter.isalnum() or letter.isspace():
                new_string += letter
            elif not letter.isalnum() or not letter.isspace():
                new_string += " "

    return new_string


def removing_stop_words(user_input: str) -> str:
    scraped = []
    for word in user_input.split():
        if word not in STOP_WORDS:
            scraped.append(word)

    return " ".join(scraped)


def getting_numero(string) -> list:
    numbers_list = []
    for word in string.split():
        if word.isdigit():
            numbers_list.append(word)

    return numbers_list


for example in examples:
    a = user_input_in_lowercase(example)
    print(a)
    a = removing_non_alnum(a)
    print(a)
    a = removing_stop_words(a)
    print(a)
# print(getting_numero(ex_input_2))
