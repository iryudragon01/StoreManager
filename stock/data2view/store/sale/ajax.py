import json
from stock.data2view.user import action,queries

def SaleEnableButton(request,worker):
    if 'verifypwd' in request.POST:
        verifypwd = request.POST['verifypwd']
        if worker.password == action.hash_pwd(verifypwd):
            worker.enable_sale=True
            worker.save()
            return {'enableBTN':'Enable','class':'btn-outline-success','value':'1'}
        else: 
            worker.enable_sale=False
            worker.save()
            return {'enableBTN':'Disable','class':'btn-outline-secondary','value':'0','message':'wrong password'}    
    if 'enableBTN' in request.POST:
            worker.enable_sale=False
            worker.save()
            return {'enableBTN':'Disable','class':'btn-outline-secondary','value':'0','message':'disalbe success'}    
    
