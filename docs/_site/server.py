#! /usr/bin/env python3.6
"""
Python 3.6 or newer required.
"""
import json
import os
import stripe

print("WE ARE IN SERVER")

# This is your test secret API key.
stripe.api_key = "sk_test_51PtDC5Hoyr0IJ02SZh06noil6dftJzv8Uw0Ve90D4FgLyjeUClEMeJWGGuWKT7XjBayXEFQTtcdkrO5cTs3lMss000VHqVckgh"
stripe.checkout.Session.create(
    mode="payment",
    success_url="https://example.com/success",
    cancel_url="https://example.com/cancel",
    line_items=[{"price": "{{PRICE_ID}}", "quantity": 1}],
    custom_fields=[
        {
            "key": "sample",
            "label": {"type": "custom", "custom": "Free sample"},
            "optional": True,
            "type": "dropdown",
            "dropdown": {
                "options": [
                    {"label": "Balm sample", "value": "balm"},
                    {"label": "BB cream sample", "value": "cream"},
                ],
            },
        },
    ],
)


from flask import Flask, render_template, jsonify, request


app = Flask(
    __name__, static_folder="public", static_url_path="", template_folder="public"
)


def calculate_order_amount(items):
    # Replace this constant with a calculation of the order's amount
    # Calculate the order total on the server to prevent
    # people from directly manipulating the amount on the client
    return 1400


@app.route("/create-payment-intent", methods=["POST"])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data["items"]),
            currency="usd",
            # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
            automatic_payment_methods={
                "enabled": True,
            },
        )
        return jsonify(
            {
                "clientSecret": intent["client_secret"],
                # [DEV]: For demo purposes only, you should avoid exposing the PaymentIntent ID in the client-side code.
                "dpmCheckerLink": "https://dashboard.stripe.com/settings/payment_methods/review?transaction_id={}".format(
                    intent["id"]
                ),
            }
        )
    except Exception as e:
        return jsonify(error=str(e)), 403


if __name__ == "__main__":
    app.run(port=4242)
