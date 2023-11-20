import pyrebase
firebaseConfig = {
  'apiKey': "AIzaSyAwXiIyWpTG2kTse4JARHQ2aKTsTWut1No",
  'authDomain': "mongotest-1e344.firebaseapp.com",
  'projectId': "mongotest-1e344",
  'storageBucket': "mongotest-1e344.appspot.com",
  'messagingSenderId': "778515725880",
  'appId': "1:778515725880:web:695ab9188414e9f07d70cd",
  'measurementId': "G-VJE271HSYR"
}

firebase = pyrebase.initialize_app(firebaseConfig)


auth = firebase.auth()
