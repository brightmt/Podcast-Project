import json
import datetime
import sys
api_key = None 
from listennotes import podcast_api

client = podcast_api.Client(api_key=api_key)

#Displays the menu
def display_menu():
    print("Podcast Project: Powered by the ListenNotes Python API")
    print()
    print("Select an item from the menu below: ")
    print("1. General search")
    print("2. Search podcast episode by ID")
    print("3. See available genres")
    print("4. See top podcast for genre")
    print("5. Find similar episodes")
    print("6. Get random podcast")
    print("7. Quit")
    return

#Parses a full text search
def parse_search(json_output):
    if len(json_output) == 0:
        print()
        print("No results found.")
        return
    for result in json_output:
        print()
        print("Title:", result["title_original"])
        print("ID:", result["id"])
        print("Link:", result["link"])
        print("Audio Link:", result["audio"])
        print("Length:", str(datetime.timedelta(seconds=result["audio_length_sec"])))
        print("Explicit Content:", result["explicit_content"])
        if result["podcast"]:
            podcast = result["podcast"]
            print("Podcast Information")
            print("\tTitle:", podcast["title_original"])
            print("\tPodcast ID:", podcast["id"])
            print("\tPublisher:", podcast["publisher_original"])
    print()

#parses a search for podcast recommendations
def parse_rec_search(result):
    print()
    print("Title:", result["title"])
    print("ID:", result["id"])
    print("Link:", result["link"])
    print("Audio Link:", result["audio"])
    print("Length:", str(datetime.timedelta(seconds=result["audio_length_sec"])))
    print("Explicit Content:", result["explicit_content"])
    if result["podcast"]:
        podcast = result["podcast"]
        print("Podcast Information")
        print("\tTitle:", podcast["title"])
        print("\tPodcast ID:", podcast["id"])
        print("\tPublisher:", podcast["publisher"])
    print()

#parses episodes searched by their ListenNotes ID
def parse_id_search(episode):
    print()
    print("Title:", episode["title"])
    print("ID:", episode["id"])
    print("Link:", episode["link"])
    print("Audio Link:", episode["audio"])
    print("Publication Date:", datetime.datetime.fromtimestamp(episode["pub_date_ms"] // 1000))
    print("Length:", str(datetime.timedelta(seconds=episode["audio_length_sec"])))
    print("Explicit Content:", episode["explicit_content"])
    if episode["podcast"]:
        podcast = episode["podcast"]
        print("Podcast Information:")
        print("\tTitle:", podcast["title"])
        print("\tID:", podcast["id"])
        print("\tCountry:", podcast["country"])
        print("\tWebsite:", podcast["website"])
        print("\tLanguage:", podcast["language"])
        print("\tPublisher:", podcast["publisher"])
        print("\tTotal Episodes:", podcast["total_episodes"])
        print("\tExplicit Content:", podcast["explicit_content"])
        print("\tMost Recent Episode:", datetime.datetime.fromtimestamp(podcast["latest_pub_date_ms"] // 1000))
        print("\tEarliest Episode:", datetime.datetime.fromtimestamp(podcast["earliest_pub_date_ms"] // 1000))
    print()

#Lists the available genres on ListenNotes
def display_genres(genre_list):
    for genre in genre_list["genres"]:
        print()
        print("Name:", genre["name"])
        print("ID:", genre["id"])
    print()

#Displays results for a search of a genre ID
def podcasts_by_genre(podcasts):
    for podcast in podcasts["podcasts"]:
        print()
        print("Title:", podcast["title"])
        print("ID:", podcast["id"])
        print("Type:", podcast["type"])
        print("Country:", podcast["country"])
        print("Website:", podcast["website"])
        print("Language:", podcast["language"])
        print("Genre IDs:", podcast["genre_ids"])
        print("Publisher:", podcast["publisher"])
        print("Number of Episodes:", podcast["total_episodes"])
        print("Explicit Content:", podcast["explicit_content"])
        print("Most Recent Episode:", datetime.datetime.fromtimestamp(podcast["latest_pub_date_ms"] // 1000))
        print("Earliest Episode:", datetime.datetime.fromtimestamp(podcast["earliest_pub_date_ms"] // 1000))
    print()


if __name__ == "__main__":
    display_menu()
    menu_selection = input("Your selection: ")
    #main loop
    while True:
        #full-text search
        if menu_selection == "1":
            search_term = input("Enter your search: ")
            search_out = client.search(q=search_term)
            parse_search(search_out.json()["results"])
        #episode ID search
        if menu_selection == "2":
            sought_id = input("Enter ID here: ")
            try:
                result = client.fetch_episode_by_id(id=sought_id)
                parse_id_search(result.json())
            except:
                print()
                print("Podcast episode not found.")
                print()
        #list genres
        if menu_selection == "3":
            genres = client.fetch_podcast_genres()
            display_genres(genres.json())
        #
        if menu_selection == "4":
            genre = input("Enter genre ID: ")
            try:
                best_genre = client.fetch_best_podcasts(genre_id=genre)
                podcasts_by_genre(best_genre.json())
            except:
                print()
                print("Genre not found.")
                print()
        if menu_selection == "5":
            try:
                similar_search = input("Enter podcast ID to find similar podcasts: ")
                similar_results = client.fetch_recommendations_for_episode(id=similar_search)
                for rec in similar_results.json()["recommendations"]:
                    parse_rec_search(rec)
            except:
               print()
               print("Podcast ID not found.")
               print()
        if menu_selection == "6":
            random = client.just_listen()
            parse_rec_search(random.json())
        if menu_selection == "7":
            print("Goodbye")
            sys.exit()
        else:
            display_menu()
            menu_selection = input("Your selection: ")

