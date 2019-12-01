from django.shortcuts import redirect,HttpResponse
from stock.data2view.user import action,queries

class ReferMiddleWare:
    def __init__(self,get_response):

        self.get_response = get_response

    def __call__(self,request):
        # check permission to access store
        subPath = request.path.split('/')
        print(subPath)
        if len(subPath) >= 3:
            if subPath[1] == 'store':
                if 'url' in request.session:
                    if subPath[2]!=request.session['url']:
                        return redirect('stock:logout_worker',url=request.session['worker'])
                    if not action.is_worker_genius(request,request.session['url']):
                        return redirect('stock:logout_worker',url=request.session['worker'])
                else:
                    if queries.is_url_exists(subPath[2]):
                        return redirect('stock:login_worker',url=subPath[2])
                    else:
                        res = redirect('stock:search_store')    
                        res['location'] +='?url='+subPath[2]
                        return res



        response = self.get_response(request )

        return response   