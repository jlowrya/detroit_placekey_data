from datetime import date

import pandas as pd
import placekey as pk
import matplotlib.pyplot as plt

def add_geo_pk(row):
    return pk.geo_to_placekey(row["Y"], row["X"])


def drop_duplicate_entries(df, key):
    """
    For any address in df that is repeated, will drop all but one
    :arg df - the dataframe to drop the duplicates from
    :arg key - the key to check for duplicates on
    """
    to_drop = []
    grouped = df.groupby(key)
    for group, rows in grouped:
        print(f"Removing duplicates for {group}...")
        to_drop.extend(rows.index[1:])
            
    return df.drop(labels=to_drop)


def drop_future_dates(df, key):
    """
    Drops any entries where key contains a date in the future
    :arg df - dataframe to operate on
    :arg key - column name containing the date to compare
    """
    today = date.today()

    today_str = today.strftime("%Y/%m/%d")

    future_violations = df[df[key] > today_str]

    return df.drop(labels=future_violations.index)


def drop_non_initial_sales_for_properties(sales_df):
    address_group = sales_df.sort_values(by="sale_date", ascending=True).groupby("address")
    to_drop = []
    for key, group in address_group:
        earliest = min(group["sale_date"])
        for index, row in group.iterrows():
            if(row["sale_date"]!=earliest):
                print(f"Dropping row {index}...")
                to_drop.append(index)

    print("Dropping columns...")
    sales_df = sales_df.drop(index=to_drop).sort_values(by="address")
    print(f"Dropped {len(to_drop)} entries with sales after the initial one for properties. Resulting df has {len(sales_df)} entries")
    return sales_df


blight_df = pd.read_csv("./Blight_Violations.csv")
blight_df = blight_df.dropna(subset=['X', 'Y', 'violation_address'])
blight_df = drop_future_dates(blight_df, "violation_date")


sales_df = pd.read_csv("./Property_Sales.csv")
sales_df = sales_df.dropna(subset=['X', 'Y', 'address'])
sales_df = drop_future_dates(sales_df, "sale_date")


blight_df["placekey"] = blight_df.apply(lambda row: pk.geo_to_placekey(row["Y"], row["X"]), axis=1)

sales_df["placekey"] = sales_df.apply(lambda row: pk.geo_to_placekey(row["Y"], row["X"]), axis=1)

blight_df["pk_violation_count"] = blight_df.groupby('placekey')['placekey'].transform('count')
sales_df["pk_sales_count"] = sales_df.groupby('placekey')['placekey'].transform('count')

blight_df = drop_duplicate_entries(blight_df, "placekey")
sales_df = drop_duplicate_entries(sales_df, "placekey")

cols_to_keep = {"placekey", "pk_violation_count", "pk_sales_count"}

blight_df = blight_df.drop(labels=[col for col in blight_df.columns if col not in cols_to_keep], axis=1)
sales_df = sales_df.drop(labels=[col for col in sales_df.columns if col not in cols_to_keep], axis=1)

pk_merged = blight_df.merge(sales_df, on="placekey")
pk_merged.sort_values("placekey")

pk_merged.to_csv("./pk_merged.csv")

plt.scatter(pk_merged["pk_violation_count"], pk_merged["pk_sales_count"])
plt.title("Number of home sales as a function of blight violations for a given placekey")
plt.xlabel("Number of blight violations")
plt.ylabel("Number of home sales")
plt.show()



