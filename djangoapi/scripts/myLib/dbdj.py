from django.forms.models import model_to_dict

class DbDjango():
    def select(self,model,dict,asDict):
        try:
            if asDict:
                b = model.objects.filter(id=dict['id']).first()
            else:
                b = model.objects.filter(id=dict['id']).values_list().first()

            if b:
                if asDict:
                    data = [model_to_dict(b)]
                else:
                    data = [b]

                d = {"ok": True,
                    "message": "Data retrieved",
                    "data": data}
            else:
                d = {"ok":False,
                    "message":"No row found with that id",
                    "data":None}
            print(d)
            return d
        except Exception as e:
                d = {"ok": False,
                    "message": str(e),
                    "data": None}
                print(d)
                return d
    
    def selectallAsDicts(self,model):
        l=model.objects.all()
        data=[]
        for b in l:
            dict=model_to_dict(b)
            data.append(dict)
        d = {'ok':True, 'message': 'Data retrieved', 'data': data}
        print(d)
        return d

    def delete(self,model,dict):
        try:
            b = model.objects.filter(id=dict['id']).first()
            if b:
                b.delete()
                d = {"ok": True,
                    "message": "Data deleted",
                    "data": [{"rows_deleted": 1}]}
            else:
                d = {"ok":False,
                    "message":"No row found with that id",
                    "data":None}
            print(d)
            return d
        except Exception as e:
            d = {"ok": False,
                "message": str(e),
                "data": None}
            print(d)
            return d   


