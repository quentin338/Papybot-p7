from scraper.parser import (removing_stop_words, user_input_in_lowercase,
                            removing_non_alnum, refine_with_verbs)


class TestScraper:
    ex_input = "salut ! Je ne sais pas vous mais je veux tout connaître du Stade de France à Paris !"
    ex_input_2 = "13, rue du Temple à Bordeaux"
    ex_input_3 = "TrolOloL TROLOLOL trololol"
    ex_input_4 = "hello plouf 33 rue des Bisounours bonjour"

    def test_user_input_in_lowercase(self):
        assert user_input_in_lowercase(self.ex_input_3) == "trololol trololol trololol"

    def test_removing_non_alnum(self):
        assert removing_non_alnum(self.ex_input_2) == "13  rue du Temple à Bordeaux"

    def test_removing_stop_words(self):
        assert removing_stop_words(self.ex_input_4) == "33 rue Bisounours"

    def test_refine_with_verbs(self):
        assert refine_with_verbs(self.ex_input) == "du Stade de France à Paris !"
