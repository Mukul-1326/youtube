# main.py

from modules.data_loader import load_dataset
from modules.data_processing import (
    count_videos, count_channels, list_categories, fetch_video_info,
    top_ten_items, avg_engagement_by_cat, trending_duration,
    odd_like_ratio, recommend_similar, tag_keywords,
    catch_anomalies, predict_trend_days
)
from modules.visualisation import (
    pie_categories, hist_engagement, cat_trend_lines,
    compare_top_bars, dashboard_view, mark_anomalies,
    tag_wordcloud
)
from modules.exporter import (
    export_video_details, export_top_ten, export_engagement_summary,
    export_filtered_dataset, export_recommendations,
    export_anomaly_report, export_trend_prediction
)
from modules.user_comm import (
    show_menu, submenu_basic, submenu_intermediate, submenu_advanced,
    submenu_visuals, submenu_export, ask_video_id, ask_title_name,
    ask_export_path, ask_csv_or_json, ask_category_id, ask_channel_name,
    show_msg
)


def main():
    data_obj = None
    show_msg("System started. Select an option from the menu.")

    while True:
        choice = show_menu()

        # -------------------------------------------------
        # LOAD DATASET
        # -------------------------------------------------
        if choice == "1":
            data_obj = load_dataset("data/youtube_trending_videos.csv")
            show_msg("Dataset loaded successfully.") if data_obj else show_msg("Dataset load failed.")

        # -------------------------------------------------
        # BASIC PROCESSING
        # -------------------------------------------------
        elif choice == "2" and data_obj:
            while True:
                opt = submenu_basic()

                if opt == "1":
                    show_msg(f"Total videos: {count_videos(data_obj)}")

                elif opt == "2":
                    show_msg(f"Total channels: {count_channels(data_obj)}")

                elif opt == "3":
                    cats = list_categories(data_obj)
                    show_msg(str(cats))

                elif opt == "4":
                    vid = ask_video_id()
                    entry = fetch_video_info(data_obj, vid_input=vid)
                    show_msg(str(entry.__dict__)) if entry else show_msg("Video not found.")

                elif opt == "5":
                    title = ask_title_name()
                    entry = fetch_video_info(data_obj, title_input=title)
                    show_msg(str(entry.__dict__)) if entry else show_msg("Video not found.")

                elif opt == "6":
                    res = top_ten_items(data_obj)
                    for x in res:
                        show_msg(x.title)

                elif opt == "0":
                    break

                else:
                    show_msg("Invalid selection.")

        # -------------------------------------------------
        # INTERMEDIATE PROCESSING
        # -------------------------------------------------
        elif choice == "3" and data_obj:
            while True:
                opt = submenu_intermediate()

                if opt == "1":
                    result = avg_engagement_by_cat(data_obj)
                    show_msg(str(result))

                elif opt == "2":
                    result = trending_duration(data_obj)
                    show_msg(str(result))

                elif opt == "3":
                    flagged = odd_like_ratio(data_obj)
                    show_msg(f"Flagged videos: {len(flagged)}")

                elif opt == "0":
                    break

                else:
                    show_msg("Invalid option.")

        # -------------------------------------------------
        # ADVANCED PROCESSING
        # -------------------------------------------------
        elif choice == "4" and data_obj:
            while True:
                opt = submenu_advanced()

                if opt == "1":
                    base_id = ask_video_id()
                    base_video = fetch_video_info(data_obj, vid_input=base_id)
                    recs = recommend_similar(data_obj, base_video)
                    for r in recs:
                        show_msg(r.title)

                elif opt == "2":
                    keys = tag_keywords(data_obj)
                    show_msg(f"Found {len(keys)} unique keywords.")

                elif opt == "3":
                    flagged = catch_anomalies(data_obj)
                    show_msg(f"Anomalies detected: {len(flagged)}")

                elif opt == "4":
                    preds = predict_trend_days(data_obj)
                    show_msg("Predictions computed.")

                elif opt == "0":
                    break

                else:
                    show_msg("Invalid option.")

        # -------------------------------------------------
        # VISUALISATIONS
        # -------------------------------------------------
        elif choice == "5" and data_obj:
            while True:
                opt = submenu_visuals()

                if opt == "1":
                    pie_categories(data_obj)

                elif opt == "2":
                    hist_engagement(data_obj)

                elif opt == "3":
                    cat_trend_lines(data_obj)

                elif opt == "4":
                    compare_top_bars(data_obj)

                elif opt == "5":
                    dashboard_view(data_obj)

                elif opt == "6":
                    mark_anomalies(data_obj)

                elif opt == "7":
                    tag_wordcloud(data_obj)

                elif opt == "0":
                    break

                else:
                    show_msg("Invalid option.")

        # -------------------------------------------------
        # EXPORTING
        # -------------------------------------------------
        elif choice == "6" and data_obj:
            while True:
                opt = submenu_export()

                if opt == "1":
                    vid = ask_video_id()
                    entry = fetch_video_info(data_obj, vid_input=vid)
                    path = ask_export_path()
                    export_video_details(entry, path)

                elif opt == "2":
                    mode = ask_csv_or_json()
                    path = ask_export_path()
                    top10 = top_ten_items(data_obj)
                    export_top_ten(top10, path, mode)

                elif opt == "3":
                    summary = avg_engagement_by_cat(data_obj)
                    path = ask_export_path()
                    export_engagement_summary(summary, path)

                elif opt == "4":
                    ask_type = input("Filter by (1) category or (2) channel: ").strip()

                    if ask_type == "1":
                        cat = ask_category_id()
                        filt_fn = lambda x: str(x.category_id) == cat
                    else:
                        chan = ask_channel_name()
                        filt_fn = lambda x: x.channel_title.lower() == chan

                    path = ask_export_path()
                    export_filtered_dataset(data_obj, filt_fn, path)

                elif opt == "5":
                    vid = ask_video_id()
                    base = fetch_video_info(data_obj, vid_input=vid)
                    recs = recommend_similar(data_obj, base)
                    path = ask_export_path()
                    export_recommendations(recs, path)

                elif opt == "6":
                    flagged = catch_anomalies(data_obj)
                    path = ask_export_path()
                    export_anomaly_report(flagged, path)

                elif opt == "7":
                    preds = predict_trend_days(data_obj)
                    path = ask_export_path()
                    export_trend_prediction(preds, path)

                elif opt == "0":
                    break

                else:
                    show_msg("Invalid option.")

        # -------------------------------------------------
        # EXIT
        # -------------------------------------------------
        elif choice == "0":
            show_msg("Closing system... Goodbye.")
            break

        else:
            show_msg("Invalid option or dataset not loaded.")


if __name__ == "__main__":
    main()
