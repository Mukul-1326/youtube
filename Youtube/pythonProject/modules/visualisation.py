# modules/visualisation.py

import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go


# ------------------------------------
# BASIC VISUALISATIONS
# ------------------------------------

def pie_categories(data_obj):
    """
    Pie chart showing distribution of videos per category.
    """
    if not data_obj:
        print("No data loaded.")
        return

    cat_count = defaultdict(int)
    for entry in data_obj:
        cat_count[entry.category_id] += 1

    labels = list(cat_count.keys())
    sizes = list(cat_count.values())

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Video Distribution by Category")
    plt.show()


def hist_engagement(data_obj):
    """
    Histograms for views, likes, and comments.
    """
    view_list = []
    like_list = []
    comment_list = []

    for entry in data_obj:
        view_list.append(entry.views)
        like_list.append(entry.likes)
        comment_list.append(entry.comment_count)

    fig, axs = plt.subplots(3, 1, figsize=(9, 14))

    sns.histplot(view_list, bins=30, ax=axs[0], color="blue")
    axs[0].set_title("Views Distribution")

    sns.histplot(like_list, bins=30, ax=axs[1], color="green")
    axs[1].set_title("Likes Distribution")

    sns.histplot(comment_list, bins=30, ax=axs[2], color="red")
    axs[2].set_title("Comment Count Distribution")

    plt.tight_layout()
    plt.show()


# ------------------------------------
# INTERMEDIATE VISUALISATIONS
# ------------------------------------

def cat_trend_lines(data_obj):
    """
    Line chart showing average trending duration per category.
    """
    dur_store = defaultdict(list)

    # collect trending dates per video first
    vid_dates = defaultdict(set)
    for entry in data_obj:
        if entry.trending_date:
            vid_dates[entry.video_id].add(entry.trending_date)

    # now map each video duration to its category
    for entry in data_obj:
        vid = entry.video_id
        days = len(vid_dates[vid])
        dur_store[entry.category_id].append(days)

    avg_list = []
    cat_list = []

    for cat, arr in dur_store.items():
        if arr:
            avg_d = sum(arr) / len(arr)
            avg_list.append(avg_d)
            cat_list.append(cat)

    plt.figure(figsize=(10, 5))
    plt.plot(cat_list, avg_list, marker='o')
    plt.title("Average Trending Duration per Category")
    plt.xlabel("Category ID")
    plt.ylabel("Average Duration (Days)")
    plt.grid(True)
    plt.show()


def compare_top_bars(data_obj):
    """
    Bar chart comparing likes/dislikes/comments for top performing videos.
    Top videos are selected based on engagement score.
    """
    scored = []
    for entry in data_obj:
        score_val = entry.views + entry.likes + entry.comment_count
        scored.append((score_val, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    picked = [x[1] for x in scored[:10]]

    names = [p.title[:20] + "..." for p in picked]
    likes = [p.likes for p in picked]
    dislikes = [p.dislikes for p in picked]
    comments = [p.comment_count for p in picked]

    x = range(len(picked))

    plt.figure(figsize=(14, 7))
    plt.bar(x, likes, width=0.25, label="Likes", color="green")
    plt.bar([i + 0.25 for i in x], dislikes, width=0.25, label="Dislikes", color="red")
    plt.bar([i + 0.50 for i in x], comments, width=0.25, label="Comments", color="blue")

    plt.xticks([i + 0.25 for i in x], names, rotation=45, ha='right')
    plt.title("Engagement Metrics for Top 10 Videos")
    plt.legend()
    plt.tight_layout()
    plt.show()


# ------------------------------------
# ADVANCED VISUALISATIONS
# ------------------------------------

def dashboard_view(data_obj):
    """
    Interactive dashboard using Plotly:
    Allows filtering by category and shows engagement metrics.
    """
    entries = {
        "title": [],
        "category_id": [],
        "views": [],
        "likes": [],
        "comments": []
    }

    for entry in data_obj:
        entries["title"].append(entry.title)
        entries["category_id"].append(entry.category_id)
        entries["views"].append(entry.views)
        entries["likes"].append(entry.likes)
        entries["comments"].append(entry.comment_count)

    fig = px.scatter(
        x=entries["views"],
        y=entries["likes"],
        color=entries["category_id"],
        hover_name=entries["title"],
        title="Interactive Engagement Dashboard"
    )

    fig.update_layout(xaxis_title="Views", yaxis_title="Likes")
    fig.show()


def mark_anomalies(data_obj):
    """
    Overlay scatter plot showing anomalies with high likes and low comments.
    """
    x_norm = []
    y_norm = []
    x_flag = []
    y_flag = []

    for entry in data_obj:
        if entry.likes > 50000 and entry.comment_count < 50:
            x_flag.append(entry.likes)
            y_flag.append(entry.comment_count)
        else:
            x_norm.append(entry.likes)
            y_norm.append(entry.comment_count)

    plt.figure(figsize=(9, 6))
    plt.scatter(x_norm, y_norm, alpha=0.4, label="Normal")
    plt.scatter(x_flag, y_flag, color='red', label="Anomalies", s=80)
    plt.title("Anomaly Detection Overlay")
    plt.xlabel("Likes")
    plt.ylabel("Comment Count")
    plt.legend()
    plt.show()


def tag_wordcloud(data_obj):
    """
    Generate a word cloud from tag frequencies.
    """
    all_tags = []

    for entry in data_obj:
        parts = entry.tags.split("|")
        for t in parts:
            t = t.strip().lower()
            if t not in ("", "nan", "[none]"):
                all_tags.append(t)

    text_blob = " ".join(all_tags)

    wc = WordCloud(width=900, height=500, background_color="white").generate(text_blob)

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title("Tag Frequency Word Cloud")
    plt.show()
