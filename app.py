from flask import Flask, request
from controller import index, login, signup, user, news, news_utils, rnews, tag_utils
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
import datetime

load_dotenv()


app = Flask(__name__)

# jwtSetup
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=356)

# Adding Routes Here

# public urls
app.add_url_rule('/', view_func=index.index)
app.add_url_rule('/signup', view_func=signup.signup,methods=['POST'])
app.add_url_rule('/login', view_func=login.login , methods=['POST'])
app.add_url_rule('/news', view_func=news.news_pagination , methods=['POST'])
app.add_url_rule('/news/<id>', view_func=news.news_by_id , methods=['POST'])
app.add_url_rule('/taglist' , view_func=tag_utils.tag_list , methods=['POST'])
app.add_url_rule('/newsbytag', view_func=tag_utils.news_by_tag, methods=['POST'])
app.add_url_rule('/taglistcount' , view_func=tag_utils.tag_list_with_count, methods=['POST'])

# private urls
app.add_url_rule('/user' , view_func=user.user , methods=['GET'])
app.add_url_rule('/rnews', view_func=rnews.recommand_news, methods=['POST'])


app.add_url_rule('/likenews' , view_func=news_utils.like_news , methods=['POST'])
# not usable for now
# app.add_url_rule('/savenews' , view_func=news_utils.save_news , methods=['POST'])


app.run(debug=True)