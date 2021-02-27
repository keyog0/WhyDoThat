from admin import app, db
# from admin.data import build_sample_db
# import os
# import os.path as op

# app_dir = op.join(op.realpath(os.path.dirname(__file__)), 'admin')
# database_path = op.join(app_dir, app.config['DATABASE_FILE'])
# if not os.path.exists(database_path):
#     build_sample_db()
# db.drop_all()
db.create_all()



if __name__ == '__main__':
    app.run(host='localhost', port='8888',debug=True)
