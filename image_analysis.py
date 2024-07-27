import numpy as np
import json


def get_patient_data(file_lines):
    """Parse patient data from input file lines.

    Read through input file lines and append as a list
    all of a patient's data. Return a list of these lists
    representing each patient's data.

    Args:
        file_lines (list): list in which each element is a row from the file

    Returns:
        list: list of lists of patient data for all patients
    """
    patient_data = []
    current_data = []

    for line in file_lines:
        line = line.strip()
        if line == "END":
            patient_data.append(current_data)
            current_data = []
        else:
            current_data.append(line.split())

    return patient_data


def count_cells(data):
    """Count live or dead cells from input data.

    Read through lines of data (either red or green)
    and count values that represent live or dead cells.

    Args:
        data (list): list in which each element is a row from the file
                     containing data points from the image

    Returns:
        int: number of live or dead cells
    """

    count = 0
    for row in data:
        for i in row[0].split(','):
            if int(i) >= 75:
                count += 1
    return count


def eval_result(live_cell_fraction, cell_density):
    """Evaluate analytical result of image.

    Evaluates analytic result of image based off of table in
    program specifications. Updates patient dictionary with new
    field indicating result of image.

    Args:
        patient_info (dict): dictionary containing all of
                             a patient's information

        live_cell_fraction (float): fraction of cells that are alive

        cell_density (float): fraction of data points that are cells

    Returns:
        None
    """
    result = ""

    if cell_density >= 0.4:
        if live_cell_fraction >= 0.7:
            result = "PASS"
        else:
            result = "FAIL"
    else:
        if live_cell_fraction >= 0.7:
            result = "TENTATIVE_PASS"
        else:
            result = "TENTATIVE_FAIL"

    return result


def analyze_data(patient):
    """Analyze a patient's data and sort into dictionary.

    Analyze a specific patient's data in a list and
    sort it into keys and values for a dictionary.
    Calculate metrics and add to dictionary, as well.

    Args:
        patient (list): list in which each element is a row from the file
                        containing data points from the image

    Returns:
        dict: dictionary containing all information for a patient
    """
    patient_info = {}
    patient_info["First Name"] = patient[0][0]
    patient_info["Last Name"] = patient[0][1]
    patient_info["DOB"] = patient[1][0]

    cols = int(patient[2][1])
    rows = int(patient[2][2])
    total_data = cols * rows

    green_data = patient[3:(3+rows)]
    red_data = patient[(3+rows+1):(3+rows+2+rows)]

    live_cells = count_cells(green_data)
    dead_cells = count_cells(red_data)
    total_cells = live_cells + dead_cells

    patient_info["Cell Total"] = total_cells

    live_cell_fraction = round(live_cells/total_cells, 2)
    dead_cell_fraction = round(dead_cells/total_cells, 2)
    cell_density = total_cells/total_data

    patient_info["Live"] = live_cell_fraction
    patient_info["Dead"] = dead_cell_fraction

    patient_info["Result"] = eval_result(live_cell_fraction, cell_density)

    return patient_info


def output_file(patient):
    """Output patient dictionary to .json file.

    Populate .json file with information from patient dictionary.

    Args:
        patient (dict): dictionary containing all of a patient's data

    Returns:
        None
    """
    first_name = patient["First Name"]
    last_name = patient["Last Name"]
    out_file = open(f"{first_name}-{last_name}.json", "w")
    json.dump(patient, out_file)
    out_file.close()


def main():
    """Read and analyze input file to create information files for patients.

    Open input file, read and store data lines. Store data for each patient in
    individual dictionaries and output dictionaries to individual .json files.

    Args:
        None

    Returns:
        None
    """
    with open("sample_data.txt", "r") as file:
        file_lines = file.readlines()

    patient_data = get_patient_data(file_lines)
    patient_metrics = []

    for patient in patient_data:
        patient_analysis = analyze_data(patient)
        patient_metrics.append(patient_analysis)

    for patient in patient_metrics:
        output_file(patient)


if __name__ == "__main__":
    main()
