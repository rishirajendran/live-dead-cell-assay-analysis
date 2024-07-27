import pytest


@pytest.mark.parametrize("input, expected", [
    (['Stephanie Lawson\n',
      '03/25/1987\n',
      'GREEN 14 14\n',
      '3,193,3,75,17,8,154,170,131,4,4,87,163,16\n', 'END'],
     [[['Stephanie', 'Lawson'],
       ['03/25/1987'],
       ['GREEN', '14', '14'],
       ['3,193,3,75,17,8,154,170,131,4,4,87,163,16']]]),
    ])
def test_get_patient_data(input, expected):
    from image_analysis import get_patient_data
    answer = get_patient_data(input)
    assert answer == expected


@pytest.mark.parametrize("input, expected", [
    ([['5,10,15,100,37,63,75']], 2),
    ([['75']], 1),
    ([['74']], 0),
    ([['75, 76, 77, 75, 74, 73, 75, 75, 1000']], 7),
    ])
def test_count_cells(input, expected):
    from image_analysis import count_cells
    answer = count_cells(input)
    assert answer == expected


@pytest.mark.parametrize("input1, input2, expected", [
    (0.7, 0.4, "PASS"),
    (0.69, 0.4, "FAIL"),
    (0.7, 0.39, "TENTATIVE_PASS"),
    (0.69, 0.39, "TENTATIVE_FAIL"),
    ])
def test_eval_result(input1, input2, expected):
    from image_analysis import eval_result
    answer = eval_result(input1, input2)
    assert answer == expected


@pytest.mark.parametrize("input, expected", [
    ([['Stephanie', 'Lawson'], ['03/25/1987'],
      ['GREEN', '14', '1'], ['3,193,3,75,17,8,154,170,131,4,4,87,163,16'],
      ['RED', '14', '1'], ['12,3,8,5,13,6,10,5,9,14,77,13,13,8']],
     {'First Name': 'Stephanie', 'Last Name': 'Lawson', 'DOB': '03/25/1987',
      'Cell Total': 8, 'Live': 0.88, 'Dead': 0.12, 'Result': 'PASS'}),
    ])
def test_analyze_data(input, expected):
    from image_analysis import analyze_data
    answer = analyze_data(input)
    assert answer == expected
