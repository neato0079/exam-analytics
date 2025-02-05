# Exam-Analytics App
### App Description: <br>
Analyzes a user uploaded radiology exam dataset and generates graphs on user-set filters.

- Runs on the `Django` frame work
- Utilizes `Pandas` library for dataset analysis
- Utilizes `Matplotlib` for data visualization
- Unit testing done with `pytest`
- Currently running on `Render` cloud service

## Progress . . .
- Allow user to upload and store `.csv` to app
- Uploaded `.csv` is parsed and formatted to a `pd.Dataframe` and then stored to the server disk as a `.pickle`
- Analysis is performed on a user selected dataset by reading the appropriate `.pickle` as a `pd.Dataframe` 
- Various filters are now functional for graph generation

## Breakdown
- Compatible datasets(just `.csv` files for now) are essentially `HL7` data organized by the following columns:

```
        COLUMN NAME                       HL7 ORM Segment
        ______________________________________________________________________
        'Exam Complete Date/Tm' . . . . . ORC.5 (order status is complete)
        'Order Procedure Accession' . . . ORC.2
        'Exam Order Date/Time'. . . . . . ORC.15 ex:'YYYY-mm-ddTHH:MM:SS'
        'Final Date/Tm' . . . . . . . . . OBR.22.1 (time of final report)
        'Exam Order Name' . . . . . . . . OBR.4
        'Modality'. . . . . . . . . . . . OBR.24
```
- Modality can be inferred if the accession number or order name implies a modality
- Typically an EHR should provide a way to export a `.csv` file with the data shown above. This will be the source of data for this app. 
- This data is then formatted and analyzed

wip.....

### Example Graphs
*The following graphs were generated using mocked datasets*
#### Totals Graph with Shift View On
This graph displays the total number of exams ordered by month over the course of a year. Each bar is broken down by shift to allow the user to visualize how the exam order volume is spread over the different work shifts.
![](/img/grph.png)

#### Shift Ratios 
The Shift Ratio graph allows for visualization of the ratio of Exam Completes(`ORC.5`) to Exam Orders (`ORC.15`) for each shift. These ratios can help make staffing descisions. For example, this graph shows us that the AM shift typically has a ratio < 1, meaning AM shift typically completes less exams than ordered on that shift. This could be used as evidence of a need of increased staffing for AM shift. 

Keep in mind no one tool should give us definitive evidence of any one particular staffing need. More analytics are needed for more definite claims about staffing needs. For example it could be the case that the hours closest to AM shift change are typically high volume hours for the Emergency Deparment. In this scenario, this ratio may not necessarily suggest any staffing issues at all as while more exams are ordered at the end of the shift, there is less time for AM shift to finish those exams before the end of the shift. This graph shows that PM shift sometimes has a ratio > 1, which could be accounting for the PM shift "cleaning up" the ED rush hour volume before the volume returns to normal.
![](/img/shft-ratio.png)


## TODO

- Provide cleaner solution for analysis summary
    - Display ratio break down for each shift (average, min, max)
    - Provide more than just a summary table
- Add a modality view bar chart
- Add after hours stat order volume
- Associate users with respective dataset. This may be organized by indivisual users or groups.
- Try to optimize. App runs slowly on large datasets
- Migrate to AWS