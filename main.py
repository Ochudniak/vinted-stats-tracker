from pathlib import Path

from apify_runner import get_item_details


LINKS_FILE = Path("data/linki.txt")


def load_item_urls(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Nie znaleziono pliku {file_path}. "
            "Najpierw uruchom skrypt w przeglądarce i wrzuć vinted_linki.txt do folderu data."
        )

    urls = []

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            url = line.strip()

            if not url:
                continue

            if "/items/" not in url:
                continue

            urls.append(url)

    unique_urls = list(dict.fromkeys(urls))

    return unique_urls


def main():
    item_urls = load_item_urls(LINKS_FILE)

    print("Liczba linków z pliku:", len(item_urls))

    if not item_urls:
        print("Brak linków do sprawdzenia.")
        return

    # Na test bierzemy pierwsze 5, żeby nie przepalać kosztów Apify.
    test_urls = item_urls[:5]

    print("Testuję pierwsze linki:")
    for url in test_urls:
        print(url)

    details = get_item_details(test_urls)

    print()
    print("Liczba wyników z Apify:", len(details))

    for item in details:
        print("------")
        print("ID:", item.get("id") or item.get("itemId"))
        print("Tytuł:", item.get("title"))
        print("Cena:", item.get("price"))
        print("Wyświetlenia:", item.get("viewCount"))
        print("Polubienia:", item.get("favouriteCount"))
        print("Sprzedane:", item.get("isSold"))
        print("URL:", item.get("url"))


if __name__ == "__main__":
    main()