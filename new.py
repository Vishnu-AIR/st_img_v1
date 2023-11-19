from ultralytics import YOLO
import sys


model = YOLO("best (2).pt")

# Define a route to process image data and return predictions

def predict(image):
    try:
   
        results = model.predict(source="public/"+image)

        # Process the results and create a response
        l = []
        names = {0: 'blackheads', 1: 'dark spot', 2: 'nodules', 3: 'papules', 4: 'pustules', 5: 'whiteheads'}

        for idx, result in enumerate(results[0].boxes.xyxy):
            l.append(names[results[0].boxes.cls[idx].item()])

        d = {}
        for key, value in names.items():
            d[value] = l.count(value)

        response_data = {
            'predictions': d,
            'message': 'Prediction successful'
        }

        print(response_data)
        #print("hi")
        return response_data

    except Exception as e:
        #print("__ERROR__ ")
        return  "__ERROR__"
    
if __name__ == '__main__':
    image = ""+ sys.argv[1]

    predict(image)
   # print(r)

# from ultralytics import YOLO
# model=YOLO("best (2).pt")
# results=model.predict(source='0',show=True)
# print(results)
#print(results)
# l=[]
# names={0: 'blackheads', 1: 'dark spot', 2: 'nodules', 3: 'papules', 4: 'pustules', 5: 'whiteheads'}
# for idx,result in enumerate(results[0].boxes.xyxy):
#     l.append(names[results[0].boxes.cls[idx].item()])
#print(l)
# d={}
# for key,values in names.items():
#     d[values]=l.count(values)