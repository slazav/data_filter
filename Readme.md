## data_filter -- a smart filter for telemetry data

This filter may be useful for a sensor which produces data regularly, to
remove/average long periods of non-changing data and keep all important
features.

Program is written in TCL and contains function which can be used as an
input filter in `graphene` database.

#### Usage:
```
data_filter [options] < <input> > <output>
```

#### Options:

* `-c, --column <v>` -- data column to use (default: 0)
* `-n|--maxn <v>`    -- maximum number of skipped/averaged points (default: 0, no limit)
* `-t|--maxt`        -- maximum time between points (default: 0, no limit)
* `-d|--maxd`        -- noise level (default: 1)
* `-a|--avrg 1|0`    -- use average/skip mode (default 1, average)

Input file contains lines with multiple columns. Empty lines and lines
started with `#` are printed to the output without changes. First column
is "time", others are "data". Filter uses a single data column which can
be selected with `--column` parameter. In averaging mode (`--avrg 1`)
only this column is printed to the output, overwise original lines with
all columns will be printed.

#### Examples

Following images are made using scripts in `examples/` folder. Magenta
points are original data, green and blue are filter output made with
options `--avrg 0` and `--avrg 1`.  Other options are `--maxd 1.5 --maxn
50`.

![data1](https://raw.githubusercontent.com/slazav/data_filter/main/img/data1.png)

![data2](https://raw.githubusercontent.com/slazav/data_filter/main/img/data2.png)