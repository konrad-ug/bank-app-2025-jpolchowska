from behave import *
import requests

URL = "http://localhost:5000/api/accounts"

@step('I make a correct transfer of type: "{type}" and amount: "{amount}" for account with pesel: "{pesel}"')
def make_correct_transfer(context, type, amount, pesel):
    json_body={ "amount": int(amount), "type": f"{type}"}
    response = requests.post(f"{URL}/{pesel}/transfer", json=json_body)
    assert response.status_code == 200

@step('I make an incorrect transfer of type: "{type}" and amount: "{amount}" for account with pesel: "{pesel}"')
def make_incorrect_transfer(context, type, amount, pesel):
    json_body = {"amount": int(amount), "type": f"{type}"}
    response = requests.post(f"{URL}/{pesel}/transfer", json=json_body)
    assert response.status_code == 422

@step('I make a transfer with too much money of type: "{type}" and amount: "{amount}" for account with pesel: "{pesel}"')
def make_too_big_transfer(context, type, amount, pesel):
    json_body = {"amount": int(amount), "type": f"{type}"}
    response = requests.post(f"{URL}/{pesel}/transfer", json=json_body)
    assert response.status_code == 422

@step('I make an incorrect transfer of type: "{type}" and amount: "{amount}" for account which does not exist with pesel: "{pesel}"')
def make_transfer_for_nonexistent_account(context, type, amount, pesel):
    json_body = {"amount": int(amount), "type": f"{type}"}
    response = requests.post(f"{URL}/{pesel}/transfer", json=json_body)
    assert response.status_code == 404