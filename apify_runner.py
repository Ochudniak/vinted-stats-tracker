import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "kazkn/vinted-smart-scraper")


def get_client() -> ApifyClient:
    token = os.getenv("APIFY_TOKEN")

    if not token:
        raise ValueError("Brakuje APIFY_TOKEN w pliku .env")

    return ApifyClient(token)


def run_actor(apify_input: dict) -> list[dict]:
    client = get_client()

    print("ACTOR_ID:", repr(ACTOR_ID))
    print("Wysyłam input do Apify:")
    print(apify_input)

    run = client.actor(ACTOR_ID).call(run_input=apify_input)

    if isinstance(run, dict):
        dataset_id = run["defaultDatasetId"]
    else:
        dataset_id = run.default_dataset_id

    print("Dataset ID:", dataset_id)

    items = list(client.dataset(dataset_id).iterate_items())

    return items


def get_item_details(item_urls: list[str]) -> list[dict]:
    if not item_urls:
        return []

    apify_input = {
        "mode": "ITEM_DETAIL",
        "itemUrls": item_urls,
        "maxItems": len(item_urls),
    }

    return run_actor(apify_input)