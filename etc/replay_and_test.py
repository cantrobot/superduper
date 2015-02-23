#   $ mitmdump -s /vagrant/replay_and_test.py &
#   $ curl -x http://localhost:8080 http://localhost:8000 # success
import re
import uuid

state = {}
matcher = re.compile('<li><a href=".bashrc">.bashrc</a>')
host_id_match = re.compile('host_id=([\S]+);')

def _all_finished(tracker_state, items):
    for item in items:
        if False in [v[item] for k,v in tracker_state.iteritems()]:
            return False
    return True

def _compare(tracker_state):
    values = [v for k,v in tracker_state.iteritems() if 'host_id' not in v.keys()]
    expected_values = len(values[0].keys())
    value_set = (set(v.items()) for v in values)
    value_set_r = reduce(set.intersection, value_set)
    total_values = [v[1] for v in value_set_r]
    if len(total_values) == expected_values:
        print "Success: %s" % str(values[0]['code'])
        return True
    else:
        print "Fail:"
        for host, result in tracker_state.iteritems():
            print "  %s: code=%s match=%s" % (host, str(result['code']), str(result['match']))
        return False
    return False

def request(context, flow):
    global state
    tracker_id = str(uuid.uuid4())
    state[tracker_id] = {
        'orig': {
            'code': False,
            'match': False
        },
        'dup': {
            'code': False,
            'match': False,
            'host_id': None,
        }
    }
    flow.request.headers["tracker"] = [tracker_id]
    flow.request.headers["group"] = ['orig']
    flow_dup = context.duplicate_flow(flow)
    flow_dup.request.port = 8001
    flow_dup.request.headers["group"] = ['dup']
    context.replay_request(flow_dup)

def response(context, flow):
    global state
    global matcher
    match = False
    if 'tracker' in flow.request.headers.keys():
        tracker_id = flow.request.headers['tracker'][0]
        if tracker_id in state.keys():
            code = flow.response.code
            group = flow.request.headers['group'][0]
            if matcher.search(flow.response.content):
                match = True
            if 'set-cookie' in flow.response.headers.keys():
                host_id = host_id_match.search(flow.response.headers['set-cookie'][0])
                state[tracker_id][group]['host_id'] = host_id.group(1)
            state[tracker_id][group]['code'] = code
            state[tracker_id][group]['match'] = match
            if _all_finished(state[tracker_id], ['code']):
                result = _compare(state[tracker_id])
                host = state[tracker_id]['dup']['host_id']
                del state[tracker_id][group]['host_id']
                o = ','.join(["%s=%s" % (k,v) for k,v in state[tracker_id]['orig'].iteritems()])
                d = ','.join(["%s=%s" % (k,v) for k,v in state[tracker_id]['dup'].iteritems()])
                out_string = "%s: dup=%s orig=%s\n" % ("Success" if result else "Failure", d, o)
                open("/var/log/superduper/%s-result.log" % host, 'a').write(out_string)
                del state[tracker_id]
