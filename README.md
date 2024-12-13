# exam-analytics
Generate graphs displaying exam volume. Allows for filtering by modality, date, shift, ect...

## Progress . . .
- Use `Pandas` to read mock `.cvs` and apply filters
- Use `matplotlib` to plot the filters that have been built so far

```Usage: python my_project.py <Modality:XR, CT, US, NM, MR> <Month:bool>```

### XR and CT by day

![](/img/ct-day.png)
![](/img/xr-day.png)

### XR and CT by month

![](/img/ct-month.png)
![](/img/xr-month.png)

### Notes

run server with `python manage.py runserver`