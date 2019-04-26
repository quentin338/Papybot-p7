import pytest

from papybotapp.input_parser.string_parser import (removing_stop_words, user_input_in_lowercase,
                                                   removing_non_alnum, refine_with_verbs,
                                                   removing_remaining_verbs)


class TestParser:
    # user_input_in_lowercase()
    def test_user_input_in_lowercase_classic_string(self):
        assert user_input_in_lowercase("TrolOloL TROLOLOL trololol") == "trololol trololol trololol"

    def test_user_input_all_special_chars(self):
        assert user_input_in_lowercase("@@@ $$$$ ^^^ €€€") == "@@@ $$$$ ^^^ €€€"

    def test_user_input_in_lowercase_raise_attribute_error(self):
        with pytest.raises(AttributeError):
            user_input_in_lowercase([1, 2, 3])

    # removing_non_alnum() -> replaces non alnum by spaces
    def test_removing_non_alnum_classic_string(self):
        assert removing_non_alnum("13, rue du Temple à Bordeaux") == "13  rue du Temple à Bordeaux"

    def test_removing_non_alnum_all_non_alnum(self):
        assert removing_non_alnum(":,;/!..") == "       "

    def test_removing_non_alnum_raise_type_error(self):
        with pytest.raises(TypeError):
            removing_non_alnum([1, 2, 3])

    # removing_stop_words()
    def test_removing_stop_words_classic_string(self):
        assert removing_stop_words("hello plouf 33 rue des Bisounours bonjour") == "33 rue Bisounours"

    def test_removing_stop_words_empty_string(self):
        assert removing_stop_words("") == ""

    def test_removing_stop_words_raise_attribute_error(self):
        with pytest.raises(AttributeError):
            removing_stop_words([1, 2, 3])

    # refine_with_verbs()
    def test_refine_with_verbs_classic_string(self):
        assert refine_with_verbs("salut ! Je ne sais pas vous mais je veux tout connaître du Stade "
                                 "de France à Paris !") == "du Stade de France à Paris !"

    def test_refine_with_verbs_empty_string(self):
        assert refine_with_verbs("") == ""

    def test_refine_with_verbs_raise_attribute_error(self):
        with pytest.raises(AttributeError):
            refine_with_verbs([1, 2, 3])

    # removing_remaining_verbs()
    def test_removing_remaining_verbs_classic_string(self):
        assert removing_remaining_verbs("montre moi la voie ou indique moi !") == "moi la voie ou moi !"

    def test_removing_remaining_verbs_no_verbs(self):
        assert removing_remaining_verbs("un deux trois") == "un deux trois"

    def test_removing_remaining_verbs_all_verbs(self):
        assert removing_remaining_verbs("montre indique connait savoir chercher") == ""

    def test_removing_remaining_verbs_raise_attribute_error(self):
        with pytest.raises(AttributeError):
            removing_remaining_verbs([1, 2, 3])
