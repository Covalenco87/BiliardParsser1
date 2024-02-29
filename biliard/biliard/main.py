from scrapy import cmdline
cmdline.execute("scrapy crawl biliard -O bil2.json".split())
cmdline.execute("scrapy crawl biliard1 -o bil2.json".split())
