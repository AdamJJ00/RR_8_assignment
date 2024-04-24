import csv

import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_breaking_bad_episodes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="wikiepisodetable")
    data_rows = []

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all(["th", "td"])
            if len(cells) == 7:
                row_data = [cell.get_text(strip=True) for cell in cells]
                if row_data[0] != "No.overall":
                    data_rows.append(row_data)

    return data_rows


def save_to_csv(finall_df, filename):
    csv_file = filename
    finall_df.to_csv(
        f"C:/Programming/reproducible_reaserch/RR_8_assignment/data/{csv_file}",
        index=False,
    )

    print(f"Data scraped successfully and saved to {csv_file}")


def correct_data(data):
    df = pd.DataFrame(
        data,
        columns=[
            "number_overall",
            "number_in_season",
            "title",
            "directed_by",
            "written_by",
            "original_air_date",
            "us_viewers",
        ],
    )

    df["original_air_date"] = df["original_air_date"].str.extract(
        r"(\d{4}-\d{2}-\d{2})"
    )

    df["title"] = df["title"].str.strip('"').astype(str)

    # Correcting data types
    df["number_overall"] = df["number_overall"].astype(int)
    df["number_in_season"] = df["number_in_season"].astype(int)
    df["us_viewers"] = df["us_viewers"].str.extract(r"([\d.]+)").astype(float)

    df = df.iloc[:62]

    return df


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/List_of_Breaking_Bad_episodes"
    data = scrape_breaking_bad_episodes(url)
    finall_df = correct_data(data)
    save_to_csv(finall_df, "breaking_bad_episodes.csv")
