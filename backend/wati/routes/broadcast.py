from fastapi import APIRouter,Depends,HTTPException, File, UploadFile,Request
from ..models import Broadcast,Contacts,ChatBox
from ..Schemas import broadcast,user,chatbox
from ..database import database
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests
import json
from fastapi.responses import JSONResponse
import csv
import io
from ..oauth2 import get_current_user
from dramatiq import get_broker
import asyncio
from datetime import datetime

from ..crud.template import send_template_to_whatsapp

from fastapi import APIRouter,Depends,HTTPException, File, UploadFile,Request
from starlette.responses import PlainTextResponse
from ..oauth2 import get_current_user
from ..crud.template import send_template_to_whatsapp# Replace with your actual WhatsApp Business API endpoint and token
import logging

# Replace with your actual WhatsApp Business API endpoint and token


router=APIRouter( tags=['Broadcast'])

WEBHOOK_VERIFY_TOKEN = "12345"  # Replace with your verification token

# Meta Webhook verification endpoint
@router.get("/meta-webhook")
async def verify_webhook(request: Request):
    verify_token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    hubmode = request.query_params.get("hub.mode")
    print(f"Received verify_token: {challenge}, Expected: {WEBHOOK_VERIFY_TOKEN}")
    if verify_token == WEBHOOK_VERIFY_TOKEN and hubmode == "subscribe" :
        return PlainTextResponse(content=request.query_params.get("hub.challenge"),status_code=200)
    
    else:
        raise HTTPException(status_code=403, detail="Verification token mismatch")
    
# Webhook event listener to receive message status updates


# @router.post("/meta-webhook")
# # async def receive_meta_webhook(request: Request, db: Session = Depends(database.get_db)):
#     try:
#         # Parse the incoming webhook request
#         body = await request.json()
#         print(body)

#         # Ensure 'entry' exists in the body
#         if "entry" not in body:
#             raise HTTPException(status_code=400, detail="Invalid webhook format")

#         # Process each entry
#         for event in body["entry"]:
#             if "changes" not in event:
#                 raise HTTPException(status_code=400, detail="Missing 'changes' key in entry")
            
#             # Iterate through each change
#             for change in event["changes"]:
#                 if "value" not in change:
#                     raise HTTPException(status_code=400, detail="Missing 'value' key in changes")

#                 value = change["value"]

#                 # Handle messages (replies)
#                 if "statuses" in value:
#                     for status in value["statuses"]:
#                         # Check if the necessary keys exist
#                         if "recipient_id" not in status or "id" not in status or "status" not in status or "timestamp" not in status:
#                             raise HTTPException(status_code=400, detail="Missing keys in statuses")

                        
#                         message_status = status["status"]
#                         wamid=status['id']

#                         message_read=False
#                         message_delivered=False
#                         message_sent=False

                        
#                         if(message_status=="read"):
#                             message_read=True
#                             message_delivered=True
#                             message_sent=True
                            
                        
#                         if(message_status=="delivered"):
#                             message_read=False
#                             message_delivered=True
#                             message_sent=True
                            


#                         if(message_status=="sent"):
#                             message_read=False
#                             message_delivered=False
#                             message_sent=True
                            



#                         broadcast_report = (
#                                 db.query(Broadcast.BroadcastAnalysis)
#                                 .filter( Broadcast.BroadcastAnalysis.message_id==wamid)
#                                 .first()
#                             )
                        
#                         if not broadcast_report:
#                                 raise HTTPException(status_code=404,detail="Broadcast not found")

#                         if wamid:
#                                 broadcast_report.read=message_read
#                                 broadcast_report.delivered=message_delivered
#                                 broadcast_report.sent=message_sent
#                                 broadcast_report.status=message_status

#                         db.add(broadcast_report)
#                         db.commit()
#                         db.refresh(broadcast_report) 
                
#                 elif "messages" in value:
#                     for message in value["messages"]:

#                         message_reply=True
#                         message_status='replied'
                         
#                         wamid=message['context']['id']
#                         broadcast_report = (
#                                 db.query(Broadcast.BroadcastAnalysis)
#                                 .filter( Broadcast.BroadcastAnalysis.message_id==wamid)
#                                 .first()
#                             )
                        
#                         if not broadcast_report:
#                                 raise HTTPException(status_code=404,detail="Broadcast not found")

#                         if wamid:
#                                 broadcast_report.replied=message_sent=message_reply
#                                 broadcast_report.status=message_status

#                         db.add(broadcast_report)
#                         db.commit()
#                         db.refresh(broadcast_report) 

#             # Handle replies (contextual messages)
#                 if "messages" in value:
#                     for message in value["messages"]:
#                         if 'context' not in message:
#                             continue  # Skip if there's no context (no reply)

#                         # Extract context information
#                         context = message['context']
#                         if 'id' not in context:
#                             continue  # Skip if there's no context ID

#                         wamid = context['id']
#                         broadcast_report = db.query(Broadcast.BroadcastAnalysis).filter(Broadcast.BroadcastAnalysis.message_id == wamid).first()

#                         if not broadcast_report:
#                             raise HTTPException(status_code=404, detail="Broadcast not found")

#                         broadcast_report.replied = True
#                         broadcast_report.status = 'replied'

#                         db.commit()
#                         db.refresh(broadcast_report)

#                         # Extract relevant details for the reply message
#                         wa_id = message['from']
#                         message_id = message['id']
#                         phone_number_id = value['metadata']['phone_number_id']
#                         message_content = message['text']['body']
#                         timestamp = int(message['timestamp'])
#                         message_type = message['type']
#                         context_message_id = context['id']

#                         # Convert timestamp to a datetime object
#                         timestamp_dt = datetime.utcfromtimestamp(timestamp)

#                         # Store the incoming reply message in the database
#                         conversation = ChatBox.Conversation(
#                             wa_id=wa_id,
#                             message_id=message_id,
#                             phone_number_id=phone_number_id,
#                             message_content=message_content,
#                             timestamp=timestamp_dt,
#                             context_message_id=context_message_id,
#                             message_type=message_type
#                         )

#                         logging.info('This is saving reply message')
#                         db.add(conversation)
#                         db.commit()
#                         db.refresh(conversation)
                         
#             # Extracting the relevant part of the JSON
#                 entry = body.get("entry", [])
#                 if entry:
#                     changes = entry[0].get("changes", [])
#                     if changes:
#                         value = changes[0].get("value", {})
                        
#                         # Check for the existence of contacts and messages
#                         if "contacts" in value and "messages" in value:
#                             contacts = value["contacts"]
#                             messages = value["messages"]

#                             if contacts and messages:  # Ensure they are not empty lists
#                                 contact = contacts[0]
#                                 message = messages[0]
                                
#                             #    Create a WebhookData object
#                                 webhook_data = chatbox.WebhookData(
#                                     messaging_product=value['messaging_product'],
#                                     phone_number_id=value['metadata']['phone_number_id'],
#                                     wa_id=contact['wa_id'],
#                                     message_id=message['id'],
#                                     text=message['text']['body'],
#                                     timestamp=int(message['timestamp']),
#                                     context_message_id=message['context']['id'] if 'context' in message else None,
#                                     message_type=message['type']
#                                 )

#                                 # Convert timestamp to a datetime object
#                                 timestamp = webhook_data.timestamp
#                                 timestamp_dt = datetime.utcfromtimestamp(timestamp) if timestamp else None

#                                 # Store the incoming message in the database
#                                 conversation = ChatBox.Conversation(
#                                     wa_id=webhook_data.wa_id,
#                                     message_id=webhook_data.message_id,
#                                     phone_number_id=webhook_data.phone_number_id,
#                                     message_content=webhook_data.text,
#                                     timestamp=timestamp_dt,
#                                     context_message_id=webhook_data.context_message_id,
#                                     message_type=webhook_data.message_type
#                                 )

#                                 logging.info('This is saving')
#                                 db.add(conversation)
#                                 db.commit()
#                                 db.refresh(conversation)
#                             else:
#                                 logging.warning("Contacts or messages are empty.")
#                         else:
#                             logging.warning("Contacts or messages fields are missing.")
#                     else:
#                         logging.warning("Changes field is missing or empty.")
#                 else:
#                     logging.warning("Entry field is missing or empty.")

#         return {"message": "Webhook data received and stored successfully"}


      


#     except KeyError as e:
#         logging.error(f"Missing key in webhook payload: {str(e)}")
#         raise HTTPException(status_code=400, detail=f"Missing key: {str(e)}")
#     except Exception as e:
#         logging.error(f"Error processing webhook: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")










# ######### WORKING ENDPOINT WITH BROADCAST REPORT ##########

# POST endpoint to handle webhook data from WhatsApp
@router.post("/meta-webhook")
async def receive_meta_webhook(request: Request, db: Session = Depends(database.get_db)):
    try:
        # Parse the incoming webhook request
        body = await request.json()
        print(body)

        # Ensure 'entry' exists in the body
        if "entry" not in body:
            raise HTTPException(status_code=400, detail="Invalid webhook format")

        # Process each entry
        for event in body["entry"]:
            if "changes" not in event:
                raise HTTPException(status_code=400, detail="Missing 'changes' key in entry")

            # Iterate through each change
            for change in event["changes"]:
                if "value" not in change:
                    raise HTTPException(status_code=400, detail="Missing 'value' key in changes")

                value = change["value"]

                # Handle message statuses (read, delivered, sent)
                if "statuses" in value:
                    for status in value["statuses"]:
                        # Validate required keys in status
                        if not all(key in status for key in ["recipient_id", "id", "status", "timestamp"]):
                            raise HTTPException(status_code=400, detail="Missing keys in statuses")

                        wamid = status['id']
                        message_status = status["status"]
                        message_read = message_status == "read"
                        message_delivered = message_status in ["read", "delivered"]
                        message_sent = message_status in ["read", "delivered", "sent"]

                        broadcast_report = db.query(Broadcast.BroadcastAnalysis).filter(Broadcast.BroadcastAnalysis.message_id == wamid).first()

                        if not broadcast_report:
                            raise HTTPException(status_code=404, detail="Broadcast not found")

                        # Update the broadcast report
                        broadcast_report.read = message_read
                        broadcast_report.delivered = message_delivered
                        broadcast_report.sent = message_sent
                        broadcast_report.status = message_status

                        db.commit()
                        db.refresh(broadcast_report)

                # Handle replies (contextual messages)
                if "messages" in value:
                    for message in value["messages"]:
                        if 'context' not in message:
                            continue  # Skip if there's no context (no reply)

                        # Extract context information
                        context = message['context']
                        if 'id' not in context:
                            continue  # Skip if there's no context ID

                        wamid = context['id']
                        broadcast_report = db.query(Broadcast.BroadcastAnalysis).filter(Broadcast.BroadcastAnalysis.message_id == wamid).first()

                        if not broadcast_report:
                            raise HTTPException(status_code=404, detail="Broadcast not found")

                        broadcast_report.replied = True
                        broadcast_report.status = 'replied'

                        db.commit()
                        db.refresh(broadcast_report)

                        # Extract relevant details for the reply message
                        wa_id = message['from']
                        message_id = message['id']
                        phone_number_id = value['metadata']['phone_number_id']
                        message_content = message['text']['body']
                        timestamp = int(message['timestamp'])
                        message_type = message['type']
                        context_message_id = context['id']

                        # Convert timestamp to a datetime object
                        timestamp_dt = datetime.utcfromtimestamp(timestamp)

                        # Store the incoming reply message in the database
                        conversation = ChatBox.Conversation(
                            wa_id=wa_id,
                            message_id=message_id,
                            phone_number_id=phone_number_id,
                            message_content=message_content,
                            timestamp=timestamp_dt,
                            context_message_id=context_message_id,
                            message_type=message_type
                        )

                        logging.info('This is saving reply message')
                        db.add(conversation)
                        db.commit()
                        db.refresh(conversation)

                # Extracting the relevant part of the JSON
                entry = body.get("entry", [])
                if entry:
                    changes = entry[0].get("changes", [])
                    if changes:
                        value = changes[0].get("value", {})
                        
                        # Check for the existence of contacts and messages
                        if "contacts" in value and "messages" in value:
                            contacts = value["contacts"]
                            messages = value["messages"]

                            if contacts and messages:  # Ensure they are not empty lists
                                contact = contacts[0]
                                message = messages[0]

                                # Create a WebhookData object
                                webhook_data = chatbox.WebhookData(
                                    messaging_product=value['messaging_product'],
                                    phone_number_id=value['metadata']['phone_number_id'],
                                    wa_id=contact['wa_id'],
                                    message_id=message['id'],
                                    text=message['text']['body'],
                                    timestamp=int(message['timestamp']),
                                    context_message_id=message['context']['id'] if 'context' in message else None,
                                    message_type=message['type']
                                )

                                
                                # Store the incoming message in the database
                                conversation = ChatBox.Conversation(
                                    wa_id=webhook_data.wa_id,
                                    message_id=webhook_data.message_id,
                                    phone_number_id=webhook_data.phone_number_id,
                                    message_content=webhook_data.text,
                                    timestamp=datetime.utcfromtimestamp(webhook_data.timestamp),
                                    context_message_id=webhook_data.context_message_id,
                                    message_type=webhook_data.message_type
                                )

                                logging.info('This is saving')
                                db.add(conversation)
                                db.commit()
                                db.refresh(conversation)
                            else:
                                logging.warning("Contacts or messages are empty.")
                        else:
                            logging.warning("Contacts or messages fields are missing.")
                    else:
                        logging.warning("Changes field is missing or empty.")
                else:
                    logging.warning("Entry field is missing or empty.")

        sender_id = body['entry'][0]['changes'][0]['value']['messages'][0]['from']  # WA ID of the sender
        receiver_id = body['entry'][0]['changes'][0]['value']['metadata']['display_phone_number']  # WA ID of the recipient
        business_account_id = body['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']  # ID of the business account

        # Check if a conversation already exists between the sender and receiver
        conversation = db.query(ChatBox.First_Conversation).filter_by(
            business_account_id=business_account_id,
            sender_wa_id=sender_id,
            receiver_wa_id=receiver_id
        ).first()

        if not conversation:
            # Create a new conversation if it doesn't exist
            conversation = ChatBox.First_Conversation(business_account_id, sender_id, receiver_id)
            db.add(conversation)
            db.commit()
        else:
            # If the conversation exists, you can optionally handle it here (e.g., check if it's active)
            if not conversation.active:
                # return {"error": "Chat has expired."}
                db.delete(conversation)  # Delete the inactive conversation
                db.commit()
            
                # Create a new conversation with a new timestamp
                new_conversation = ChatBox.First_Conversation(business_account_id=business_account_id, sender_wa_id=sender_id, receiver_wa_id=receiver_id)
                new_conversation.first_chat_time = datetime.now()  # Set the new first chat time
                db.add(new_conversation)
                db.commit()
                return {"message": "New conversation created as the previous one was inactive."}

        return {"message": "Webhook data received and stored successfully"}

    except KeyError as e:
        logging.error(f"Missing key in webhook payload: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Missing key: {str(e)}")

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



# GET endpoint to retrieve conversation history
@router.get("/conversations/{wa_id}")
def get_conversation(wa_id: str, db: Session = Depends(database.get_db)):
    conversations = db.query(ChatBox.Conversation).filter(ChatBox.Conversation.wa_id == wa_id).all()
    
    if not conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversations



# Broadcast 2 routes

# test

# @router.post("/send-template-message/")
# async def send_template_message(
#     request: broadcast.input_broadcast, 
#     get_current_user: user.newuser = Depends(get_current_user), 
#     db: Session = Depends(database.get_db)
# ):
#     print(request)

#     # Save broadcast details
#     broadcastList = Broadcast.BroadcastList(
#         user_id=get_current_user.id,
#         name=request.name,
#         template=request.template,
#         contacts=request.recipients,
#         type=request.type,
#         success=0,
#         failed=0,
#         status="processing..."
#     )
#     db.add(broadcastList)
#     db.commit()
#     db.refresh(broadcastList)
    
#     saved_broadcast_id = broadcastList.id


#     # Prepare API URL and headers
#     API_url = f"https://graph.facebook.com/v20.0/{get_current_user.Phone_id}/messages"
#     headers = {
#         "Authorization": f"Bearer {get_current_user.PAccessToken}",
#         "Content-Type": "application/json"
#     }

#     success_count = 0
#     errors = []
#     failed_count = 0

#     for recipient in request.recipients:
#         # Create the base payload
#         data = {
#             "messaging_product": "whatsapp",
#             "to": recipient,
#             "type": "template",
#             "template": {
#                 "name": request.template,
#                 "language": {"code": "en_US"}
#             }
#         }

#         # Check if the image URL is provided and add it to the payload
#         if request.image_id:
#             data["template"]["components"] = [
#                 {
#                     "type": "header",
#                     "parameters": [
#                         {
#                             "type": "image",
#                             "image": {
#                                         "id": request.image_id
#                         }
#                         }
#                     ]
#                 }
#             ]

#         # Check if body parameters are provided and add them to the payload
#         # if request.body_parameters:
#         #     body_params = [{"type": "text", "text": param} for param in request.body_parameters]
#         #     if "components" not in data["template"]:
#         #         data["template"]["components"] = []
#         #     data["template"]["components"].append({
#         #         "type": "body",
#         #         "parameters": body_params
#         #     })

#         # Send the request to the WhatsApp API
#         response = requests.post(API_url, headers=headers, data=json.dumps(data))
#         response_data = response.json()

#         if response.status_code == 200:
#             success_count += 1
#             wamid = response_data['messages'][0]['id']
#             phone_num = response_data['contacts'][0]["wa_id"]

#             MessageIdLog = Broadcast.BroadcastAnalysis(
#                 user_id=get_current_user.id,
#                 broadcast_id=saved_broadcast_id,
#                 message_id=wamid,
#                 status="sent",
#                 phone_no=phone_num,
#             )
#             db.add(MessageIdLog)
#             db.commit()
#             db.refresh(MessageIdLog)
#         else:
#             failed_count += 1
#             errors.append({"recipient": recipient, "error": response_data})

#             MessageIdLog = Broadcast.BroadcastAnalysis(
#                 user_id=get_current_user.id,
#                 broadcast_id=saved_broadcast_id,
#                 status="failed",
#                 phone_no=recipient,
#             )
#             db.add(MessageIdLog)
#             db.commit()
#             db.refresh(MessageIdLog)

#     # Update broadcast status
#     broadcast = db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.id == saved_broadcast_id).first()
#     if not broadcast:
#         raise HTTPException(status_code=404, detail="Broadcast not found")

#     if saved_broadcast_id:
#         broadcast.success = success_count
#         broadcast.status = "Successful" if failed_count == 0 else "Partially Successful"
#         broadcast.failed = failed_count
#     db.add(broadcast)
#     db.commit()
#     db.refresh(broadcast)

#     return {
#         "status": "completed",
#         "successful_messages": success_count,
#         "errors": errors
#     }

@router.post("/send-text-message/")
def send_message(payload: chatbox.MessagePayload):
    # Construct the URL for sending the message
    whatsapp_url = f"https://graph.facebook.com/v20.0/{payload.phone_number_id}/messages"

    # Set up headers with the access token provided by the frontend
    headers = {
        "Authorization": f"Bearer {payload.access_token}",
        "Content-Type": "application/json"
    }

    # Construct the message payload to be sent to the WhatsApp Business API
    data = {
        "messaging_product": "whatsapp",
        "to": payload.wa_id,
        "type": "text",
        "text": {
            "body": payload.body
        }
    }

    # Send POST request to WhatsApp API
    response = requests.post(whatsapp_url, headers=headers, json=data)

    # Check for errors in the response
    if response.status_code != 200:
        print(response.json())
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return {"status": "Message sent", "response": response.json()}

@router.post("/send-template-message/")
async def send_template_message(
    request: broadcast.input_broadcast,
    get_current_user: user.newuser = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):

    # Save broadcast details
    broadcastList = Broadcast.BroadcastList(
        user_id=get_current_user.id,
        name=request.name,
        template=request.template,
        contacts=[contact.phone for contact in request.recipients],  # Only storing phone numbers for now
        type=request.type,
        success=0,
        failed=0,
        status="processing..."
    )
    db.add(broadcastList)
    db.commit()
    db.refresh(broadcastList)

    saved_broadcast_id = broadcastList.id

    API_url = f"https://graph.facebook.com/v20.0/{get_current_user.Phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {get_current_user.PAccessToken}",
        "Content-Type": "application/json"
    }

    success_count = 0
    errors = []
    failed_count = 0

    for contact in request.recipients:
        recipient_name = contact.name
        recipient_phone = contact.phone

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_phone,
            "type": "template",
            "template": {
                "name": request.template,
                "language": {"code": "en_US"},
                # You can insert recipient_name into your message template if needed
            }
        }

        if request.image_id:
            data["template"]["components"] = [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {"id": request.image_id}
                        }
                    ]
                }
            ]

        
        
        if request.body_parameters:
            if request.body_parameters == "Name":
                body_params = [{"type": "text","text": f"{recipient_name}"}]
                
            else:
                data["template"]["components"] = []

            if "components" not in data["template"]:
                data["template"]["components"] = []
            data["template"]["components"].append({
                "type": "body",
                "parameters": body_params
            })

        

        response = requests.post(API_url, headers=headers, data=json.dumps(data))
        response_data = response.json()

        if response.status_code == 200:
            success_count += 1
            wamid = response_data['messages'][0]['id']
            phone_num = response_data['contacts'][0]["wa_id"]

            MessageIdLog = Broadcast.BroadcastAnalysis(
                user_id=get_current_user.id,
                broadcast_id=saved_broadcast_id,
                message_id=wamid,
                status="sent",
                phone_no=phone_num,
                contact_name=recipient_name,
            )
            db.add(MessageIdLog)
            db.commit()
            db.refresh(MessageIdLog)
        else:
            failed_count += 1
            errors.append({"recipient": recipient_phone, "error": response_data})

            MessageIdLog = Broadcast.BroadcastAnalysis(
                user_id=get_current_user.id,
                broadcast_id=saved_broadcast_id,
                status="failed",
                phone_no=recipient_phone,
                contact_name=recipient_name,
            )
            db.add(MessageIdLog)
            db.commit()
            db.refresh(MessageIdLog)

    # Update broadcast status
    broadcast = db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.id == saved_broadcast_id).first()
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")

    broadcast.success = success_count
    broadcast.status = "Successful" if failed_count == 0 else "Partially Successful"
    broadcast.failed = failed_count
    db.add(broadcast)
    db.commit()
    db.refresh(broadcast)

    return {
        "status": "completed",
        "successful_messages": success_count,
        "errors": errors
    }



# route for fetchlist in Broadcast template
@router.get("/templates")
def get_templates(get_current_user: user.newuser=Depends(get_current_user)):

    API_URL = f'https://graph.facebook.com/v15.0/{get_current_user.WABAID}/message_templates'
    headers = {
        'Authorization': f'Bearer {get_current_user.PAccessToken}'
    }

    response = requests.get(API_URL, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()
    # Extract template names
    template_names = [template['name'] for template in data.get('data', [])]
    return JSONResponse(content=template_names)

# Route to create add broadcast in the list 
@router.post("/broadcast")
def broadcastList(request:broadcast.BroadcastListCreate,db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    broadcastList=Broadcast.BroadcastList(
        user_id=get_current_user.id,
        name=request.name,
        template=request.template,
        contacts=request.contacts,
        type=request.type,
        success=request.success,
        failed=request.failed,
        status=request.status,
        scheduled_time=request.scheduled_time,
        task_id=request.task_id
    )
    db.add(broadcastList)
    db.commit()
    db.refresh(broadcastList)
    return{
        "broadcast_id":broadcastList.id
    } 

# Route to fetch the broadcastlist
@router.get('/broadcast')
def fetchbroadcastList(skip: int = 0, limit: int = 10, tag: str = None, db: Session = Depends(database.get_db),
                      get_current_user: user.newuser=Depends(get_current_user) ):
    broadcastList=db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.user_id==get_current_user.id).order_by(Broadcast.BroadcastList.id.desc()).all()
    return broadcastList
# Put route for the broadcastlist (rightnow primaryly used for updating the task_id )
@router.put("/broadcast/{broadcast_id}")
async def update_broadcast(broadcast_id: int, broadcast_update: broadcast.BroadcastListUpdate, db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    # Retrieve the broadcast entry from the database
    broadcast = db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.id == broadcast_id).first()

    # If the broadcast entry does not exist, raise an HTTP 404 error
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")

    # Update the broadcast entry with new data
    if broadcast_update.task_id:
        broadcast.task_id = broadcast_update.task_id

    # Commit the changes to the database
    db.add(broadcast)
    db.commit()
    db.refresh(broadcast)

    # Return the updated broadcast entry
    return {"message": "Broadcast updated successfully", "broadcast_id": broadcast_id, "task_id": broadcast.task_id}


# Route to fetch the scheduled broadcastlist
@router.get("/scheduled-broadcast")
def fetchScheduledbroadcastList(skip: int = 0, limit: int = 10, tag: str = None, db: Session = Depends(database.get_db),
                      get_current_user: user.newuser=Depends(get_current_user) ):
    ScheduledbroadcastList=db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.status=="Scheduled").order_by(Broadcast.BroadcastList.id.desc()).all()
    return ScheduledbroadcastList

# Route to CSV import contacts in the broadcast form
@router.post("/import-contacts")
def import_contacts(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    contents = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(contents))

    contacts = []
    for row in reader:
        contact = Contacts.Contact(name=row['name'], phone=row['phone'])
        contacts.append(contact)
       

    return {"contacts": contacts}
   
# Broadcast 1 routes

@router.get("/template")
def get_templates( get_current_user: user.newuser=Depends(get_current_user)):

    API_URL = f'https://graph.facebook.com/v15.0/{get_current_user.WABAID}/message_templates'
    headers = {
        'Authorization': f'Bearer {get_current_user.PAccessToken}'
    }

    response = requests.get(API_URL, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    return data


@router.delete("/broadcasts-delete/{broadcast_id}")
async def delete_scheduled_broadcast(broadcast_id: str, db: Session = Depends(database.get_db),get_current_user: user.newuser=Depends(get_current_user)):
    # Fetch the broadcast
    broadcast = db.query(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.id==broadcast_id).first()
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    
    # Update the status to 'canceled'
    broadcast.status = "Cancelled"
    db.commit()
    
    return {"detail": "Scheduled broadcast has been canceled."}



import logging

@router.post("/create-template", response_model=broadcast.TemplateResponse)
async def create_template(template: broadcast.TemplateCreate , request : Request , get_current_user: user.newuser=Depends(get_current_user)):
    try:
        template = await request.json()
        broadcast.TemplateCreate.validate_template(template)
        response = await send_template_to_whatsapp(template , get_current_user.PAccessToken , get_current_user.WABAID )
        return response
    except HTTPException as e:
        logging.critical(e)
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    

@router.get("/broadcast-report/{broadcast_id}")
def BroadcastReport(broadcast_id:int,get_current_user: user.newuser=Depends(get_current_user),db: Session = Depends(database.get_db)):

    broadcast_data=db.query(Broadcast.BroadcastAnalysis).filter((Broadcast.BroadcastAnalysis.user_id==get_current_user.id) &(Broadcast.BroadcastAnalysis.broadcast_id==broadcast_id)).all()

    if not broadcast_data:
        raise HTTPException(status_code=404,detail="Broadcast data not found")

    return broadcast_data

@router.post("/upload-media")
async def upload_file(file: UploadFile = File(...),get_current_user: user.newuser=Depends(get_current_user)):
    # Read the contents of the uploaded file
    contents = await file.read()
    

    # Upload the file to WhatsApp directly from memory (no need to save it)
    try:
        media_url = f"https://graph.facebook.com/v20.0/{get_current_user.Phone_id}/media"
        headers = {
            "Authorization": f"Bearer {get_current_user.PAccessToken}"
        }
        files = {
            'file': (file.filename, contents, file.content_type),  # File from memory
        }
        data = {
            'type': file.content_type.split("/")[0],
            'messaging_product': 'whatsapp' # Extract media type (image, video, etc.)
        }

        # Make the POST request to upload media to WhatsApp
        response = requests.post(media_url, headers=headers, files=files, data=data)

        # Check for errors in the WhatsApp API response
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        # Get the media ID from the response
        media_id = response.json().get("id")

        return JSONResponse(content={
            "filename": file.filename,
            "file_size": len(contents),
            "content_type": file.content_type,
            "whatsapp_media_id": media_id
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file to WhatsApp: {str(e)}")

