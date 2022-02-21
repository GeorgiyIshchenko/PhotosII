from Functions import Education

from redis import Redis
import rq
queue = rq.Queue('list0', connection=Redis.from_url('redis://'))
args = []
job = queue.enqueue(Education, *args, job_timeout=3000)