from nft_api import app, db, env, auth, authentication, nft, git_update
from nft_api.models import User
import migrate_manager

if __name__  == '__main__':
    app.run(debug=env.str("DEBUG", default=True), host="0.0.0.0", port="5000")
    db.create_all()