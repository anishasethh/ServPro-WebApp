from flask import Flask,render_template,request,url_for,redirect
from backend.models import *
from flask import current_app as app
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plot

        
@app.route("/admin")
def admin():
    services=getservices()
    customer=getcustomers()
    for cust in customer:
        cust.avg_cust_rating=get_average_crating(cust.cust_id)
    professional=getprofessionals()
    for prof in professional:
        prof.avg_prof_rating=get_average_prating(prof.prof_id)
    db.session.commit()   
    service_requests=getrequests()
    return render_template("admin_dashb.html",services=services,customer=customer,professional=professional,service_requests=service_requests)


@app.route("/customer/<username>")
def customer(username):
    services=getservices()
    new_services=[service for service in services if service.serv_id < 6]
    professional=getprofessionals()
    customer=Customer.query.filter_by(username=username).first()
    service_requests=get_cservice_req(customer.cust_id)
    return render_template("customer_dashb.html",username=username,professional=professional,cust_id=customer.cust_id,services=new_services,service_requests=service_requests)


@app.route("/professional/<username>")
def professional(username):
    professional=Professional.query.filter_by(username=username).first()
    serv_id=professional.serv_id
    service_requests=get_service_req(serv_id)
    prof_service_requests=Service_Requests.query.filter_by(prof_id=professional.prof_id).all()
    customers=getcustomers()
    return render_template("professional_dashb.html",professional=professional,username=username,customers=customers,prof_service_requests=prof_service_requests,service_requests=service_requests,prof_id=professional.prof_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html",error_message="",success_message="")
    if request.method=="POST":
        username=request.form.get("username")   
        password1=request.form.get("password")   
        login_name=request.form.get("login_name")
        user1=User.query.filter_by(username=username,password=password1).first()
        if user1 and user1.role==int(login_name):
            if user1.role==1:
                return redirect(url_for("admin"))
            elif user1.role==2:
                return redirect(url_for("professional",username=username))
        
            else:
                return redirect(url_for("customer",username=username))
        else:
            return render_template("login.html",error_message="Account Not Found :(",success_message="")


@app.route("/customer_signup",methods=["GET","POST"])
def customer_signup():
    if request.method=="GET":
        return render_template("customer_signup.html",error_message="")
    if request.method=="POST":
        Fname=request.form.get("fname")   #variable can be anything
        Lname=request.form.get("lname")   
        Phone=request.form.get("phone")   
        Address=request.form.get("address")   
        Pincode=request.form.get("pincode")   
        username=request.form.get("username")   
        password1=request.form.get("password")   
        Role=3
        action="True"
        jdate=datetime.now()
        new=User.query.filter_by(username=username,password=password1).first()
        if new:
            return render_template("customer_signup.html",error_message="Username already exists!")
        else:
            new_user1=User(username=username,password=password1,role=Role)
            new_user2=Customer(username=username,fname=Fname,lname=Lname,phone=Phone,address=Address,pincode=Pincode,jdate=jdate,action=action)
            db.session.add(new_user1)
            db.session.add(new_user2)
            db.session.commit()
            return render_template("login.html",success_message="Registration Successful! LOGIN TO CONTINUE :)",error_message="")


@app.route("/professional_signup",methods=["GET","POST"])
def professional_signup():
    if request.method=="GET":
        services=getservices()
        return render_template("professional_signup.html",services=services,error_message="")
    if request.method=="POST":
        Fname=request.form.get("fname")   
        Lname=request.form.get("lname")   
        Phone=request.form.get("phone")  
        username=request.form.get("username")   
        password1=request.form.get("password")  
        Address=request.form.get("address")   
        pincode=request.form.get("pincode")   
        servexp=request.form.get("servexp")  
        service1=Services.query.filter_by(servexp=servexp).first()
        Exp=request.form.get("exp")   
        Role=2
        action="Under Verification"
        #doc_upload
        file=request.files["docs"]
        doc_url=""
        if file.filename:
            resume=secure_filename(file.filename)
            doc_url = os.path.join("./uploads", resume+"_"+username)   
            file.save(doc_url)
        #-----------------------  
        new1=User.query.filter_by(username=username,password=password1).first()
        if new1:
            return render_template("professional_signup.html",error_message="Username already exists!")
        else:
            new_user1=User(username=username,password=password1,role=Role)
            new_user2=Professional(username=username,fname=Fname,lname=Lname,phone=Phone,address=Address,serv_id=service1.serv_id,exp=Exp,docs=doc_url,pincode=pincode,action=action)
            db.session.add(new_user1)
            db.session.add(new_user2)
            db.session.commit()
            return render_template("login.html",success_message="Registration Successful! LOGIN TO CONTINUE :)",error_message="")



"""---------------------------------------------------ADMIN ROUTES-------------------------------------------------------------"""



@app.route("/new_service", methods=["GET","POST"])
def new_service():
    if request.method=="GET":
        return render_template("new_service.html")
    if request.method=="POST":
        servexp=request.form.get("servexp")   #variable can be anything
        description=request.form.get("description")   
        base_price=request.form.get("base_price")
        new_servicee=Services.query.filter_by(servexp=servexp).first()
        if new_servicee:
            return render_template("new_service.html",error_message="Service already exists!")
        else:
            new_service=Services(servexp=servexp,description=description,base_price=base_price)
            db.session.add(new_service)
            db.session.commit()
            return redirect(url_for("admin",success_message="New Service Created!"))
        

@app.route("/search",methods=["GET","POST"])
def search():
    services=getservices()
    if request.method=="GET":
        return redirect(url_for("admin"))
    if request.method=="POST":
        search=request.form.get("search")
        serv_srch=service_search(search)        
        cust_srch=customer_search(search)
        pincode_srch=pincode_search(search)   
        if serv_srch:
            return render_template("admin_service_search.html",services=serv_srch) 
        elif cust_srch:
            return render_template("admin_customer_search.html",customer=cust_srch) 
        elif pincode_srch:
            return render_template("admin_pincode_search.html",professional=pincode_srch,services=services) 
        else:
            return render_template("admin_dashb.html", services=None,professional=None,customer=None,service_requests=None)
        

@app.route("/edit_service/<serv_id>", methods=["GET","POST"])
def edit_service(serv_id):
    serv=get_service(serv_id)
    if request.method=="GET":
        return render_template("edit_service.html", service=serv,serv_id=serv_id)
        
    if request.method=="POST":
        servexp1=request.form.get("servexp")   #variable can be anything
        description1=request.form.get("description")   
        base_price1=request.form.get("base_price")
        serv.servexp=servexp1
        serv.base_price=base_price1
        serv.description=description1
        db.session.commit()
        return redirect(url_for("admin"))
        
        
@app.route("/delete_service/<serv_id>")
def delete_service(serv_id):
    serv=get_service(serv_id)
    db.session.delete(serv)
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/delete_customer/<cust_id>")
def delete_customer(cust_id):
    cust=get_customer(cust_id)
    user=User.query.filter_by(username=cust.username).first()
    db.session.delete(user)
    db.session.delete(cust)
    db.session.commit()
    return redirect(url_for("admin"))

@app.route("/delete_professional/<prof_id>")
def delete_professional(prof_id):
    prof=get_professional(prof_id)
    os.remove(prof.docs)
    user=User.query.filter_by(username=prof.username).first()
    db.session.delete(user)
    db.session.delete(prof)
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/approval/<prof_id>")
def approval(prof_id):
    prof=get_professional(prof_id)
    if prof.action=="Under Verification":
        prof.action="True"
        db.session.commit()
        return redirect(url_for("admin"))
    


@app.route("/admin_summary")
def admin_summary():    
    admn_summary=plot_admin_summary()
    admn_summary.savefig("./static/admin_summary.jpeg")
    plot.clf()
    plot.switch_backend('agg')
    return render_template("admin_summary.html")





"""---------------------------------------------------CUSTOMER ROUTES---------------------------------------------------------"""


@app.route("/customer_search/<username>",methods=["GET","POST"])
def customer_search(username):
    professional=getprofessionals()
    customer=Customer.query.filter_by(username=username).first()  
    services=getservices()
    if request.method=="GET":
        return redirect(url_for("customer",username=username))
    if request.method=="POST":
        search=request.form.get("search")
        serv_srch=service_search(search) 
        req_srch=request_search(search)   
        if serv_srch:
            return render_template("customer_service_search.html",username=username,services=serv_srch,cust_id=customer.cust_id) 
        elif req_srch:
            return render_template("customer_req_search.html",username=username,service_requests=req_srch,professional=professional,services=services,cust_id=customer.cust_id)
        else:
            return render_template("customer_dashb.html", username=username,services=None,service_requests=None,cust_id=customer.cust_id)
        

@app.route("/customer_profile/<cust_id>/<username>", methods=["GET","POST"])
def customer_profile(cust_id,username):
    cust=get_customer(cust_id)
    user=User.query.filter_by(username=username).first()
    if request.method=="GET":
        return render_template("customer_profile.html",username=username,password=user.password,customer1=cust,cust_id=cust_id)
        
    if request.method=="POST":
        Fname=request.form.get("fname")   #variable can be anything
        Lname=request.form.get("lname")   
        Phone=request.form.get("phone")   
        Address=request.form.get("address")   
        Pincode=request.form.get("pincode")     
        password=request.form.get("password")
        cust.fname=Fname
        cust.lname=Lname
        cust.phone=Phone
        cust.address=Address
        cust.pincode=Pincode
        cust.password=password
        db.session.commit()
        return redirect(url_for("customer", username=username))        



@app.route("/more_services/<username>")
def more_services(username):
    services=getservices()
    customer=Customer.query.filter_by(username=username).first()
    return render_template("more_services.html",username=username,cust_id=customer.cust_id,services=services)



@app.route("/book_service/<servexp>/<username>",methods=["GET","POST"])
def book_service(servexp,username):
    if request.method=="GET":
        return render_template("customer_dashb.html",username=username)
    if request.method=="POST":
        customer=Customer.query.filter_by(username=username).first()
        service=Services.query.filter_by(servexp=servexp).first()
        rdate=datetime.now()
        base_price=service.base_price
        action="Requested"
        prof_id=None
        request1=Service_Requests(cust_id=customer.cust_id,serv_id=service.serv_id,rdate=rdate,action=action,prof_id=prof_id,base_price=base_price)
        db.session.add(request1)
        db.session.commit()
        return redirect(url_for("customer",username=username))



@app.route("/close/<request_id>/<username>",methods=["GET","POST"])
def close(request_id,username):
    if request.method=="GET":
        return render_template("feedback.html",request_id=request_id,username=username)
    if request.method=="POST":
        request1=Service_Requests.query.filter_by(request_id=request_id).first()
        rating=request.form.get("rating")
        review=request.form.get("review")
        request1.serv_rating=rating
        request1.serv_review=review
        request1.cdate=datetime.now()
        request1.action="Closed"
        db.session.commit()
        return redirect(url_for("customer",username=username))



@app.route("/customer_summary/<username>")
def customer_summary(username):  
    customer=Customer.query.filter_by(username=username).first()  
    cust_summary=plot_customer_summary(username)
    cust_summary.savefig("./static/customer/"+username+"customer_summary.jpeg")
    plot.clf()
    plot.switch_backend('agg')
    return render_template("customer_summary.html",username=username,cust_id=customer.cust_id)
   



"""--------------------------------------------------PROFESSIONAL ROUTES-------------------------------------------------------"""


@app.route("/professional_search/<username>",methods=["GET","POST"])
def professional_search(username):
    prof=Professional.query.filter_by(username=username).first()
    professional=getprofessionals()
    customers=getcustomers()
    if request.method=="GET":
        return redirect(url_for("professional",username=username))
    if request.method=="POST":
        search=request.form.get("search")
        req_srch=prof_request_search(search,username)   
        if req_srch:
            return render_template("professional_service_search.html",professional=professional,prof_id=prof.prof_id,username=username,customers=customers,prof_service_requests=req_srch)
        else:
            return render_template("professional_service_search.html",prof_id=prof.prof_id, username=username)


@app.route("/professional_profile/<prof_id>/<username>", methods=["GET","POST"])
def professional_profile(prof_id,username):
    prof=get_professional(prof_id)
    user=User.query.filter_by(username=username).first()
    serv_id=prof.serv_id
    service=get_service(serv_id)
    if request.method=="GET":
        return render_template("professional_profile.html",username=username,password=user.password,servexp=service.servexp,prof=prof,prof_id=prof_id)
        
    if request.method=="POST":
        fname=request.form.get("fname")   #variable can be anything
        lname=request.form.get("lname")   
        phone=request.form.get("phone")   
        address=request.form.get("address")   
        pincode=request.form.get("pincode")     
        password=request.form.get("password")
        exp=request.form.get("exp")
        prof.fname=fname
        prof.lname=lname
        prof.phone=phone
        prof.address=address
        prof.pincode=pincode
        prof.password=password
        prof.exp=exp
        db.session.commit()
        return redirect(url_for("professional", username=username))
    

@app.route("/accept/<request_id>/<username>")
def accept(request_id,username):
    serv_req=get_req(request_id)
    professional=Professional.query.filter_by(username=username).first()
    active = Service_Requests.query.filter_by(prof_id=professional.prof_id, action="In Process").first()
    if active:
        serv_id=professional.serv_id
        service_requests=get_service_req(serv_id)
        prof_service_requests=Service_Requests.query.filter_by(prof_id=professional.prof_id).all()
        customers=getcustomers()
        return render_template("professional_dashb.html",active=active,professional=professional,username=username,customers=customers,prof_service_requests=prof_service_requests,service_requests=service_requests,prof_id=professional.prof_id)

    if serv_req.action=="Requested" and username not in serv_req.req_rejected:
        serv_req.action="In Process"
        serv_req.prof_id=professional.prof_id
        db.session.commit()
        return redirect(url_for("professional",username=username))
    

@app.route("/rejected/<request_id>/<username>")
def rejected(request_id,username):
    serv_req=get_req(request_id)
    if not serv_req.req_rejected:
        serv_req.req_rejected = []
    if serv_req.action=="Requested":
        serv_req.req_rejected.append(username) 
        db.session.commit()
        return redirect(url_for("professional",username=username))   
   


@app.route("/close_1/<request_id>/<username>",methods=["GET","POST"])
def close_1(request_id,username):
    if request.method=="GET":
        return render_template("feedback_1.html",request_id=request_id,username=username)
    if request.method=="POST":
        request1=Service_Requests.query.filter_by(request_id=request_id).first()
        rating=request.form.get("rating")
        request1.cust_rating=rating
        request1.action="Closed"
        db.session.commit()
        return redirect(url_for("professional",username=username))



@app.route("/professional_summary/<username>")
def professional_summary(username):  
    professional=Professional.query.filter_by(username=username).first()  
    prof_summary=plot_professional_summary(username)
    prof_summary.savefig("./static/professional/"+username+"professional_summary.jpeg")
    plot.clf()
    plot.switch_backend('agg')
    return render_template("professional_summary.html",username=username,prof_id=professional.prof_id)



    
    

""""------------------------------------------------Other Supporting Functions--------------------------------------------- """ 





#get all entries in the services table
def getservices():
    services=Services.query.all()
    return services

def getprofessionals():
    professionals=Professional.query.all()
    return professionals

def getcustomers():
    customers=Customer.query.all()
    return customers

def getrequests():
    requests=Service_Requests.query.all()
    return requests


#search a particular service based on a part of its name, irrespective of its case
def service_search(search):
    services=Services.query.filter(Services.servexp.ilike(f"%{search}%")).all() #ilike makes the search var case insenitive and dbms query ilike is used
    return services

def professional_search(search):
    professional=Professional.query.filter(Professional.fname.ilike(f"%{search}%")).all()
    return professional

def customer_search(search):
    customer=Customer.query.filter(Customer.fname.ilike(f"%{search}%")).all()
    return customer

def pincode_search(search):
    professional=Professional.query.filter(Professional.pincode.ilike(f"%{search}%")).all()
    return professional

def request_search(search):
    requests=Service_Requests.query.filter(Service_Requests.action.ilike(f"%{search}%")).all() 
    return requests

def prof_request_search(search,username):
    professional=Professional.query.filter_by(username=username).first()
    requests=Service_Requests.query.filter(Service_Requests.action.ilike(f"%{search}%")).all() 
    prof_requests=[req for req in requests if req.prof_id== professional.prof_id]
    return prof_requests

#to get all detials of a particular service through its id
def get_service(serv_id):
    service=Services.query.filter_by(serv_id=serv_id).first()
    return service

def get_customer(cust_id):
    customer=Customer.query.filter_by(cust_id=cust_id).first()
    return customer

def get_professional(prof_id):
    professional=Professional.query.filter_by(prof_id=prof_id).first()
    return professional

def get_req(request_id):
    request=Service_Requests.query.filter_by(request_id=request_id).first()
    return request

def get_service_req(serv_id):
    services=Service_Requests.query.filter_by(serv_id=serv_id).all()
    return services

def get_cservice_req(cust_id):
    services=Service_Requests.query.filter_by(cust_id=cust_id).all()
    return services

def get_average_crating(cust_id):
    requests=get_cservice_req(cust_id)
    sum=0
    count=0
    for request in requests:
        if request.action=="Closed":
            if request.cust_rating:
                count+=1
                sum+=request.cust_rating
    if count==0:
        avg=None
    else:
        avg=(sum/count)   
    return avg        

def get_average_prating(prof_id):
    requests=Service_Requests.query.filter_by(prof_id=prof_id).all()
    sum=0
    count=0
    for request in requests:
        if request.action=="Closed":
            count+=1
            sum+=int(request.serv_rating)
    if count==0:
        avg=None
    else:
        avg=(sum/count)   
    return avg 


def plot_admin_summary():
    services=getservices()
    summary={}
    for service in services:
        summary[service.servexp]=len(service.professionals)
    service_name=list(summary.keys())
    no_of_prof=list(summary.values())
    plot.bar(service_name,no_of_prof,color='darkblue',width=0.5)
    plot.title("Services/Service Professionals")
    plot.xlabel("Service Names")
    plot.ylabel("Number of Service Professionals per Service")
    return plot

def plot_customer_summary(username):
    customer=Customer.query.filter_by(username=username).first()
    service_requests=get_cservice_req(customer.cust_id)
    summary={"Requested":0,"In Process":0,"Closed":0}   
    for req in service_requests:
        if req.action in summary.keys():
            summary[req.action]+=1  
    action_status=list(summary.keys())
    number_req=list(summary.values())
    plot.bar(action_status,number_req,color='darkblue',width=0.5)
    plot.title("Service Requests/Ongoing/History")
    plot.xlabel("Service Request Status")
    plot.ylabel("Number of Requests per Status")
    return plot


def plot_professional_summary(username):
    professional=Professional.query.filter_by(username=username).first()
    requested=Service_Requests.query.filter_by(serv_id=professional.serv_id,action="Requested").all()
    service_requests=Service_Requests.query.filter_by(prof_id=professional.prof_id).all()
    summary={"Requested":0,"In Process":0,"Closed":0}  
    for req1 in requested:
        if professional.username not in req1.req_rejected and req1.action in summary.keys():
            summary[req1.action]+=1
    for req in service_requests:
        if req.action in summary.keys():
            summary[req.action]+=1  
    action_status=list(summary.keys())
    number_req=list(summary.values())
    plot.bar(action_status,number_req,color='darkblue',width=0.5)
    plot.title("Service Requests/Ongoing/History")
    plot.xlabel("Service Request Status")
    plot.ylabel("Number of Requests per Status")
    return plot