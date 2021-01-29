from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")

#create Activities and assign it to the users
@app.route('/api/PBXMLActivities/AddPBXMLActivities', methods=['POST']) 
def AddPBXMLActivities():
    print(request.is_json)
    content = request.get_json()
    print(content)

    Cccd = request.args['Cccd']
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLActivities as val
        merge(Activities: activities
        {
        CCCD : {CCCD},
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
    add_to_activity = """
    match(aa:Activities),(a:activities)
    where aa.CCCD={CCCD}
    create(aa)-[:has]->(a)
    """
    graph.run(query,jsonobj=content,CCCD=Cccd)
    graph.run(add_to_activity,jsonobj=content,CCCD=Cccd)
    
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
    where Activities.ActivityNo={ActivityNo} and Activities.CCCD={Cccd}
    SET
    Activities.CCCD = val.Cccd,
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
    where Activities.ActivityNo={ActivityNo} and Activities.CCCD={Cccd}
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
         where Activities.ActivityNo={ActivityNo} and Activities.CCCD={Cccd}
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
         where Activities.CCCD={Cccd}
         return Activities
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 


app.run(host='0.0.0.0', port=5000) 