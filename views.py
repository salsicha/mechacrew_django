# Create your views here.
from django.core import serializers
from mechacrew.basic.models import Vehicle, Game, Turret, Crew
from django.http import HttpResponse, HttpRequest


def game_json(request, game_id, controlled_id, do_dict=False, log_message='No log message.'):

    results = [   ]
    game = Game.objects.get(pk=game_id)
    
    #as_dict = {'game':game, 'players' : {}}
    for c in game.crew_set.all():
        results.append(c)
        #as_dict['players'][p.id] = {'player': p, 'vehicles':{}, 'turrets':{}}
        for v in c.vehicle_set.all():
            results.append(v)
            #as_dict['players'][p.id]['vehicles'][v.id] = {'vehicle':v, 'turrets': {}}
        for t in c.turret_set.all():
            results.append(t)
                #as_dict['players'][p.id]['vehicles'][v.id]['turrets'][t.id] = {'turret':t}

    data = serializers.serialize("json", results, indent=4)
    format_param = request.GET.get('format', 'json')            
    if format_param == 'json':        
        return HttpResponse(data, mimetype='text/json')
    else:   
        return HttpResponse(log_message + "\n<hr>\n\n" +  data, mimetype='text/plain')

def make_game(setup_conf=None):
    if setup_conf:
        pass
    else:
        g = Game(name='random game')
        g.save()
        crew_names = ['player one', 'ai']
        for p in [Crew(name=x, game=g) for x in crew_names]:
            p.save()

            v = Vehicle(crew=p, pos_x = 20.0, pos_y = 20.0)
            v.save()
            t = Turret(crew=p, vehicle=v)
            t.save()
            

def process_input(request, game_id, crew_id):
    orders=request.REQUEST.get('orders', 'No Orders!')
    limits = {'t':[], 'v':[]}
    limits_raw=request.REQUEST.get('limit', None)
    if limits_raw:
        limit_pairs = limits_raw.split(",")
        for l in limit_pairs:
            thing_type, thing_id = l[0],int(l[1:])
            limits[thing_type].append(thing_id)
            
    game = Game.objects.get(pk=game_id)
    thing = Crew.objects.get(pk=crew_id)

    action, req_params = orders.split(':', 1)    
    if action == 'moveto':
        x,y = [float(p) for p in req_params.split(',')]
        for v in thing.vehicle_set.all():
            if v.id in limits['v']:
                continue
            v.pos_x, v.pos_y = x,y
            v.save()
    elif action == 'fireat':
        x,y = [float(p) for p in req_params.split(',')]
        for t in thing.turret_set.all():
            if t.id in limits['t']:
                continue
            t.ammo -= 1
            t.save()
    elif action == 'rotate':
        r = float(req_params)
        for t in thing.turret_set.all():
            if t.id in limits['t']:
                continue
            t.rotation = r
            t.save()
        for v in thing.vehicle_set.all():
            if v.id in limits['v']:
                continue
            v.rotation = r
            v.save()



            
    
    return game_json(request, game_id, crew_id, log_message="Processing orders: '%s' + limits: %s" % (str(orders), str(limits)))
                     
