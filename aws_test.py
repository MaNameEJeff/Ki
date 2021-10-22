import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont
from dotenv import load_dotenv
import os

def display_image(bucket,photo,response):
    # Load image from S3 bucket
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), region_name='us-east-1')
    s3_connection = session.resource('s3')

    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image=Image.open(stream)

    # Ready image to draw bounding boxes on it.
    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected custom label
    print('Detected custom labels for ' + photo)
    for customLabel in response['CustomLabels']:
        print('Label ' + str(customLabel['Name']))
        print('Confidence ' + str(customLabel['Confidence']))
        if 'Geometry' in customLabel:
            box = customLabel['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
            draw.text((left,top), customLabel['Name'], fill='#00d400', font=fnt)

            print('Left: ' + '{0:.0f}'.format(left))
            print('Top: ' + '{0:.0f}'.format(top))
            print('Label Width: ' + "{0:.0f}".format(width))
            print('Label Height: ' + "{0:.0f}".format(height))

            points = (
                (left,top),
                (left + width, top),
                (left + width, top + height),
                (left , top + height),
                (left, top))
            draw.line(points, fill='#00d400', width=5)

    image.show()

def show_custom_labels(model,bucket,photo, min_confidence):
    client=boto3.client('rekognition', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),region_name='us-east-1')

    #Call DetectCustomLabels
    with open(photo, 'rb') as img:
    #response = client.detect_custom_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        response = client.detect_custom_labels(Image={'Bytes': img.read()},
            MinConfidence=min_confidence,
            ProjectVersionArn=model)

    # For object detection use case, uncomment below code to display image.
    # display_image(bucket,photo,response)
    print(response['CustomLabels'])
    return len(response['CustomLabels'])

def main():

    load_dotenv('.env')

    bucket='custom-labels-console-us-east-1-abf8d01876'
    photo='E:\\Ki\\data\\Tympole\\17.jpg'
    model='arn:aws:rekognition:us-east-1:041119809924:project/Pokemon-classifier-2021-10-19-02/version/Pokemon-classifier-2021-10-19-02.2021-10-19T20.41.39/1634656299492'
    min_confidence=60

    label_count=show_custom_labels(model,bucket,photo, min_confidence)
    print("Custom labels detected: " + str(label_count))


if __name__ == "__main__":
    main()