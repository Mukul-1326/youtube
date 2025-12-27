# modules/user_comm.py
# Handles all user interactions, questions, input prompts, and menus.


def show_menu():
    """
    Display the main menu and return the selected option.
    """
    print("\n======================")
    print("   MAIN MENU")
    print("======================")
    print("1. Load Dataset")
    print("2. Basic Processing")
    print("3. Intermediate Processing")
    print("4. Advanced Processing")
    print("5. Visualisations")
    print("6. Export Options")
    print("0. Exit")
    print("----------------------")

    choice = input("Select an option: ").strip()
    return choice


def submenu_basic():
    """
    Menu for Basic Processing operations.
    """
    print("\n--- BASIC PROCESSING ---")
    print("1. Count total videos")
    print("2. Count total channels")
    print("3. List all categories")
    print("4. Fetch video details (ID)")
    print("5. Fetch video details (Title)")
    print("6. Show top 10 videos")
    print("0. Back to main menu")

    return input("Pick an option: ").strip()


def submenu_intermediate():
    """
    Intermediate-level processing menu.
    """
    print("\n--- INTERMEDIATE PROCESSING ---")
    print("1. Average engagement per category")
    print("2. Trending duration of each video")
    print("3. Videos with unusual like/dislike ratio")
    print("0. Back")

    return input("Pick an option: ").strip()


def submenu_advanced():
    """
    Advanced processing (recommendation, keyword extraction, anomaly detection).
    """
    print("\n--- ADVANCED PROCESSING ---")
    print("1. Recommend similar videos")
    print("2. Extract tag keywords")
    print("3. Detect anomalies")
    print("4. Predict trending duration")
    print("0. Back")

    return input("Pick an option: ").strip()


def submenu_visuals():
    """
    Menu for all visualisation options.
    """
    print("\n--- VISUALISATIONS ---")
    print("1. Category pie chart")
    print("2. Histograms (views/likes/comments)")
    print("3. Category trending duration lines")
    print("4. Top-video bar comparison")
    print("5. Interactive dashboard")
    print("6. Anomaly overlay chart")
    print("7. Tag word cloud")
    print("0. Back")

    return input("Pick an option: ").strip()


def submenu_export():
    """
    Menu for export operations.
    """
    print("\n--- EXPORT OPTIONS ---")
    print("1. Export video details (JSON)")
    print("2. Export top 10 videos (JSON/CSV)")
    print("3. Export engagement summary (JSON)")
    print("4. Export filtered dataset")
    print("5. Export recommendations")
    print("6. Export anomaly report")
    print("7. Export trending prediction results")
    print("0. Back")

    return input("Pick an option: ").strip()


def ask_video_id():
    """Ask the user for a video ID."""
    return input("Enter Video ID: ").strip()


def ask_title_name():
    """Ask the user for a video title."""
    return input("Enter Video Title: ").strip()


def ask_export_path():
    """Ask the user for an export file path."""
    return input("Enter file save path (e.g., exports/report.json): ").strip()


def ask_csv_or_json():
    """Ask whether output should be CSV or JSON."""
    v = input("Choose file type (csv/json): ").strip().lower()
    if v not in ("csv", "json"):
        return "json"
    return v


def ask_category_id():
    """Ask for a category ID filter."""
    return input("Enter category ID to filter: ").strip()


def ask_channel_name():
    """Ask for channel name filter."""
    return input("Enter channel name to filter: ").strip().lower()


def show_msg(text_line):
    """Print a friendly message."""
    print(text_line)
