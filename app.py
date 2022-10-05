from stars7.rectangle import Rectangle
from stars7.feed import Feed
from stars7.strategies import serialsum, simple, twins


feed1 = Feed()
rect1 = Rectangle(start_col=1, rows=3, cols=5)
strategy1 = serialsum.SerialSumStrategy(rect=rect1, elements=4, works_at_least=3)

strategy2 = simple.SimpleStrategy(rect=rect1, pos=3, works_at_least=2)

strategy3 = twins.TwinsStrategy(rect=rect1, works_at_least=2)

# strategy1.execute(feed1)
strategy2.execute(feed1)
# strategy3.execute(feed1)
