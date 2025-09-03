from pyexpat.errors import messages

from flask import Flask,request
from flask_restful import Api, Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)

class VideoModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    views=db.Column(db.Integer,nullable=False)
    likes= db.Column(db.Integer, nullable=False)
    No_of_comments= db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Video(name={self.name},views={self.views},likes={self.likes},No_of_comments={self.No_of_comments})'





video_put_agrs =reqparse.RequestParser()
video_put_agrs.add_argument("name",type=str,help='name of the video is req ',required=True)
video_put_agrs.add_argument("likes",type=int,help='likes of the video is req ',required=True)
video_put_agrs.add_argument("views",type=int,help='views of the video is req ',required=True)
video_put_agrs.add_argument("No_of_comments",type=int,help='no of comments of the video is req ',required=True)


video_update_args=reqparse.RequestParser()
video_update_args.add_argument("name",type=str,help='name of the video is req ')
video_update_args.add_argument("likes",type=int,help='likes of the video is req ')
video_update_args.add_argument("views",type=int,help='views of the video is req ')
video_update_args.add_argument("No_of_comments",type=int,help='no of comments of the video is req ')



resource_fields={
    'id':fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes': fields.Integer,
    'No_of_comments':fields.Integer,


}



class Video(Resource):
    @marshal_with(resource_fields)
    def get(self,video_id):
        result=VideoModel.query.get(video_id)
        if not result:
            abort(404, message="Video not found")
        return result

    @marshal_with(resource_fields)
    def put(self,video_id):
        args=video_put_agrs.parse_args()
        result=VideoModel.query.get(video_id)
        if result:
            abort(409, message="Video already exists")
        video=VideoModel(id=video_id,name=args['name'],views=args['views'],
                         likes=args['likes'],
                         No_of_comments=args['No_of_comments'])
        db.session.add(video)
        db.session.commit()
        return video,201


    @marshal_with(resource_fields)
    def patch(self,video_id):
        args=video_update_args.parse_args()
        result = VideoModel.query.get(video_id)
        if not result:
            abort(404, message="Video doen't exist ,cannot update ")
        if  args['name'] is not None:
            result.name=args['name']
        if  args['likes'] is not None:
            result.likes=args['likes']
        if  args['No_of_comments' ]is not None:
            result.No_of_comments=args['No_of_comments']
        if args['views'] is not None:
            result.views = args['views']

        db.session.commit()
        return result

api.add_resource(Video,'/video/<int:video_id>')


if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)