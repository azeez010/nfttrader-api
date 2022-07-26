import git
from . import app

#Route for the GitHub webhook
@app.route('/git-update', methods=['POST'])
def git_update():
    repo = git.Repo('./nfttraderio_api')
    origin = repo.remotes.origin
    repo.create_head('master',
    origin.refs.master).set_tracking_branch(origin.refs.master).checkout()
    #all note
    origin.pull()
    return '', 200