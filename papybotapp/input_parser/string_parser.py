from papybotapp.stop_words import STOP_WORDS, VERBS

examples = ["Salut ! Je ne sais pas vous mais je veux tout connaître du Stade de France à Paris !",
            "1, avenue du Général Leclerc à Bordeaux",
            "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?",
            "Bonjour je veux savoir l'adresse du 13 rue des Bisounours à Paris, merci Papybot.",
            "Salut grandpy! Comment s'est passé ta soirée avec Madame Pahud hier soir? Au fait, pendant que j'y pense,"
            " pourrais-tu m'indiquer où se trouve le musée d'art et d'histoire de Fribourg, s'il te plaît ?",
            "le 12 rue du Pigeon, tu connais ?", "où se situe l'adresse du Magasin de chaussures "
            "à Pouet-les-Bains ?", "où est la rue chaudron 54 ?", "Tour Eiffel"]


def user_input_in_lowercase(user_input: str) -> str:
    """
    :param user_input: what the user will enter on the website
    :return: all user_input in lowercase
    """
    return user_input.lower()


def removing_non_alnum(user_input: str) -> str:
    """
    :param user_input: string that the user entered
    :return: string with all non alnum chars removed
    """
    new_string = ""
    for word in user_input:
        for letter in word:
            if letter.isalnum() or letter.isspace():
                new_string += letter
            elif not letter.isalnum() or not letter.isspace():
                new_string += " "

    return new_string


def removing_stop_words(user_input: str) -> str:
    """
    :param user_input: string that user entered
    :return: string without all stop words in STOP_WORDS in stop_words.py
    """
    scraped = []
    for word in user_input.split():
        if word not in STOP_WORDS:
            scraped.append(word)

    return " ".join(scraped)


def refine_with_verbs(user_input: str) -> str:
    """
    :param user_input: string that the user entered
    :return: string splitted FROM a verb that we caught with VERBS in stop_words.py
    """
    for i, word in enumerate(user_input.split()[:-1]):
        for verb in VERBS:
            if verb in word:
                return " ".join(user_input.split()[i + 1:])

    return user_input


def removing_remaining_verbs(user_input: str) -> str:
    """
    :param user_input: string that the user entered
    :return: string without the verbs caught with VERBS in stop_words.py
    """
    clean_string = ""

    user_input = user_input.split()
    for word in user_input:
        verb_found = False
        for verb in VERBS:
            if verb in word:
                verb_found = True

        if not verb_found:
            clean_string += word + " "

    return clean_string.strip()


def clean(user_input: str):
    """
    Main function. Pass the user_input to all "cleaning functions" above
    :param user_input: string that the user entered
    :return: string in lower case, without alnum char, without stop words, splitted from the first verb caught
    and without the remaining verbs caught.
    """
    clean_string = user_input_in_lowercase(user_input)
    clean_string = removing_non_alnum(clean_string)
    clean_string = removing_stop_words(clean_string)
    clean_string = refine_with_verbs(clean_string)
    clean_string = removing_remaining_verbs(clean_string)

    return clean_string


if __name__ == '__main__':
    # for example in examples:
    #     clean(example)
    print(removing_remaining_verbs("savoir montrer indiquer"))
