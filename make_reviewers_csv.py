import pandas as pd
from tqdm import tqdm
import serpapi
import os

client = serpapi.Client(api_key=os.getenv("SERP_API_KEY"))

reviewers = pd.read_csv("DH2024WashingtonDC_reviewers_2023-12-11_04-35-28.csv")
reviewer_fields = ["personID", "name", "firstname", "topics", "maxreviews"]
reviewer_df = reviewers[reviewer_fields]

# only 147 have a maxreviews, set default of 3
reviewer_df["maxreviews"] = reviewer_df["maxreviews"].fillna(3)
pbar = tqdm(total=len(reviewer_df))


def scholar(row):
    results = client.search(
        {
            "engine": "google_scholar",
            "q": f'{row["firstname"]} {row["name"]} digital humanities',
        }
    )
    text = ""
    for result in results.get("organic_results", []):
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        text += f"{title} {snippet}"
    # Remove person name from text
    text = (
        text.replace(row["firstname"], "")
        .replace(row["firstname"].lower(), "")
        .replace(row["firstname"].upper(), "")
    )
    text = (
        text.replace(row["name"], "")
        .replace(row["name"].lower(), "")
        .replace(row["name"].upper(), "")
    )
    pbar.update(0.5)
    return text


def google(row):
    results = client.search(
        {
            "engine": "google",
            "q": f'{row["firstname"]} {row["name"]} digital humanities',
        }
    )
    text = ""
    for result in results.get("organic_results", []):
        title = result.get("title", "")
        snippet = result.get("snippet", "")
        text += f"{title} {snippet}"
    # Remove person name from text
    text = (
        text.replace(row["firstname"], "")
        .replace(row["firstname"].lower(), "")
        .replace(row["firstname"].upper(), "")
    )
    text = (
        text.replace(row["name"], "")
        .replace(row["name"].lower(), "")
        .replace(row["name"].upper(), "")
    )
    pbar.update(0.5)
    return text


reviewer_df["google"] = reviewer_df.apply(google, axis=1)
reviewer_df["scholar"] = reviewer_df.apply(scholar, axis=1)
reviewer_df.to_csv("reviewers.csv", index=False)
