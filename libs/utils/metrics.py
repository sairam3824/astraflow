from prometheus_client import Counter, Histogram, Gauge
import time
from functools import wraps

# HTTP Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Celery Metrics
celery_task_duration_seconds = Histogram(
    'celery_task_duration_seconds',
    'Celery task duration',
    ['task_name']
)

# LLM Metrics
llm_api_calls_total = Counter(
    'llm_api_calls_total',
    'Total LLM API calls',
    ['provider', 'model']
)

llm_tokens_used_total = Counter(
    'llm_tokens_used_total',
    'Total tokens used',
    ['provider', 'model']
)

# Vector Search Metrics
vector_search_duration_seconds = Histogram(
    'vector_search_duration_seconds',
    'Vector search duration',
    ['collection_id']
)

def track_time(metric: Histogram, labels: dict = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start
                if labels:
                    metric.labels(**labels).observe(duration)
                else:
                    metric.observe(duration)
        return wrapper
    return decorator
