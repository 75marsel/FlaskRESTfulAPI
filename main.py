from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

video_data_args = reqparse.RequestParser()
video_data_args.add_argument("name", type=str, help="Name is required", required=True)
video_data_args.add_argument("views", type=int, help="Views is required", required=True)
video_data_args.add_argument("likes", type=int, help="Likes is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name is required")
video_update_args.add_argument("views", type=int, help="Views is required")
video_update_args.add_argument("likes", type=int, help="Likes is required")
        
resources_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}

# documentation for 3.x versions
# https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/queries/
class Video(Resource):
    @marshal_with(resources_fields) # transform result object to json format
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() # or .all()
        if not result:
            abort(404, message=f"Video ID: {video_id} not found")
        return result
    
    @marshal_with(resources_fields) # transform result object to json format
    def put(self, video_id):
        args = video_data_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message=f"Video ID Already Exist! ID existed: {video_id}")
        
        video = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resources_fields) # transform result object to json format 
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        
        if not result:
            abort(404, message=f"Video ID: {video_id} not found, cannot update.")
            
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.name = args["likes"]
        
        db.session.commit()
        
        return result, 200
    
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            db.session.delete(result)
            db.session.commit()
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        app.run(debug=True)