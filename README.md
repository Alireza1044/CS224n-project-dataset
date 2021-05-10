# CS224n Final Project Dataset

Code to gather dataset for Stanford CS224n course project.

To gather the dataset run:
```bash
python main.py -c -p -s
```

All arguments are optional and default to False:
```bash
usage: main.py [-h] [-c] [-p] [-s]

optional arguments:
  -h, --help     show help message and exit
  -c, --crawl    Whether to crawl the raw data or not. default: False
  -p, --process  Whether to clean and process the raw data or not. default: False
  -s, --stats    Whether to report statistics of the data. default: False
```
All of the data is also available [here](data).

Please read the [documentation](Dataset%20Documentation.pdf) for more info about the dataset.
