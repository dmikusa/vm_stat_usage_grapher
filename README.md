# Usage Grapher

A simple app that will capture output from vm_stat, save and graph it.  This was put together as a demo for the [2015 MacAdmins Conference at Penn State University](http://macadmins.psu.edu/).

## Usage

Here's the full usage.

```
$ python usage_grapher/usage_grapher.py
USAGE:
	usage_grapher/usage_grapher.py collect [interval]
	usage_grapher/usage_grapher.py render [keys]
```

Run `collect` first.  This will append data to the CSV file at `/tmp/usage_grapher.csv`.  Then run `render` to create a graph from the data that has accumulated.

## Development

To get started.

1. Create a virtualenv.  `virtualenv env`.
2. Activate.  `source ./env/bin/activate`.
3. Install test deps.  `pip install -r requirements-dev.txt`.
4. Run `nosetests .` for a single test or `tdaemon --ignore-dir=env` for continuous testing.

## Ideas to Expand Project

If you're interested in expanding on this project, here are some ideas.

1. Parse arguments using `argparse` or `click`.
2. Make data storage more flexible.  
  - Don't keep it in `/tmp`.
  - Handle when the file doesn't exists (with `render`)
  - Offer a way to clear the data
3. Add date time stamp to the data file
4. Use date time stamp as X-series on generated graphs
5. Be more memory efficient (i.e. don't load entire data set into memory)

