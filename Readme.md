## data_filter -- a smart filter for telemetry data

# V.Zavjalov, 2021.03.06

This filter may be useful for a sensor which produces data regularly, to
remove long periods of non-changing data and keep all important
features.

Example 1. Plot of original and filtered data, low noise level.
![data1](https://raw.githubusercontent.com/slazav/data_filter/main/img/data1.png)

Example 2. Here noise level is determined automatically, all features
above the noise are shown on the output:
![data1](https://raw.githubusercontent.com/slazav/data_filter/main/img/data2.png)

Example 3. Noisy data processed with different filter settings: narrow
peaks are skipped by limiting minimum buffer size, noise level set
manually.
![data1](https://raw.githubusercontent.com/slazav/data_filter/main/img/data3.png)

Program is written in TCL and contains function which can be used as an
input filter in `graphene` database ( https://github.com/slazav/graphene ).

#### Usage:
```
data_filter.tcl [options] < <input> > <output>
```

#### Options:

* `--column <v>` -- data column to use (default: 0)
* `--maxn <v>`    -- upper limit for buffer size (default: 100 points, use 0 for no limit)
* `--maxt <v>`    -- upper limit for buffer time span (default: 0, no limit)
* `--minn <v>`    -- lower limit for buffer size (default: 0)
* `--mint <v>`    -- lower limit for buffer time span (default: 0)
* `--noise <v>`       -- noise level (default: 0)
* `--auto_noise <v>`  -- strength of automatic noise calibration (default 1, use 0 to switch off the calibration)

Input file contains lines with multiple columns. Empty lines and lines
started with `#` are printed to the output without changes. First column
is "time", it should monotonically increase, other columns are "data".
Filter uses a single data column which can be selected with `--column`
parameter. Filter modifies data by either removing data lines from the
input or sending them to the output without modification.

Parameters `--maxn` and `--maxt` control largest size of the working data
buffer. Usually, if there is no interesting features in the data,
distance between points on the output is approximately 1/2 of the maximum
buffer size.

Parameters `--minn` and `--mint` control smallest size of the working data
buffer. All features shorter then this size are filtered out. This may be
useful for smoothing noisy data.

Parameter `--noise` allows to set noise level manually. There is also
an automatic noise calibration controlled by `--auto_noise` option. If
both are non-zero, then maximum of manual and automatic values is used.
It may be reasonable to set `--noise` to resolution of your sensor and
keep default `--auto_noise` setting too.


#### Algorithm (without noise calibration)

On each step the filter function receives one point with timestamp and
data and can return a point, or skip it. It also has a storage to
keep data (buffer and previous point `t0,d0`) between steps.

The very first point is immediately printed to the output.
Every incoming point is added to the buffer. Before this, if buffer contains
more then 3 points following steps are done:

* Buffer of length `n>=3` is fitted with a 2-segment line which start at the
first buffer point (which is also the previously printed point), has a node at a
timestamp with index `0<j<n` inside the buffer, and ends at the last point.
The only one fitting parameter is index `j`.

* When finding best `j` weighting function `f(j) = 1 + 2j(j-n-1)/(n-1)^2` is
used (quadratic function with `f(0) = f(n-1) = 1`, `f((n-1)/2) = 1/2` ).
Without this weighting, for flat noisy data a simple 2-segment fit will
give almost random position of the node point. Without a good reason we
do not want to have it close to the beginning (to avoid too short
segments), or to the end (to avoid random slope of the second segment and
bad evaluation of the stopping condition).

* Stopping condition is evaluated. We want to print the node point
to the output in the following cases:

  * Number of points in the buffer is larger then `--maxn`.

  * Time span of the buffer is longer then `--maxt` parameter

  * Second segment is much longer (4 or more times) then the first one.
  If the first segment in the fit is short, it means that there is an
  important feature in the beginning of the buffer, and there is no need
  to continue adding points. This always happens after sharp steps or
  peaks.

  * Difference between the incoming point (which is not in the buffer yet)
  and the fit is larger then 2*(noise level).

  * Maximum deviation of the buffer data from the fit is larger then
  the noise level.

* If buffer size is smaller then `--minn/--mint` settings, then stopping
condition is cleared.

* If the stopping condition is satisfied, the node point (`tj,dj`)
is sent to the output. First `j-1` points are removed from the buffer.

#### Noise calibration

If parameter `--auto_noise` is not 0, then noise calibration is
done in the beginning of each cycle. First non-trivial problem is
to choose data for calibration. We want to use a fixed number of points (30)
located near beginning of the buffer. If buffer is large enough we use it.
If not (this happens near data features when points are printed ), we use
a separate sliding buffer of correct size.

#### Non-standard timestamps

Time column can be non-numeric. Functions `dt = time_diff(t1,t2)` and `t
= time_add(t0,dt)` can be defined to calculate numeric difference
`dt=t2-t1` and to add numeric difference to a timestamp `t=t0+dt`. When
used in `graphene` database, existing library functions can be used.
