# modules/data_processing.py

from collections import defaultdict, Counter
from datetime import datetime

# -------------------------------
# BASIC PROCESSING FUNCTIONS
# -------------------------------

def count_videos(data_obj):
    """Return total number of unique video entries."""
    if not data_obj:
        return 0
    return len(data_obj)


def count_channels(data_obj):
    """Return number of distinct channels."""
    chan_set = set()
    for item in data_obj:
        chan_set.add(item.channel_title)
    return len(chan_set)


def list_categories(data_obj):
    """Return dict: category_id -> count of videos."""
    store = defaultdict(int)
    for entry in data_obj:
        store[entry.category_id] += 1
    return dict(store)


def fetch_video_info(data_obj, vid_input=None, title_input=None):
    """
    Retrieve video info by video_id OR title.
    Returns first matched VideoEntry or None.
    """
    for entry in data_obj:
        if vid_input and entry.video_id == vid_input:
            return entry
        if title_input and entry.title.lower().strip() == title_input.lower().strip():
            return entry
    return None


def top_ten_items(data_obj):
    """
    Identify top 10 videos by combined engagement:
    engagement score = views + likes + comment_count
    """
    scored = []
    for entry in data_obj:
        score_val = entry.views + entry.likes + entry.comment_count
        scored.append((score_val, entry))

    # manual sort without numpy/pandas
    scored.sort(key=lambda x: x[0], reverse=True)

    result = [item[1] for item in scored[:10]]
    return result


# -------------------------------
# INTERMEDIATE PROCESSING
# -------------------------------

def avg_engagement_by_cat(data_obj):
    """
    Compute average likes/dislikes/comments per category.
    Return: category_id -> {avg_likes, avg_dislikes, avg_comments}
    """
    agg = defaultdict(lambda: {"likes": 0, "dislikes": 0, "comments": 0, "count": 0})

    for entry in data_obj:
        cat = entry.category_id
        agg[cat]["likes"] += entry.likes
        agg[cat]["dislikes"] += entry.dislikes
        agg[cat]["comments"] += entry.comment_count
        agg[cat]["count"] += 1

    final = {}
    for cat, vals in agg.items():
        if vals["count"] > 0:
            final[cat] = {
                "avg_likes": vals["likes"] // vals["count"],
                "avg_dislikes": vals["dislikes"] // vals["count"],
                "avg_comments": vals["comments"] // vals["count"]
            }
    return final


def trending_duration(data_obj):
    """
    Count how many days each video_id appears in trending list.
    Return: video_id -> number_of_days
    """
    cache = defaultdict(set)

    for entry in data_obj:
        if entry.trending_date:
            cache[entry.video_id].add(entry.trending_date)

    result = {vid: len(days) for vid, days in cache.items()}
    return result


def odd_like_ratio(data_obj):
    """
    Videos where like/dislike ratio is unusually high (> 20).
    Return a list of VideoEntry.
    """
    flagged = []

    for entry in data_obj:
        if entry.dislikes > 0:
            ratio = entry.likes / entry.dislikes
        else:
            ratio = entry.likes  # if dislikes = 0, extremely high ratio

        if ratio > 20:
            flagged.append(entry)

    return flagged


# -------------------------------
# ADVANCED PROCESSING
# -------------------------------

def recommend_similar(data_obj, base_vid):
    """
    Recommend videos with same category or overlapping tags.
    Returns top 5 closest matches.
    """
    if not base_vid:
        return []

    base_tags = set(t.strip().lower() for t in base_vid.tags.split("|"))

    scored = []

    for entry in data_obj:
        if entry.video_id == base_vid.video_id:
            continue

        score = 0

        # category match
        if entry.category_id == base_vid.category_id:
            score += 3

        # tag intersection
        other_tags = set(t.strip().lower() for t in entry.tags.split("|"))
        overlap = len(base_tags.intersection(other_tags))
        score += overlap

        scored.append((score, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored[:5]]


def tag_keywords(data_obj):
    """
    Count frequency of all tags.
    """
    bag = Counter()

    for entry in data_obj:
        tags = entry.tags.split("|")
        for t in tags:
            clean_t = t.strip().lower()
            if clean_t not in ("", "nan", "[none]"):
                bag[clean_t] += 1

    return dict(bag)


def catch_anomalies(data_obj):
    """
    Detect videos with strange engagement patterns:
    High likes + very low comments
    """
    anomaly_list = []

    for entry in data_obj:
        if entry.likes > 50000 and entry.comment_count < 50:
            anomaly_list.append(entry)

    return anomaly_list


def predict_trend_days(data_obj):
    """
    Predict trending duration using crude scoring:
    More views + likes = longer prediction.
    Returns dict video_id -> predicted_days
    """
    pred = {}

    for entry in data_obj:
        score = (entry.views // 100000) + (entry.likes // 5000)
        if score < 1:
            score = 1
        pred[entry.video_id] = score

    return pred
