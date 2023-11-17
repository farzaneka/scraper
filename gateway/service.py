import json

from nameko.exceptions import BadRequest
from nameko.rpc import RpcProxy
from nameko.standalone.rpc import ClusterRpcProxy
from nameko.web.handlers import http


config = {
    'AMQP_URI': "pyamqp://guest:guest@localhost"
}


class GatewayService(object):
    """
    Service acts as a gateway to other services over http.
    """

    name = 'gateway'

    feeds_rpc = RpcProxy('feeds')
    users_rpc = RpcProxy('authentication')

    @http("POST", "/login")
    def login_member(self, request):
        with ClusterRpcProxy(config) as cluster_rpc:
            authentication = cluster_rpc.authentication.login_member(
                request.get_json()

            )
        return authentication

    @http("POST", "/register")
    def register_member(self, request):
        with ClusterRpcProxy(config) as cluster_rpc:
            register = cluster_rpc.authentication.register_member(
                request.get_json()

            )
        return register

    @http("POST", "/feeds", expected_exceptions=BadRequest)
    def create_feed(self, request):
        with ClusterRpcProxy(config) as cluster_rpc:
            # self._verify_token(request)
            expected_member = cluster_rpc.authentication.get_member(
                request.get_json()['member_id']
            )
            if expected_member is not None:
                feed = cluster_rpc.feeds.create_feed(
                    request.get_json()['url'],
                    expected_member,
                )
                cluster_rpc.feeds.create_feed_items.call_async(
                    request.get_json()['url'],
                    json.loads(feed)['id'],
                )
            else:
                raise BadRequest('Member not found')

        return feed

    @http("PATCH", "/feeds", expected_exceptions=BadRequest)
    def update_feed(self, request):
        with ClusterRpcProxy(config) as cluster_rpc:
            # self._verify_token(request)
            expected_member = cluster_rpc.authentication.get_member(
                request.get_json()['member_id']
            )
            if expected_member is not None:
                data = request.get_json()
                feed = cluster_rpc.feeds.update_feed(
                    data['feed_id'],
                    data['url'],
                )
                cluster_rpc.feeds.create_feed_items.call_async(
                    data['url'],
                    data['feed_id'],
                )
            else:
                raise BadRequest('Member not found')

        return feed

    @http("POST", "/feeds/<int:feed_id>/subscribe")
    def subscribe_feed_item(self, request, feed_id):
        with ClusterRpcProxy(config) as cluster_rpc:
            result = cluster_rpc.feeds.subscribe_feed_item(feed_id)

        return result

    @http("POST", "/bookmarks", expected_exceptions=BadRequest)
    def create_bookmark(self, request):
        with ClusterRpcProxy(config) as cluster_rpc:
            # self._verify_token(request)
            expected_member = cluster_rpc.authentication.get_member(
                request.get_json()['member_id']
            )
            if expected_member is not None:
                data = request.get_json()
                feed = cluster_rpc.feeds.create_bookmark(
                    data['feed_item_id'],
                    expected_member
                )
            else:
                raise BadRequest('Member not found')

        return feed

    @http("GET", "/bookmarks/<int:member_id>", expected_exceptions=BadRequest)
    def list_bookmark(self, request, member_id):
        with ClusterRpcProxy(config) as cluster_rpc:
            # self._verify_token(request)
            expected_member = cluster_rpc.authentication.get_member(member_id)
            if expected_member is not None:
                bookmarks = cluster_rpc.feeds.list_bookmark(expected_member)
            else:
                raise BadRequest('Member not found')

        return bookmarks

    # @staticmethod
    # def _verify_token(request):
    #     with ClusterRpcProxy(config) as cluster_rpc:
    #         cluster_rpc.authentication.verify_token(request)

