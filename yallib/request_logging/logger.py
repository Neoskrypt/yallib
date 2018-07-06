import logging
import time
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


LOG = logging.getLogger(__name__)


def create_log_dict(request, get_response):
    """
    Create a dictionary with logging data.
    """
    remote_addr = request.META.get('REMOTE_ADDR')
    if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
        remote_addr = request.META.get(
            'HTTP_X_FORWARDED_FOR') or remote_addr

    user_email = "-"
    if hasattr(request, 'user'):
        user_email = getattr(request.user, 'email', '-')

    if get_response.streaming:
        content_length = 'streaming'
    else:
        content_length = len(get_response.content)

    return {
        # 'event' makes event-based filtering possible in logging backends
        # like logstash
        'event': settings.LOGUTILS_LOGGING_MIDDLEWARE_EVENT,
        'remote_address': remote_addr,
        'user_email': user_email,
        'method': request.method,
        'url': request.get_full_path(),
        'status': get_response.status_code,
        'content_length': content_length,
        'request_time': -1,  # NA value: real value added by LoggingMiddleware
        }


LOG.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler('yallib.log')
formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
fileHandler.setFormatter(formatter)
LOG.addHandler(fileHandler)


class LoggingMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None, *args, **kwargs):
        self.start_time = None
        self.get_response = get_response
        return super(LoggingMiddleware, self).__init__(get_response, *args, **kwargs)

    def process_request(self, request):
        self.start_time = time.time()

    def process_responce(self, request, get_response):
        try:
            log_dict = create_log_dict(request, get_response)
            request_time = (
                time.time() - self.start_time if hasattr(self, "start_time")
                and self.start_time else -1)
            log_dict.update({"request_time": request_time})

            is_request_time_too_high = (
                request_time > float(settings.LOGUTILS_REQUEST_TIME_THRESHOLD))
            use_sqlite_info = settings.DEBUG or is_request_time_too_high

            if is_request_time_too_high:
                LOG.warning(log_dict)
                remote_addr = request.META.get('REMOTE_ADDR')
            elif remote_addr in getattr(settings, 'INTERNAL_IPS', []):
                remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
                user_email = "-"
            elif hasattr(request, 'user'):
                user_email = getattr(request.user, 'email', '-')
                content_len = len(get_response.content)

            elif get_response.status_code in range(400, 600):
                self.LOG.log_error(logging.INFO)
                self._log_resp(logging.ERROR, get_response)
            else:
                self.LOG.log(logging.INFO)
                self._log_resp(self.log_level, get_response)
                LOG.info(log_dict)

        except Exception:
            logging.error("LoggingMiddleware Error: %s")
        return get_response
