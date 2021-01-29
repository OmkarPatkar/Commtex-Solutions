from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")
  
#create lead and assign it to the users
@app.route('/api/PBXMLLead/AddPBXMLLead', methods=['POST']) 
def AddPBXMLLead():
    print(request.is_json)
    content = request.get_json()
    print(content)

    cccd = request.args['cccd']
    
    create_lead=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLLead as val
        merge(Lead: lead
        {
        CCCD : {CCCD},
        LeadNo: val.LeadNo,
        LeadOwner : val.LeadOwner,
        Company : val.Company,
        FirstName: val.FirstName,
        LastName :val.LastName,
        Title : val.Title,
        Email : val.Email,
        Phone : val.Phone,
        Fax: val.Fax,
        Mobile : val.Mobile,
        Website : val.Website,
        LeadSource: val.LeadSource,
        LeadStatus :val.LeadStatus,
        Industry : val.Industry,
        NoOfEmployees : val.NoOfEmployees,
        AnnualRevenue : val.AnnualRevenue,
        Rating: val.Rating,
        SkypeID : val.SkypeID,
        Street : val.Street,
        City: val.City,
        State :val.State,
        ZipCodeSpecified : val.ZipCodeSpecified,
        Country : val.Country,
        Description: val.Description,
        CreatedBy : val.CreatedBy,
        CreatedDate : val.CreatedDate,
        LastUpdatedBy : val.LastUpdatedBy,
        LastUpdatedDate : val.LastUpdatedDate
        })

    """
    add_to_lead = """
    match(ll:Lead),(l:lead)
    where ll.CCCD={CCCD}
    create(ll)-[:has]->(l)
    """
    graph.run(create_lead,jsonobj=content,CCCD=cccd)
    graph.run(add_to_lead,jsonobj=content,CCCD=cccd)
    
    return "Lead Created successfully"


#Edit Lead details
@app.route('/api/PBXMLLead/EditPBXMLLead', methods=['POST'])
def EditPBXMLLead():

    Title=request.args['Title']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLLead as vl
    with vl
    match(Lead:lead)
    where Lead.Title={Title} and Lead.CCCD={Cccd}
    SET
    Lead.LeadNo= vl.LeadNo,
    Lead.LeadOwner = vl.LeadOwner,
    Lead.Company = vl.Company,
    Lead.FirstName= vl.FirstName,
    Lead.LastName =vl.LastName,
    Lead.Email = vl.Email,
    Lead.Phone = vl.Phone,
    Lead.Fax= vl.Fax,
    Lead.Mobile = vl.Mobile,
    Lead.Website = vl.Website,
    Lead.LeadSource= vl.LeadSource,
    Lead.LeadStatus =vl.LeadStatus,
    Lead.Industry = vl.Industry,
    Lead.NoOfEmployees = vl.NoOfEmployees,
    Lead.AnnualRevenue = vl.AnnualRevenue,
    Lead.Rating= vl.Rating,
    Lead.SkypeID = vl.SkypeID,
    Lead.Street = vl.Street,
    Lead.City= vl.City,
    Lead.State =vl.State,
    Lead.ZipCodeSpecified = vl.ZipCodeSpecified,
    Lead.Country = vl.Country,
    Lead.Description= vl.Description,
    Lead.CreatedBy = vl.CreatedBy,
    Lead.CreatedDate = vl.CreatedDate,
    Lead.LastUpdatedBy = vl.LastUpdatedBy,
    Lead.LastUpdatedDate = vl.LastUpdatedDate

    """
    graph.run(query,jsonobj=content,Title=Title,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
	

#Delete lead details and relationship 
@app.route('/api/PBXMLLead/DeletePBXMLLead', methods=['GET']) 
def DeletePBXMLLead():
    Title=request.args['Title']
    Cccd=request.args['Cccd']

    query=""" 
    match(Lead:lead)  
    where Lead.Title={Title} and Lead.CCCD={Cccd}
    detach delete Lead
    """
    graph.run(query,Title=Title,Cccd=Cccd)
    return "Lead deleted Successfully"
	

#Get lead details
@app.route('/api/PBXMLLead/GetPBXMLLead', methods=['GET'])
def GetPBXMLLead():
    Title=request.args['Title']
    Cccd=request.args['Cccd']
    
    query = """
         match(Lead:lead)
         where Lead.Title={Title} and Lead.CCCD={Cccd}
         return Lead
        """
    result = []
    for res in graph.run(query,Title=Title,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 
	
#Getall lead details
@app.route('/api/PBXMLLead/GetAllPBXMLLead', methods=['GET'])
def GetAllPBXMLLead():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Lead:lead)
         where Lead.CCCD={Cccd}
         return Lead
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 


app.run(host='0.0.0.0', port=5000)