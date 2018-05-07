# coding: utf-8


from chalice import Chalice

app = Chalice(app_name='recording')


@app.route('/signup')
def sign_up():
    pass
    
