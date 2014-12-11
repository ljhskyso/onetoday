# -----------------------------------------------begin: 12/11 by Jiheng
from NSL_get_keyword import NSL_get_keyword
# -----------------------------------------------end:   12/11 by Jiheng

txt = "@onetoday what i can do for #africa? i want to be a #hero! find me a project"
rsp = NSL_get_keyword( txt )
print( len(rsp) )