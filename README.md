
# README

### Introduction

These are spripts written to take part in recruitment for Python Intern.

### TASK 1 - CSV Report Processing

##### About
Script converts report containing data about daily impression numbers and CTRs for ad campaign, aggregated per state into new report with the daily number of impression and clicks aggregated per country.
##### Input file
Input file has to be csv file with 4 columns containing date (format %m/%d/%Y), state name (according to standard ISO 3166-2), number of impressions and CTR. Encoding of input file has to be `utf-8` or `utf-16`.

Path to the input file has to be passed while running the scrpit. 
Example execution:
`python add-report-processor.py 'example.csv'`
##### Output file
Final result is saved in `outputReport.csv` file created in directory where script was executed. Output csv contains columns `date`, `countryCode`, `impressions` and `clicks` containing date (fomat %Y-%m-%d), country code (according to standard ISO 3166) or XXX when country hasn't been recognized, number of impressions and number of clicks.
##### Critical errors
Every error that makes it impossible to read or write data is considered as critical and results in breaking operations without generating report. Examples of critical errors:
- no input file
- wrong extension of input file
- unexpected encoding of input file
- no authorization to create output file

If input file contain row with incorrect data, this row will be ignored and report will be generated despite this.

### TASK 2 - Web Crawler 

##### About
web-crawler.py file contain site_map(url) function that creates map of given domain with accessible links (within that domain) contained in a and area tags. Map has form of Python dictionary.
##### Output 
Map has following structure:
```
{<url addres> : {'title' : <title of page>, 'links' : <set of accessible links on page>}, ...}
```


```python

```
