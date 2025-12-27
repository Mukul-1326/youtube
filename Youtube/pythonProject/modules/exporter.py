# modules/exporter.py

import json
import csv
import os


# ----------------------------------------------------
# INTERNAL HELPERS
# ----------------------------------------------------

def _ensure_folder(pathname):
    """Create folder if it does not exist."""
    if pathname and not os.path.exists(pathname):
        os.makedirs(pathname)


def _entry_to_dict(entry):
    """Convert VideoEntry object into serialisable dict."""
    return {
        "video_id": entry.video_id,
        "title": entry.title,
        "publish_time": entry.publish_time,
        "channel_title": entry.channel_title,
        "category_id": entry.category_id,
        "tags": entry.tags,
        "views": entry.views,
        "likes": entry.likes,
        "dislikes": entry.dislikes,
        "comment_count": entry.comment_count,
        "thumbnail_link": entry.thumbnail_link,
        "comments_disabled": entry.comments_disabled,
        "ratings_disabled": entry.ratings_disabled,
        "video_error_or_removed": entry.video_error_or_removed,
        "description": entry.description,
        "trending_date": entry.trending_date
    }



# ----------------------------------------------------
# BASIC EXPORTS
# ----------------------------------------------------

def export_video_details(entry, save_path):
    """Save detailed JSON info for a single selected video."""
    if not entry:
        print("No matching video found.")
        return

    folder = os.path.dirname(save_path)
    _ensure_folder(folder)

    with open(save_path, "w", encoding="utf-8") as jf:
        json.dump(_entry_to_dict(entry), jf, indent=4)

    print(f"Saved video details at: {save_path}")


def export_top_ten(top_list, save_path, mode="json"):
    """
    Save top 10 videos in JSON or CSV format.
    top_list contains raw dictionary entries.
    """
    folder = os.path.dirname(save_path)
    _ensure_folder(folder)

    if mode.lower() == "json":
        block = [_entry_to_dict(e) for e in top_list]
        with open(save_path, "w", encoding="utf-8") as jf:
            json.dump(block, jf, indent=4)


    else:  # CSV mode
        with open(save_path, "w", newline="", encoding="utf-8") as cf:
            wr = csv.writer(cf)
            # Write ALL columns you want in CSV
            wr.writerow([
                "video_id", "title", "channel_title", "category_id",
                "publish_time", "trending_date", "tags",
                "views", "likes", "dislikes", "comment_count",
                "thumbnail_link", "comments_disabled",
                "ratings_disabled", "video_error_or_removed",
                "description"
            ])
            for e in top_list:
                wr.writerow([
                    e.video_id,
                    e.title,
                    e.channel_title,
                    e.category_id,
                    e.publish_time,
                    e.trending_date,
                    e.tags,
                    e.views,
                    e.likes,
                    e.dislikes,
                    e.comment_count,
                    e.thumbnail_link,
                    e.comments_disabled,
                    e.ratings_disabled,
                    e.video_error_or_removed,
                    e.description
                ])

    print(f"Top-10 list saved at: {save_path}")


# ----------------------------------------------------
# INTERMEDIATE EXPORTS
# ----------------------------------------------------

def export_engagement_summary(stats_dict, save_path):
    """Export aggregated category-level engagement metrics into JSON."""
    folder = os.path.dirname(save_path)
    _ensure_folder(folder)

    with open(save_path, "w", encoding="utf-8") as jf:
        json.dump(stats_dict, jf, indent=4)

    print(f"Engagement summary saved at: {save_path}")


def export_filtered_dataset(data_list, filter_fn, save_path):
    """
    Export filtered dataset based on category/channel/trending period.
    filter_fn must be a function that accepts entry and returns True/False.
    """
    filtered = [_entry_to_dict(e) for e in data_list if filter_fn(e)]

    folder = os.path.dirname(save_path)
    _ensure_folder(folder)

    with open(save_path, "w", encoding="utf-8") as jf:
        json.dump(filtered, jf, indent=4)

    print(f"Filtered dataset saved at: {save_path}")


# ----------------------------------------------------
# ADVANCED EXPORTS
# ----------------------------------------------------

def export_recommendations(rec_list, save_path):
    """Export recommended videos for a selected base video."""
    block = [_entry_to_dict(v) for v in rec_list]

    folder = os.path.dirname(save_path)
    _ensure_folder(folder)

    with open(save_path, "w", encoding="utf-8") as jf:
        json.dump(block, jf, indent=4)

    print(f"Recommendations saved at: {save_path}")


def export_anomaly_report(flagged_list, save_path):
    """Export anomaly detection results into a JSON report."""
    anomalies = [_entry_to_dict(v) for v in flagged_list]

    folder = os.path.dirname(save_path)
    _ensure_folder(folder)

    with open(save_path, "w", encoding="utf-8") as jf:
        json.dump({"anomalies": anomalies}, jf, indent=4)

    print(f"Anomaly report saved at: {save_path}")


def export_trend_prediction(pred_dict, save_path):
    """
    Export predicted trending duration for videos.
    pred_dict should be: { video_id: predicted_days }
    """
    folder = os.path.dirname(save_path)
    _ensure_folder(folder)

    with open(save_path, "w", encoding="utf-8") as jf:
        json.dump(pred_dict, jf, indent=4)

    print(f"Trend prediction saved at: {save_path}")
