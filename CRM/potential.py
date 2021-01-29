from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")

#create Potential and assign it to the users
@app.route('/api/PBXMLPotential/AddPBXMLPotential', methods=['POST']) 
def AddPBXMLPotential():
    print(request.is_json)
    content = request.get_json()
    print(content)

    Cccd = request.args['Cccd']
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLPotential as val
        merge(Potential: potential
        {
        CCCD : {Cccd},
        PotentialNo: val.PotentialNo,
        PotentialOwner : val.PotentialOwner,
        Amount : val.Amount,
        PotentialName : val.PotentialName,
        ClosingDate: val.ClosingDate,
        AccountName :val.AccountName,
        Stage : val.Stage,
        Type : val.Type,
        Probability : val.Probability,
        NextStep : val.NextStep,
        ExpectedRevenue : val.ExpectedRevenue,
        LeadSource : val.LeadSource,
        CampaignSource : val.CampaignSource,
        ContactName : val.ContactName,
        CreatedBy: val.CreatedBy,
        CreatedDate : val.CreatedDate,
        LastUpdatedBy : val.LastUpdatedBy,
        LastUpdatedDate: val.LastUpdatedDate
        })

		
    """
    add_to_potential = """
    match(pp:Potential),(p:potential)
    where pp.CCCD={Cccd}
    create(pp)-[:has]->(p)
    """
    graph.run(query,jsonobj=content,Cccd = Cccd)
    graph.run(add_to_potential,jsonobj=content,Cccd = Cccd)
    return "Potential Created successfully"


#Edit Potential details
@app.route('/api/PBXMLPotential/EditPBXMLPotential', methods=['POST'])
def EditPBXMLPotential():

    PotentialNo=request.args['PotentialNo']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLPotential as val
    with val
    match(Potential:potential)
    where Potential.PotentialNo={PotentialNo} and Potential.CCCD={Cccd}
    SET
    Potential.CCCD = val.CCCD,
    Potential.PotentialNo= val.PotentialNo,
    Potential.PotentialOwner = val.PotentialOwner,
    Potential.Amount = val.Amount,
    Potential.PotentialName = val.PotentialName,
    Potential.ClosingDate= val.ClosingDate,
    Potential.AccountName =val.AccountName,
    Potential.Stage = val.Stage,
    Potential.Type = val.Type,
    Potential.Probability = val.Probability,
    Potential.NextStep = val.NextStep,
    Potential.ExpectedRevenue = val.ExpectedRevenue,
    Potential.LeadSource = val.LeadSource,
    Potential.CampaignSource = val.CampaignSource,
    Potential.ContactName = val.ContactName,
    Potential.CreatedBy= val.CreatedBy,
    Potential.CreatedDate = val.CreatedDate,
    Potential.LastUpdatedBy = val.LastUpdatedBy,
    Potential.LastUpdatedDate= val.LastUpdatedDate
    """
    graph.run(query,jsonobj=content,PotentialNo=PotentialNo,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
	

#Delete Potential details and relationship 
@app.route('/api/PBXMLPotential/DeletePBXMLPotential', methods=['GET']) 
def DeletePBXMLPotential():
    PotentialNo=request.args['PotentialNo']
    Cccd=request.args['Cccd']

    query=""" 
    match(Potential:potential)  
    where Potential.PotentialNo={PotentialNo} and Potential.CCCD={Cccd}
    detach delete Potential
    """
    graph.run(query,PotentialNo=PotentialNo,Cccd=Cccd)
    return "Potential deleted Successfully"
	

#Get Potential details
@app.route('/api/PBXMLPotential/GetPBXMLPotential', methods=['GET'])
def GetPBXMLPotential():
    PotentialNo=request.args['PotentialNo']
    Cccd=request.args['Cccd']
    
    query = """
         match(Potential:potential)
         where Potential.PotentialNo={PotentialNo} and Potential.CCCD={Cccd}
         return Potential
        """
    result = []
    for res in graph.run(query,PotentialNo=PotentialNo,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 	
	
#Getall Potential details
@app.route('/api/PBXMLPotential/GetAllPBXMLPotential', methods=['GET'])
def GetAllPBXMLPotential():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Potential:potential)
         where Potential.CCCD={Cccd}
         return Potential
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result)


app.run(host='0.0.0.0', port=5000) 
