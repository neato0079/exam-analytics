
filters = {
    "date_range": {
        "start": "2024-01-01",
        "end": "2024-12-31"
    },
    
    "x_axis": { # Time filters
        "group_by": "month",  # Options: "day", "month", "year"
        "shift_filter": ["AM", "PM", "NOC"],  # List of shifts to include
        "week_view": None  # Options: "weekends", "weekdays", None
    },

    "y_axis": { # Metrics
        "metric": "number_of_exams",  # Options: "number_of_exams", "exam_start_to_finish_time", etc.
    },

    "exam_filters": {
        "modalities": ["CT", "MRI"],  # List of selected modalities
        "exam_name": "Head CT"  # Specific exam name
    },

    "shift_color_indicators": False,
}

# VALID OPTIONS FOR FILTERS:

metric_options = [
    'number_of_exams',
    'exam_start_to_finish_time'
    'ratio_of_completed_exams_to_ordered_exams'
]

groupby_options = [
    'hour'
    'day'
    'month',
    'year'
]

modalities = [
    'XR',
    'CT',
    'MR',
    'US',
    'NM'
    ]

week_view_options = [
    'weekends',
    'weekdays',
    None
]