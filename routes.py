from loafer.ext.aws.routes import SQSRoute
from .handlers import norm_handler, error_handler

# assuming a queue named "loafer-test"
routes = (
    SQSRoute('incoming', {'options': {'WaitTimeSeconds': 3}},
             handler=norm_handler,
             error_handler=error_handler),
)
