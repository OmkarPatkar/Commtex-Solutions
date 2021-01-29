from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")

#create Opportunity and assign it to the users
@app.route('/api/PBXMLOpportunity/AddPBXMLOpportunity', methods=['POST']) 
def AddPBXMLOpportunity():
    print(request.is_json)
    content = request.get_json()
    print(content)
    Cccd = request.args['Cccd']
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLOpportunity as val
        merge(Opportunity: opportunity
        {
        CCCD : {Cccd},
        Status: val.Status,
        ApprovedByASM : val.ApprovedByASM,
        ApprovedByRSM : val.ApprovedByRSM,
        CreatedDate : val.CreatedDate,
        LastUpdatedBy : val.LastUpdatedBy,
        LastUpdatedDate : val.LastUpdatedDate,
        CreatedBy : val.CreatedBy,
        OppNo : val.OppNo,
        OppName :val.OppName,
        Currency : val.Currency,
        AccountName : val.AccountName,
        Amount : val.Amount,
        Type : val.Type,
        ExpCloseDate : val.ExpCloseDate,
        LeadSource : val.LeadSource,
        NextStep : val.NextStep,
        Campaign : val.Campaign,
        SalesStage : val.SalesStage,
        AssignedTo : val.AssignedTo,
        Probability : val.Probability,
        Description : val.Description
        })


    """
    add_to_opportunity = """
    match(oo:Opportunity),(o:opportunity)
    where oo.CCCD = {Cccd}
    create(oo)-[:has]->(o)
    """

    graph.run(query,jsonobj=content,Cccd=Cccd)
    graph.run(add_to_opportunity,jsonobj=content,Cccd=Cccd)
    return "Opportunity Created successfully"

#Edit Opportunity details
@app.route('/api/PBXMLOpportunity/EditPBXMLOpportunity', methods=['POST'])
def EditPBXMLOpportunity():

    OppNo=request.args['OppNo']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLOpportunity as val
    with val
    match(Opportunity:opportunity)
    where Opportunity.OppNo={OppNo} and Opportunity.CCCD={Cccd}
    SET
    Opportunity.CCCD = val.Cccd,
    Opportunity.Status= val.Status,
    Opportunity.ApprovedByASM = val.ApprovedByASM,
    Opportunity.ApprovedByRSM = val.ApprovedByRSM,
    Opportunity.CreatedDate = val.CreatedDate,
    Opportunity.LastUpdatedBy = val.LastUpdatedBy,
    Opportunity.LastUpdatedDate = val.LastUpdatedDate,
    Opportunity.CreatedBy = val.CreatedBy,
    Opportunity.OppNo = val.OppNo,
    Opportunity.OppName =val.OppName,
    Opportunity.Currency = val.Currency,
    Opportunity.AccountName = val.AccountName,
    Opportunity.Amount = val.Amount,
    Opportunity.Type = val.Type,
    Opportunity.ExpCloseDate = val.ExpCloseDate,
    Opportunity.LeadSource = val.LeadSource,
    Opportunity.NextStep = val.NextStep,
    Opportunity.Campaign = val.Campaign,
    Opportunity.SalesStage = val.SalesStage,
    Opportunity.AssignedTo = val.AssignedTo,
    Opportunity.Probability = val.Probability,
    Opportunity.Description = val.Description
    """
    graph.run(query,jsonobj=content,OppNo=OppNo,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
		

#Delete Opportunity details and relationship 
@app.route('/api/PBXMLOpportunity/DeletePBXMLOpportunity', methods=['GET']) 
def DeletePBXMLOpportunity():
    OppNo=request.args['OppNo']
    Cccd=request.args['Cccd']

    query=""" 
    match(Opportunity:opportunity)  
    where Opportunity.OppNo={OppNo} and Opportunity.CCCD={Cccd}
    detach delete Opportunity
    """
    graph.run(query,OppNo=OppNo,Cccd=Cccd)
    return "Opportunity deleted Successfully"
	

#Get Opportunity details
@app.route('/api/PBXMLOpportunity/GetPBXMLOpportunity', methods=['GET'])
def GetPBXMLOpportunity():
    OppNo=request.args['OppNo']
    Cccd=request.args['Cccd']
    
    query = """
         match(Opportunity:opportunity)
         where Opportunity.OppNo={OppNo} and Opportunity.CCCD={Cccd}
         return Opportunity
        """
    result = []
    for res in graph.run(query,OppNo=OppNo,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 
	
#Getall Opportunity details
@app.route('/api/PBXMLOpportunity/GetAllPBXMLOpportunity', methods=['GET'])
def GetAllPBXMLOpportunity():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Opportunity:opportunity)
         where Opportunity.CCCD={Cccd}
         return Opportunity
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 


app.run(host='0.0.0.0', port=5000)