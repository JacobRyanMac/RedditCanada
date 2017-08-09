select label, count(label) as count
from submissions
group by label
order by count desc;