from deepface import DeepFace


models = [
  "VGG-Face",
  "Facenet",
  "Facenet512",
  "OpenFace",
  "DeepFace",
  "DeepID",
  "ArcFace",
  "Dlib",
  "SFace",
]


def find_face(path):
    dfs = DeepFace.represent(path,model_name=models[3])
    print("sad")



find_face("/Users/yanghengxing/Pictures/WechatIMG205.jpg")