from django.db.models.functions import Coalesce
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.contrib import auth
from .models import Item, Sr, Customer, Supplier, Memo, SaleItem, PurchaseItem , PurchaseMemo

from django.db.models import Sum, Avg,Count

from django.contrib.auth import logout
from datetime import datetime

#---------------------------------------------

def logout_view(request):
    logout(request)

    return HttpResponseRedirect('/login')

#-------------------- login management --------------
def show_login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home')

    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def auth_method(request):
    username = request.POST.get('username', '')

    password = request.POST.get('password', '')
    value = request.POST.get('Select1')


    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)

        if value == 'Administrator':
            return HttpResponseRedirect("/admin")
        elif value == 'User':
            return HttpResponseRedirect("/home")



    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)
#-----------------------user authienticate method end


#------------------------------home page-------------
def show_home_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')


    c = {}
    c.update(csrf(request))
    return render_to_response('home.html', c)



#--------------------- item ------------------

def show_item_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')


    c = {}
    c.update(csrf(request))
    return render_to_response('item.html', c)

def show_item_add_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    #------------------- Add part --------------------------
    if request.POST.get('btnAdd'):
        name = request.POST.get('name', '')
        size = request.POST.get('size', '')
        stock_rate = request.POST.get('stock_rate', '')
        sale_rate = request.POST.get('sale_rate', '')

        obj = Item(name=name, size=size, stock_rate=float(stock_rate), sale_rate=float(sale_rate))

        obj.save();

        return HttpResponseRedirect("/item/add/")


    #------------------------- search part---------------
    if request.POST.get('Search_button'):

        type = request.POST.get('stype', '')
        value = request.POST.get('value', '')

        print(type)

        if value == '':
            obj = Item.objects.all
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_add.html', c)

        if type == 'ID':
            value = request.POST.get('value', '-1')
            try:
                value = int(value)
            except:
                return  HttpResponseRedirect('/item/add/')

            obj = Item.objects.filter(id=int(value))
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_add.html', c)

        if type == 'Name':
            obj = Item.objects.filter(name__icontains=value)
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_add.html', c)

        if type == 'Size':
            obj = Item.objects.filter(size__icontains=value)
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_add.html', c)

        # default return -----------
        c = {}
        c.update(csrf(request))
        return render_to_response('item_add.html', c)



    c = {}
    c.update(csrf(request))
    return render_to_response('item_add.html', c)









def show_item_delete_page(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')


#---------------------- for  delete------------
    if request.POST.get('Delete_button'):
        id = request.POST.get('slctId', '')

        if id == '':
            print('invalid')
        else:
            Item.objects.filter(id=id).delete()
            #print(id)
            return HttpResponseRedirect('/item/delete/')






        #------------------------- for search----------------------

    if request.POST.get('Search_button'):

        type = request.POST.get('stype', '')
        value = request.POST.get('value', '')

        #print(type)

        if value == '':
            obj = Item.objects.all
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_delete.html', c)

        if type == 'ID':
            value = request.POST.get('value', '-1')
            print(value)
            obj = Item.objects.filter(id=int(value))
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_delete.html', c)

        if type == 'Name':
            obj = Item.objects.filter(name__icontains=value)
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_delete.html', c)

        if type == 'Size':
            obj = Item.objects.filter(size__icontains=value)
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_delete.html', c)

        # default return -----------
        c = {}
        c.update(csrf(request))
        return render_to_response('item_add.html', c)



    item = Item.objects.filter(id=-1)
    c = {'Item': item}
    c.update(csrf(request))
    return render_to_response('item_delete.html', c)



def show_item_edit_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.POST.get('Save_button'):
        id = request.POST.get('Id_value', '')
        obj = Item.objects.filter(id=int(id)).get()
        obj.name = request.POST.get('Name', '')
        obj.size = request.POST.get('Size', '')
        obj.stock_rate = float(request.POST.get('Stock_rate', ''))
        obj.sale_rate = float(request.POST.get('Sale_rate', ''))
        obj.save()
        c = {'Item': Item.objects.all(), 'SUCCESS_EDIT':'true',}
        c.update(csrf(request))
        return render_to_response('item_edit.html', c)

    if request.POST.get('Edit_button'):
        item_id= request.POST.get('Select_id','')
        if item_id=='':
            return HttpResponseRedirect('/item/edit')

        obj = Item.objects.filter(id=int(item_id)).get()
        if obj.id:
            c = {'obj': obj,'EDIT':'true',}
            c.update(csrf(request))
            return render_to_response('item_edit.html', c)





    if request.POST.get('Search_button'):

        type = request.POST.get('stype', '')
        value = request.POST.get('value', '')

        #print(type)

        if value == '':
            obj = Item.objects.all
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_edit.html', c)

        if type == 'ID':
            value = request.POST.get('value', '-1')
            print(value)
            obj = Item.objects.filter(id=int(value))
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_edit.html', c)

        if type == 'Name':
            obj = Item.objects.filter(name__icontains=value)
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_edit.html', c)

        if type == 'Size':
            obj = Item.objects.filter(size__icontains=value)
            if obj is not None:
                c = {'Item': obj}
                c.update(csrf(request))
                return render_to_response('item_edit.html', c)

        # default return -----------
        c = {}
        c.update(csrf(request))
        return render_to_response('item_edit.html', c)





    c = {'Item':Item.objects.all()}
    c.update(csrf(request))
    return render_to_response('item_edit.html', c)


#----------------------------------------item finish---------------------------


#-----------------------------supplier and customer---------------------

def show_sc_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    c = {}
    c.update(csrf(request))
    return render_to_response('sc.html', c)

def show_sc_add_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

#-------------------------- add -------------------------------
    if request.POST.get('Add_button'):
        s = request.POST.get('Sr', '')
        a, b = s.split(':')
        print(int(a))

        name = request.POST.get('Name', '')
        address = request.POST.get('Address', '')
        mobile_no = request.POST.get('Mobile_no', '')
        sr = Sr.objects.get(id=int(a))
        type = request.POST.get('Type', '')

        if type == 'Customer':
            obj = Customer(name=name, address=address, mobile_no=mobile_no, sr=sr)
            obj.save()

        if type == 'Supplier':
            obj = Supplier(name=name, address=address, mobile_no=mobile_no, sr=sr)
            obj.save()

        c = {'sr': Sr.objects.all()}
        c.update(csrf(request))
        return render_to_response('sc_add.html', c)




    #-----------------------------search-------------------------
    if request.POST.get('Search_button'):
        type = request.POST.get('stype', '')
        value = request.POST.get('value', '')

        print(type)

        if value == '':
            obj1 = Supplier.objects.all()
            obj2 = Customer.objects.all()
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2, 'sr': Sr.objects.all()}
                c.update(csrf(request))
                return render_to_response('sc_add.html', c)

        if type == 'Name':
            obj1 = Supplier.objects.filter(name__icontains=value)
            obj2 = Customer.objects.filter(name__icontains=value)
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2, 'sr': Sr.objects.all()}
                c.update(csrf(request))
                return render_to_response('sc_add.html', c)

        if type == 'Mobile No':
            obj1 = Supplier.objects.filter(mobile_no__icontains=value)
            obj2 = Customer.objects.filter(mobile_no__icontains=value)
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2, 'sr': Sr.objects.all()}
                c.update(csrf(request))
                return render_to_response('sc_add.html', c)

        if type == 'Show All':
            obj1 = Supplier.objects.all()
            obj2 = Customer.objects.all()
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2, 'sr': Sr.objects.all()}
                c.update(csrf(request))
                return render_to_response('sc_add.html', c)

        c = {}
        c.update(csrf(request))
        return render_to_response('sc_add.html', c)




    c = {'sr':Sr.objects.all()}
    c.update(csrf(request))
    return render_to_response('sc_add.html', c)


def show_sc_delete_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

#------------------------------delete ---------------------------
    if request.POST.get('Delete_button'):
        strng = request.POST.get('id', '')
        a, b = strng.split('_')

        if a == 'S':
            Supplier.objects.filter(id=int(b)).delete()
        if a == 'C':
            Customer.objects.filter(id=int(b)).delete()





    #---------------------------------------search---------------------------
    if request.POST.get('Search_button'):
        type = request.POST.get('stype', '')
        value = request.POST.get('value', '')

        print(type)

        if value == '':
            obj1 = Supplier.objects.all()
            obj2 = Customer.objects.all()
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2, 'sr': Sr.objects.all()}
                c.update(csrf(request))
                return render_to_response('sc_delete.html', c)

        if type == 'Name':
            obj1 = Supplier.objects.filter(name__icontains=value)
            obj2 = Customer.objects.filter(name__icontains=value)
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2, 'sr': Sr.objects.all()}
                c.update(csrf(request))
                return render_to_response('sc_delete.html', c)

        if type == 'Mobile No':
            obj1 = Supplier.objects.filter(mobile_no__icontains=value)
            obj2 = Customer.objects.filter(mobile_no__icontains=value)
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2, 'sr': Sr.objects.all()}
                c.update(csrf(request))
                return render_to_response('sc_delete.html', c)

        if type == 'Show All':
            obj1 = Supplier.objects.all()
            obj2 = Customer.objects.all()
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2, 'sr': Sr.objects.all()}
                c.update(csrf(request))
                return render_to_response('sc_delete.html', c)

        c = {}
        c.update(csrf(request))
        return render_to_response('sc_delete.html', c)

    c = {'supplier':Supplier.objects.all, 'customer': Customer.objects.all()}
    c.update(csrf(request))
    return render_to_response('sc_delete.html', c)
def show_sc_edit_page(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
#------------------------ edit select ------------------------

    if request.POST.get('Select_button'):
        t,id= request.POST.get('Select_id','-').split('_')

        if t=='S':

            obj = Supplier.objects.filter(id=int(id)).get()
            type = 'S_'

            c = {'supplier': Supplier.objects.all(), 'customer': Customer.objects.all(), 'sr': Sr.objects.all(),
                 'type': type, 'obj': obj, 'DEFAULT': 'Supplier', 'EDIT':'true', }
            c.update(csrf(request))
            return render_to_response('sc_edit.html', c)

        if t == 'C':
            obj = Customer.objects.filter(id=int(id)).get()
            type = 'C_'

            c = {'supplier': Supplier.objects.all(), 'customer': Customer.objects.all(), 'sr': Sr.objects.all(),
                 'type': type, 'obj': obj, 'DEFAULT': 'Customer', 'EDIT': 'true', }
            c.update(csrf(request))
            return render_to_response('sc_edit.html', c)


#-----------------------edit save--------------------------------

    if request.POST.get('Save_button'):
        t, id = request.POST.get('Id', '').split('_')

        if t == 'C':
            obj = Customer.objects.filter(id=int(id)).get()

            obj.name = request.POST.get('Name', '')
            obj.address = request.POST.get('Address', '')
            obj.mobile_no = request.POST.get('Mobile_no', '')
            a, b = request.POST.get('Sr', '').split(':')
            obj.sr = Sr.objects.filter(id=int(a)).get()

            type = request.POST.get('Type', '')
            if type == 'Customer':
                obj.save()
            else:
                Supplier.objects.create(name=obj.name, address=obj.address, mobile_no=obj.mobile_no, sr=obj.sr)
                Customer.objects.filter(id=obj.id).delete()

        if t == 'S':
            obj = Supplier.objects.filter(id=int(id)).get()

            obj.name = request.POST.get('Name', '')
            obj.address = request.POST.get('Address', '')
            obj.mobile_no = request.POST.get('Mobile_no', '')
            a, b = request.POST.get('Sr', '').split(':')
            obj.sr = Sr.objects.filter(id=int(a)).get()
            type = request.POST.get('Type', '')

            if type == 'Supplier':

                obj.save()
            else:
                Customer.objects.create(name=obj.name, address=obj.address, mobile_no=obj.mobile_no, sr=obj.sr)
                Supplier.objects.filter(id=obj.id).delete()

        c = {'supplier': Supplier.objects.all(), 'customer': Customer.objects.all(), 'sr': Sr.objects.all()}
        c.update(csrf(request))
        return render_to_response('sc_edit.html', c)

    #----------------------- search ----------------------------
    if request.POST.get('Search_button'):
        type = request.POST.get('stype', '')
        value = request.POST.get('value', '')

        print(type)

        if type == 'Name':
            obj1 = Supplier.objects.filter(name__icontains=value)
            obj2 = Customer.objects.filter(name__icontains=value)
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2}
                c.update(csrf(request))
                return render_to_response('sc_edit.html', c)

        if type == 'Mobile No':
            obj1 = Supplier.objects.filter(mobile_no__icontains=value)
            obj2 = Customer.objects.filter(mobile_no__icontains=value)
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2}
                c.update(csrf(request))
                return render_to_response('sc_edit.html', c)

        if type == 'Show All':
            obj1 = Supplier.objects.all()
            obj2 = Customer.objects.all()
            if obj1 is not None and obj2 is not None:
                c = {'supplier': obj1, 'customer': obj2}
                c.update(csrf(request))
                return render_to_response('sc_edit.html', c)


    c = {'supplier':Supplier.objects.all(), 'customer':Customer.objects.all(),'sr':Sr.objects.all()}
    c.update(csrf(request))
    return render_to_response('sc_edit.html', c)


#----------------------------- sale--------------------------------------

def sale_page_load(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    c = {}
    c.update(csrf(request))
    return render_to_response('sale.html', c)



def sale_add_page_load(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.POST.get('Select_button'):
        str= request.POST.get('Select_party')
        if str=='-':
            return HttpResponseRedirect('/sale/sale_add')

        id = request.POST.get('Select_party','0--').split('-')
        obj = Customer.objects.filter(id=int(id[0])).get()

        c = {'CUSTOMER': obj, 'SELECTED':'true', }
        c.update(csrf(request))
        return render_to_response('sale_add.html', c)

    elif request.POST.get('Confirm_button'):
        c_id, c_name = request.POST.get('Select_party', '').split('-')
        customer = Customer.objects.filter(id=int(c_id)).get()
        dd,mm,yy = request.POST.get('Date').split('/')
        date = yy+'-'+mm+'-'+dd
        obj = Memo(party=customer, date=date)
        obj.save()

        dt = request.POST.get('Date')


        all_item = Item.objects.all

        c = {'SALE_OBJ': obj,
             'ALLITEM': all_item,
             'SELECTED':'true',
             'DATE':dt,
             }
        c.update(csrf(request))
        return render_to_response('sale_add.html', c)

    elif request.POST.get('Add_item_button'):
        id = request.POST.get('Memo_no', '')
        objMemo = Memo.objects.filter(id=int(id)).get()

        item_id, item_name, item_size = request.POST.get('Select_item', '').split('-')
        selected_item = Item.objects.filter(id=int(item_id)).get()

        quantity = request.POST.get('Unit', '0')
        free = request.POST.get('Free', '0')

        objSaleItem = SaleItem(quantity=quantity, free=free, item=selected_item)
        objSaleItem.save()
        objMemo.sale_item.filter(item=objSaleItem.item).delete()
        objMemo.sale_item.add(objSaleItem)

        objMemo.save()
        total = objMemo.get_total

        allitem = Item.objects.all

        dt = objMemo.date.strftime("%d/%m/%Y")
        c = {'SALE_OBJ': objMemo,
             'ALLITEM': allitem,
             'TOTAL': total,
             'GRAND_TOTAL':total,
             'PAID':'0',
             'DUE':'0',
             'DISCOUNT':'0',
             'SELECTED':'true',
             'DATE':dt,}
        c.update(csrf(request))
        return render_to_response('sale_add.html', c)

    elif request.POST.get('Save_memo_button'):
        id = request.POST.get('Memo_no', '')
        objMemo = Memo.objects.filter(id=int(id)).get()
        objMemo.paid = request.POST.get('Paid')
        objMemo.discount = request.POST.get('Discount')
        objMemo.save()

        total = objMemo.get_total()
        paid= objMemo.paid
        discount = objMemo.discount
        grand_total=(int(total)-int(discount))
        due=(int(total) - int(discount) - int(paid))

        dt = objMemo.date.strftime("%d/%m/%Y")


        c = {'SALE_OBJ': objMemo,
             'TOTAL': total,
             'GRAND_TOTAL':grand_total,
             'PAID':paid,
             'DISCOUNT': discount,
             'DUE':due ,
             'SELECTED': 'true',
             'PRINT': 'true',
             'DATE': dt,
             }
        c.update(csrf(request))
        return render_to_response('sale_add.html', c)

    elif request.POST.get('Print_memo_button'):
        return HttpResponse('Under construction')





    elif not request.POST.get('Memo_no', '')=='':
        id = request.POST.get('Memo_no', '')
        objMemo = Memo.objects.filter(id=int(id)).get()
        item_name, item_size = request.POST.get('Select_item', '').split('-')
        item = Item.objects.filter(name=item_name, size=item_size).get()

        total = objMemo.get_total

        all_item = Item.objects.all

        dt = objMemo.date.strftime("%d/%m/%Y")

        c = {'SALE_OBJ': objMemo,
             'CURRENT_ITEM': item,
             'ALLITEM': all_item,
             'TOTAL': total,
             'SELECTED':'true',
             'ITEM_SELECTED':'true',
             'DATE':dt,
             }
        c.update(csrf(request))
        return render_to_response('sale_add.html', c)

    c = {'party':Customer.objects.all(),}
    c.update(csrf(request))
    return render_to_response('sale_add.html', c)


def sale_edit_delete(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.POST.get('Edit_button'):

        id = request.POST.get('Select_memo')
        if  id == 'null':
            return HttpResponseRedirect('/sale/sale_edit_delete/')

        memo_obj = Memo.objects.get(id=int(id))

        #error handled
        if not memo_obj:
            return HttpResponseRedirect('/sale/sale_edit_delete/')



        all_sale_obj = Memo.objects.all

        total = memo_obj.get_total()
        gt =int(total) - int(memo_obj.discount)
        due = gt - memo_obj.paid

        dt=memo_obj.date.strftime("%d/%m/%Y")

        customer = Customer.objects.all()
        item = Item.objects.all()
        c = {'ITEM': item,
             'SALE_OBJ': memo_obj,
             'ALL_SALE_OBJ': all_sale_obj,
             'CUSTOMER': customer,
             'EDIT': 'true',
             'TOTAL': memo_obj.get_total,
             'GT': gt,
             'DUE': due,
             'DATE': dt,


             }
        c.update(csrf(request))
        return render_to_response('sale_edit_delete.html', c)


    elif request.POST.get('Save_head_button'):
        id= request.POST.get('Memo_no')
        if id =='':
            return HttpResponse('error')

        memo_obj = Memo.objects.get(id=int(id))

        customer_id = request.POST.get('Party', '').split('-')

        dd, mm, yy = request.POST.get('Date').split('/')
        date_got = yy + '-' + mm + '-' + dd

        memo_obj.party = Customer.objects.get(id=int(customer_id[0]))
        memo_obj.date = date_got
        memo_obj.save()

        all_sale_obj = Memo.objects.all

        gt = memo_obj.get_total() - memo_obj.discount
        due = gt - memo_obj.paid

        #dt = memo_obj.date.strftime("%d/%m/%Y")
        dt=request.POST.get('Date')


        customer = Customer.objects.all()
        item = Item.objects.all()
        c = {'ITEM': item,
             'SALE_OBJ': memo_obj,
             'ALL_SALE_OBJ': all_sale_obj,
             'CUSTOMER': customer,
             'EDIT': 'true',
             'TOTAL': memo_obj.get_total(),
             'GT': gt,
             'DUE': due,
             'DATE': dt,
             }
        c.update(csrf(request))
        return render_to_response('sale_edit_delete.html', c)


    elif request.POST.get('Add_item_button') or request.POST.get('Save_item_button'):

        id = request.POST.get('Memo_no')
        objMemo = Memo.objects.filter(id=int(id)).get()

        item_id= request.POST.get('Select_item', '').split('-')
        selected_item = Item.objects.filter(id=int(item_id[0])).get()

        quantity = request.POST.get('Unit', '')
        free = request.POST.get('Free', '')

        objSaleItem = SaleItem(quantity=int(quantity), free=int(free), item=selected_item)
        objSaleItem.save()

        objMemo.sale_item.filter(item=objSaleItem.item).delete()
        objMemo.sale_item.add(objSaleItem)

        objMemo.save()

        customer = Customer.objects.all()
        item = Item.objects.all()
        all_sale_obj = Memo.objects.all
        gt = objMemo.get_total() - objMemo.discount
        due = gt - objMemo.paid

        dt = objMemo.date.strftime("%d/%m/%Y")


        c = {
            'ITEM': item,
            'SALE_OBJ': objMemo,
            'ALL_SALE_OBJ': all_sale_obj,
            'CUSTOMER': customer,
            'EDIT': 'true',
            'TOTAL': objMemo.get_total(),
            'GT': gt,
            'DUE': due,
            'DATE':dt,
        }
        c.update(csrf(request))
        return render_to_response('sale_edit_delete.html', c)


    elif request.POST.get('Delete_item_button'):
        id = request.POST.get('Memo_no')
        objMemo = Memo.objects.filter(id=int(id)).get()

        item_id, item_name, item_size = request.POST.get('Select_item', '').split('-')
        selected_item = Item.objects.filter(id=int(item_id)).get()

        quantity = request.POST.get('Unit', '')
        free = request.POST.get('Free', '')

        objSaleItem = SaleItem(quantity=quantity, free=free, item=selected_item)

        objMemo.sale_item.filter(item=objSaleItem.item).delete()

        objMemo.save()

        customer = Customer.objects.all()
        item = Item.objects.all()
        all_sale_obj = Memo.objects.all
        gt = objMemo.get_total() - objMemo.discount
        due = gt - objMemo.paid

        dt = objMemo.date.strftime("%d/%m/%Y")

        c = {

            'ITEM': item,
            'SALE_OBJ': objMemo,
            'ALL_SALE_OBJ': all_sale_obj,
            'CUSTOMER': customer,
            'EDIT': 'true',
            'TOTAL': objMemo.get_total(),
            'GT': gt,
            'DUE': due,
            'DATE':dt,

        }
        c.update(csrf(request))
        return render_to_response('sale_edit_delete.html', c)


    elif request.POST.get('Save_all_button'):
        id = request.POST.get('Memo_no')

        objMemo = Memo.objects.filter(id=int(id)).get()

        discount = request.POST.get('Discount', '')
        paid = request.POST.get('Paid', '')

        objMemo.discount = discount
        objMemo.paid = paid

        objMemo.save()

        all_sale_obj = Memo.objects.all

        c = {'ALL_SALE_OBJ': all_sale_obj}
        c.update(csrf(request))
        return render_to_response('sale_edit_delete.html', c)


    elif request.POST.get('Delete_button'):
        id = request.POST.get('Select_memo')
        if  id == 'null':
            return HttpResponseRedirect('/sale/sale_edit_delete/')
        memo_obj = Memo.objects.get(id=int(id))
        all_sale_obj = Memo.objects.all

        gt = memo_obj.get_total() - memo_obj.discount
        due = gt - memo_obj.paid

        dt = memo_obj.date.strftime("%d/%m/%Y")

        c = {'SALE_OBJ': memo_obj,
             'ALL_SALE_OBJ': all_sale_obj,
             'DELETE': 'true',
             'TOTAL': memo_obj.get_total(),
             'GT': gt,
             'DUE': due,
             'DATE':dt,
        }
        c.update(csrf(request))
        return render_to_response('sale_edit_delete.html', c)


    elif request.POST.get('Print_button'):
        id = request.POST.get('Select_memo')
        if  id == 'null':
            return HttpResponseRedirect('/sale/sale_edit_delete/')
        memo_obj = Memo.objects.get(id=int(id))
        all_sale_obj = Memo.objects.all

        gt = memo_obj.get_total() - memo_obj.discount
        due = gt - memo_obj.paid

        dt = memo_obj.date.strftime("%d/%m/%Y")

        c = {'SALE_OBJ': memo_obj,
             'ALL_SALE_OBJ': all_sale_obj,
             'PRINT': 'true',
             'TOTAL': memo_obj.get_total(),
             'GT': gt,
             'DUE': due,
             'DATE':dt,
        }
        c.update(csrf(request))
        return render_to_response('sale_edit_delete.html', c)


    elif request.POST.get('Delete_confirm_button'):
        id = request.POST.get('Memo_no')
        Memo.objects.filter(id=int(id)).delete()

        return HttpResponseRedirect('/sale/sale_edit_delete/')


    elif request.POST.get('Print_confirm_button'):
        id = request.POST.get('Memo_no')
        # PRINT SHOUD BE DONE HERE

        return HttpResponseRedirect('/sale/sale_edit_delete/')






    else:
        if request.POST.get('Select_item'):

            id = request.POST.get('Memo_no')

            objMemo = Memo.objects.filter(id=int(id)).get()

            item_id, item_name, item_size = request.POST.get('Select_item', '').split('-')

            if item_id == '':

                #not handled
                all_sale_obj = Memo.objects.all
                c = {'ALL_SALE_OBJ': all_sale_obj}
                c.update(csrf(request))
                return render_to_response('sale_edit_delete.html', c)
            else:
                s_item = Item.objects.get(id=int(item_id))

                selected_sale_item = objMemo.sale_item.filter(item=s_item)
                if selected_sale_item:
                    # not new element
                    selected_sale_item = objMemo.sale_item.filter(item=s_item).get()

                    id = request.POST.get('Memo_no')
                    memo_obj = Memo.objects.get(id=int(id))
                    all_sale_obj = Memo.objects.all

                    gt = memo_obj.get_total() - memo_obj.discount
                    due = gt - memo_obj.paid

                    customer = Customer.objects.all()
                    item = Item.objects.all()

                    dt = memo_obj.date.strftime("%d/%m/%Y")

                    c = {'CURRENT_ITEM': s_item,
                         'OLD': 'true',
                         'SALE_ITEM': selected_sale_item,
                         'ITEM': item,
                         'SALE_OBJ': memo_obj,
                         'ALL_SALE_OBJ': all_sale_obj,
                         'CUSTOMER': customer,
                         'EDIT': 'true',
                         'TOTAL': memo_obj.get_total(),
                         'GT': gt,
                         'DUE': due,
                         'DATE':dt,
                         }
                    c.update(csrf(request))
                    return render_to_response('sale_edit_delete.html', c)




                else:

                    #new item

                    id = request.POST.get('Memo_no')
                    memo_obj = Memo.objects.get(id=int(id))
                    all_sale_obj = Memo.objects.all

                    gt = memo_obj.get_total() - memo_obj.discount
                    due = gt - memo_obj.paid

                    customer = Customer.objects.all()
                    item = Item.objects.all()

                    dt = memo_obj.date.strftime("%d/%m/%Y")

                    c = {'CURRENT_ITEM': s_item,
                         'NEW': 'true',
                         'ITEM': item,
                         'SALE_OBJ': memo_obj,
                         'ALL_SALE_OBJ': all_sale_obj,
                         'CUSTOMER': customer,
                         'EDIT': 'true',
                         'TOTAL': memo_obj.get_total(),
                         'GT': gt,
                         'DUE': due,
                         'DATE':dt,
                         }
                    c.update(csrf(request))
                    return render_to_response('sale_edit_delete.html', c)


    print('HAHAHA ')
    all_sale_obj = Memo.objects.all
    c = {'ALL_SALE_OBJ': all_sale_obj}
    c.update(csrf(request))
    return render_to_response('sale_edit_delete.html', c)



# ----------------------------- PURCHASE --------------------------------



def purchase_page_load(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    c = {}
    c.update(csrf(request))
    return render_to_response('purchase.html', c)



def purchase_add_page_load(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.POST.get('Select_button'):
        str= request.POST.get('Select_party')
        if str=='-':
            return HttpResponseRedirect('/purchase/purchase_add')

        id = request.POST.get('Select_party','0--').split('-')
        obj = Supplier.objects.filter(id=int(id[0])).get()

        c = {'CUSTOMER': obj, 'SELECTED':'true', }
        c.update(csrf(request))
        return render_to_response('purchase_add.html', c)

    elif request.POST.get('Confirm_button'):
        c_id, c_name = request.POST.get('Select_party', '').split('-')
        customer = Supplier.objects.filter(id=int(c_id)).get()
        dd,mm,yy = request.POST.get('Date').split('/')
        date = yy+'-'+mm+'-'+dd
        obj = PurchaseMemo(party=customer, date=date)
        obj.save()

        dt = request.POST.get('Date')


        all_item = Item.objects.all

        c = {'SALE_OBJ': obj,
             'ALLITEM': all_item,
             'SELECTED':'true',
             'DATE':dt,
             }
        c.update(csrf(request))
        return render_to_response('purchase_add.html', c)

    elif request.POST.get('Add_item_button'):
        id = request.POST.get('Memo_no', '')
        objMemo =PurchaseMemo.objects.filter(id=int(id)).get()

        item_id, item_name, item_size = request.POST.get('Select_item', '').split('-')
        selected_item = Item.objects.filter(id=int(item_id)).get()

        quantity = request.POST.get('Unit', '0')
        free = request.POST.get('Free', '0')

        objSaleItem = PurchaseItem(quantity=quantity, free=free, item=selected_item)
        objSaleItem.save()
        objMemo.purchase_item.filter(item=objSaleItem.item).delete()
        objMemo.purchase_item.add(objSaleItem)


        objMemo.save()
        total = objMemo.get_total

        allitem = Item.objects.all

        dt = objMemo.date.strftime("%d/%m/%Y")
        c = {'SALE_OBJ': objMemo,
             'ALLITEM': allitem,
             'TOTAL': total,
             'GRAND_TOTAL':total,
             'PAID':'0',
             'DUE':'0',
             'DISCOUNT':'0',
             'SELECTED':'true',
             'DATE':dt,}
        c.update(csrf(request))
        return render_to_response('purchase_add.html', c)

    elif request.POST.get('Save_memo_button'):
        id = request.POST.get('Memo_no', '')
        objMemo = PurchaseMemo.objects.filter(id=int(id)).get()
        objMemo.paid = request.POST.get('Paid')
        objMemo.discount = request.POST.get('Discount')
        objMemo.save()

        total = objMemo.get_total()
        paid= objMemo.paid
        discount = objMemo.discount
        grand_total=(int(total)-int(discount))
        due=(int(total) - int(discount) - int(paid))

        dt = objMemo.date.strftime("%d/%m/%Y")


        c = {'SALE_OBJ': objMemo,
             'TOTAL': total,
             'GRAND_TOTAL':grand_total,
             'PAID':paid,
             'DISCOUNT': discount,
             'DUE':due ,
             'SELECTED': 'true',
             'PRINT': 'true',
             'DATE': dt,
             }
        c.update(csrf(request))
        return render_to_response('purchase_add.html', c)

    elif request.POST.get('Print_memo_button'):
        return HttpResponse('Under construction')





    elif not request.POST.get('Memo_no', '')=='':
        id = request.POST.get('Memo_no', '')
        objMemo = PurchaseMemo.objects.filter(id=int(id)).get()
        item_name, item_size = request.POST.get('Select_item', '').split('-')
        item = Item.objects.filter(name=item_name, size=item_size).get()

        total = objMemo.get_total

        all_item = Item.objects.all

        dt = objMemo.date.strftime("%d/%m/%Y")

        c = {'SALE_OBJ': objMemo,
             'CURRENT_ITEM': item,
             'ALLITEM': all_item,
             'TOTAL': total,
             'SELECTED':'true',
             'ITEM_SELECTED':'true',
             'DATE':dt,
             }
        c.update(csrf(request))
        return render_to_response('purchase_add.html', c)

    c = {'party':Supplier.objects.all(),}
    c.update(csrf(request))
    return render_to_response('purchase_add.html', c)


def purchase_edit_delete(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.POST.get('Edit_button'):

        id = request.POST.get('Select_memo')
        if  id == 'null':
            return HttpResponseRedirect('/purchase/purchase_edit_delete/')

        memo_obj = PurchaseMemo.objects.get(id=int(id))

        #error handled
        if not memo_obj:
            return HttpResponseRedirect('/purchase/purchase_edit_delete/')



        all_sale_obj = PurchaseMemo.objects.all

        total = memo_obj.get_total()
        gt =int(total) - int(memo_obj.discount)
        due = gt - memo_obj.paid

        dt=memo_obj.date.strftime("%d/%m/%Y")

        customer = Supplier.objects.all()
        item = Item.objects.all()
        c = {'ITEM': item,
             'SALE_OBJ': memo_obj,
             'ALL_SALE_OBJ': all_sale_obj,
             'CUSTOMER': customer,
             'EDIT': 'true',
             'TOTAL': memo_obj.get_total,
             'GT': gt,
             'DUE': due,
             'DATE': dt,


             }
        c.update(csrf(request))
        return render_to_response('purchase_edit_delete.html', c)


    elif request.POST.get('Save_head_button'):
        id= request.POST.get('Memo_no')
        if id =='':
            return HttpResponse('error')

        memo_obj = PurchaseMemo.objects.get(id=int(id))

        customer_id = request.POST.get('Party', '').split('-')

        dd, mm, yy = request.POST.get('Date').split('/')
        date_got = yy + '-' + mm + '-' + dd

        memo_obj.party = Supplier.objects.get(id=int(customer_id[0]))
        memo_obj.date = date_got
        memo_obj.save()

        all_sale_obj = PurchaseMemo.objects.all

        gt = memo_obj.get_total() - memo_obj.discount
        due = gt - memo_obj.paid

        #dt = memo_obj.date.strftime("%d/%m/%Y")
        dt=request.POST.get('Date')


        customer = Supplier.objects.all()
        item = Item.objects.all()
        c = {'ITEM': item,
             'SALE_OBJ': memo_obj,
             'ALL_SALE_OBJ': all_sale_obj,
             'CUSTOMER': customer,
             'EDIT': 'true',
             'TOTAL': memo_obj.get_total(),
             'GT': gt,
             'DUE': due,
             'DATE': dt,
             }
        c.update(csrf(request))
        return render_to_response('Purchase_edit_delete.html', c)


    elif request.POST.get('Add_item_button') or request.POST.get('Save_item_button'):

        id = request.POST.get('Memo_no')
        objMemo = PurchaseMemo.objects.filter(id=int(id)).get()

        item_id= request.POST.get('Select_item', '').split('-')
        selected_item = Item.objects.filter(id=int(item_id[0])).get()

        quantity = request.POST.get('Unit', '')
        free = request.POST.get('Free', '')

        objSaleItem = PurchaseItem(quantity=int(quantity), free=int(free), item=selected_item)
        objSaleItem.save()

        objMemo.purchase_item.filter(item=objSaleItem.item).delete()
        objMemo.purchase_item.add(objSaleItem)

        objMemo.save()

        customer = Supplier.objects.all()
        item = Item.objects.all()
        all_sale_obj = PurchaseMemo.objects.all
        gt = objMemo.get_total() - objMemo.discount
        due = gt - objMemo.paid

        dt = objMemo.date.strftime("%d/%m/%Y")


        c = {
            'ITEM': item,
            'SALE_OBJ': objMemo,
            'ALL_SALE_OBJ': all_sale_obj,
            'CUSTOMER': customer,
            'EDIT': 'true',
            'TOTAL': objMemo.get_total(),
            'GT': gt,
            'DUE': due,
            'DATE':dt,
        }
        c.update(csrf(request))
        return render_to_response('purchase_edit_delete.html', c)


    elif request.POST.get('Delete_item_button'):
        id = request.POST.get('Memo_no')
        objMemo = PurchaseMemo.objects.filter(id=int(id)).get()

        item_id, item_name, item_size = request.POST.get('Select_item', '').split('-')
        selected_item = Item.objects.filter(id=int(item_id)).get()

        quantity = request.POST.get('Unit', '')
        free = request.POST.get('Free', '')

        objSaleItem = PurchaseItem(quantity=quantity, free=free, item=selected_item)

        objMemo.purchase_item.filter(item=objSaleItem.item).delete()

        objMemo.save()

        customer = Supplier.objects.all()
        item = Item.objects.all()
        all_sale_obj = PurchaseMemo.objects.all
        gt = objMemo.get_total() - objMemo.discount
        due = gt - objMemo.paid

        dt = objMemo.date.strftime("%d/%m/%Y")

        c = {

            'ITEM': item,
            'SALE_OBJ': objMemo,
            'ALL_SALE_OBJ': all_sale_obj,
            'CUSTOMER': customer,
            'EDIT': 'true',
            'TOTAL': objMemo.get_total(),
            'GT': gt,
            'DUE': due,
            'DATE':dt,

        }
        c.update(csrf(request))
        return render_to_response('purchase_edit_delete.html', c)


    elif request.POST.get('Save_all_button'):
        id = request.POST.get('Memo_no')

        objMemo = PurchaseMemo.objects.filter(id=int(id)).get()

        discount = request.POST.get('Discount', '')
        paid = request.POST.get('Paid', '')

        objMemo.discount = discount
        objMemo.paid = paid

        objMemo.save()

        all_sale_obj = PurchaseMemo.objects.all

        c = {'ALL_SALE_OBJ': all_sale_obj}
        c.update(csrf(request))
        return render_to_response('purchase_edit_delete.html', c)


    elif request.POST.get('Delete_button'):
        id = request.POST.get('Select_memo')
        if  id == 'null':
            return HttpResponseRedirect('/purchase/purchase_edit_delete/')
        memo_obj = PurchaseMemo.objects.get(id=int(id))
        all_sale_obj = PurchaseMemo.objects.all

        gt = memo_obj.get_total() - memo_obj.discount
        due = gt - memo_obj.paid

        dt = memo_obj.date.strftime("%d/%m/%Y")

        c = {'SALE_OBJ': memo_obj,
             'ALL_SALE_OBJ': all_sale_obj,
             'DELETE': 'true',
             'TOTAL': memo_obj.get_total(),
             'GT': gt,
             'DUE': due,
             'DATE':dt,
        }
        c.update(csrf(request))
        return render_to_response('purchase_edit_delete.html', c)


    elif request.POST.get('Print_button'):
        id = request.POST.get('Select_memo')
        if  id == 'null':
            return HttpResponseRedirect('/purchase/purchase_edit_delete/')
        memo_obj = PurchaseMemo.objects.get(id=int(id))
        all_sale_obj = PurchaseMemo.objects.all

        gt = memo_obj.get_total() - memo_obj.discount
        due = gt - memo_obj.paid

        dt = memo_obj.date.strftime("%d/%m/%Y")

        c = {'SALE_OBJ': memo_obj,
             'ALL_SALE_OBJ': all_sale_obj,
             'PRINT': 'true',
             'TOTAL': memo_obj.get_total(),
             'GT': gt,
             'DUE': due,
             'DATE':dt,
        }
        c.update(csrf(request))
        return render_to_response('purchase_edit_delete.html', c)


    elif request.POST.get('Delete_confirm_button'):
        id = request.POST.get('Memo_no')
        PurchaseMemo.objects.filter(id=int(id)).delete()

        return HttpResponseRedirect('/purchase/purchase_edit_delete/')


    elif request.POST.get('Print_confirm_button'):
        id = request.POST.get('Memo_no')
        # PRINT SHOUD BE DONE HERE

        return HttpResponseRedirect('/purchase/purchase_edit_delete/')






    else:
        if request.POST.get('Select_item'):

            id = request.POST.get('Memo_no')

            objMemo = PurchaseMemo.objects.filter(id=int(id)).get()

            item_id, item_name, item_size = request.POST.get('Select_item', '').split('-')

            if item_id == '':

                #not handled
                all_sale_obj = PurchaseMemo.objects.all
                c = {'ALL_SALE_OBJ': all_sale_obj}
                c.update(csrf(request))
                return render_to_response('sale_edit_delete.html', c)
            else:
                s_item = Item.objects.get(id=int(item_id))

                selected_sale_item = objMemo.purchase_item.filter(item=s_item)
                if selected_sale_item:
                    # not new element
                    selected_sale_item = objMemo.purchase_item.filter(item=s_item).get()

                    id = request.POST.get('Memo_no')
                    memo_obj = PurchaseMemo.objects.get(id=int(id))
                    all_sale_obj = PurchaseMemo.objects.all

                    gt = memo_obj.get_total() - memo_obj.discount
                    due = gt - memo_obj.paid

                    customer = Supplier.objects.all()
                    item = Item.objects.all()

                    dt = memo_obj.date.strftime("%d/%m/%Y")

                    c = {'CURRENT_ITEM': s_item,
                         'OLD': 'true',
                         'SALE_ITEM': selected_sale_item,
                         'ITEM': item,
                         'SALE_OBJ': memo_obj,
                         'ALL_SALE_OBJ': all_sale_obj,
                         'CUSTOMER': customer,
                         'EDIT': 'true',
                         'TOTAL': memo_obj.get_total(),
                         'GT': gt,
                         'DUE': due,
                         'DATE':dt,
                         }
                    c.update(csrf(request))
                    return render_to_response('purchase_edit_delete.html', c)




                else:

                    #new item

                    id = request.POST.get('Memo_no')
                    memo_obj = PurchaseMemo.objects.get(id=int(id))
                    all_sale_obj = PurchaseMemo.objects.all

                    gt = memo_obj.get_total() - memo_obj.discount
                    due = gt - memo_obj.paid

                    customer = Supplier.objects.all()
                    item = Item.objects.all()

                    dt = memo_obj.date.strftime("%d/%m/%Y")

                    c = {'CURRENT_ITEM': s_item,
                         'NEW': 'true',
                         'ITEM': item,
                         'SALE_OBJ': memo_obj,
                         'ALL_SALE_OBJ': all_sale_obj,
                         'CUSTOMER': customer,
                         'EDIT': 'true',
                         'TOTAL': memo_obj.get_total(),
                         'GT': gt,
                         'DUE': due,
                         'DATE':dt,
                         }
                    c.update(csrf(request))
                    return render_to_response('purchase_edit_delete.html', c)


    print('HAHAHA ')
    all_sale_obj = PurchaseMemo.objects.all
    c = {'ALL_SALE_OBJ': all_sale_obj}
    c.update(csrf(request))
    return render_to_response('purchase_edit_delete.html', c)



#----------------------------report------------------------------

def report_item_list(request):
    col, row = 3, 0;
    row= int(Item.objects.count())
    Matrix = [[0 for x in range(col)] for y in range(row)]



    all_item = Item.objects.all()

    counter=0
    for i in all_item:
        Matrix[counter][0]=i.id
        Matrix[counter][1]=i.name
        Matrix[counter][2]=i.size
        counter=counter+1




    for x in range(0,row-1):

        print(Matrix[x])

    ran= row-1

    c={'MATRIX':Matrix, 'RANGE':ran,}
    c.update(csrf(request))
    return render_to_response('report_item_list.html', c)


def report_stock_ledger(request):


    all_item = Item.objects.all()

    col, row = 12, 0;
    row = int(Item.objects.count())
    matrix = [[0 for x in range(col)] for y in range(row+1)]

    matrix[0][0] ='Name'
    matrix[0][1] = 'Size'
    matrix[0][2] = 'Starting'
    matrix[0][3] = 'Purchased'
    matrix[0][4] = 'Sales Return'
    matrix[0][5] = 'Free'
    matrix[0][6] = '3+4+5'
    matrix[0][7] = 'Sold'
    matrix[0][8] = 'Purchase return'
    matrix[0][9] = 'Free'
    matrix[0][10]= '7+8+9'
    matrix[0][11]= '2+6-10'


    counter = 0

    for i in all_item:
        counter=counter+1
        #name
        matrix[counter][0]= i.name
        #size
        matrix[counter][1]=i.size
        #starting
        matrix[counter][2] = 0


        #----- purchased  quantity calculation for each object
        purchased = PurchaseItem.objects.filter(item=i).aggregate(x=Coalesce(Sum('quantity'),0)).get('x')
        matrix[counter][3]=int(purchased)

        #sales return ------------------------------- not done
        matrix[counter][4] =0

        #got free
        got_free =  PurchaseItem.objects.filter(item=i).aggregate(x=Coalesce(Sum('free'),0)).get('x')
        matrix[counter][5]=int(got_free)

        # summation of 2,3,4

        matrix[counter][6] =matrix[counter][2]+matrix[counter][3]+matrix[counter][4]

        # ----- Sold quantity calculation for each object
        sold = SaleItem.objects.filter(item=i).aggregate(x=Coalesce(Sum('quantity'),0)).get('x')

        matrix[counter][7] = int(sold)


        #purchase return
        matrix[counter][8] =0


        # given free
        given_free = SaleItem.objects.filter(item=i).aggregate(x=Coalesce(Sum('free'),0)).get('x')
        matrix[counter][9] = int(given_free)


        # summation   of 7,8,9

        matrix[counter][10] = matrix[counter][7]+matrix[counter][8]+matrix[counter][9]

        # total
        matrix[counter][11] = matrix[counter][6] -matrix[counter][10]



        i.item_available= int(purchased)-int(sold)
        i.item_free= int(got_free)-int(given_free)


        print(i.id)
        print('available')
        print(i.item_available)
        print('free')
        print(i.item_free)



    c = {'MATRIX': matrix, }
    c.update(csrf(request))
    return render_to_response('report_item_list.html', c)








