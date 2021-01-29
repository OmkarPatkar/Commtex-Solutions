from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")
  

#create Campaign and assign it to the users
@app.route('/api/PBXMLCampaign/AddPBXMLCampaign', methods=['POST']) 
def AddPBXMLCampaign():
    print(request.is_json)
    content = request.get_json()
    print(content)

    Cccd = request.args['Cccd']
    
    query=""" 
        WITH {jsonobj} as v
      
        unwind v.PBXMLCampaign as val
        merge(Campaign: campaign
        {
        CCCD : {Cccd},
        ProductName: val.ProductName,
        SkuName : val.SkuName,
        Location : val.Location,
        Industry : val.Industry,
        CampaignNo : val.CampaignNo,
        CampaignOwner : val.CampaignOwner,
        Type : val.Type,
        CampaignName : val.CampaignName,
        Status :val.Status,
        StartDate : val.StartDate,
        EndDate : val.EndDate,
        ExpectedRevenue : val.ExpectedRevenue,
        BudgetCost : val.BudgetCost,
        ActualCost : val.ActualCost,
        ExpectedResponse : val.ExpectedResponse,
        Description : val.Description,
        CreatedBy : val.CreatedBy,
        CreatedDate : val.CreatedDate,
        LastUpdatedBy : val.LastUpdatedBy,
        LastUpdatedDate : val.LastUpdatedDate
        })
    """

    add_to_campaign = """
    match(Camp:Campaign),(camp:campaign)
    where Camp.CCCD = {Cccd}
    create(Camp)-[:has]->(camp)
    """
    graph.run(query,jsonobj=content,Cccd=Cccd)
    graph.run(add_to_campaign,jsonobj=content,Cccd=Cccd)
    return "Campaign Created successfully"

#Edit Campaign details
@app.route('/api/PBXMLCampaign/EditPBXMLCampaign', methods=['POST'])
def EditPBXMLCampaign():

    CampaignName=request.args['CampaignName']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLCampaign as val
    with val
    match(Campaign:campaign)
    where Campaign.CampaignName={CampaignName} and Campaign.CCCD={Cccd}
    SET
    Campaign.CCCD = val.Cccd,
    Campaign.ProductName= val.ProductName,
    Campaign.SkuName = val.SkuName,
    Campaign.Location = val.Location,
    Campaign.Industry = val.Industry,
    Campaign.CampaignNo = val.CampaignNo,
    Campaign.CampaignOwner = val.CampaignOwner,
    Campaign.Type = val.Type,
    Campaign.CampaignName = val.CampaignName,
    Campaign.Status =val.Status,
    Campaign.StartDate = val.StartDate,
    Campaign.EndDate = val.EndDate,
    Campaign.ExpectedRevenue = val.ExpectedRevenue,
    Campaign.BudgetCost = val.BudgetCost,
    Campaign.ActualCost = val.ActualCost,
    Campaign.ExpectedResponse = val.ExpectedResponse,
    Campaign.Description = val.Description,
    Campaign.CreatedBy = val.CreatedBy,
    Campaign.CreatedDate = val.CreatedDate,
    Campaign.LastUpdatedBy = val.LastUpdatedBy,
    Campaign.LastUpdatedDate = val.LastUpdatedDate
    """
    graph.run(query,jsonobj=content,CampaignName=CampaignName,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
		

#Delete Campaign details and relationship 
@app.route('/api/PBXMLCampaign/DeletePBXMLCampaign', methods=['GET']) 
def DeletePBXMLCampaign():
    CampaignName=request.args['CampaignName']
    Cccd=request.args['Cccd']

    query=""" 
    match(Campaign:campaign)  
    where Campaign.CampaignName={CampaignName} and Campaign.CCCD={Cccd}
    detach delete Campaign
    """
    graph.run(query,CampaignName=CampaignName,Cccd=Cccd)
    return "Campaign deleted Successfully"
	

#Get Campaign details
@app.route('/api/PBXMLCampaign/GetPBXMLCampaign', methods=['GET'])
def GetPBXMLCampaign():
    CampaignName=request.args['CampaignName']
    Cccd=request.args['Cccd']
    
    query = """
         match(Campaign:campaign)
         where Campaign.CampaignName={CampaignName} and Campaign.CCCD={Cccd}
         return Campaign
        """
    result = []
    for res in graph.run(query,CampaignName=CampaignName,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 
	
#Getall Campaign details
@app.route('/api/PBXMLCampaign/GetAllPBXMLCampaign', methods=['GET'])
def GetAllPBXMLCampaign():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Campaign:campaign)
         where Campaign.CCCD={Cccd}
         return Campaign
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result)

app.run(host='0.0.0.0', port=5000) 
