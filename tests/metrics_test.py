from .env import metrics


def test_levenshtein_substitutions():
    a = "crafting"
    b = "crawling"
    assert metrics.levenshtein(a, b) == 2
    assert metrics.levenshtein(b, a) == 2


def test_levenshtein_additions():
    a = "craft"
    b = "crafting"
    assert metrics.levenshtein(a, b) == 3
    assert metrics.levenshtein(b, a) == 3


def test_levenshtein_inversions():
    a = "crafting"
    b = "cratfing"
    assert metrics.levenshtein(a, b) == 2
    assert metrics.levenshtein(b, a) == 2


def test_levenshtein_complete():
    a = "carwl"
    b = "cratfing"
    assert metrics.levenshtein(a, b) == 6
    assert metrics.levenshtein(b, a) == 6


def test_evaluate_answer_1():
    result = metrics.evaluate_answer(ground_truth="300", prediction="270", prompt="prompt", response="response")
    assert result["prompt"] == "prompt"
    assert result["response"] == "response"
    assert result["metrics"]["ground_truth"] == "300"
    assert result["metrics"]["prediction"] == "270"
    assert result["metrics"]["abs_edit_distance"] == 2
    assert result["metrics"]["rel_edit_distance"] == (2 / 3)
    assert result["metrics"]["abs_distance"] == 30
    assert result["metrics"]["rel_distance"] == (1 / 10)


def test_evaluate_answer_2():
    result = metrics.evaluate_answer(ground_truth="10000", prediction="200000", prompt="prompt", response="response")
    assert result["prompt"] == "prompt"
    assert result["response"] == "response"
    assert result["metrics"]["ground_truth"] == "10000"
    assert result["metrics"]["prediction"] == "200000"
    assert result["metrics"]["abs_edit_distance"] == 2
    assert result["metrics"]["rel_edit_distance"] == (2 / 5)
    assert result["metrics"]["abs_distance"] == 190000
    assert result["metrics"]["rel_distance"] == 19


def run_metrics_tests():
    test_levenshtein_substitutions()
    test_levenshtein_additions()
    test_levenshtein_inversions()
    test_levenshtein_complete()
    test_evaluate_answer_1()
    test_evaluate_answer_2()
