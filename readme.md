# twitter
twitter.py is a small python script for searching twitter on a linux shell. twitter uses the TwitterSearch module.

# requirements
- TwitterSearch (sudo -H pip install TwitterSearch)
- [Twitter developer api access](https://dev.twitter.com/)


# installation
```shell
$ sudo -H pip install TwitterSearch
$ git clone https://github.com/hvanderlaan/twitter
$ cd twitter
$ ./twitter.py --help
usage: twitter.py [-h] [-a AMOUNT] [-c CONFIG] [-d] [-l {en,nl}]
                  [-t TAG [TAG ...]] [-u USER]

optional arguments:
    -h, --help            show this help message and exit
    -a AMOUNT, --amount AMOUNT
                          display amount of tweets
    -c CONFIG, --config CONFIG
                          configuration file
    -d, --daemon          automatic refresh every 60 seconds
    -l {en,nl}, --lang {en,nl}
                          language of the tweet
    -t TAG [TAG ...], --tag TAG [TAG ...]
                          display tweets with hashtag
    -u USER, --user USER  display tweets from user
```
