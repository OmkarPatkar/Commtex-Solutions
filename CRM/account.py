from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")

#create Accounts and assign it to the users
@app.route('/api/PBXMLAccounts/AddPBXMLAccounts', methods=['POST']) 
def AddPBXMLAccounts():
    print(request.is_json)
    content = request.get_json()
    print(content)

    Cccd = request.args['Cccd']
    
    query=""" 
        WITH {jsonobj} as v
    
                
        unwind v.PBXMLLedger as val
        merge(Ledger: ledger
        {
        CCCD : {Cccd},
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

    add_to_account = """
    match(Acc:Account),(led:ledger)
    where Acc.CCCD = {Cccd}
    create(Acc)-[:has]->(led)
    """
    graph.run(query,jsonobj=content,Cccd=Cccd)
    graph.run(add_to_account,jsonobj=content,Cccd=Cccd)
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
    where Accounts.AccNo={AccNo} and Accounts.CCCD={Cccd}
    SET
    Ledger.CCCD = val.cccd,
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
    where Accounts.AccNo={AccNo} and Campaign.CCCD={Cccd}
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
         where Accounts.AccNo={AccNo} and Accounts.CCCD={Cccd}
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
         where Accounts.CCCD={Cccd}
         return Accounts
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 


app.run(host='0.0.0.0', port=5000)