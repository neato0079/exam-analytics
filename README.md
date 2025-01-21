# Exam-Analytics
Analyzes a radiology exam dataset and generates graphs on user-set filters.

- Runs on the `Django` frame work.
- Utilizes `Pandas` library for dataset analysis.
- Utilizes `Matplotlib` for data visualization.
- Unit testing done with `pytest`
- Currently running on `Render` cloud service

## Progress . . .
- Allow user to upload and store `.csv` to app
- Various filters are now functional for graph generation

## Breakdown
- Compatible datasets(just `.csv` files for now) is essentially HL7 data organized by the following columns:

```
        COLUMN NAME                      HL7 ORM Segment
        ______________________________________________________________________
        'Exam Complete Date/Tm' . . . . . ORC.5 (order status is complete)
        'Order Procedure Accession' . . . ORC.2
        'Exam Order Date/Time'. . . . . . ORC.15 ex:'YYYY-mm-ddTHH:MM:SS'
        'Final Date/Tm' . . . . . . . . . OBR.22.1 (time of final report)
        'Exam Order Name' . . . . . . . . OBR.4
        'Modality'. . . . . . . . . . . . OBR.24
```
- Modality can be inferred if the accession number or order name implies a modality
- This data is then formatted and analyzed

wip.....

### Example graph

![](/img/grph.png)

### Notes

- Run server with `python manage.py runserver`
- Get back into the python env looking into the env/bin directory. instructions there