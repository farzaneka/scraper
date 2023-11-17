from nameko.standalone.rpc import ClusterRpcProxy

from gateway.service import config


def authenticate(func):
    def wrapper(request):
        with ClusterRpcProxy(config) as cluster_rpc:
            is_verify = cluster_rpc.authentication.verify_user(
                request

            )
            if is_verify is True:
                return func(request)

    return wrapper

