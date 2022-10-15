from stars7.rectangle import Rectangle
from stars7.feed import Feed
from stars7.strategies import even, serialsum, single, twins
from stars7.database import SportDatabase


db = SportDatabase()
db.refresh()

feed1 = Feed()
rect1 = Rectangle(start_col=1, rows=4, cols=5)

strategy1 = serialsum.EqualSumStrategy(rect=rect1, offset=0, column_offset=1, elements=1, works_at_least=3)
strategy1.execute(feed1)

strategy5 = serialsum.OddEvenSumStrategy(rect=rect1, offset=0, elements=2, works_at_least=4)
strategy5.execute(feed1)

strategy21 = single.SingleSameStrategy(rect=rect1, column_offset=-1, works_at_least=2)
strategy22 = single.SingleIncreaseStrategy(rect=rect1, column_offset=1, works_at_least=2)
strategy23 = single.SingleDecreaseStrategy(rect=rect1, column_offset=0, works_at_least=2)

strategy21.execute(feed1)
strategy22.execute(feed1)
strategy23.execute(feed1)

strategy3 = twins.TwinsStrategy(rect=rect1, works_at_least=2)
strategy3.execute(feed1)

strategy6 = twins.OppositeStrategy(rect=rect1, works_at_least=3)
strategy6.execute(feed1)

strategy4 = even.AlternatedSumStrategy(rect=rect1, offset=0, elements=4, works_at_least=3)
strategy4.execute(feed1)
