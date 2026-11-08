import json,sys
def compile_policy(policy):
    ids=[r['id'] for r in policy['requirements']]
    if len(ids)!=len(set(ids)): raise ValueError('requirement IDs must be unique')
    return policy['requirements']
def evaluate(requirements,events):
    out=[]
    for r in requirements:
        found=any(e.get('type')==r['event_type'] and e.get(r['field'])==r['equals'] for e in events)
        out.append({'requirement':r['id'],'satisfied':found})
    return {'satisfied':sum(x['satisfied'] for x in out),'total':len(out),'checks':out}
if __name__=='__main__':
    policy=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'policy.json',encoding='utf-8'))
    events=[{'type':'evaluation','result':'passed'},{'type':'risk_review','result':'approved'},{'type':'human_approval','result':'approved'}]
    print(json.dumps({'policy_version':policy['policy_version'],**evaluate(compile_policy(policy),events)},indent=2))
