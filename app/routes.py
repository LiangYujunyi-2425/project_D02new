from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post ,Mobile_c,Health_care,Voice_c,Purchase_plan, user_phone_number, start_date,Insurance,Insurance_con, live, End_date
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.prev_num else None
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    insurance = Insurance.query.filter_by(id=10001).first()
    insurance_con = Insurance_con.query.get_or_404(insurance.insurance_con_id)
    return render_template('index.html.j2', title=_('Home'), form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url,mobile_c=mobile_c,health_care=health_care,voice_c = voice_c,insurance=insurance,insurance_con=insurance_con)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'explore', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'explore', page=posts.prev_num) if posts.prev_num else None
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    insurance = Insurance.query.filter_by(id=10001).first()
    return render_template('index.html.j2', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url,mobile_c=mobile_c,health_care=health_care,voice_c = voice_c,insurance=insurance)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    return render_template('login.html.j2', title=_('Sign In'), form=form,mobile_c=mobile_c,health_care=health_care,voice_c = voice_c)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    return render_template('register.html.j2', title=_('Register'), form=form,mobile_c=mobile_c,health_care=health_care,voice_c = voice_c)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html.j2',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    return render_template('reset_password.html.j2', form=form,mobile_c=mobile_c,health_care=health_care,voice_c = voice_c)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.followed_posts().paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.prev_num else None
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    return render_template('user.html.j2', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url,mobile_c=mobile_c,health_care=health_care,voice_c = voice_c)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    return render_template('edit_profile.html.j2', title=_('Edit Profile'),
                           form=form ,mobile_c=mobile_c,health_care=health_care,voice_c = voice_c)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    return redirect(url_for('user', username=username,mobile_c=mobile_c,health_care=health_care,voice_c = voice_c))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    mobile_c = Mobile_c.query.filter_by(id=10001).first()
    health_care = Health_care.query.filter_by(id=10001).first()
    voice_c = Voice_c.query.filter_by(id=1002).first()
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user', username=username,health_care=health_care,mobile_c = mobile_c,voice_c = voice_c))

@app.route('/partnership_benefits', methods=['GET', 'POST'])
@login_required
def partnership_benefits():
        mobile_c = Mobile_c.query.filter_by(id=10001).first()
        health_care = Health_care.query.filter_by(id=10001).first()
        voice_c = Voice_c.query.filter_by(id=1002).first()
        return render_template('partnership_benefits.html.j2',title=_('partnership_benefits') , mobile_c = mobile_c,health_care=health_care,voice_c = voice_c )

@app.route('/禮遇及支援', methods=['GET', 'POST'])
@login_required
def benefits_and_support():
        mobile_c = Mobile_c.query.filter_by(id=10001).first()
        health_care = Health_care.query.filter_by(id=10001).first()
        voice_c = Voice_c.query.filter_by(id=1002).first()
        return render_template('benefits_and_support.html.j2', title=_('benefits_and_support'),mobile_c = mobile_c,health_care=health_care,voice_c = voice_c)

@app.route('/services', methods=['GET', 'POST'])
@login_required
def services():
        mobile_c = Mobile_c.query.filter_by(id=10001).first()
        health_care = Health_care.query.filter_by(id=10001).first()
        voice_c = Voice_c.query.filter_by(id=1002).first()
        return render_template('services.html.j2', title=_('services'),mobile_c = mobile_c,health_care=health_care,voice_c = voice_c)

@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
        mobile_c = Mobile_c.query.filter_by(id=10001).first()
        health_care = Health_care.query.filter_by(id=10001).first()
        voice_c = Voice_c.query.filter_by(id=1002).first()
        return render_template('buy.html.j2',title=_('buy'),mobile_c = mobile_c,health_care=health_care,voice_c = voice_c)

@app.route('/custommer_buy', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        address = request.form.get('address')
        phone_number = request.form.get('phoneNumber')
        start_date_value = request.form.get('startDate')
        purchase_plan = request.form.get('purchasePlan')
        id = request.form.get('id')  # 从表单中获取用户 ID

        # 儲存用戶電話號碼
        new_phone = user_phone_number(phone_number=phone_number)
        db.session.add(new_phone)

        # 儲存開始日期
        new_start_date = start_date(start_date=start_date_value, user_id=new_phone.id)  # 假設你已經有用戶 ID
        db.session.add(new_start_date)

        # 儲存購買計劃
        new_purchase_plan = Purchase_plan(name=address, Purchase_plan=purchase_plan, user_id=new_phone.id)
        db.session.add(new_purchase_plan)

        new_purchase_plan = Purchase_plan(name=address, Purchase_plan=purchase_plan, user_id=id)
        db.session.add(new_purchase_plan)

        db.session.commit()
        flash('註冊成功！', 'success')
        return redirect(url_for('register_customer'))

    return render_template('buy.html.j2')