REASEARCH NOTE
Hypothesis- "After a significant one-day fall in NIFTY, the market tends to recover over the next few trading days."
So the hypothesis says a significant fall without any number so when i was assuming the number i kept this in mind that the number can't be too small like 0.05% because it is not that significant and it is common in the regular market so i choose 2% which makes it a significant dip in the market.

Data - i extracted the data using python in vs code, I downloded roughly about 19 years of data (daily trading data) spanning from september 2207 to september 2026 (4,664 trading days).
I validated the dataset to confirm that the data is not missing dates or that none  of the data is corrupted.
And after research i got the result that the mark which i choose 2% had several dip around 200 times and after filtering the data , removing incorrect or overlapping event the number was 101 .
So if there is a dip of 2% in the market and buying the share that day is quite uncommon occurrence because it can either be luck or prior knowledge.
So I assume the buying of the share next day. eg: if the 2% dip happened on monday so i bought the share on tuesday morning at that price.
Cost- deduction of 0.20% on every round trip trade to account for brokerage, government taxes and real world friction.
Returns-1 day : average return was nearly zero (+0.09%).
        3 day : average return was +0.39%.
        5 day : average return was +0.44%.
        10 day: average return was +0.81%

CONCLUSION:
Yes, the market does drifts up slightly over 10 days but it is not statistically proven,
After running the bootstrap test the result was that a result must have a p-value below 0.05 to be considered statistically significant. this means the slight recovery could easily be randon variation.
It makes far less money than doing nothing, while taking massive risk and the pattern is not exactly full prove truth because the hypothesis will totally fall apart at the time like 2008 crisis or covid crisis.
