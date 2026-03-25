from datetime import date
import math

series_titles = [
    "Maximum temperature (Degree C)",
    "Minimum temperature (Degree C)",
    "Rainfall amount (millimetres)",
    "Temperature range (Degree C)"
]

calculation_titles = [
    "Mean",
    "Variance",
    "Standard deviation",
    "Range",
    "Interquartile range"
]

def clean_series(in_series):
    return [value for value in in_series if value is not None]

def mean(in_series):
    values = clean_series(in_series)
    if len(values) == 0:
        return None
    return sum(values) / len(values)

def variance(in_series):
    values = clean_series(in_series)
    if len(values) == 0:
        return None

    avg = mean(values)
    total = 0

    for value in values:
        total += (value - avg) ** 2

    return total / len(values)

def standard_deviation(in_series):
    var = variance(in_series)
    if var is None:
        return None
    return math.sqrt(var)

def data_range(in_series):
    values = clean_series(in_series)
    if len(values) == 0:
        return None
    return max(values) - min(values)

def median(in_series):
    values = sorted(clean_series(in_series))
    n = len(values)

    if n == 0:
        return None

    middle = n // 2

    if n % 2 == 0:
        return (values[middle - 1] + values[middle]) / 2
    else:
        return values[middle]

def interquartile_range(in_series):
    values = sorted(clean_series(in_series))
    n = len(values)

    if n == 0:
        return None

    middle = n // 2

    if n % 2 == 0:
        lower_half = values[:middle]
        upper_half = values[middle:]
    else:
        lower_half = values[:middle]
        upper_half = values[middle + 1:]

    q1 = median(lower_half)
    q3 = median(upper_half)

    if q1 is None or q3 is None:
        return None

    return q3 - q1

def filter_series(year_series, month_series, day_series, data_series, max_date=None, min_date=None):
    filtered_data = []

    for year, month, day, value in zip(year_series, month_series, day_series, data_series):
        current_date = date(int(year), int(month), int(day))

        if min_date is not None and current_date < min_date:
            continue

        if max_date is not None and current_date > max_date:
            continue

        filtered_data.append(value)

    return filtered_data

def add_temperature_range(data_table):
    max_series = data_table["Maximum temperature (Degree C)"]
    min_series = data_table["Minimum temperature (Degree C)"]

    temp_range_series = []
    for max_temp, min_temp in zip(max_series, min_series):
        if max_temp is None or min_temp is None:
            temp_range_series.append(None)
        else:
            temp_range_series.append(max_temp - min_temp)

    data_table["Temperature range (Degree C)"] = temp_range_series
    return data_table

def read_csv(file, default_value=None):
    data_table = {}
    with open(file) as f:
        lines = f.readlines()

    lines = [line.strip().split(',') for line in lines]

    for i in range(len(lines[0])):
        data_table[lines[0][i]] = [
            default_value if (len(line[i]) == 0) else float(line[i])
            for line in lines[1:]
        ]

    return data_table

def get_user_choice(options):
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    choice = input("Enter the number of your choice, or type 'exit': ").strip()

    if choice.lower() == "exit":
        return None

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
        print("Invalid choice. Please try again.")
        return get_user_choice(options)

    return options[int(choice) - 1]

def get_date_input(prompt_text):
    user_input = input(prompt_text).strip()
    parts = user_input.split("-")

    if len(parts) != 3:
        print("Invalid date format. Use YYYY-MM-DD.")
        return get_date_input(prompt_text)

    year, month, day = parts

    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        print("Invalid date format. Use YYYY-MM-DD.")
        return get_date_input(prompt_text)

    try:
        return date(int(year), int(month), int(day))
    except ValueError:
        print("Invalid date. Please enter a real date in YYYY-MM-DD format.")
        return get_date_input(prompt_text)

def apply_calculation(series, calculation_name):
    if calculation_name == "Mean":
        return mean(series)
    elif calculation_name == "Variance":
        return variance(series)
    elif calculation_name == "Standard deviation":
        return standard_deviation(series)
    elif calculation_name == "Range":
        return data_range(series)
    elif calculation_name == "Interquartile range":
        return interquartile_range(series)
    else:
        return None

def menu(data_table):
    while True:
        print("\nWeather Data Analysis App")
        print("Choose a data series, or type 'exit' to quit.")

        selected_series_name = get_user_choice(series_titles)
        if selected_series_name is None:
            print("Exiting program.")
            break

        print("\nChoose a statistical calculation, or type 'exit' to quit.")
        selected_calculation = get_user_choice(calculation_titles)
        if selected_calculation is None:
            print("Exiting program.")
            break

        use_filter = input("\nWould you like to filter by date range? (yes/no): ").strip().lower()

        selected_series = data_table[selected_series_name]

        if use_filter == "yes":
            min_date = get_date_input("Enter start date (YYYY-MM-DD): ")
            max_date = get_date_input("Enter end date (YYYY-MM-DD): ")

            if min_date > max_date:
                print("Start date cannot be after end date.")
                continue

            selected_series = filter_series(
                data_table["Year"],
                data_table["Month"],
                data_table["Day"],
                selected_series,
                max_date=max_date,
                min_date=min_date
            )

        result = apply_calculation(selected_series, selected_calculation)

        if result is None:
            print("\nNo valid data available for that calculation.")
        else:
            print(f"\n{selected_calculation} of {selected_series_name}: {result}")

        again = input("\nWould you like to perform another calculation? (yes/no): ").strip().lower()
        if again != "yes":
            print("Exiting program.")
            break

if __name__ == "__main__":
    data = read_csv("weather.csv")
    data = add_temperature_range(data)
    menu(data)