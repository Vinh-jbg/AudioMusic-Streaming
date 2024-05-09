from flask import Flask, jsonify, request, render_template, send_file, Response
from flask_restful import Resource, Api, reqparse
import os
from services.db.connect import Store
from datetime import datetime
import json

#os.add_dll_directory(os.getcwd())

app = Flask(__name__,template_folder='templates')
app.config['UPLOAD_RADIO_DIR'] = 'assets\\radio'
app.config['UPLOAD_IMAGE_DIR'] = 'assets\\image'
api = Api(app)
store = Store()

headers = {'Content-Type: audio/mpeg'}
#postgres://db_radio_app_user:sJYleDSbvhy2VHvpEpcmRawkI3h7ujXw@dpg-chglomak728sd6hfbvs0-a.oregon-postgres.render.com/db_radio_app

@app.route("/stream-music/<name>", methods=['GET'])
def stream_music(name):
    path = os.path.abspath("assets/radio/" + name)
    def generate():
        with open(path, "rb") as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    return Response(generate(), mimetype="audio/mpeg")

@app.route("/uploads", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file_to_upload = request.files['file']
            image = ""
            if "image" in request.files:
                image = request.files['image']
            data = json.loads(request.form['data'])
            artists = data.get('artists', '')
            if file_to_upload and data:
                now = str(datetime.now().timestamp())
                file_name, file_extension = os.path.splitext(file_to_upload.filename)
                radio_name = now + file_extension
                file_to_upload.save(os.path.join(app.config['UPLOAD_RADIO_DIR'], radio_name))
                image_name = ""
                if (image != ""):
                    split_tup = os.path.splitext(image.filename)
                    file_extension = split_tup[1]
                    image_name = now + file_extension
                    image.save(os.path.join(
                        app.config['UPLOAD_IMAGE_DIR'], image_name))
                store.add_music(name=" " + data['name'],
                                image=image_name, path=radio_name, artists=artists)
                data = store.getMusicLast()
                res = {
                    "id": data[0],
                    "name": data[1],
                    "image": data[2],
                    "path": data[3],
                    "artists": data[4]  # Giả sử cơ sở dữ liệu đã được cập nhật để lưu trữ thông tin nghệ sĩ
                }
                return jsonify(res)
            
        
    
            
            return Response("Oh No ! Exception :(((", status=400, mimetype='application/json')
        except Exception as e:
         print(f"Server Exception: {e}")
         return Response(f"Internal Server Error: {e}", status=500, mimetype='application/json')
@app.route("/delete-music/<id>", methods=['GET'])
def delete_music_by_id(id):
    if request.method == 'GET':
        music = store.getMusicById(id)
        if (len(music) > 0):
            image_name = music[0][2]
            if image_name != "":
                image_path = os.path.abspath("assets/image/" + image_name)
                if os.path.exists(image_path):
                    os.remove(image_path)

            radio_name = music[0][3]
            radio_path = os.path.abspath("assets/radio/" + radio_name)
            if os.path.exists(radio_path):
                os.remove(radio_path)
                store.delete_music(id)
                return jsonify({"message": "Delete Success", "id": id}), 200
            else:
                return jsonify({"error": "File Not Exists"}), 404
        # Linh hoạt thêm trong việc xử lý lỗi
        return jsonify({"error": "ID Music Not Exists"}), 404

@app.route("/get-music/<id>", methods=['GET'])
def get_music_by_id(id):
    if request.method == 'GET':
        data = store.getMusicById(id)
        if (len(data) > 0):
            for row in data:
                res = '{"id": ' + str(row[0]) + ',"name": "' + str(row[1]) + \
                    '","image": "' + str(row[2]) + \
                    '","path": "' + str(row[3]) + '"}'
            return json.loads(res)

        return "ID Music Not Exists !!!"


@app.route("/get-all-music", methods=['GET'])
def get_all():
    if request.method == 'GET':
        data = store.getAll()
        if (len(data) > 0):
            res = []
            for row in data:
                res.append({
                    "id": row[0],
                    "name": row[1],
                    "image": row[2],
                    "path": row[3],
                    "artists": row[4]
                })
            return json.dumps(res)
        return "List Music Is Empty !!!"


@app.route("/play-music/<name>", methods=['GET'])
def play_music(name):
    if request.method == 'GET':
        path = os.path.abspath("assets/radio/" + name)
        file = open(
            path, 'rb')
        file.close()
        return send_file(path, mimetype="audio/wav")


@app.route("/photo/<name>", methods=['GET'])
def get_photo(name):
    if request.method == 'GET':
        path = os.path.abspath("assets/image/" + name)
        file = open(
            path, 'rb')
        file.close()
        return send_file(path, mimetype="image/png")
@app.route('/list-songs')
def list_songs():
    songs = store.getAll()
    return render_template('songs.html', songs=songs)
@app.route("/update-music/<id>", methods=['POST'])
def update_music(id):
    if request.method == 'POST':
        name = request.form['name']
        artists = request.form['artists']
        # Giả sử bạn không cho phép thay đổi image và path qua form
        music = store.getMusicById(id)
        if music:
            store.update_music(id, name, music[0][2], music[0][3], artists)
            return jsonify({"message": "Bài hát đã được cập nhật thành công!", 
                            "id": id,
                            "name": name,
                            "image": music[0][2],
                            "path": music[0][3],
                            "artists": artists }), 200
        else:
            return "Song not found", 404
   
    return jsonify({"error": str(e)}), 500
@app.route("/add-music", methods=['POST'])
def add_music():
    if request.method == 'POST':
        try:
            file_to_upload = request.files.get('file')
            image = request.files.get('image')
            name = request.form.get('name')
            artists = request.form.get('artists')
            if file_to_upload and image and name and artists:
                now = str(datetime.now().timestamp())
                radio_name = now + os.path.splitext(file_to_upload.filename)[1]
                image_name = now + os.path.splitext(image.filename)[1]
                file_to_upload.save(os.path.join(app.config['UPLOAD_RADIO_DIR'], radio_name))
                image.save(os.path.join(app.config['UPLOAD_IMAGE_DIR'], image_name))
                
                store.add_music(name=name, image=image_name, path=radio_name, artists=artists)
                
                return jsonify({"message": "Music added successfully"}), 200
            else:
                return jsonify({"error": "Missing data"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
# @app.route("/get-all-artists", methods=['GET'])
# def get_all_artists():
#     data = store.getAll_artists()
#     if data:
#         artists = [artist[0] for artist in data]
#         return json.dumps(artists)
#     else:
#         return "No artists found"

if __name__ == '__main__':
    app.run()
