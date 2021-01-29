from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")

@app.route('/addpart', methods=['POST'])
def addpart():
    print(request.is_json)
    content = request.get_json()
    print(content)
    # call apoc.load.json("C://inetpub//vhosts//commtexsolutions.com//httpdocs//Ideeza//API//json//part.json") yield value as part
    query=""" 
     
        WITH {jsonobj} as part

        unwind part.form as pt
        unwind pt.dimensions as dt
        unwind pt.silkscreen as sl
        unwind part.engine as engine
        unwind engine.transform as T
        unwind part.data as dat

        create(f:form{name2d:pt.name2d,package:pt.package,legs:pt.legs,name:pt.name,PinStartAt:pt.PinStartAt,hasValue:pt.hasValue,isClockwise:pt.isClockwise,nameFontSize:pt.nameFontSize,value:pt.value})
        create(d:Dimension{t_min_bandwidth:dt.t_min_bandwidth,t_max_bandwidth:dt.t_max_bandwidth,max_body_length_l:dt.max_body_length_l,min_body_length_l:dt.min_body_length_l,package_type:dt.package_type,tw_min_bandwidth:dt.tw_min_bandwidth,tw_max_bandwidth:dt.tw_max_bandwidth,in_location:dt.in_location,aximum_height:dt.aximum_height})

        create(s:silkscreen{r2:sl.r2,LineWidth:sl.LineWidth,isCalculated:sl.isCalculated,r1:sl.r1})
        CREATE (f)-[a:Has]->(d)
        CREATE (f)-[b:Has]->(s)

        create (e:engine{name:engine.name,name2d:engine.name2d,schematic:engine.schematic,url:engine.url,design:engine.design})
        create(l:transform{pivot:T.pivot,position:T.posposition,best_p:T.best_p,best_sc:T.best_sc,rotation:T.rotation})
        create(e)-[r:contain]->(l)

        create(da:data{Fsize:dat.Fsize,sizeL1:dat.sizeL1,size:dat.size})

        create(p:part{name:"part"})
        CREATE (p)-[:Has]->(f)
        CREATE (p)-[:Has]->(e)
        CREATE (p)-[:Has]->(da)

      
     """
    graph.run(query,jsonobj=content)
    return "Part added successfully"

@app.route('/getpart', methods=['GET'])
def getpart():
    name=request.args['name']

    query = '''
      match(p:part)-[r:Has]->(f:form),(f:form)-[a:Has]->(d:Dimension),(f:form)-[b:Has]->(sl:silkscreen),(e:engine)-[c:contain]->(t:transform),(p:part)-[con:Has]->(dt:data)
with dt,p,f,e,REDUCE(s={},x IN COLLECT(d)| apoc.map.merge(s,x)) as dim,REDUCE(t={},u IN COLLECT(sl)| apoc.map.merge(t,u)) as silkscreen,REDUCE(t={},u IN COLLECT(t)| apoc.map.merge(t,u)) as trans
 
return apoc.map.merge(p,{engine:(apoc.map.merge(e,{transform:trans})),form:(apoc.map.merge(f,{dimensions:dim,silkscreen:silkscreen})),data:(apoc.map.merge(dt,{}))})

        '''
    # result=jsonify(graph.run(query, ID=ID).data())
    # print (result)
    result = []
    for res in graph.run(query,name=name):
        result.append(str(res[0]))

    result1=jsonify(result)

    return (result1)



app.run(host='0.0.0.0', port=5000)
