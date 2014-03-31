sunglasses
==========

A small weekend project to asynchronously scrape the Ontario Public Sector Salary Disclosure list (a.k.a. the sunshine
list), using `asyncio` (formerly `tulip`) available for Python 3.3 (and built-in to Python 3.4)

Requirements
------------
* Python 3.3+
* asyncio (built-in to Python 3.4 and above)
* aiohttp
* lxml
* tqdm

How to use
----------

Simply run:

```python sunglasses.py
```

And it'll show you the progress as it downloads and saves data to CSV files in their respective categories. By default,
this tool dumps everything into a `data` folder in the same folder as the script.

Future Plans
------------

* Option to merge all data into 1 big file
* Option to only download certain data categories
* Option to save output elsewhere