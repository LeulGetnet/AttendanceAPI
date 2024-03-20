
import face_recognition
from Account.models import Account
import urllib

def face_match(request, img):
      
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #MEDIA_ROOT = os.path.join(BASE_DIR, "Account")
   
    loc = Account.objects.get(user = request.user).profile_pic.url
    resp = urllib.request.urlopen(loc)
    
    #loc = (str(MEDIA_ROOT) + loc)
    # Load a sample picture and learn how to recognize it.
    user_image = face_recognition.load_image_file(resp)
    user_face_encoding = face_recognition.face_encodings(user_image)[0]

    unknown_image = face_recognition.load_image_file(img)
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

    # Compare faces
    results = face_recognition.compare_faces(
        [user_face_encoding], unknown_face_encoding, tolerance=0.5
        )

    if results[0]:
        return True
    else:
        return False



