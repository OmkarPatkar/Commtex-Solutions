from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:11003/db/data/")


#create project and assign it to the users
@app.route('/api/PBXMLGroup/AddPBXMLGroups', methods=['POST']) 
def AddPBXMLGroups():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
        WITH {jsonobj} as v
    
        unwind v.PBXMLGroups as val
        unwind val.PBXMLGroup as gg
        unwind gg.SERVICETAXDETAILSLIST as st
        unwind gg.GSTDETAILSLIST as gst 

        foreach(grp in gg|
        merge
        (group : Group 
        {
        cccd : grp.cccd,
        NAME : grp.NAME,
        RESERVEDNAME : grp.RESERVEDNAME,
        GUID : grp.GUID,
        PARENT : grp.PARENT,
        BASICGROUPISCALCULABLE : grp.BASICGROUPISCALCULABLE,
        GRPDEBITPARENT : grp.GRPDEBITPARENT,
        GRPCREDITPARENT : grp.GRPCREDITPARENT,
        ADDLALLOCTYPE : grp.ADDLALLOCTYPE,
        ISBILLWISEON : grp.ISBILLWISEON,
        ISCOSTCENTRESON : grp.ISCOSTCENTRESON,
        ISREVENUE : grp.ISREVENUE,
        ISADDABLE : grp.ISADDABLE,
        ISUPDATINGTARGETID : grp.ISUPDATINGTARGETID,
        ASORIGINAL : grp.ASORIGINAL,
        ISSUBLEDGER : grp.ISSUBLEDGER,
        AFFECTSGROSSPROFIT : grp.AFFECTSGROSSPROFIT,
        ISDEEMEDPOSITIVE : grp.ISDEEMEDPOSITIVE,
        TRACKNEGATIVEBALANCES : grp.TRACKNEGATIVEBALANCES,
        ISCONDENSED : grp.ISCONDENSED,
        AFFECTSSTOCK : grp.AFFECTSSTOCK,
        ISGROUPFORLOANRCPT : grp.ISGROUPFORLOANRCPT,
        ISGROUPFORLOANPYMNT : grp.ISGROUPFORLOANPYMNT,
        ISRATEINCLUSIVEVAT : grp.ISRATEINCLUSIVEVAT,
        ISINVDETAILSENABLE : grp.ISINVDETAILSENABLE,
        ALTERID : grp.ALTERID,
        SORTPOSITION : grp.SORTPOSITION,
        SALESTAXCESSDETAILSLIST : grp.SALESTAXCESSDETAILSLIST,
        XBRLDETAILLIST : grp.XBRLDETAILLIST,
        AUDITDETAILSLIST : grp.AUDITDETAILSLIST,
        SCHVIDETAILSLIST : grp.SCHVIDETAILSLIST,
        TCSCATEGORYDETAILSLIST : grp.TCSCATEGORYDETAILSLIST,
        GSTCLASSFNIGSTRATESLIST : grp.GSTCLASSFNIGSTRATESLIST,
        EXTARIFFDUTYHEADDETAILSLIST :grp.EXTARIFFDUTYHEADDETAILSLIST
        }
        )

        foreach (pdl in st.SERVICETAXDETAILSLIST | merge(group)-[:has]->(:ServiceTaxDetails
        {APPLICABLEFROM:pdl.APPLICABLEFROM,
        CATEGORYNAME:pdl.CATEGORYNAME,
        ISREVERSEAPPLICABLE:pdl.ISREVERSEAPPLICABLE,
        ISNEGATIVELISTSERVICE:pdl.ISNEGATIVELISTSERVICE,
        USEFORISD:pdl.USEFORISD,
        ISRECIPIENTLIAB:pdl.USEFORISD,
        SERVICETAXRATE:pdl.SERVICETAXRATE,
        CESSRATE:pdl.CESSRATE,
        SECONDARYCESSRATE:pdl.SECONDARYCESSRATE,
        SWACHBHARATCESS:pdl.SWACHBHARATCESS,
        KRISHIKALYANCESS:pdl.KRISHIKALYANCESS
        })
        )
        foreach (vl in gg.VATDETAILSLIST | merge(group)-[:has]->(:VatDetails
        {FROMDATE:vl.FROMDATE,
        FRMDATE:vl.FRMDATE,
        TAXTYPE:vl.TAXTYPE,
        ISINZRBASICSERVICES:vl.ISINZRBASICSERVICES,
        ISINVDETAILSENABLE:vl.ISINVDETAILSENABLE,
        ISCALCONACTUALQTY:vl.ISCALCONACTUALQTY,
        RATEOFVAT:vl.RATEOFVAT,
        VATITEMSLABRATESLIST:vl.VATITEMSLABRATESLIST
        })
        )

        foreach (gdl in gg.GSTDETAILSLIST | merge(group)-[:has]->(:GstDetails
        {APPLICABLEFROM:gdl.APPLICABLEFROM,
        HSNMASTERNAME:gdl.HSNMASTERNAME,
        TAXABILITY:gdl.TAXABILITY,
        ISREVERSECHARGEAPPLICABLE:gdl.ISREVERSECHARGEAPPLICABLE,
        ISNONGSTGOODS:gdl.ISNONGSTGOODS,
        GSTINELIGIBLEITC:gdl.GSTINELIGIBLEITC,
        INCLUDEEXPFORSLABCALC:gdl.INCLUDEEXPFORSLABCALC
        })
        )
        foreach (etd in gg.EXCISETARIFFDETAILSLIST | merge(group)-[:has]->(:ExciseDetails
        {APPLICABLEFROM:etd.APPLICABLEFROM,
        TYPEOFTARIFF:etd.TYPEOFTARIFF,
        REPORTINGUOM:etd.REPORTINGUOM,
        TARIFFNAME:etd.TARIFFNAME,
        HSNCODE:etd.HSNCODE,
        VALUATIONTYPE:etd.VALUATIONTYPE,
        ISEXCISECALCULATEONMRP:etd.ISEXCISECALCULATEONMRP,
        ISNONDUTIABLE:etd.ISNONDUTIABLE
        })
        )
        foreach (tds in gg.TDSCATEGORYDETAILSLIST | merge(group)-[:has]->(:TDSCategory
        {
        CATEGORYDATE:tds.CATEGORYDATE,
        CATEGORYNAME:tds.CATEGORYNAME
        })
        )
        )
    """
    graph.run(query,jsonobj=content)
    # return jsonify(content)
    return "Group Created successfully"

@app.route('/api/PBXMLGroup/AddPBXMLGroup', methods=['POST']) 
def AddPBXMLGroup():
    print(request.is_json)
    content = request.get_json()
    print(content)
    
    query=""" 
    WITH {jsonobj} as v
    
        unwind v.PBXMLGroups as val
        unwind val.PBXMLGroup as gg
        unwind gg.SERVICETAXDETAILSLIST as st
        unwind gg.GSTDETAILSLIST as gst 


        merge
        (group : Group 
        {
        cccd : gg.cccd,
        NAME : gg.NAME,
        RESERVEDNAME : gg.RESERVEDNAME,
        GUID : gg.GUID,
        PARENT : gg.PARENT,
        BASICGROUPISCALCULABLE : gg.BASICGROUPISCALCULABLE,
        GRPDEBITPARENT : gg.GRPDEBITPARENT,
        GRPCREDITPARENT : gg.GRPCREDITPARENT,
        ADDLALLOCTYPE : gg.ADDLALLOCTYPE,
        ISBILLWISEON : gg.ISBILLWISEON,
        ISCOSTCENTRESON : gg.ISCOSTCENTRESON,
        ISREVENUE : gg.ISREVENUE,
        ISADDABLE : gg.ISADDABLE,
        ISUPDATINGTARGETID : gg.ISUPDATINGTARGETID,
        ASORIGINAL : gg.ASORIGINAL,
        ISSUBLEDGER : gg.ISSUBLEDGER,
        AFFECTSGROSSPROFIT : gg.AFFECTSGROSSPROFIT,
        ISDEEMEDPOSITIVE : gg.ISDEEMEDPOSITIVE,
        TRACKNEGATIVEBALANCES : gg.TRACKNEGATIVEBALANCES,
        ISCONDENSED : gg.ISCONDENSED,
        AFFECTSSTOCK : gg.AFFECTSSTOCK,
        ISGROUPFORLOANRCPT : gg.ISGROUPFORLOANRCPT,
        ISGROUPFORLOANPYMNT : gg.ISGROUPFORLOANPYMNT,
        ISRATEINCLUSIVEVAT : gg.ISRATEINCLUSIVEVAT,
        ISINVDETAILSENABLE : gg.ISINVDETAILSENABLE,
        ALTERID : gg.ALTERID,
        SORTPOSITION : gg.SORTPOSITION,
        SALESTAXCESSDETAILSLIST : gg.SALESTAXCESSDETAILSLIST,
        XBRLDETAILLIST : gg.XBRLDETAILLIST,
        AUDITDETAILSLIST : gg.AUDITDETAILSLIST,
        SCHVIDETAILSLIST : gg.SCHVIDETAILSLIST,
        TCSCATEGORYDETAILSLIST : gg.TCSCATEGORYDETAILSLIST,
        GSTCLASSFNIGSTRATESLIST : gg.GSTCLASSFNIGSTRATESLIST,
        EXTARIFFDUTYHEADDETAILSLIST :gg.EXTARIFFDUTYHEADDETAILSLIST
        }
        )

        foreach (pdl in st.SERVICETAXDETAILSLIST | merge(group)-[:has]->(:ServiceTaxDetails
        {APPLICABLEFROM:pdl.APPLICABLEFROM,
        CATEGORYNAME:pdl.CATEGORYNAME,
        ISREVERSEAPPLICABLE:pdl.ISREVERSEAPPLICABLE,
        ISNEGATIVELISTSERVICE:pdl.ISNEGATIVELISTSERVICE,
        USEFORISD:pdl.USEFORISD,
        ISRECIPIENTLIAB:pdl.USEFORISD,
        SERVICETAXRATE:pdl.SERVICETAXRATE,
        CESSRATE:pdl.CESSRATE,
        SECONDARYCESSRATE:pdl.SECONDARYCESSRATE,
        SWACHBHARATCESS:pdl.SWACHBHARATCESS,
        KRISHIKALYANCESS:pdl.KRISHIKALYANCESS
        })
        )
        foreach (vl in gg.VATDETAILSLIST | merge(group)-[:has]->(:VatDetails
        {FROMDATE:vl.FROMDATE,
        FRMDATE:vl.FRMDATE,
        TAXTYPE:vl.TAXTYPE,
        ISINZRBASICSERVICES:vl.ISINZRBASICSERVICES,
        ISINVDETAILSENABLE:vl.ISINVDETAILSENABLE,
        ISCALCONACTUALQTY:vl.ISCALCONACTUALQTY,
        RATEOFVAT:vl.RATEOFVAT,
        VATITEMSLABRATESLIST:vl.VATITEMSLABRATESLIST
        })
        )

        foreach (gdl in gg.GSTDETAILSLIST | merge(group)-[:has]->(:GstDetails
        {APPLICABLEFROM:gdl.APPLICABLEFROM,
        HSNMASTERNAME:gdl.HSNMASTERNAME,
        TAXABILITY:gdl.TAXABILITY,
        ISREVERSECHARGEAPPLICABLE:gdl.ISREVERSECHARGEAPPLICABLE,
        ISNONGSTGOODS:gdl.ISNONGSTGOODS,
        GSTINELIGIBLEITC:gdl.GSTINELIGIBLEITC,
        INCLUDEEXPFORSLABCALC:gdl.INCLUDEEXPFORSLABCALC
        })
        )
        foreach (etd in gg.EXCISETARIFFDETAILSLIST | merge(group)-[:has]->(:ExciseDetails
        {APPLICABLEFROM:etd.APPLICABLEFROM,
        TYPEOFTARIFF:etd.TYPEOFTARIFF,
        REPORTINGUOM:etd.REPORTINGUOM,
        TARIFFNAME:etd.TARIFFNAME,
        HSNCODE:etd.HSNCODE,
        VALUATIONTYPE:etd.VALUATIONTYPE,
        ISEXCISECALCULATEONMRP:etd.ISEXCISECALCULATEONMRP,
        ISNONDUTIABLE:etd.ISNONDUTIABLE
        })
        )
        foreach (tds in gg.TDSCATEGORYDETAILSLIST | merge(group)-[:has]->(:TDSCategory
        {
        CATEGORYDATE:tds.CATEGORYDATE,
        CATEGORYNAME:tds.CATEGORYNAME
        })
        )
#Edit project details
@app.route('/api/PBXMLGroup/EditPBXMLGroup', methods=['POST'])
def EditPBXMLGroup():
    NAME=request.args['NAME']
    cccd=request.args['cccd']
    content = request.get_json()
    print(content)
    query=""" 
    WITH {jsonobj} as v
    match(group:Group) 
        where group.NAME={NAME} and group.cccd={cccd}
        unwind v.PBXMLGroups as val
        unwind val.PBXMLGroup as we
        foreach (grp in we| SET group.NAME=grp.NAME,
        group.PARENT=grp.PARENT,
        group.GUID=grp.GUID,
        group.ISBILLWISEON=grp.ISBILLWISEON,
        group.ISCOSTCENTRESON=grp.ISCOSTCENTRESON,
        group.ISREVENUE=grp.ISREVENUE,
        group.ISADDABLE=grp.ISADDABLE,
        group.ISUPDATINGTARGETID=grp.ISUPDATINGTARGETID,
        group.ASORIGINAL=grp.ASORIGINAL,
        group.ISSUBLEDGER=grp.ISSUBLEDGER,
        group.AFFECTSGROSSPROFIT=grp.AFFECTSGROSSPROFIT,
        group.ISDEEMEDPOSITIVE=grp.ISDEEMEDPOSITIVE,
        group.TRACKNEGATIVEBALANCES=grp.TRACKNEGATIVEBALANCES,
        group.ISCONDENSED=grp.ISCONDENSED,
        group.AFFECTSSTOCK=grp.AFFECTSSTOCK,
        group.ISGROUPFORLOANRCPT=grp.ISGROUPFORLOANRCPT,
        group.ISGROUPFORLOANPYMNT=grp.ISGROUPFORLOANPYMNT,
        group.ISRATEINCLUSIVEVAT=grp.ISRATEINCLUSIVEVAT,
        group.ISINVDETAILSENABLE=grp.ISINVDETAILSENABLE,
        group.ALTERID=grp.ALTERID,
        group.SORTPOSITION=grp.SORTPOSITION,
        group.SALESTAXCESSDETAILSLIST = grp.SALESTAXCESSDETAILSLIST,
        group.XBRLDETAILLIST = grp.XBRLDETAILLIST,
        group.AUDITDETAILSLIST = grp.AUDITDETAILSLIST,
        group.SCHVIDETAILSLIST = grp.SCHVIDETAILSLIST,
        group.TCSCATEGORYDETAILSLIST = grp.TCSCATEGORYDETAILSLIST,
        group.GSTCLASSFNIGSTRATESLIST = grp.GSTCLASSFNIGSTRATESLIST,
        group.EXTARIFFDUTYHEADDETAILSLIST = grp.EXTARIFFDUTYHEADDETAILSLIST
        
        )

        foreach (pdl in st.SERVICETAXDETAILSLIST | SET group.APPLICABLEFROM=pdl.APPLICABLEFROM,
        group.CATEGORYNAME=pdl.CATEGORYNAME,
        group.ISREVERSEAPPLICABLE=pdl.ISREVERSEAPPLICABLE,
        group.ISNEGATIVELISTSERVICE=pdl.ISNEGATIVELISTSERVICE,
        group.USEFORISD=pdl.USEFORISD,
        group.ISRECIPIENTLIAB=pdl.USEFORISD,
        group.SERVICETAXRATE=pdl.SERVICETAXRATE,
        group.CESSRATE=pdl.CESSRATE,
        group.SECONDARYCESSRATE=pdl.SECONDARYCESSRATE,
        group.SWACHBHARATCESS=pdl.SWACHBHARATCESS,
        group.KRISHIKALYANCESS=pdl.KRISHIKALYANCESS
        )
        )
        foreach (vl in gg.VATDETAILSLIST | SET group.FROMDATE=vl.FROMDATE,
        group.FRMDATE=vl.FRMDATE,
        group.TAXTYPE=vl.TAXTYPE,
        group.ISINZRBASICSERVICES=vl.ISINZRBASICSERVICES,
        group.ISINVDETAILSENABLE=vl.ISINVDETAILSENABLE,
        group.ISCALCONACTUALQTY=vl.ISCALCONACTUALQTY,
        group.RATEOFVAT=vl.RATEOFVAT,
        group.VATITEMSLABRATESLIST=vl.VATITEMSLABRATESLIST
        )
        )

        foreach (gdl in gg.GSTDETAILSLIST | SET group.APPLICABLEFROM=gdl.APPLICABLEFROM,
        group.HSNMASTERNAME=gdl.HSNMASTERNAME,
        group.TAXABILITY=gdl.TAXABILITY,
        group.ISREVERSECHARGEAPPLICABLE=gdl.ISREVERSECHARGEAPPLICABLE,
        group.ISNONGSTGOODS=gdl.ISNONGSTGOODS,
        group.GSTINELIGIBLEITC=gdl.GSTINELIGIBLEITC,
        group.INCLUDEEXPFORSLABCALC=gdl.INCLUDEEXPFORSLABCALC
        )
        )
        foreach (etd in gg.EXCISETARIFFDETAILSLIST | SET group.APPLICABLEFROM=etd.APPLICABLEFROM,
        group.TYPEOFTARIFF=etd.TYPEOFTARIFF,
        group.REPORTINGUOM=etd.REPORTINGUOM,
        group.TARIFFNAME=etd.TARIFFNAME,
        group.HSNCODE=etd.HSNCODE,
        group.VALUATIONTYPE=etd.VALUATIONTYPE,
        group.ISEXCISECALCULATEONMRP=etd.ISEXCISECALCULATEONMRP,
        group.ISNONDUTIABLE=etd.ISNONDUTIABLE
        )
        )
        foreach (tds in gg.TDSCATEGORYDETAILSLIST | SET
        group.CATEGORYDATE=tds.CATEGORYDATE,
        group.CATEGORYNAME=tds.CATEGORYNAME
        )
        )
        )
    """
    graph.cypher.execute(query,jsonobj=content,NAME=NAME,cccd=cccd)
    return "SUCCESFULLY UPDATED"

#Delete Project details and relationship 
@app.route('/api/PBXMLGroup/DeletePBXMLGroup', methods=['GET']) 
def DeletePBXMLGroup():
    NAME=request.args['NAME']
    cccd=request.args['cccd']
    #UserId=request.args['UserId']
    query=""" 
    match(group:Group)  
    where group.NAME={NAME} and group.cccd={cccd}
    detach delete group
    """
    graph.cypher.execute(query,NAME=NAME)
    return "Group deleted Successfully"

#Get project details
@app.route('/api/PBXMLGroup/GetPBXMLGroup', methods=['GET'])
def GetPBXMLGroup():
    ID=request.args['NAME']
    cccd=request.args['cccd']
    #project=request.args['ProjectName']
    query = '''
         match(group:Group)  
         where group.NAME={ID} and group.cccd={cccd}
         RETURN group 
        '''
    result = []
    for res in graph.cypher.execute(query, ID=ID,cccd=cccd):
        result.append(str(res[0]))
    return jsonify(result) 

#Get all project details
@app.route('/api/PBXMLGroup/GetAllPBXMLGroup', methods=['GET'])
def GetAllPBXMLGroup():
    ID=request.args['cccd']
    query = '''
         match(group:Group) where group.cccd={ID}
         RETURN group
        '''
    result = []
    for res in graph.cypher.execute(query,ID=ID):
        result.append(str(res[0]))

    return jsonify(result) 

@app.route('/api/PBXMLGroup/GetNamePBXMLGroup', methods=['GET'])
def GetNamePBXMLGroup():
    #ID=request.args['NAME']
    cccd=request.args['cccd']
    query = '''
         match(group:Group) where group.cccd={cccd}
         RETURN group.NAME
        '''
    result = []
    for res in graph.cypher.execute(query):
        result.append(str(res[0]))
    
    return jsonify(result) 

app.run(host='0.0.0.0', port=5000)