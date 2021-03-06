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

#### Algorithm

On each step the filter function receives one point with timestamp and
data and can return a point, or skip it. It also has a storage to
keep data (buffer and previous point `t0,d0`) between steps.

The very first point is printed to the output without modifications.
Every incoming point is added to the buffer. Before this, if buffer contains
more then 3 points following steps are done:

* Buffer of length `n>=3` is fitted with a 2-segment line which start at the previous point
and has a node at a timestamp with index `0<j<3` inside the buffer.
The fitting function is `d0 + A*(t-t0) + (t>tj)? B*(t-tj):0` with free
parameters A, B and tj. Optimisation for `A` and `B` is done analytically
for all possible values of `j`, and then the best position of the node `j`
is found.

* When finding best `j` weighting function `f(j) = 1 + 2j(j-n-1)/(n-1)^2` is
used (quadratic function with `f(0) = f(n-1) = 1`, `f((n-1)/2) = 1/2` ).
If we have flat noisy data than simple 2-segment fit will give almost
random position of the node point. Without a good reason we do not want
to have it close to the beginning (to avoid too short segments), or to
the end (to avoid random slope of the second segment and bad evaluation
of the stopping condition).

* Stopping condition is evaluated. We want to print the node point
to the output in the following cases:

  * Number of points in the buffer is larger then `--maxn`.

  * Time span of the buffer is longer then `--maxt` parameter

  * Second segment is much longer (5 or more times) then the first one.
  If the first segment in the fit is short, it means that there is an
  important feature in the beginning of the buffer, and there is no need
  to continue adding points. This always happens after sharp steps or
  peaks.

  * Difference between the incoming point (which is not in the buffer yet)
  and the fit is larger then the noise level `--maxd`.

* If the stopping condition is satisfied, the node point (`tj, d0 + A*(tj-t0)`)
is sent to the output. First `j-1` points are removed from the buffer.

#### Non-standard timestamps

Time column can be non-numeric. Functions `dt = time_diff(t1,t2)` and `t
= time_add(t0,dt)` can be defined to calculate numeric difference
`dt=t2-t1` and to add numeric difference to a timestamp `t=t0+dt`. When
used in `graphene` database, existing library functions can be used.
