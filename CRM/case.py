from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")

#create Case and assign it to the users
@app.route('/api/PBXMLCase/AddPBXMLCase', methods=['POST']) 
def AddPBXMLCase():
    print(request.is_json)
    content = request.get_json()
    print(content)

    Cccd = request.args['Cccd']
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLCase as val
        merge(Case: case
        {
        CCCD : {Cccd},
        CaseNo: val.CaseNo,
        ProductNameSpecified : val.ProductNameSpecified,
        CaseOwnerSpecified : val.CaseOwnerSpecified,
        TypeSpecified : val.TypeSpecified,
        StatusSpecified : val.StatusSpecified,
        CaseOriginSpecified : val.CaseOriginSpecified,
        RelatedTo : val.RelatedTo,
        PrioritySpecified : val.PrioritySpecified,
        CaseReasonSpecified :val.CaseReasonSpecified,
        AccountNameSpecified : val.AccountNameSpecified,
        Subject : val.Subject,
        PotentialName : val.PotentialName,
        ReportedBy : val.ReportedBy,
        Phone : val.Phone,
        Email : val.Email,
        Description : val.Description,
        InternalComments : val.InternalComments,
        CreatedBySpecified : val.CreatedBySpecified,
        CreatedDateSpecified : val.CreatedDateSpecified,
        LastUpdatedBySpecified : val.LastUpdatedBySpecified,
        LastUpdatedDateSpecified : val.LastUpdatedDateSpecified
        })

		
    """
    add_to_case = """
    match(Cas:Case),(cas:case)
    where Cas.CCCD = {Cccd}
    create(Cas)-[:has]->(cas)
    """
    graph.run(query,jsonobj=content,Cccd=Cccd)
    graph.run(add_to_case,jsonobj=content,Cccd=Cccd)
    return "Case Created successfully"

#Edit Case details
@app.route('/api/PBXMLCase/EditPBXMLCase', methods=['POST'])
def EditPBXMLCase():

    CaseNo=request.args['CaseNo']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLCase as val
    with val
    match(Case:case)
    where Case.CaseNo={CaseNo} and Case.CCCD={Cccd}
    SET
    Case.CCCD = val.CCCD,
    Case.CaseNo= val.CaseNo,
    Case.ProductNameSpecified = val.ProductNameSpecified,
    Case.CaseOwnerSpecified = val.CaseOwnerSpecified,
    Case.TypeSpecified = val.TypeSpecified,
    Case.StatusSpecified = val.StatusSpecified,
    Case.CaseOriginSpecified = val.CaseOriginSpecified,
    Case.RelatedTo = val.RelatedTo,
    Case.PrioritySpecified = val.PrioritySpecified,
    Case.CaseReasonSpecified =val.CaseReasonSpecified,
    Case.AccountNameSpecified = val.AccountNameSpecified,
    Case.Subject = val.Subject,
    Case.PotentialName = val.PotentialName,
    Case.ReportedBy = val.ReportedBy,
    Case.Phone = val.Phone,
    Case.Email = val.Email,
    Case.Description = val.Description,
    Case.InternalComments = val.InternalComments,
    Case.CreatedBySpecified = val.CreatedBySpecified,
    Case.CreatedDateSpecified = val.CreatedDateSpecified,
    Case.LastUpdatedBySpecified = val.LastUpdatedBySpecified,
    Case.LastUpdatedDateSpecified = val.LastUpdatedDateSpecified
    
    """
    graph.run(query,jsonobj=content,CaseNo=CaseNo,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
		

#Delete Case details and relationship 
@app.route('/api/PBXMLCase/DeletePBXMLCase', methods=['GET']) 
def DeletePBXMLCase():
    CaseNo=request.args['CaseNo']
    Cccd=request.args['Cccd']

    query=""" 
    match(Case:case)  
    where Case.CaseNo={CaseNo} and Opportunity.CCCD={Cccd}
    detach delete Case
    """
    graph.run(query,CaseNo=CaseNo,Cccd=Cccd)
    return "Case deleted Successfully"
	

#Get Case details
@app.route('/api/PBXMLCase/GetPBXMLCase', methods=['GET'])
def GetPBXMLCase():
    CaseNo=request.args['CaseNo']
    Cccd=request.args['Cccd']
    
    query = """
         match(Case:case)
         where Case.CaseNo={CaseNo} and Case.CCCD={Cccd}
         return Case
        """
    result = []
    for res in graph.run(query,CaseNo=CaseNo,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 	
	
#Getall Case details
@app.route('/api/PBXMLCase/GetAllPBXMLCase', methods=['GET'])
def GetAllPBXMLCase():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Case:case)
         where Case.CCCD={Cccd}
         return Case
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 


app.run(host='0.0.0.0', port=5000)