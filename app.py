from stars7.rectangle import Rectangle
from stars7.feed import Feed
from stars7.strategies import alternatedsum, serialsum, simple, twins


feed1 = Feed()
split_row = feed1.split_row
rect1 = Rectangle(start_col=1, rows=4, cols=5)
strategy1 = serialsum.SerialSumStrategy(rect=rect1, offset=split_row, column_offset=0, elements=3, works_at_least=3)

strategy2 = simple.SimpleStrategy(rect=rect1, pos=3, works_at_least=2)

strategy3 = twins.TwinsStrategy(rect=rect1, works_at_least=2)

strategy4 = alternatedsum.AlternatedSumStrategy(rect=rect1, offset=split_row, elements=2, works_at_least=2)

strategy4.execute(feed1)
# strategy2.execute(feed1)
# strategy3.execute(feed1)
