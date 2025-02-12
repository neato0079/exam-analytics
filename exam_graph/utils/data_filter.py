from exam_graph import filters
from django.http import JsonResponse, HttpRequest, QueryDict
from datetime import datetime

class FilterRequest:
    def __init__(self, post_form:dict):
        self.post_form = post_form
        self.parse_POST(self.post_form)
    
    # this takes a request.POST from HttpRequest 
    def parse_POST(self, post_form:QueryDict):
            start_str = post_form.get('start_date')
            end_str = post_form.get('end_date')
            start_date = datetime.strptime(start_str, '%Y-%m-%d') if start_str else None
            end_date = datetime.strptime(end_str, '%Y-%m-%d') if end_str else None

            self.date_range:list[datetime | None] = [start_date, end_date]
            self.metric:str = post_form['User_selected_metric']
            self.modalities:list[str] = post_form.getlist('User_selected_modality')
            self.period = post_form['period']
            self.shift_view: str | None = post_form['shift_view'] if 'shift_view' in post_form else None
            self.date_range_string:list[str | None] = [start_str, end_str]

            log_form = post_form.dict() # query obj is immutable. convert to dict
            del log_form['csrfmiddlewaretoken'] # we don't want to see the CSRF token in the logs
            print(f'Parsed filter form request{log_form}')
    
    def get_x_filts(self):
        return {
                'period': self.period,
                'modalities': self.modalities
                }




# this will contain the selected filters for a given analysis
# class UserFilters:

#     # Metric function dict
#     metric_dict = {
#         'totals': filters.totals,
#         'mean': filters.mean,
#         'tat': filters.tat,
#         'shift_view': filters.shift_view,
#         'tat_shift': filters.tat_shift_view,
#         'shift_ratios': filters.shift_ratios,
#     }

#     def __init__(self, metric:str, view:str, granular_view:str, date_range:str):
#         self.metric = metric
#         columns = []
#         # each filter can tell us what columns to keep. in other words, what columns are relevant to out neccessary calculations
#         # the goal is to cut down as much of data we can so that we are working with a small amount, recuding any excessive overhead. As we read through the filters, toss the needed column names into an array or something

#         # first thing to consider is the date range. this is an easy cut because the only data we need for calculations is within that range

#         # next we can look at the selected modalities. We can delete any rows that don't match the selected modalities. We can also just delete the modality column if the user wants to view all the modalities. Same for shifts

#         # next, we can look at the metric. Right now we only have totals and tat. for totals, row count is enough so no specific column needed there. for tat we need exam compelete time, and exam final time so keep those columns

#         # next we can look at the view. This should tell us a lot about what we can cut. default view is just value of the metric(y) over time(x). But if our view is set to Shift ?....


#     def averages(self, period):
#         # if the user has selected a monthly period, the x axis will represent months in a range. the value of each month for this filter is a weekly avgerage. so july would have a weekly average 

#         # maybe make the user choose a specific average. given the user selected period, you can get averages of any time unit smaller than the selected period. so if the user chose a selected priod of "month", the would then be able to look at weekly, daily, and hourly averages per month
#         # 
#         # Give the user 4 filters with wich to get averages from our large dataset of exams.
#         # 1. A date range in which to limit the amount of data we intend to calculate averages on
#         # 2. A period that will let us know how to increment our averages
#         # 3. A time window that will specify how we are gathering averages.
#         # 4. A metric that tells us what we are averaging(ie totals, duration, ect...)
#         # So for example, a user selects a date range of 7-01-24 to 7-31-24. Then they give us a period of "week". Then they give us a averge time window of "daily". Then they give us a metric of "totals". Now we will analize the large data set such that we can see the daily averge number of exams per week within our given time range. 
#         # 
#         # 
#         # Questions:
#         # What can I name that "time window" so that it is understandable to the user and also readable in the codebase(open to having two different names if that makes things easier)
#         #  


#         # Concept	               Current Name	  Suggested Name (User-Facing)	Suggested Code Name
#         # Date Range	            date range	          "Date Range"	             date_range
#         # Period for averaging 
#         # (How often we summarize 
#         # averages, e.g., per week)	  period	       "Averaging Period"	          avg_period
#         # Time window for 
#         # aggregation (Granularity 
#         # of averages, e.g., daily)	time window	       "Aggregation Window"	          agg_window
#         # Metric to be averaged
#         # (Total exams, 
#         # durations, etc.)	          metric	             "Metric"	                metric
#         pass


# # validated df goes here and a filter
# # this is where we apply all the filters


if __name__ == '__main__':
    pass
