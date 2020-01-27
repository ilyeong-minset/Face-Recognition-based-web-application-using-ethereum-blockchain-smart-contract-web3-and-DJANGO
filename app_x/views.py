from __future__ import unicode_literals
from django.shortcuts import render, redirect
from web3 import Web3
import face_recognition
import cv2
import numpy as np
import matplotlib.pyplot as plt
from project_x.settings import BASE_DIR
from .models import Records
from . import forms
from django.http import HttpResponse, HttpResponseRedirect

def ethereum(request):
    ganache_url="http://127.0.0.1:7545"
    web3=Web3(Web3.HTTPProvider(ganache_url))
    acct1="0x316B08860E958050f45755327C928Fb6940cF431"
    #acct1=Records.objects.get()
    acct2="0xDF705903046bF9b38E0E6cb06c7794626357dd4b"

    private_key="c3e146b8e2b9f3facc919358f36fbecdc4f4cd0987f8da1d8f9c1ef45f0696ff"

    nonce=web3.eth.getTransactionCount(acct1)
    tx={
        'nonce':nonce,
        'to':acct2,
        'value':web3.toWei(1,'ether'),
        'gas':2000000,
        'gasPrice':web3.toWei('50','gwei')
        }

    signed_tx=web3.eth.account.signTransaction(tx,private_key)
    tx_hash=web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    add=web3.toHex(tx_hash)
    return redirect('/admin/app_x/records/'+'1'+'/change/')


def index(request):
    return render(request,'app_x/index.html')


def details(request, id):
    record = Records.objects.get(id=id)
    context = {
        'record' : record
    }
    return render(request, 'app_x/details.html', context)

def form_name_view(request):
    form=forms.FormName()
    if request.method=='POST':
        form=forms.FormName(request.POST)
        if form.is_valid():
            return ethereum(request)
    return render(request,'app_x/form_page.html',{'form':form})




def detect(request):
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    sumit_image = face_recognition.load_image_file(BASE_DIR+'/pic/1.jpg')
    sumit_face_encoding = face_recognition.face_encodings(sumit_image)[0]

    # Load a second sample picture and learn how to recognize it.
    somesh_image = face_recognition.load_image_file(BASE_DIR+'/pic/2.jpg')
    somesh_face_encoding = face_recognition.face_encodings(somesh_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        sumit_face_encoding,
        somesh_face_encoding
    ]
    known_face_names = [
        "sumit",
        "somesh"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    userId=0
    getId = 0
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if name=="sumit":
                        userId = 1
                    elif name=="somesh":
                        userId = 2

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        if(userId != 0):
            cv2.waitKey(4000)
            video_capture.release()
            cv2.destroyAllWindows()
            return redirect('/records/details/'+str(userId))

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return redirect('/')
