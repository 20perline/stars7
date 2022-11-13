import pstats
import os
from stars7 import settings

p = pstats.Stats(os.path.join(settings.DATA_DIR, 'profile.out'))
# "cumulative"对每个函数的执行时间进行排序，可以优先看到代码最慢的部分
p.sort_stats("cumtime")
p.print_stats()
# 可以显示函数被哪些函数调用
# p.print_callers()
# 可以显示哪个函数调用了哪些函数
# p.print_callees()
