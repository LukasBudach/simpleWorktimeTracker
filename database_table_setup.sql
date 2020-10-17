CREATE TABLE jobs (
    title           varchar(100) PRIMARY KEY,
    summary_table   varchar(100),
    data_table      varchar(100)
);

CREATE TABLE abstractsummary (
    month           varchar(15),
    time_done       integer,
    time_required   integer,
    overtime_done   integer,
    hours_per_week  real,
    running_total   integer,
    total_overtime  integer,
    PRIMARY KEY(month)
);

CREATE TABLE abstractdata (
    start_time      timestamp,
    end_time        timestamp,
    running_total   integer,
    description     text,
    PRIMARY KEY(start_time)
);