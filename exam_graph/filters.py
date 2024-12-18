filters = {
    'date_range': {
        # make this ISO. edit later. sample data set is small enough for this not to matter yet
        'start': '00:00:0000',
        'end': '00:00:0000'
    },
    'modalities': {
        'XR': 0,
        'CT': 0,
        'MR': 0,
        'US': 0,
        'NM': 0,
    },
    'x_plot_filters': {
        'day': False,
        'month': True,
        'year': False,
        'shift' : False,
        'modalities': [],
        'tat': False,
        'weekends only': False,
        'weekdays only': False,
    },
    'y_plot_filters': {
        'number of exams': True,
        'exam start to finish time': '00:00',
        'ratio of completed exams to ordered exams': {
            'completed': 0,
            'ordered':0
        }
    }
}

filter_selections = {
    "x_axis": "Month",
    "y_axis": "Exam Count",
    "modality": "CT",
    "date_range": ("2024-01", "2024-12"),
    "view_shifts": False
}
