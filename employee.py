from flask import Flask, render_template, request,jsonify
from py2neo import Graph, Node, Relationship

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data")

# API to create employee nodes.
@app.route('/api/PBXMLEmployee/AddSPBXMLEmployees',methods=['POST'])
def AddSPBXMLEmployees():
    print(request.is_json)
    content = request.get_json()
    print(content)

    cccd = request.args['cccd']

    create_employees = """
    WITH {jsonobj} as v
        create(c:PBXMLEmployees{NAME:"Employees",CCCD:{CCCD}})
        with c, v.PBXMLEmployee as vl
        unwind vl as val
        unwind val.COSTCENTRE as eg
        foreach(employee in eg|
        merge
        (employees : Employees
        {
            CCCD : {CCCD},
            NAME : employee.NAME,
            RESERVEDNAME : employee.RESERVEDNAME,
            ADDRESS : employee.ADDRESS,
            MAILINGNAME : employee.MAILINGNAME,
            DATEOFBIRTH : employee.DATEOFBIRTH,
            DATEOFJOIN : employee.DATEOFJOIN,
            GUID : employee.GUID,
            DEACTIVATIONDATE : employee.DEACTIVATIONDATE,
            VISAEXPIRYDATE : employee.VISAEXPIRYDATE,
            CONTRACTSTARTDATE : employee.CONTRACTSTARTDATE,
            CONTRACTEXPIRYDATE : employee.CONTRACTEXPIRYDATE,
            PASSPORTEXPIRYDATE : employee.PASSPORTEXPIRYDATE,
            PFJOININGDATE : employee.PFJOININGDATE,
            PFJOININGDATE : employee.PFJOININGDATE,
            PFRELIEVINGDATE : employee.PFRELIEVINGDATE,
            PARENT : employee.PARENT,
            CATEGORY : employee.CATEGORY,
            MICRCODE : employee.MICRCODE,
            IFSCODE : employee.IFSCODE,
            NARRATION : employee.NARRATION,
            BANKDETAILS : employee.BANKDETAILS,
            FUNCTION : employee.FUNCTION,
            LOCATION : employee.LOCATION,
            DESIGNATION : employee.DESIGNATION,
            PFACCOUNTNUMBER : employee.PFACCOUNTNUMBER,
            PANNUMBER : employee.PANNUMBER,
            ESINUMBER : employee.ESINUMBER,
            PASSPORTDETAILS : employee.PASSPORTDETAILS,
            GENDER : employee.GENDER,
            BLOODGROUP : employee.BLOODGROUP,
            FATHERNAME : employee.FATHERNAME,
            CONTACTNUMBERS : employee.CONTACTNUMBERS,
            EMAILID : employee.EMAILID,
            BANKACCOUNTNUMBER : employee.BANKACCOUNTNUMBER,
            BANKBRANCH : employee.BANKBRANCH,
            VISANUMBER : employee.VISANUMBER,
            WORKPERMITNUMBER : employee.WORKPERMITNUMBER,
            COUNTRYOFISSUE : employee.COUNTRYOFISSUE,
            SPOUSENAME : employee.SPOUSENAME,
            FPFACCOUNTNUMBER : employee.FPFACCOUNTNUMBER,
            REASONSFORLEAVING : employee.REASONSFORLEAVING,
            ESIDISPENSARYNAME : employee.ESIDISPENSARYNAME,
            EMPDISPLAYNAME : employee.EMPDISPLAYNAME,
            PRACCOUNTNUMBER : employee.PRACCOUNTNUMBER,
            REVENUELEDFOROPBAL : employee.REVENUELEDFOROPBAL,
            ISUPDATINGTARGETID : employee.ISUPDATINGTARGETID,
            ASORIGINAL : employee.ASORIGINAL,
            AFFECTSSTOCK : employee.AFFECTSSTOCK,
            FORPAYROLL : employee.FORPAYROLL,
            FORJOBCOSTING : employee.FORJOBCOSTING,
            ISEMPLOYEEGROUP : employee.ISEMPLOYEEGROUP,
            SORTPOSITION : employee.SORTPOSITION,
            ALTERID : employee.ALTERID,
            ITPREVEMPLYRDETAILSLIST : employee.ITPREVEMPLYRDETAILSLIST,
            ITOPENINGBALDETAILSLIST : employee.ITOPENINGBALDETAILSLIST
        }
    )<- [:contains]-(c)
    foreach (pdl in eg.PAYMENTDETAILSLIST | merge(employees)-[:has]->(:PaymentDetails
        {
            PAYDETSRL:pdl.PAYDETSRL,
            IFSCODE:pdl.IFSCODE,
            BANKNAME:pdl.BANKNAME,
            ACCOUNTNUMBER:pdl.ACCOUNTNUMBER,
            PAYMENTFAVOURING:pdl.PAYMENTFAVOURING,
            TRANSACTIONNAME:pdl.TRANSACTIONNAME,
            SETASDEFAULT:pdl.SETASDEFAULT,
            DEFAULTTRANSACTIONTYPE:pdl.DEFAULTTRANSACTIONTYPE}))   
    foreach (pdl in eg.EMPLOYEEPERIODLIST | merge(employees)-[:has]->(:PeriodDetails
        {
            MPPRDSRL:pdl.EMPPRDSRL,
            PERIODFROM:pdl.PERIODFROM,
            PERIODTO:pdl.PERIODTO
        })
        -[:has]->(:EMPLOYEERATELIST
        {  
            EMPRATESRL:"",
            EMPRATENAME:"",
            EMPTIMERATE:"",
            EMPRATE:""
        })
    )
    foreach (pdl in eg.ITDEDUCTIONDETAILSLIST | merge(employees)-[:has]->(:DeductionDetails
        {
            PERIODFROM:pdl.PERIODFROM,
            PERIODTO:pdl.PERIODTO,
            BANKNAME:pdl.BANKNAME,
            TYPE:pdl.TYPE,
            TANNO:pdl.TANNO,
            CHARGEABLEAMOUNT:pdl.CHARGEABLEAMOUNT,
            DEDUCTEDAMOUNT:pdl.DEDUCTEDAMOUNT,
            TAXABLEAMOUNT:pdl.TAXABLEAMOUNT,
            PAYABLEAMOUNT:pdl.PAYABLEAMOUNT,
            REFUNDABLEAMOUNT:pdl.REFUNDABLEAMOUNT
        })
    )
    foreach (pdl in eg.ITOVERRIDEDETAILSLIST | merge(employees)-[:has]->(:OverrideDetails
        {
            COMPONENTNAME:pdl.COMPONENTNAME,
            COMPONENTYEAR:pdl.COMPONENTYEAR
        })
    )
    foreach (pdl in eg.ITDECLARATIONDETAILSLIST | merge(employees)-[:has]->(:DeclarationDetails
        {
            COMPONENTNAME:pdl.COMPONENTNAME,
            COMPONENTYEAR:pdl.COMPONENTYEAR
        })
    )
    )
    """   
    add_to_company = """
    match(c:Company),(e:PBXMLEmployees)
    where c.CCCD = {CCCD}
    create(c)-[:has]->(e)
    """
    graph.run(create_employees,jsonobj=content,CCCD=cccd)
    graph.run(add_to_company,jsonobj=content,CCCD=cccd)
    return "Employee group created successfully"

# API to edit employee Details.
@app.route('/editemployeeDetails',methods=['POST'])
def editemployeeDetails():
    NAME=request.args['NAME']
    CCCD=request.args['CCCD']
    content = request.get_json()
    print(content)

    edit_employee_details = """
    WITH {jsonobj} as v
        UNWIND v.PBXMLEmployee as val
        UNWIND val.COSTCENTRE as we
        UNWIND we.PAYMENTDETAILSLIST as pdl
        UNWIND we.EMPLOYEEPERIODLIST as epl
        UNWIND epl.EMPLOYEERATELIST as erl
        UNWIND we.ITDEDUCTIONDETAILSLIST as idl
        UNWIND we.ITOVERRIDEDETAILSLIST as iol
        UNWIND we.ITDECLARATIONDETAILSLIST as iddl
        with val,we,pdl,epl,erl,idl,iol,iddl
       
        match(employees : Employees)
        where employees.NAME={NAME} and employees.CCCD={CCCD}
        SET
            employees.NAME : we.NAME,
            employees.RESERVEDNAME : we.RESERVEDNAME,
            employees.ADDRESS : we.ADDRESS,
            employees.MAILINGNAME : we.MAILINGNAME,
            employees.DATEOFBIRTH : we.DATEOFBIRTH,
            employees.DATEOFJOIN : we.DATEOFJOIN,
            employees.GUID : we.GUID,
            employees.DEACTIVATIONDATE : we.DEACTIVATIONDATE,
            employees.VISAEXPIRYDATE : we.VISAEXPIRYDATE,
            employees.CONTRACTSTARTDATE : we.CONTRACTSTARTDATE,
            employees.CONTRACTEXPIRYDATE : we.CONTRACTEXPIRYDATE,
            employees.PASSPORTEXPIRYDATE : we.PASSPORTEXPIRYDATE,
            employees.PFJOININGDATE : we.PFJOININGDATE,
            employees.PFJOININGDATE : we.PFJOININGDATE,
            employees.PFRELIEVINGDATE : we.PFRELIEVINGDATE,
            employees.PARENT : we.PARENT,
            employees.CATEGORY : we.CATEGORY,
            employees.MICRCODE : we.MICRCODE,
            employees.IFSCODE : we.IFSCODE,
            employees.NARRATION : we.NARRATION,
            employees.BANKDETAILS : we.BANKDETAILS,
            employees.FUNCTION : we.FUNCTION,
            employees.LOCATION : we.LOCATION,
            employees.DESIGNATION : we.DESIGNATION,
            employees.PFACCOUNTNUMBER : we.PFACCOUNTNUMBER,
            employees.PANNUMBER : we.PANNUMBER,
            employees.ESINUMBER : we.ESINUMBER,
            employees.PASSPORTDETAILS : we.PASSPORTDETAILS,
            employees.GENDER : we.GENDER,
            employees.BLOODGROUP : we.BLOODGROUP,
            employees.FATHERNAME : we.FATHERNAME,
            employees.CONTACTNUMBERS : we.CONTACTNUMBERS,
            employees.EMAILID : we.EMAILID,
            employees.BANKACCOUNTNUMBER : we.BANKACCOUNTNUMBER,
            employees.BANKBRANCH : we.BANKBRANCH,
            employees.VISANUMBER : we.VISANUMBER,
            employees.WORKPERMITNUMBER : we.WORKPERMITNUMBER,
            employees.COUNTRYOFISSUE : we.COUNTRYOFISSUE,
            employees.SPOUSENAME : we.SPOUSENAME,
            employees.FPFACCOUNTNUMBER : we.FPFACCOUNTNUMBER,
            employees.REASONSFORLEAVING : we.REASONSFORLEAVING,
            employees.ESIDISPENSARYNAME : we.ESIDISPENSARYNAME,
            employees.EMPDISPLAYNAME : we.EMPDISPLAYNAME,
            employees.PRACCOUNTNUMBER : we.PRACCOUNTNUMBER,
            employees.REVENUELEDFOROPBAL : we.REVENUELEDFOROPBAL,
            employees.ISUPDATINGTARGETID : we.ISUPDATINGTARGETID,
            employees.ASORIGINAL : we.ASORIGINAL,
            employees.AFFECTSSTOCK : we.AFFECTSSTOCK,
            employees.FORPAYROLL : we.FORPAYROLL,
            employees.FORJOBCOSTING : we.FORJOBCOSTING,
            employees.ISEMPLOYEEGROUP : we.ISEMPLOYEEGROUP,
            employees.SORTPOSITION : we.SORTPOSITION,
            employees.ALTERID : we.ALTERID,
            employees.ITPREVEMPLYRDETAILSLIST : we.ITPREVEMPLYRDETAILSLIST,
            employees.ITOPENINGBALDETAILSLIST : we.ITOPENINGBALDETAILSLIST

        WITH we.PAYMENTDETAILSLIST as val,we,pdl
        match(pdl:PAYMENTDETAILSLIST),(employees : Employees)
        where employees.NAME={NAME} and employees.Cccd={Cccd}
        SET
            we.PAYDETSRL:pdl.PAYDETSRL,
            we.IFSCODE:pdl.IFSCODE,
            we.BANKNAME:pdl.BANKNAME,
            we.ACCOUNTNUMBER:pdl.ACCOUNTNUMBER,
            we.PAYMENTFAVOURING:pdl.PAYMENTFAVOURING,
            we.TRANSACTIONNAME:pdl.TRANSACTIONNAME,
            we.SETASDEFAULT:pdl.SETASDEFAULT,
            we.DEFAULTTRANSACTIONTYPE:pdl.DEFAULTTRANSACTIONTYPE
        
        WITH we.EMPLOYEEPERIODLIST as val,we,pdl
        match(pdl:PAYMENTDETAILSLIST),(employees : Employees)
        where employees.NAME={NAME} and employees.Cccd={Cccd}
        SET

        WITH we.ITDEDUCTIONDETAILSLIST as iddl
        match(pdl:PAYMENTDETAILSLIST),(employees : Employees)
        where employees.NAME={NAME} and employees.Cccd={Cccd}
        SET
            we.PERIODFROM:pdl.PERIODFROM,
            we.PERIODTO:pdl.PERIODTO,
            we.BANKNAME:pdl.BANKNAME,
            we.TYPE:pdl.TYPE,
            we.TANNO:pdl.TANNO,
            we.CHARGEABLEAMOUNT:pdl.CHARGEABLEAMOUNT,
            we.DEDUCTEDAMOUNT:pdl.DEDUCTEDAMOUNT,
            we.TAXABLEAMOUNT:pdl.TAXABLEAMOUNT,
            we.PAYABLEAMOUNT:pdl.PAYABLEAMOUNT,
            we.REFUNDABLEAMOUNT:pdl.REFUNDABLEAMOUNT

        WITH we.ITOVERRIDEDETAILSLIST as val,we,pdl
        match(pdl:PAYMENTDETAILSLIST),(employees : Employees)
        where employees.NAME={NAME} and employees.Cccd={Cccd}
        SET
            we.COMPONENTNAME:pdl.COMPONENTNAME,
            we.COMPONENTYEAR:pdl.COMPONENTYEAR

        WITH we.ITDECLARATIONDETAILSLIST as val,we,pdl
        match(pdl:PAYMENTDETAILSLIST),(employees : Employees)
        where employees.NAME={NAME} and employees.Cccd={Cccd}
        SET
            we.COMPONENTNAME:pdl.COMPONENTNAME,
            we.COMPONENTYEAR:pdl.COMPONENTYEAR
    """
    graph.run(edit_employee_details,jsonobj=content,NAME=NAME,CCCD=CCCD)
    return "SUCCESFULLY UPDATED"
    


# API to delete employee
@app.route('/deleteemployee',methods=['GET'])
def deleteemployee():
    NAME = request.args['NAME']
    delete_employee = """
        MATCH (employees : Employees)
        WHERE employees.NAME={NAME}
        DETACH DELETE employees
    """
    graph.run(delete_employee,NAME=NAME)
    return "employee deleted successfully"

# API to get employee details
@app.route('/getemployee',methods=['GET'])
def getemployee():
    NAME = request.args['NAME']
    get_employee_details = """
    MATCH(employees : Employees)
    where employees.NAME = {NAME}
    return employees
    """
    result = jsonify(graph.run(get_employee_details,NAME=NAME).data())
    return result

# API to get all employee details
@app.route('/getAllemployee',methods=['GET'])
def getAllemployee():
    get_all_employee = """
    match(employees : Employees)
    RETURN employees
    """
    result = []
    for res in graph.run(get_all_employee):
        result.append(str(res[0]))
    return jsonify(result)

app.run(host='127.0.0.1', port=5000)