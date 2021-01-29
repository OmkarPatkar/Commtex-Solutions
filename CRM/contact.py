from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")
  

#create contact and assign it to the users
@app.route('/api/PBXMLContacts/AddPBXMLContacts', methods=['POST']) 
def AddPBXMLContacts():
    print(request.is_json)
    content = request.get_json()
    print(content)
    cccd = request.args['cccd']
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLContacts as val
		merge(Contact: contact
		{
		CCCD : {CCCD},
		ContactNo: val.ContactNo,
		ContactOwner : val.ContactOwner,
		Salutation : val.Salutation,
		LeadSource : val.LeadSource,
		FirstName: val.FirstName,
		LastName :val.LastName,
		AccountName : val.AccountName,
		VendorName : val.VendorName,
		Email : val.Email,
		Title : val.Title,
		Phone : val.Phone,
		Department : val.Department,
		OtherPhone : val.OtherPhone,
		HomePhone : val.HomePhone,
		Fax: val.Fax,
		Mobile : val.Mobile,
		DOB : val.DOB,
		Assistant: val.Assistant,
		ReportsTo :val.ReportsTo,
		AssPhone : val.AssPhone,
		EmailOptOut : val.EmailOptOut,
		SkypeID : val.SkypeID,
		SecondaryEmail: val.SecondaryEmail,
		MailingZip : val.MailingZip,
		MailingStrt : val.MailingStrt,
		OtherStrt: val.OtherStrt,
		MailingCity :val.MailingCity,
		OtherCity : val.OtherCity,
		MailingState : val.MailingState,
		OtherState: val.OtherState,
		OtherZip : val.OtherZip,
		MailingCountry : val.MailingCountry,
		OtherCountry : val.OtherCountry,
		Description : val.Description,
		CreatedBy : val.CreatedBy,
		LastUpdatedBy : val.LastUpdatedBy,
		UID : val.UID
		})
		
    """
    add_to_contact = """
    match(cc:Contact),(c:contact)
    where cc.CCCD={CCCD}
    create(cc)-[:has]->(c)
    """
    graph.run(query,jsonobj=content,CCCD=cccd)
    graph.run(add_to_contact,jsonobj=content,CCCD=cccd)
    return "Contact Created successfully"
	

#Edit Contacts details
@app.route('/api/PBXMLContacts/EditPBXMLContacts', methods=['POST'])
def EditPBXMLContacts():

    Title=request.args['Title']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLContacts as val
    with val
    match(Contact:contact)
    where Contact.Title={Title} and Contact.CCCD={Cccd}
    SET
    Contact.CCCD = val.Cccd,
	Contact.ContactNo= val.ContactNo,
    Contact.ContactOwner = val.ContactOwner,
    Contact.Salutation = val.Salutation,
    Contact.LeadSource = val.LeadSource,
    Contact.FirstName= val.FirstName,
    Contact.LastName =val.LastName,
    Contact.AccountName = val.AccountName,
    Contact.VendorName = val.VendorName,
    Contact.Email = val.Email,
    Contact.Title = val.Title,
    Contact.Phone = val.Phone,
    Contact.Department = val.Department,
    Contact.OtherPhone = val.OtherPhone,
    Contact.HomePhone = val.HomePhone,
    Contact.Fax= val.Fax,
    Contact.Mobile = val.Mobile,
    Contact.DOB = val.DOB,
    Contact.Assistant= val.Assistant,
    Contact.ReportsTo =val.ReportsTo,
    Contact.AssPhone = val.AssPhone,
    Contact.EmailOptOut = val.EmailOptOut,
    Contact.SkypeID = val.SkypeID,
    Contact.SecondaryEmail= val.SecondaryEmail,
    Contact.MailingZip = val.MailingZip,
    Contact.MailingStrt = val.MailingStrt,
    Contact.OtherStrt= val.OtherStrt,
    Contact.MailingCity =val.MailingCity,
    Contact.OtherCity = val.OtherCity,
    Contact.MailingState = val.MailingState,
    Contact.OtherState= val.OtherState,
    Contact.OtherZip = val.OtherZip,
    Contact.MailingCountry = val.MailingCountry,
    Contact.OtherCountry = val.OtherCountry,
    Contact.Description = val.Description,
    Contact.CreatedBy = val.CreatedBy,
    Contact.LastUpdatedBy = val.LastUpdatedBy,
    Contact.UID = val.UID
    """
    graph.run(query,jsonobj=content,Title=Title,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
	


#Delete contact details and relationship 
@app.route('/api/PBXMLContacts/DeletePBXMLContacts', methods=['GET']) 
def DeletePBXMLContacts():
    Title=request.args['Title']
    Cccd=request.args['Cccd']

    query=""" 
    match(Contact:contact)  
    where Contact.Title={Title} and Contact.CCCD={Cccd}
    detach delete Contact
    """
    graph.run(query,Title=Title,Cccd=Cccd)
    return "contact deleted Successfully"
	

#Get contact details
@app.route('/api/PBXMLContacts/GetPBXMLContacts', methods=['GET'])
def GetPBXMLContacts():
    Title=request.args['Title']
    Cccd=request.args['Cccd']
    
    query = """
         match(Contact:contact)
         where Contact.Title={Title} and Contact.CCCD={Cccd}
         return Contact
        """
    result = []
    for res in graph.run(query,Title=Title,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 	
	
#Getall contact details
@app.route('/api/PBXMLContacts/GetAllPBXMLContacts', methods=['GET'])
def GetAllPBXMLContacts():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Contact:contact)
         where Contact.CCCD={Cccd}
         return Contact
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 


app.run(host='0.0.0.0', port=5000) 