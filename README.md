
# Detecting Bursty Terms in Computer sSience
*burst-detection*

Research topics rise and fall in popularity over time, some more swiftly than others. The fastest rising topics are typically called *bursts*; e.g. "deep learning", "internet of things" and "big data". Being able to detect and track bursty terms in the literature could give insight into how scientific thought evolves over time.

In this repository, we take a trend detection algorithm from technical stock market analysis and apply it to 31 years of computer science research abstracts, treating the prevalence of each term in the dataset like the price of a stock. Unlike previous work in this domain, we use the free text of abstracts and titles, resulting in a finer-grained analysis. We report a list of bursty terms, then use historical data to build a classifier to predict whether they will rise or fall in popularity in the future, obtaining accuracy in the region of 80%. As a consequence, we now have a pipeline that can be applied to any time-ordered collection of text to yield past and present bursty terms and predict their probable fate.
