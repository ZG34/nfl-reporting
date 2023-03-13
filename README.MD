## Football Data Reporting Dashboard

<img src="https://i.gyazo.com/9ce330c34fcefa5cf6b1046a38f2f554.png " width="400">

<img src="https://i.gyazo.com/a639a9a1556cea884af232a4199c6841.png " width="300">

<img src="https://i.gyazo.com/00e5024f5ee7dfd2fba3f000fc5144c7.png " width="300">

### Why use this dashboard / what does it solve?
* You track play-by-play data via a spreadsheet, and would like tranform spreadsheet data to generate specific insights.

* With this dashboard, you can formulate and answer fairly specific questions dynamically. Questions such as:
  - In 4th quarters vs Seattle, which plays have success against their Cover 1 calls?
    Answer: Pass calls attack the backside cornerback. Run calls are often inside zone with good success. 
  - When New England's final formation is 3x1 on 3rd & 6, what are they aiming to attack? 
    Answer: underneath interior zones with quick concepts.

### Process
> Track play-by-play data manually in Excel.

> Use pandas to read Excel sheet into an SQL database.

> Use SQL queries to clean and standardize the data.

> Explore available data, and formulate questions to be answered.

> Translate questions into SQL queries.

> Design user interface to allow for generation of SQL queries along similar lines, to allow for dynamic question-answer workflow for any user.

> Implement visualizations to assist in recognition of answers to posed questions. 


### Features
* Specific, multi variable filters for large sets of data
* Generate printable report for 3rd down data

### Primary Tools Used
* SQLite
* Matplotlob & Seaborn
* Tkinter
* Pandas
* PIL
