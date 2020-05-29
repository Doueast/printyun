from flask import Blueprint, request
from app.models import Order
from app.utils import sign
import requests



vx_pay = Blueprint('vx_pay', __name__)


@vx_pay.route('vxpay', methods=['GET','POST'])
def vxpay():
    data = request.form
    tradeid = data["tradeid"]
    tel_num = data["tel_num"]
    dati = Order.query.filter(Order.Trade_Number == tradeid).first()
    cost = dati.Print_Money
    name = dati.File_Name
    pay_data = {
        'name': str(name),
        'pay_type': 'jsapi',
        'price': str(cost),
        'order_id': str(tradeid),
        'expire': 600,
        'order_uid': str(tel_num),
        'notify_url': 'http://a.yichengruanjian.cn:8000/jsons/native',
        'return_url': 'http://a.yichengruanjian.cn:8000/admin/select',
    }
    pay_data['sign'] = sign(
        pay_data['pay_type'],
        pay_data['name'],
        pay_data['price'],
        pay_data['order_id'],
        pay_data['notify_url'],
        '55ab2edb80e34ae3bee47b4b32c7e1e5'
    )
    print(str(pay_data))
    resp = requests.post('https://xorpay.com/api/pay/5296', data=pay_data)
    # return redirect('https://xorpay.com/api/pay/5296' + pay_data)
    return resp.text