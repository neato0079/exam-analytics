modalities = [
    'XR',
    'CT',
    'MR',
    'US',
    'NM'
    ]

filters = {
    'date_range': {
        # make this ISO. edit later. sample data set is small enough for this not to matter yet
        'start': '00:00:0000',
        'end': '00:00:0000'
    },

    'shift_color_indicators': False,

    'x_plot_filters': {
        'period_increments':{
            'day': False,
            'month': True,
            'year': False,
        },
        'period_filters': {
            'shift' : {
                'AM': True,
                'PM': True,
                'NOC': True,
            },
        'weekends only': False,
        'weekdays only': False,
        },
        'exam_filters': {
            'modalities': [],
            'exam_name':'',
        }
    },

    'y_plot_filters': {
        'number_of_exams': True,
        'exam_start_to_finish_time': '00:00',
        'ratio_of_completed_exams_to_ordered_exams': {
            'completed': 0,
            'ordered':0
        },
    },
}

filter_selections = {
    "x_axis": "Month",
    "y_axis": "Exam Count",
    "modality": "CT",
    "date_range": ("2024-01", "2024-12"),
    "view_shifts": False,
    "only_weekends": False,
    "only_weekdays": False
}
