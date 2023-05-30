from trycourier import Courier


def send_email():
    client = Courier(auth_token="pk_prod_VZBZM4377R44KPPY70Y9AB39SA5M")
    templateType = "MTPRTRG6NKMH11G45S2AFP3CJAEY"
    resp = client.send_message(
        message={
            "to": {
                "email": "erfanfi79@gmail.com",
            },
            "template": templateType
        }
    )
