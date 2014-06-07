import webapp2

route_list = [
	webapp2.Route(r'/', handler='handlers.RoutingHandler:base_url', methods="GET"),
	webapp2.Route(r'/_ah/warmup', handler='handlers.RoutingHandler:warm_up', methods="GET"),
    webapp2.Route(r'/route', handler='handlers.RoutingHandler:route'),
    webapp2.Route(r'/end', handler='handlers.RoutingHandler:end'),
    webapp2.Route(r'/message', handler='handlers.RoutingHandler:message'),
    webapp2.Route(r'/agent', handler='handlers.AgentHandler:post', methods="POST"),
    webapp2.Route(r'/agent/<id>', handler='handlers.AgentHandler:delete', methods="DELETE"),
    webapp2.Route(r'/calls/active/count', handler='handlers.RoutingHandler:get_active_calls', methods="GET")
]