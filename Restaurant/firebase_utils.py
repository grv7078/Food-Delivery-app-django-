from firebase_admin import messaging

def send_push_notification_to_user(user_device_token, title, message):
    # Create the message to be sent
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=message,
        ),
        token=user_device_token,  # Device token for the specific user
    )

    # Send the message
    try:
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
    except Exception as e:
        print(f"Error sending message: {e}")


def send_order_status_update(user_device_token, order_id, new_status):
    title = f"Order {order_id} Status Update"
    message = f"Your order is now {new_status}."

    # Send the push notification
    send_push_notification_to_user(user_device_token, title, message)
