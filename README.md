# Simple Working Time Tracking
> The *simpleWorktimeTracker* is currently a mere private project, still being actively developed and extended as I see
> fit and depending on my free time.

This project is a simple work time tracker. It currently only provides a command line interface, but may be extended to
include a web or desktop based graphical user interface. It stores all of the data saved in comma separated files in 
order to facilitate a wide range of further use of the data generated (e.g. loading in different data processing
applications, visualization in applications such as Excel...).

When using this project, you can do the following:
1. Select whether you want to enter working times for a single day or multiple days.
2. Select the date you want to add entries for. This defaults to the current date if simply left empty.
3. Enter start and end times as well as a description for as many work blocks on the selected date as you want.

For usage instructions see the [usage section](#Usage) below.

---

In it's current form, this project will save the inserted data into multiple ``csv`` files. There will be a file called
``year_month_monthName.csv`` (e.g. ``2020_05_May.csv``) created for each month that has some dates tracked. The columns
in each of these files are (spaces added for readability):
```text
date, start, end, work time, running total, description
```
The *running total* describes how much time has been worked after this entry is taken into consideration. As the 
entries are always sorted, this means that the running total is always the total time worked until the end of the work
 block.

One entry in such a file may look like this (spaces added for readability):
```text
03.05.2020, 10:00, 12:30, 2:30, 5:00, Wrote a README file
```

---

Additionally to this monthly work time tracking, a ``Summary.csv`` file will be created, which provides an overview 
over the total time worked each month as well as tracking required working time for that month and showing overtime
done all-time and per month. The columns in this file are (spaces added for readability):
```text
month, time done, running total, time required, overtime done, total overtime, hours per week
```
The *running total* and *total overtime* are again calculated by adding up all the total monthly working times 
respectively overtimes from the start of the file and including the current entry. The *hours per week* column keeps
track of hours that you are required to work each week in this month. This allows for different months to have 
different contractual requirements, which can be useful.

An example for the first two entries of a summary file would be (with spaces added for readability):
```text
March 2020, 154:30, 154:30, 155:00, -00:30, -00:30, 35.0
April 2020, 182:20, 332:50, 180:00, 02:20, 01:50, 42.0
```

## Usage
As the project is currently quite small, there aren't too many usage options. Invoke the tracking by calling:
```shell script
python TrackedMonth.py
```
If you want to add entries for multiple different dates, add the flag ``-m``.

After starting the tracking process, you will be prompted to enter a date for the entries. This currently needs to be in
the format ``dd.mm.yyyy``. Afterwards, you can add the start and end times for a work block in the format ``hh:mm`` or 
``h:mm``. For simplicity, seconds are not supported at this time. You can also add a description for the work block.
After having done this, you will be asked whether you want to add another entry for the same date. If you ran the 
tracking with the ``-m`` option, you will be asked whether you want to add another entry for a different date after you
are done with one date. 

For clarity, this is an example of what usage of this project may look like:
```shell script
python TrackedMonth.py -m

Date of work (dd.mm.yyyy), leave empty if today: 03.05.2020
Start time (hh:mm): 8:30
End time (hh:mm): 12:30
Work description: Work block one
Add another entry for the same date? (y/n) y

Start time (hh:mm): 13:30
End time (hh:mm): 17:30
Work description: Work block two
Add another entry for the same date? (y/n) n
Do you want to want to add entries for another date? (y/n) y

Date of work (dd.mm.yyyy), leave empty if today: 04.05.2020
Start time (hh:mm): 8:30
End time (hh:mm): 12:30
Work description: Work block one, Day two
Add another entry for the same date? (y/n) y

Start time (hh:mm): 13:30
End time (hh:mm): 17:30
Work description: Work block two, Day two
Add another entry for the same date? (y/n) n
Do you want to want to add entries for another date? (y/n) n
```
