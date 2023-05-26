## Project for scrapy product info from aliexpress
Give a keyword or a file contain keyword , then the program will start a spider to scrawl the aliexpress, and grap product info

## Installation
scrapyexpress is written in python3,You can also install it comfortably with pip
```
virtualenv --python python3 env
source env/bin/activate
pip3 install -e .
```

## Usage
1. Scrapy the data from aliexpress site use one keyword
```
scrapyexpress -k keyword
```

2. Scrapy the data from aliexpress site use one keyword file
```
scrapyexpress -f /path/to/keyword
```

