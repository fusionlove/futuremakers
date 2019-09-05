import boto3
from IPython.display import Image, display
from pdb import set_trace

import passwords

access_key = passwords.access_key
secret_access_key = passwords.secret_access_key

def test_futuremakers():
  translate_english_to_spanish('Hello World')
  print("The FutureMakers library is imported and ready to use.")

def show_image(path):
    display(Image(filename=path))
    
def translate_english_to_spanish(sentence):
  translate_client = boto3.client(
      'translate',
      region_name='eu-west-1',
      aws_access_key_id = access_key ,
      aws_secret_access_key = secret_access_key,
  )

  result = translate_client.translate_text(Text=sentence, 
              SourceLanguageCode="en", TargetLanguageCode="es")
  return result.get('TranslatedText')
  #print('TranslatedText: ' + result.get('TranslatedText'))
  #print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
  #print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
  
def translate(source, target, sentence):
  translate_client = boto3.client(
      'translate',
      region_name='eu-west-1',
      aws_access_key_id = access_key ,
      aws_secret_access_key = secret_access_key,
  )

  result = translate_client.translate_text(Text=sentence, 
              SourceLanguageCode=source, TargetLanguageCode=target)
  return result.get('TranslatedText')
  
  
def find_celebrities_util(image_path):
  client=boto3.client('rekognition',  region_name='eu-west-1',
  aws_access_key_id= access_key,
  aws_secret_access_key=secret_access_key,)

  with open(image_path, 'rb') as image:
      response = client.recognize_celebrities(Image={'Bytes': image.read()})
      
  results = []


  for celebrity in response['CelebrityFaces']:
      result = {}
      result['name'] = celebrity['Name']
      #print ('Name: ' + celebrity['Name'])
      #print ('Id: ' + celebrity['Id'])
      #print ('Position:')
      #print ('   Left: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Height']))
      #print ('   Top: ' + '{:.2f}'.format(celebrity['Face']['BoundingBox']['Top']))
      #print ('Info')
      #for url in celebrity['Urls']:
      #    print ('   ' + url)
      results.append(result)
  return results

def detect_objects_util(image_path):
  client=boto3.client('rekognition',  region_name='eu-west-1',
  aws_access_key_id= access_key,
  aws_secret_access_key=secret_access_key,)

  with open(image_path, 'rb') as image:
      response = client.detect_labels(Image={'Bytes': image.read()}, MaxLabels=100, MinConfidence=40)
      
  return response

def detect_objects(image_path):
  response = detect_objects_util(image_path)

  
  no = len(response['Labels'])
  msg = ''
  if no == 0:
    print(f"Amazon Rekognition didn't find any objects in {image_path}.")
  else:
    print(f"Amazon Rekognition found {no} objects in {image_path}.")
    print('The objects are:')
    
    for o in response['Labels']:
      print(f"I am {pf(o['Confidence'])} sure that I see a {o['Name'].lower()}.")

    

def detect_faces_util(image_path):
  client=boto3.client('rekognition',  region_name='eu-west-1',
  aws_access_key_id= access_key,
  aws_secret_access_key=secret_access_key,)

  with open(image_path, 'rb') as image:
      response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL'])
      
  return response

def detect_faces(image_path):
  response = detect_faces_util(image_path)
  
  face_details = response['FaceDetails']
  nf = len(face_details)
  
  if nf == 1:
    print(f'Amazon Rekognition found {str(nf)} face in this image.')
  else:
    print(f'Amazon Rekognition found {str(nf)} faces in this image.')
  
  for fd in face_details:
    emotions = fd['Emotions']
    sorted_emotions = sorted(emotions, key = lambda item: item['Confidence'], reverse=True)
    emotion_msg = f"I am {pf(sorted_emotions[0]['Confidence'])} sure that they are feeling {sorted_emotions[0]['Type'].lower()}."
    if fd['Beard']['Value']:
      beard = f"I am {pf(fd['Beard']['Confidence'])} sure that they have a beard."
    else:
      beard = f"I am {pf(fd['Beard']['Confidence'])} sure that they do not have a beard."
    print(f"I think this person is between {fd['AgeRange']['Low']} and {fd['AgeRange']['High']} years old."\
          + ' ' + beard\
          + ' ' + emotion_msg
         )
  
def pf(x):
  return str(round(x)) + ' percent'
  

def find_celebrities(image_path):
  results = find_celebrities_util(image_path)
  n = len(results)
  if n>0:
    msg = 'Amazon Rekognition found one celebrity in ' + image_path + ': ' + results[0]['name'] + '.'
  elif n>1:
    msg = 'Amazon Rekognition found '+str(n)+' celebrities in ' + image_path + ': '

    for i,result in enumerate(results):
      if i<(n-1):
        msg += result['name'] + ', '
      else:
        msg += 'and ' +result['name'] + '.'
  else:
    msg = 'Amazon Rekognition did not find any celebrities in ' + image_path + '.'
  print(msg)
  return msg
  

def speak(text):
  """Getting Started Example for Python 2.7+/3.3+"""
  from boto3 import Session
  from botocore.exceptions import BotoCoreError, ClientError
  from contextlib import closing
  import os
  import sys
  import subprocess
  import uuid
  from tempfile import gettempdir


  # Create a client using the credentials and region defined in the [adminuser]
  # section of the AWS credentials file (~/.aws/credentials).
  polly = boto3.client("polly",   region_name='eu-west-1',
    aws_access_key_id= access_key ,
    aws_secret_access_key=secret_access_key,)

  try:
      # Request speech synthesis
      response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                          VoiceId="Joanna")
  except (BotoCoreError, ClientError) as error:
      # The service returned an error, exit gracefully
      print(error)
      sys.exit(-1)

  # Access the audio stream from the response
  if "AudioStream" in response:
      # Note: Closing the stream is important as the service throttles on the
      # number of parallel connections. Here we are using contextlib.closing to
      # ensure the close method of the stream object will be called automatically
      # at the end of the with statement's scope.
      with closing(response["AudioStream"]) as stream:
          #output = os.path.join(gettempdir(), "speech.mp3")
          if sys.platform == "win32":
              output = 'polly\\' + text.split()[0] + text.split()[1] + str(uuid.uuid1())[:5] + '.mp3'
          else:
              output = 'polly/' + text.split()[0] + text.split()[1] + str(uuid.uuid1())[:5] + '.mp3'

          try:
              # Open a file for writing the output as a binary stream
              with open(output, "wb") as file:
                  file.write(stream.read())
          except IOError as error:
              # Could not write to file, exit gracefully
              print(error)
              sys.exit(-1)

  else:
      # The response didn't contain audio data, exit gracefully
      print("Could not stream audio")
      sys.exit(-1)

  print(f"File saved as {output}.")
  # Play the audio using the platform's default player
  if sys.platform == "win32":
      os.startfile(output)
  else:
      # the following works on Mac and Linux. (Darwin = mac, xdg-open = linux).
      opener = "open" if sys.platform == "darwin" else "xdg-open"
      subprocess.call([opener, output])
