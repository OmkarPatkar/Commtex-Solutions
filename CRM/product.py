from flask import Flask, jsonify
from flask import request
from py2neo import Graph, Node, Relationship,cypher

app = Flask(__name__)

graph = Graph("http://localhost:7474/db/data/")

#create Product and assign it to the users
@app.route('/api/PBXMLProduct/AddPBXMLProduct', methods=['POST']) 
def AddPBXMLProduct():
    print(request.is_json)
    content = request.get_json()
    print(content)

    Cccd = request.args['Cccd']
    
    query=""" 
        WITH {jsonobj} as v
    
           
        unwind v.PBXMLProduct as val
        merge(Product: product
        {
        CCCD : {Cccd},
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
    add_to_product = """
    match(Prod:Product),(prod:product)
    where Prod.CCCD = {Cccd}
    create(Prod)-[:has]->(prod)
    """
    graph.run(query,jsonobj=content,Cccd=Cccd)
    graph.run(add_to_product,jsonobj=content,Cccd=Cccd)
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
    where Product.Title={Title} and Product.CCCD={Cccd}
    SET
    Product.CCCD = val.CCCD,
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
    where Product.Title={Title} and Product.CCCD={Cccd}
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
         where Product.Title={Title} and Product.CCCD={Cccd}
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
         where Product.CCCD={Cccd}
         return Product
        """
    result = []
    for res in graph.run(query,Cccd=Cccd):
        result.append(str(res[0]))
    return jsonify(result) 


app.run(host='0.0.0.0', port=5000)