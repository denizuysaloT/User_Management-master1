from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


users = [
    {'id': 1, 'username': '	AdminUser', 'email': 'admin@piworks.net	', 'enabled': True},
    {'id': 2, 'username': 'TestUser', 'email': 'testuser@piworks.net', 'enabled': False},

]

@app.route('/')
def index():
    sort_by = request.args.get('sort_by', 'id')
    filter_id = request.args.get('filter_id', '')
    filter_username = request.args.get('filter_username', '')
    filter_email = request.args.get('filter_email', '')
    filter_enabled = request.args.get('filter_enabled', '')
    hide_disabled = request.args.get('hide_disabled') == 'true'


    filtered_users = [user for user in users
                      if (not filter_id or str(user['id']) == filter_id) and
                         (not filter_username or filter_username.lower() in user['username'].lower()) and
                         (not filter_email or filter_email.lower() in user['email'].lower()) and
                         (filter_enabled == '' or str(user['enabled']) == filter_enabled)]


    if hide_disabled:
        filtered_users = [user for user in filtered_users if user['enabled']]


    reverse = False
    if sort_by.startswith('-'):
        sort_by = sort_by[1:]
        reverse = True

    if sort_by in ['id', 'username', 'email', 'enabled']:
        filtered_users = sorted(filtered_users, key=lambda x: x.get(sort_by, ''), reverse=reverse)

    return render_template('index.html', users=filtered_users, hide_disabled=hide_disabled, sort_by=sort_by)


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    display_name = request.form.get('display_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    user_role = request.form.get('user_role')
    enabled = request.form.get('enabled') == 'on'


    users.append({
        'id': len(users) + 1,
        'username': username,
        'email': email,
        'enabled': enabled
    })

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
