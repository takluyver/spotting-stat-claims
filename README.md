# Spotting statistical claims

Full Fact Hackathon at PyData London 2017

We are scanning text to identify statistical claims. We look for numbers,
monetary amounts, percentages, and terms such as 'increase' or 'decrease'. We
try to avoid false positives, such as "Article 37".

This works with XML files [from this Hansard data set](https://fullfact.org/media/hansard.zip).

To run the demo:

    ./statclaims.py --html hansard/src/debates2017-01-23d.xml

Then open `index.html` to see the output. You can pass multiple files at once.
Leaving out `--html` will show output in the terminal.

Notes [in a Google Doc](https://docs.google.com/document/d/1Bc3wGsILL6EaWMXLJPDLIwMDk3R-k4o-AF-7ILgCEDQ/edit?usp=sharing).
