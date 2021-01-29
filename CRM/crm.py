from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")

#---------------------------------------------------------lead start--------------------------------------------------------------------

#create lead and assign it to the users
@app.route('/api/PBXMLLead/AddPBXMLLead', methods=['POST']) 
def AddPBXMLLead():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLLead as val
        merge(Lead: lead
        {
        Cccd : val.Cccd,
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
    graph.run(query,jsonobj=content)
    
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
    where Lead.Title={Title} and Lead.Cccd={Cccd}
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
    where Lead.Title={Title} and Lead.Cccd={Cccd}
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
         where Lead.Title={Title} and Lead.Cccd={Cccd}
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
         where Lead.Cccd={Cccd}
         return Lead
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLLead/GetNamePBXMLLead', methods=['GET'])
def GetNamePBXMLLead():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Lead:lead) where Lead.cccd={cccd}
         RETURN Lead.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------lead end--------------------------------------------------------------------




#---------------------------------------------------------contact start--------------------------------------------------------------------

#create contact and assign it to the users
@app.route('/api/PBXMLContacts/AddPBXMLContacts', methods=['POST']) 
def AddPBXMLContacts():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLContacts as val
		merge(Contact: contact
		{
		Cccd : val.Cccd,
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
    graph.run(query,jsonobj=content)
    return "contact Created successfully"
	

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
    where Contact.Title={Title} and Contact.Cccd={Cccd}
    SET
    Contact.Cccd = val.Cccd,
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
    where Contact.Title={Title} and Lead.Cccd={Cccd}
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
         where Contact.Title={Title} and Contact.Cccd={Cccd}
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
         where Contact.Cccd={Cccd}
         return Contact
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLContacts/GetNamePBXMLContacts', methods=['GET'])
def GetNamePBXMLContacts():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Contact:contact) where Contacts.cccd={cccd}
         RETURN Contacts.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------contact end--------------------------------------------------------------------


#---------------------------------------------------------Activities start--------------------------------------------------------------------

#create Activities and assign it to the users
@app.route('/api/PBXMLActivities/AddPBXMLActivities', methods=['POST']) 
def AddPBXMLActivities():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLActivities as val
        merge(Activities: activities
        {
        Cccd : val.Cccd,
        ActivityNo: val.ActivityNo,
        ContactLead : val.ContactLead,
        AccountOption : val.AccountOption,
        ActivityOwner : val.ActivityOwner,
        Subject: val.Subject,
        ActivityType :val.ActivityType,
        ContactName : val.ContactName,
        RelatedTo : val.RelatedTo,
        Description : val.Description,
        DueDate : val.DueDate,
        Status : val.Status,
        Priority : val.Priority,
        SendNoficatnEmail : val.SendNoficatnEmail,
        StartDateTime : val.StartDateTime,
        EndDateTime: val.EndDateTime,
        CallType : val.CallType,
        CallPurpose : val.CallPurpose,
        CallStartTime: val.CallStartTime,
        CallDurationInSec :val.CallDurationInSec,
        Billable : val.Billable,
        CallResult : val.CallResult,
        CreatedBy : val.CreatedBy,
        CreatedDate: val.CreatedDate,
        LastUpdatedBy : val.LastUpdatedBy,
        LastUpdatedDate : val.LastUpdatedDate
        })


    """
    graph.run(query,jsonobj=content)
    
    return "Activities Created successfully"


#Edit Activities details
@app.route('/api/PBXMLActivities/EditPBXMLActivities', methods=['POST'])
def EditPBXMLActivities():

    ActivityNo=request.args['ActivityNo']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLActivities as val
    with val
    match(Activities:activities)
    where Activities.ActivityNo={ActivityNo} and Activities.Cccd={Cccd}
    SET
    Activities.Cccd = val.Cccd,
    Activities.ActivityNo= val.ActivityNo,
    Activities.ContactLead = val.ContactLead,
    Activities.AccountOption = val.AccountOption,
    Activities.ActivityOwner = val.ActivityOwner,
    Activities.Subject= val.Subject,
    Activities.ActivityType =val.ActivityType,
    Activities.ContactName = val.ContactName,
    Activities.RelatedTo = val.RelatedTo,
    Activities.Description = val.Description,
    Activities.DueDate = val.DueDate,
    Activities.Status = val.Status,
    Activities.Priority = val.Priority,
    Activities.SendNoficatnEmail = val.SendNoficatnEmail,
    Activities.StartDateTime = val.StartDateTime,
    Activities.EndDateTime= val.EndDateTime,
    Activities.CallType = val.CallType,
    Activities.CallPurpose = val.CallPurpose,
    Activities.CallStartTime= val.CallStartTime,
    Activities.CallDurationInSec =val.CallDurationInSec,
    Activities.Billable = val.Billable,
    Activities.CallResult = val.CallResult,
    Activities.CreatedBy = val.CreatedBy,
    Activities.CreatedDate= val.CreatedDate,
    Activities.LastUpdatedBy = val.LastUpdatedBy,
    Activities.LastUpdatedDate = val.LastUpdatedDate
    """
    graph.run(query,jsonobj=content,ActivityNo=ActivityNo,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
	

#Delete Activities details and relationship 
@app.route('/api/PBXMLActivities/DeletePBXMLActivities', methods=['GET']) 
def DeletePBXMLActivities():
    ActivityNo=request.args['ActivityNo']
    Cccd=request.args['Cccd']

    query=""" 
    match(Activities:activities)  
    where Activities.ActivityNo={ActivityNo} and Activities.Cccd={Cccd}
    detach delete Activities
    """
    graph.run(query,ActivityNo=ActivityNo,Cccd=Cccd)
    return "Activities deleted Successfully"
	

#Get Activities details
@app.route('/api/PBXMLActivities/GetPBXMLActivities', methods=['GET'])
def GetPBXMLActivities():
    ActivityNo=request.args['ActivityNo']
    Cccd=request.args['Cccd']
    
    query = """
         match(Activities:activities)
         where Activities.ActivityNo={ActivityNo} and Activities.Cccd={Cccd}
         return Activities
        """
    result = []
    for res in graph.run(query,ActivityNo=ActivityNo,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 
	
#Getall Activities details
@app.route('/api/PBXMLActivities/GetAllPBXMLActivities', methods=['GET'])
def GetAllPBXMLActivities():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Activities:activities)
         where Activities.Cccd={Cccd}
         return Activities
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLActivities/GetNamePBXMLActivities', methods=['GET'])
def GetNamePBXMLActivities():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Activities:activities) where Activities.cccd={cccd}
         RETURN Activities.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------Activities end--------------------------------------------------------------------


#---------------------------------------------------------Potential start--------------------------------------------------------------------

#create Potential and assign it to the users
@app.route('/api/PBXMLPotential/AddPBXMLPotential', methods=['POST']) 
def AddPBXMLPotential():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLPotential as val
        merge(Potential: potential
        {
        Cccd : val.Cccd,
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
    graph.run(query,jsonobj=content)
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
    where Potential.PotentialNo={PotentialNo} and Potential.Cccd={Cccd}
    SET
    Potential.Cccd = val.Cccd,
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
    where Potential.PotentialNo={PotentialNo} and Activities.Cccd={Cccd}
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
         where Potential.PotentialNo={PotentialNo} and Potential.Cccd={Cccd}
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
         where Potential.Cccd={Cccd}
         return Potential
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLPotential/GetNamePBXMLPotential', methods=['GET'])
def GetNamePBXMLPotential():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Potential:potential) where Potential.cccd={cccd}
         RETURN Potential.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------Potential end--------------------------------------------------------------------


#---------------------------------------------------------Opportunity start--------------------------------------------------------------------

#create Opportunity and assign it to the users
@app.route('/api/PBXMLOpportunity/AddPBXMLOpportunity', methods=['POST']) 
def AddPBXMLOpportunity():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLOpportunity as val
        merge(Opportunity: opportunity
        {
        Cccd : val.Cccd,
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
    graph.run(query,jsonobj=content)
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
    where Opportunity.OppNo={OppNo} and Opportunity.Cccd={Cccd}
    SET
    Opportunity.Cccd = val.Cccd,
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
    where Opportunity.OppNo={OppNo} and Opportunity.Cccd={Cccd}
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
         where Opportunity.OppNo={OppNo} and Opportunity.Cccd={Cccd}
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
         where Opportunity.Cccd={Cccd}
         return Opportunity
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLOpportunity/GetNamePBXMLOpportunity', methods=['GET'])
def GetNamePBXMLOpportunity():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Opportunity:opportunity) where Opportunity.cccd={cccd}
         RETURN Opportunity.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------Opportunity end--------------------------------------------------------------------


#---------------------------------------------------------Case start--------------------------------------------------------------------

#create Case and assign it to the users
@app.route('/api/PBXMLCase/AddPBXMLCase', methods=['POST']) 
def AddPBXMLCase():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLCase as val
        merge(Case: case
        {
        Cccd : val.Cccd,
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
    graph.run(query,jsonobj=content)
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
    where Case.CaseNo={CaseNo} and Case.Cccd={Cccd}
    SET
    Case.Cccd = val.Cccd,
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
    where Case.CaseNo={CaseNo} and Opportunity.Cccd={Cccd}
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
         where Case.CaseNo={CaseNo} and Case.Cccd={Cccd}
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
         where Case.Cccd={Cccd}
         return Case
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLCase/GetNamePBXMLCase', methods=['GET'])
def GetNamePBXMLCase():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Case:case) where Case.cccd={cccd}
         RETURN Case.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------Case end--------------------------------------------------------------------


#---------------------------------------------------------Campaign start--------------------------------------------------------------------

#create Campaign and assign it to the users
@app.route('/api/PBXMLCampaign/AddPBXMLCampaign', methods=['POST']) 
def AddPBXMLCampaign():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLCampaign as val
        merge(Campaign: campaign
        {
        Cccd : val.Cccd,
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
    graph.run(query,jsonobj=content)
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
    where Campaign.CampaignName={CampaignName} and Campaign.Cccd={Cccd}
    SET
    Campaign.Cccd = val.Cccd,
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
    where Campaign.CampaignName={CampaignName} and Campaign.Cccd={Cccd}
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
         where Campaign.CampaignName={CampaignName} and Campaign.Cccd={Cccd}
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
         where Campaign.Cccd={Cccd}
         return Campaign
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLCampaign/GetNamePBXMLCampaign', methods=['GET'])
def GetNamePBXMLCampaign():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Campaign:campaign) where Campaign.cccd={cccd}
         RETURN Campaign.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------Campaign end--------------------------------------------------------------------


#---------------------------------------------------------Accounts start--------------------------------------------------------------------

#create Accounts and assign it to the users
@app.route('/api/PBXMLAccounts/AddPBXMLAccounts', methods=['POST']) 
def AddPBXMLAccounts():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
                
        unwind v.PBXMLLedger as val
        merge(Ledger: ledger
        {
        Cccd : val.cccd,
        SrlNo: val.SrlNo,
        LeadOwner : val.LeadOwner,
        AccNo : val.AccNo,
        LEDGERNAME : val.LEDGERNAME,
        RESERVEDNAME : val.RESERVEDNAME,
        STATUS : val.STATUS,
        MAILINGNAME : val.MAILINGNAME,
        ADDRESS : val.ADDRESS,
        STATENAME :val.STATENAME,
        PINCODE : val.PINCODE,
        VATTINNUMBER : val.VATTINNUMBER,
        VATDEALERTYPE : val.VATDEALERTYPE,
        TAXTYPE : val.TAXTYPE,
        LEDGERPHONE : val.LEDGERPHONE,
        LEDGERCONTACT : val.LEDGERCONTACT,
        LEDGERFAX : val.LEDGERFAX
        })

		
    """
    graph.run(query,jsonobj=content)
    return "Accounts Created successfully"

#Edit Accounts details
@app.route('/api/PBXMLAccounts/EditPBXMLAccounts', methods=['POST'])
def EditPBXMLAccounts():

    AccNo=request.args['AccNo']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLLedger as val
    with val
    match(Ledger:ledger)
    where Accounts.AccNo={AccNo} and Accounts.Cccd={Cccd}
    SET
    Ledger.Cccd = val.cccd,
    Ledger.SrlNo= val.SrlNo,
    Ledger.LeadOwner = val.LeadOwner,
    Ledger.AccNo = val.AccNo,
    Ledger.LEDGERNAME = val.LEDGERNAME,
    Ledger.RESERVEDNAME = val.RESERVEDNAME,
    Ledger.STATUS = val.STATUS,
    Ledger.MAILINGNAME = val.MAILINGNAME,
    Ledger.ADDRESS = val.ADDRESS,
    Ledger.STATENAME =val.STATENAME,
    Ledger.PINCODE = val.PINCODE,
    Ledger.VATTINNUMBER = val.VATTINNUMBER,
    Ledger.VATDEALERTYPE = val.VATDEALERTYPE,
    Ledger.TAXTYPE = val.TAXTYPE,
    Ledger.LEDGERPHONE = val.LEDGERPHONE,
    Ledger.LEDGERCONTACT = val.LEDGERCONTACT,
    Ledger.LEDGERFAX = val.LEDGERFAX
    """
    graph.run(query,jsonobj=content,AccNo=AccNo,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
	

#Delete Accounts details and relationship 
@app.route('/api/PBXMLAccounts/DeletePBXMLAccounts', methods=['GET']) 
def DeletePBXMLAccounts():
    AccNo=request.args['AccNo']
    Cccd=request.args['Cccd']

    query=""" 
    match(Ledger: ledger)  
    where Accounts.AccNo={AccNo} and Campaign.Cccd={Cccd}
    detach delete Accounts
    """
    graph.run(query,AccNo=AccNo,Cccd=Cccd)
    return "Accounts deleted Successfully"
	

#Get Accounts details
@app.route('/api/PBXMLAccounts/GetPBXMLAccounts', methods=['GET'])
def GetPBXMLAccounts():
    AccNo=request.args['AccNo']
    Cccd=request.args['Cccd']
    
    query = """
         match(Ledger: ledger)
         where Accounts.AccNo={AccNo} and Accounts.Cccd={Cccd}
         return Accounts
        """
    result = []
    for res in graph.run(query,AccNo=AccNo,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 	
	
#Getall Accounts details
@app.route('/api/PBXMLAccounts/GetAllPBXMLAccounts', methods=['GET'])
def GetAllPBXMLAccounts():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Ledger: ledger)
         where Accounts.Cccd={Cccd}
         return Accounts
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLAccounts/GetNamePBXMLAccounts', methods=['GET'])
def GetNamePBXMLAccounts():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Ledger: ledger) where Accounts.cccd={cccd}
         RETURN Accounts.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------Accounts end--------------------------------------------------------------------


#---------------------------------------------------------Product start--------------------------------------------------------------------

#create Product and assign it to the users
@app.route('/api/PBXMLProduct/AddPBXMLProduct', methods=['POST']) 
def AddPBXMLProduct():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLProduct as val
        merge(Product: product
        {
        Cccd : val.Cccd,
        ProductNo: val.ProductNo,
        ProductOwner : val.ProductOwner,
        Company : val.Company,
        FirstName: val.FirstName,
        LastName :val.LastName,
        Title : val.Title,
        Email : val.Email,
        Phone : val.Phone,
        Fax: val.Fax,
        Mobile : val.Mobile,
        Website : val.Website,
        ProductSource: val.ProductSource,
        ProductStatus :val.ProductStatus,
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
    graph.run(query,jsonobj=content)
    return "Product Created successfully"

#Edit Product details
@app.route('/api/PBXMLProduct/EditPBXMLProduct', methods=['POST'])
def EditPBXMLProduct():

    Title=request.args['Title']
    Cccd=request.args['Cccd']
    content = request.get_json()
    print(content)
    print(id)
    query="""
    WITH {jsonobj} as value
    unwind value.PBXMLProduct as val
    with val
    match(Product:product)
    where Product.Title={Title} and Product.Cccd={Cccd}
    SET
    Product.Cccd = val.Cccd,
    Product.ProductNo= val.ProductNo,
    Product.ProductOwner = val.ProductOwner,
    Product.Company = val.Company,
    Product.FirstName= val.FirstName,
    Product.LastName =val.LastName,
    Product.Title = val.Title,
    Product.Email = val.Email,
    Product.Phone = val.Phone,
    Product.Fax= val.Fax,
    Product.Mobile = val.Mobile,
    Product.Website = val.Website,
    Product.ProductSource= val.ProductSource,
    Product.ProductStatus =val.ProductStatus,
    Product.Industry = val.Industry,
    Product.NoOfEmployees = val.NoOfEmployees,
    Product.AnnualRevenue = val.AnnualRevenue,
    Product.Rating= val.Rating,
    Product.SkypeID = val.SkypeID,
    Product.Street = val.Street,
    Product.City= val.City,
    Product.State =val.State,
    Product.ZipCodeSpecified = val.ZipCodeSpecified,
    Product.Country = val.Country,
    Product.Description= val.Description,
    Product.CreatedBy = val.CreatedBy,
    Product.CreatedDate = val.CreatedDate,
    Product.LastUpdatedBy = val.LastUpdatedBy,
    Product.LastUpdatedDate = val.LastUpdatedDate
    """
    graph.run(query,jsonobj=content,Title=Title,Cccd=Cccd)
    return "SUCCESFULLY UPDATED"
		

#Delete Product details and relationship 
@app.route('/api/PBXMLProduct/DeletePBXMLProduct', methods=['GET']) 
def DeletePBXMLProduct():
    Title=request.args['Title']
    Cccd=request.args['Cccd']

    query=""" 
    match(Product:Product)  
    where Product.Title={Title} and Product.Cccd={Cccd}
    detach delete Product
    """
    graph.run(query,Title=Title,Cccd=Cccd)
    return "Product deleted Successfully"
	

#Get Product details
@app.route('/api/PBXMLProduct/GetPBXMLProduct', methods=['GET'])
def GetPBXMLProduct():
    Title=request.args['Title']
    Cccd=request.args['Cccd']
    
    query = """
         match(Product:Product)
         where Product.Title={Title} and Product.Cccd={Cccd}
         return Product
        """
    result = []
    for res in graph.run(query,Title=Title,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 
	
#Getall Product details
@app.route('/api/PBXMLProduct/GetAllPBXMLProduct', methods=['GET'])
def GetAllPBXMLProduct():
    
    Cccd=request.args['Cccd']
    
    query = """
         match(Product:Product)
         where Product.Cccd={Cccd}
         return Product
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#get  name
@app.route('/api/PBXMLProduct/GetNamePBXMLProduct', methods=['GET'])
def GetNamePBXMLProduct():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(Product:Product) where Product.cccd={cccd}
         RETURN Product.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 
#---------------------------------------------------------Product end--------------------------------------------------------------------


app.run(host='127.0.0.1', port=5000)
