import pandas as pd

# data = pd.read_csv("timeseries.csv", parse_dates=[0])
# print(data.columns.values.tolist())
# print(data)
# print(data.describe())
# print(data.set_index("date"))
# print(data.index)
# print(data["date"])
# print(data.dtypes)
# data = data.set_index("date")
# print(data.index)

data = pd.read_csv("timeseries2.csv", index_col=0, parse_dates=True)
# print(data.index)
# print(data.index.year)
# print(data.index.day)
# print(data.loc["2019-01-03"])
# print(data.loc["2019-01-03"]["precipitation (mm/day)"])
# print(data.loc["2019-01-03":"2019-01-05"]["precipitation (mm/day)"])

column_short_names = {
    "precipitation (mm/day)": "precipitation",
    "temperature (celsius)": "temperature",
    "pet (mm/day)": "pet",
    "flow observed (mm/day)": "flow_observed",
}

data.rename(columns=column_short_names, inplace=True)
print(data)
print(data.loc["2019-01-03"]["precipitation"])
print(data.loc["2019-01-03":"2019-01-05"]["precipitation"])

