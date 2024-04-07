from flask import Flask, render_template, request,jsonify
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:11003/db/data")

@app.route('/api/PBXMLCostCategories/AddPBXMLCostCategory', methods=['POST']) 
def AddPBXMLCostCategory():
    print(request.is_json)
    content = request.get_json()
    print(content)
    Cccd= request.args['Cccd']
    
    query=""" 
    WITH {jsonobj} as v

        create (c:CostCat{name:"CostCats"})
        with c, v.PBXMLCostCategories as vl
        unwind vl as val
        unwind val.PBXMLCostCategory as cc
         with cc, val,c
        foreach (costcat in cc|
        merge
        (costcate: Costcategories
        {
        Cccd: {Cccd},
        NAME : costcat.NAME,
        RESERVEDNAME:costcat.RESERVEDNAME,
        GUID: costcat.GUID,
        ISUPDATINGTARGETID : costcat.ISUPDATINGTARGETID,
        ASORIGINAL : costcat.ASORIGINAL,
        AFFECTSSTOCK: costcat.AFFECTSSTOCK,
        ALLOCATEREVENUE :costcat.ALLOCATEREVENUE, 
        ALLOCATENONREVENUE : costcat.ALLOCATENONREVENUE,
        ALTERID : costcat.ALTERID
        }
        )<- [:contains]-(c)
        )
    """
    graph.run(query,jsonobj=content,Cccd=Cccd)
    return "Cost Category created successfully"

#Edit project details
@app.route('/api/PBXMLCostCategories/EditPBXMLCostCategory', methods=['POST'])
def EditPBXMLCostCategory():
    Cccd=request.args['Cccd']
    NAME = request.args['NAME']
    content = request.get_json()
    print(content)
    print(id)
    query=""" 
    WITH {jsonobj} as value
    unwind value.PBXMLCostCategories as val
    unwind val.PBXMLCostCategory as cc
    with cc, val, value
    match(costcate:Costcategories) 
    where costcate.Cccd={Cccd} and costcate.NAME={NAME}
    SET
        costcate.NAME = cc.NAME,
        costcate.RESERVEDNAME=cc.RESERVEDNAME,
        costcate.GUID= cc.GUID,
        costcate.ISUPDATINGTARGETID = cc.ISUPDATINGTARGETID,
        costcate.ASORIGINAL = cc.ASORIGINAL,
        costcate.AFFECTSSTOCK= cc.AFFECTSSTOCK,
        costcate.ALLOCATEREVENUE =cc.ALLOCATEREVENUE, 
        costcate.ALLOCATENONREVENUE = cc.ALLOCATENONREVENUE,
        costcate.ALTERID = cc.ALTERID 
    """
    graph.run(query,jsonobj=content,Cccd=Cccd,NAME=NAME)
    return "successful"

#Delete Project details and relationship 
@app.route('/api/PBXMLCostCategories/DeletePBXMLCostCategory', methods=['GET']) 
def DeletePBXMLCostCategory():
    NAME=request.args['NAME']
    cccd=request.args['cccd']
    #UserId=request.args['UserId']
    query=""" 
    match(costcate:Costcategories)  
    where costcate.NAME={NAME} and costcate.cccd={cccd}
    detach delete costcate
    """
    graph.run(query,NAME=NAME,cccd=cccd)
    return "costcatgories deleted Successfully"

#Get project details
@app.route('/api/PBXMLCostCategories/GetPBXMLCostCategories', methods=['GET'])
def GetPBXMLCostCategories():
    ID=request.args['NAME']
    cccd=request.args['cccd']
    
    query = '''
         match(costcate:Costcategories)  
         where costcate.NAME={ID} and costcate.cccd={cccd}
         RETURN costcate
        '''
    result = []
    for res in graph.run(query, ID=ID,cccd=cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#Get all project details
@app.route('/api/PBXMLCostCategories/GetAllPBXMLCostCategories', methods=['GET'])
def GetAllPBXMLCostCategories():
    ID=request.args['cccd']
    query = '''
         match(costcate:Costcategories) where costcate.cccd={ID}
         RETURN costcate
        '''
    result = []
    for res in graph.run(query,ID=ID):
        result.append(str(res[0]))

    return jsonify(result) 

@app.route('/api/PBXMLCostCategories/GetNamePBXMLCostCategory', methods=['GET'])
def GetNamePBXMLCostCategory():
    cccd=request.args['cccd']
    
    query = '''
         match(costcate:Costcategories) where costcate.cccd={cccd}
         RETURN costcate.NAME
        '''
    result = []
    for res in graph.run(query,cccd=cccd):
        result.append(str(res[0]))
    
    return jsonify(result) 

app.run(host='0.0.0.0', port=5000)