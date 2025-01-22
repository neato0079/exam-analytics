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

### Example graph

![](/img/grph.png)

## TODO

- Provide cleaner solution for analysis summary
    - Add totals for shift views
    - Display avg number of exams
- Add a modality view bar chart
- Add exam complete: exam ordered ratio view
- Add after hours stat order volume
- Add user log in