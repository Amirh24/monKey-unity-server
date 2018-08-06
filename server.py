from script import MonKeyTextureGenerator
from flask import Flask, render_template, redirect
from flask_s3 import FlaskS3
from flask_cors import CORS
import urllib.request, json, re, os, boto3
from botocore.client import Config
from botocore.exceptions import ClientError


def is_a_banano_address(address):

    pattern = '^ban_[13][013-9a-km-uw-z]{59}$'
    match = re.match(pattern, address, flags=0)
    return match is not None


def connect_to_s3_bucket():

    s3_resource = boto3.resource(
        's3',
        aws_access_key_id=os.environ.get('AWS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
        config=Config(signature_version='s3v4')
    )

    return s3_resource


def file_exists_in_s3_bucket(file_name):

    try:
        s3_resource.Object('bananomonkeys', file_name).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        return True


app = Flask(__name__)
app.config['FLASKS3_BUCKET_NAME'] = os.environ.get('S3_BUCKET_NAMEING')
app.config['USE_S3_DEBUG'] = True
s3 = FlaskS3(app)
s3_resource = connect_to_s3_bucket()
CORS(app)

monKey_texture_generator = MonKeyTextureGenerator()
@app.route("/")
def home():
    return 'monKey Unity and floodfill for PNG script'


@app.route('/<address>', methods=['GET'])
def monkey_image(address):
    if address and is_a_banano_address(address):
        path = 'images/png/texture/monKey-' + address + '.png'
        s3_bucket_key = 'static/' + path
        # if texture image does not exist, generate it and upload it to the s3 bucket
        if not file_exists_in_s3_bucket(s3_bucket_key):
            # Get data from the api
            monKey_data = ''
            with urllib.request.urlopen("http://bananomonkeys.herokuapp.com/api/" + address) as url:
                monKey_data = json.load(url)
            print(monKey_data)
            texture = monKey_texture_generator.generate_unity_texture(monKey_data=monKey_data)
            # Upload image to S3-Bucket
            s3_resource.Bucket(os.environ.get('S3_BUCKET_NAMEING')).put_object(Key=s3_bucket_key, Body=texture,
                                                                               ACL='public-read',
                                                                               ContentType='image/jpeg',
                                                                               ContentLength=len(texture),
                                                                  CacheControl='max-age=604800')
        # Retrieve the image from cloudfront
        return redirect('http://d3tynpbz5c31ci.cloudfront.net/static/' + path)
    else:
        return render_template("NotABananoAddress.html"), 400


if __name__ == "__main__":
    app.run(debug=True)
