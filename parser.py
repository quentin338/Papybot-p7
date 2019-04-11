from stop_words import STOP_WORDS, VERBS

examples = ["Salut ! Je ne sais pas vous mais je veux tout connaître du Stade de France à Paris !",
            "1, avenue du Général Leclerc à Bordeaux",
            "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?",
            "Bonjour je veux savoir l'adresse du 13 rue des Bisounours à Paris, merci Papybot.",
            "Salut grandpy! Comment s'est passé ta soirée avec Madame Pahud hier soir? Au fait, pendant que j'y pense,"
            " pourrais-tu m'indiquer où se trouve le musée d'art et d'histoire de Fribourg, s'il te plaît ?",
            "le 12 rue du Pigeon, tu connais ?", "où se situe l'adresse du Magasin de chaussures "
            "à Pouet-les-Bains ?", "où est la rue chaudron 54 ?", "Tour Eiffel"]


def user_input_in_lowercase(user_input: str) -> str:
    """"""
    return user_input.lower()


def removing_non_alnum(user_input: str) -> str:
    """"""
    new_string = ""
    for word in user_input:
        for letter in word:
            if letter.isalnum() or letter.isspace():
                new_string += letter
            elif not letter.isalnum() or not letter.isspace():
                new_string += " "

    return new_string


def removing_stop_words(user_input: str) -> str:
    """"""
    scraped = []
    for word in user_input.split():
        if word not in STOP_WORDS:
            scraped.append(word)

    return " ".join(scraped)


def refine_with_verbs(user_input: str) -> str:
    """"""
    # We remove the last word in case there is a verb AFTER the address
    for i, word in enumerate(user_input.split()[:-1]):
        for verb in VERBS:
            if verb in word:
                return " ".join(user_input.split()[i + 1:])

    return user_input


def removing_remaining_verbs(user_input: str) -> str:
    """"""
    user_input = user_input.split()
    for i, word in enumerate(user_input):
        for verb in VERBS:
            if verb in word:
                user_input.pop(i)

    return " ".join(user_input)


def clean(example_string: str):
        test_string = user_input_in_lowercase(example_string)
        print(f'LOWERCASE : {test_string}')
        test_string = removing_non_alnum(test_string)
        print(f'ALPHANUM  : {test_string}')
        test_string = removing_stop_words(test_string)
        print(f'STOPWORDS : {test_string}')
        test_string = refine_with_verbs(test_string)
        print(f'VERBS     : {test_string}')
        test_string = removing_remaining_verbs(test_string)
        print(f'RE. VERBS : {test_string}')

        return test_string


if __name__ == '__main__':
    for example in examples:
        clean(example)
