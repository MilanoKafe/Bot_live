
# from flask import Flask, request, render_template_string, redirect, url_for, session, flash
# from utils import add_question, _normalize_category, load_questions, get_questions_by_category, save_questions, load_users, get_user, update_user, load_admins, add_admin, remove_admin, load_help_requests, update_help_request, load_history
# from config import ADMIN_WEB_TOKEN, BOT_TOKEN
# import os
# import json
# import urllib.request
# import urllib.parse

# app = Flask(__name__)
# # WEB_ADMIN_SECRET ni o'rnating yoki tasodifiy kalitdan foydalaning
# app.secret_key = os.getenv('WEB_ADMIN_SECRET', os.urandom(24))

# # === YANGILANGAN BASE_TEMPLATE (Kuchli CSS bilan) ===
# BASE_TEMPLATE = '''
# <!doctype html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Quiz Admin Panel</title>
#     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
#     <style>
#         /* Modern, high-contrast, professional theme */
#         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
#         :root{
#             --primary-color: #5b46e3; /* Kuchi rang: Mor/Ko'k */
#             --primary-color-dark: #4a34d0;
#             --secondary-color: #6c757d;
#             --bg-light: #f4f7f9; /* Eng yorug' fon */
#             --bg-surface: #ffffff; /* Kartochkalar foni */
#             --text-primary: #1f2937;
#             --text-muted: #6b7280;
#             --border-color: #e5e7eb;
#             --shadow-light: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
#             --shadow-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.08);
#         }

#         html, body {
#             height: 100%;
#             margin: 0;
#         }
#         body {
#             font-family: 'Poppins', sans-serif;
#             background: var(--bg-light);
#             color: var(--text-primary);
#             transition: background-color 0.3s, color 0.3s;
#         }

#         /* Header/Topbar */
#         .topbar {
#             background: var(--primary-color);
#             color: #fff;
#             padding: 15px 20px;
#             border-radius: 0;
#             box-shadow: var(--shadow-light);
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             margin-bottom: 25px;
#         }
#         .topbar .brand {
#             color: #fff;
#             display: flex;
#             align-items: center;
#             font-size: 1.5rem;
#             font-weight: 600;
#         }
#         .topbar .brand small {
#             color: rgba(255, 255, 255, 0.7);
#             margin-left: 10px;
#             font-weight: 400;
#         }
#         .topbar .top-actions a {
#             color: #fff;
#             border-color: rgba(255, 255, 255, 0.3);
#         }

#         .container {
#             max-width: 1400px;
#             margin: 0 auto;
#             padding: 0 20px;
#         }

#         /* Sidebar Navigation */
#         .sidebar {
#             padding-right: 20px;
#         }
#         .list-group {
#             border: none;
#             padding-right: 0;
#         }
#         .list-group-item {
#             background: transparent;
#             border: none;
#             border-radius: 8px;
#             padding: 12px 15px;
#             color: var(--text-muted);
#             font-weight: 500;
#             margin-bottom: 5px;
#             transition: background-color 0.2s, color 0.2s;
#         }
#         .list-group-item:hover, .list-group-item.active {
#             background: var(--primary-color);
#             color: #fff;
#             box-shadow: var(--shadow-light);
#         }
#         .list-group-item:hover {
#             background: #e9ecef; /* Light mode hover */
#             color: var(--primary-color-dark);
#         }
#         .list-group-item.active:hover {
#             background: var(--primary-color-dark);
#         }

#         /* Cards */
#         .card {
#             background: var(--bg-surface);
#             border: 1px solid var(--border-color);
#             border-radius: 12px;
#             padding: 20px;
#             margin-bottom: 15px;
#             transition: box-shadow 0.3s;
#             box-shadow: var(--shadow-light);
#         }
#         .card:hover {
#             box-shadow: var(--shadow-hover);
#         }

#         h4, h5 {
#             color: var(--text-primary);
#             font-weight: 600;
#             margin-bottom: 15px;
#         }
#         .small-muted {
#             color: var(--text-muted);
#         }

#         /* Tables */
#         table {
#             border-radius: 8px;
#             overflow: hidden;
#         }
#         thead th {
#             background: var(--primary-color);
#             color: #fff;
#             padding: 12px 15px;
#             text-align: left;
#             border-bottom: 1px solid var(--primary-color-dark);
#         }
#         tbody td {
#             padding: 12px 15px;
#             border-bottom: 1px solid var(--border-color);
#             background: var(--bg-surface);
#         }

#         /* Buttons */
#         .btn-primary {
#             background: var(--primary-color);
#             border-color: var(--primary-color);
#             transition: background-color 0.2s, border-color 0.2s;
#             font-weight: 500;
#             padding: 8px 15px;
#             border-radius: 6px;
#         }
#         .btn-primary:hover {
#             background: var(--primary-color-dark);
#             border-color: var(--primary-color-dark);
#         }
#         .btn-outline-secondary {
#             color: var(--secondary-color);
#             border-color: var(--secondary-color);
#         }
#         .btn-outline-secondary:hover {
#             color: #fff;
#             background: var(--secondary-color);
#         }
#         .btn-danger {
#             background-color: #dc3545;
#             border-color: #dc3545;
#         }
#         .btn-danger:hover {
#             background-color: #c82333;
#             border-color: #c82333;
#         }

#         /* Forms */
#         .form-control {
#             border: 1px solid var(--border-color);
#             border-radius: 6px;
#             padding: 10px 12px;
#             transition: border-color 0.2s, box-shadow 0.2s;
#         }
#         .form-control:focus {
#             border-color: var(--primary-color);
#             box-shadow: 0 0 0 0.25rem rgba(91, 70, 227, 0.25); /* Primary rang soya */
#         }

#         /* Utility classes */
#         .alert {
#             border-radius: 8px;
#             padding: 15px;
#         }

#         /* compact responsive */
#         @media (max-width: 992px) {
#             .container {
#                 padding: 0 15px;
#             }
#             .col-md-3.sidebar {
#                 display: none;
#             }
#             .col-md-9 {
#                 width: 100%;
#             }
#             .topbar .brand {
#                 font-size: 1.25rem;
#             }
#         }
#     </style>
# </head>
# <body class="{{ 'dark-mode' if session.get('theme')=='dark' else '' }}">
# <div class="topbar">
#     <div class="container">
#         <div class="d-flex justify-content-between align-items-center">
#             <div class="brand">
#                 <span style="font-size:24px; margin-right: 10px;">⚡</span>
#                 <span>Quiz Admin</span>
#                 <small class="small-muted d-none d-md-inline ms-2">Administration Panel</small>
#             </div>
#             <div class="top-actions d-flex align-items-center">
#                 <a href="/toggle_theme" class="btn btn-sm btn-outline-light me-2">Toggle Theme</a>
#                 <a href="/logout" class="btn btn-sm btn-outline-light">Logout</a>
#             </div>
#         </div>
#     </div>
# </div>
# <div class="container">
#     {% with messages = get_flashed_messages() %}
#         {% if messages %}
#             {% for m in messages %}
#                 <div class="alert alert-info">{{ m }}</div>
#             {% endfor %}
#         {% endif %}
#     {% endwith %}
#     <div class="row">
#         <div class="col-md-3 sidebar">
#             <div class="list-group">
#                 <a href="/" class="list-group-item list-group-item-action">Dashboard</a>
#                 <a href="/questions" class="list-group-item list-group-item-action">Questions</a>
#                 <a href="/users" class="list-group-item list-group-item-action">Users</a>
#                 <a href="/admins" class="list-group-item list-group-item-action">Admins</a>
#                 <a href="/help" class="list-group-item list-group-item-action">Help Requests</a>
#                 <a href="/users_history" class="list-group-item list-group-item-action">Users History</a>
#                 <a href="/broadcast" class="list-group-item list-group-item-action">Broadcast</a>
#             </div>
#         </div>
#         <div class="col-md-9">
#             {% block content %}{% endblock %}
#         </div>
#     </div>
#     <div class="text-center small-muted mt-4 p-3">Web admin uses token-based login. Keep token secret.</div>
# </div>
# </body>
# </html>
# '''
# # === YANGILANGAN BASE_TEMPLATE TUGADI ===

# def require_login(func):
#     def wrapper(*args, **kwargs):
#         # token via query param can log in once
#         token = request.args.get('token')
#         if token and token == ADMIN_WEB_TOKEN:
#             session['logged_in'] = True
#             session['is_owner'] = True
        
#         if not session.get('logged_in'):
#             return redirect(url_for('login', next=request.path))
#         return func(*args, **kwargs)
#     wrapper.__name__ = func.__name__ # Funksiyaning asl nomini saqlash
#     return wrapper

# def render_with_template(body_html: str):
#     """Helper to inject theme CSS and render the base template with body."""
#     tpl = BASE_TEMPLATE
#     if session.get('theme') == 'dark':
#         # === YANGILANGAN DARK_CSS ===
#         dark_css = '''
# <style>
# /* Dark Mode Overrides */
# :root {
#     --bg-light: #0d1117; /* Qorong'i fon */
#     --bg-surface: #161b22; /* Qorong'i kartochkalar */
#     --text-primary: #f0f6fc;
#     --text-muted: #8b949e;
#     --border-color: #30363d;
# }

# body {
#     background: var(--bg-light);
#     color: var(--text-primary);
# }

# .topbar {
#     background: #010409; /* Eng qorong'i tepa panel */
#     box-shadow: none;
# }
# .list-group-item {
#     color: var(--text-muted);
# }
# .list-group-item:hover {
#     background: #1a1f26;
#     color: var(--text-primary);
# }
# .list-group-item.active:hover {
#     background: var(--primary-color-dark);
# }

# .card {
#     background: var(--bg-surface);
#     border-color: var(--border-color);
#     box-shadow: none;
# }
# .card:hover {
#     box-shadow: 0 0 10px rgba(91, 70, 227, 0.15); /* Primary rang soya (dark) */
# }

# thead th {
#     background: #010409;
#     border-bottom-color: var(--border-color);
# }
# tbody td {
#     background: var(--bg-surface);
#     border-bottom-color: #1f2937;
# }

# .form-control {
#     background-color: #0d1117;
#     color: var(--text-primary);
#     border-color: #30363d;
# }
# .form-control:focus {
#     background-color: #161b22;
#     border-color: var(--primary-color);
#     box-shadow: 0 0 0 0.25rem rgba(91, 70, 227, 0.35);
# }

# .alert-info {
#     background-color: #1a253a;
#     border-color: #2b3954;
#     color: #90b8f0;
# }
# .alert-secondary {
#     background-color: #1a1f26;
#     border-color: #30363d;
#     color: #8b949e;
# }

# .btn-outline-secondary {
#     color: var(--text-muted);
#     border-color: var(--border-color);
# }
# .btn-outline-secondary:hover {
#     color: var(--text-primary);
#     background: #30363d;
# }
# </style>
# '''
#         # === YANGILANGAN DARK_CSS TUGADI ===
#     else:
#         dark_css = ''
    
#     tpl = tpl.replace('', dark_css)
#     return render_template_string(tpl.replace('{% block content %}{% endblock %}', body_html))

# def require_owner(func):
#     def wrapper(*args, **kwargs):
#         if not session.get('is_owner'):
#             flash('Faqat owner buyrug\'i')
#             return redirect(url_for('index'))
#         return func(*args, **kwargs)
#     wrapper.__name__ = func.__name__
#     return wrapper

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     next_url = request.args.get('next') or url_for('index')
#     if request.method == 'POST':
#         token = request.form.get('token')
#         if token == ADMIN_WEB_TOKEN:
#             session['logged_in'] = True
#             session['is_owner'] = True
#             return redirect(next_url)
#         flash('Invalid token')
#     return render_with_template('''
#         <div class="card p-4">
#             <h4>Login</h4>
#             <form method="post">
#                 <div class="mb-3">
#                     <label class="form-label">Admin token</label>
#                     <input name="token" class="form-control" required>
#                 </div>
#                 <button class="btn btn-primary">Login</button>
#             </form>
#         </div>
#     ''')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))

# @app.route('/toggle_theme')
# @require_login
# def toggle_theme():
#     cur = session.get('theme')
#     session['theme'] = None if cur == 'dark' else 'dark'
#     # redirect back to referring page or index
#     ref = request.headers.get('Referer') or url_for('index')
#     return redirect(ref)

# @app.route('/')
# @require_login
# def index():
#     qs = load_questions()
#     users = load_users()
#     admins = load_admins()
    
#     content = '<div class="card p-4"><h5>Overview</h5>'
#     content += f'<p>Categories: <b>{len(qs)}</b> | Users: <b>{len(users)}</b> | Admins: <b>{len(admins)}</b></p>'
#     content += '</div>'
#     return render_with_template(content)

# @app.route('/questions')
# @require_login
# def questions_index():
#     qs = load_questions()
#     items = '<h4>Savollar Kategoriyalari</h4>'

#     for cat, qlist in qs.items():
#         safe_cat = urllib.parse.quote(cat, safe='')
#         items += f"""
#         <div class="card p-3 d-flex justify-content-between align-items-center">
#             <div>
#                 <h5>{cat} <small class=\"text-muted\">({len(qlist)} savol)</small></h5>
#             </div>
#             <div>
#                 <a class=\"btn btn-sm btn-outline-primary me-2\" href=\"/questions/{safe_cat}\">Ko'rish</a>
#             </div>
#         </div>
#         """
#     # Separate actions: add question (choose existing category) or create new category
#     items += '<div class="card p-3"><a class="btn btn-primary me-2" href="/questions/new">➕ Yangi savol</a><a class="btn btn-outline-secondary" href="/categories/new">➕ Yangi kategoriya</a></div>'
#     return render_with_template(items)

# @app.route('/questions/new', methods=['GET', 'POST'])
# @require_login
# def questions_new():
#     qs = load_questions()
#     categories = list(qs.keys())
#     if request.method == 'POST':
#         selected = request.form.get('category_select')
#         if not selected:
#             flash('Iltimos, mavjud kategoriyani tanlang yoki yangi kategoriya yarating.')
#             return redirect(url_for('questions_new'))
#         category = urllib.parse.unquote(selected)
#         question = request.form['question'].strip()
#         answers = [request.form[f'ans{i}'].strip() for i in range(1,5)]
#         try:
#             correct = int(request.form['correct']) - 1
#             if correct < 0 or correct >= 4:
#                 raise ValueError()
#         except Exception:
#             flash('To\'g\'ri javob indeksida xatolik (1-4 bo\'lishi kerak)')
#             return redirect(url_for('questions_new'))
#         answers_struct = [{'text': a, 'correct': (i==correct)} for i,a in enumerate(answers)]
#         add_question(category, question, answers_struct)
#         flash(f"Savol '{category}' kategoriyasiga qo'shildi.")
#         return redirect(url_for('questions_view', category=urllib.parse.quote(category, safe='')))

#     if not categories:
#         form = "<div class='card p-3'>Hech qanday kategoriya mavjud emas. Iltimos avval <a href='/categories/new'>kategoriya yarating</a>.</div>"
#         return render_with_template(form)

#     opts = ''.join([f"<option value=\"{urllib.parse.quote(cat, safe='')}\">{cat}</option>" for cat in categories])
#     form = f"""
#         <h4>Yangi savol qo\'shish</h4>
#         <div class=\"card p-4\">
#             <form method=\"post\">
#                 <div class=\"mb-3\"><label class=\"form-label\">Kategoriya</label><select name=\"category_select\" class=\"form-control\" required>{opts}</select></div>
#                 <div class=\"mb-3\"><label class=\"form-label\">Savol</label><textarea name=\"question\" class=\"form-control\" rows=3 required></textarea></div>
#                 <div class=\"row\">
#                     <div class=\"col-md-6 mb-3\"><input name=\"ans1\" class=\"form-control\" placeholder=\"Javob 1\" required></div>
#                     <div class=\"col-md-6 mb-3\"><input name=\"ans2\" class=\"form-control\" placeholder=\"Javob 2\" required></div>
#                 </div>
#                 <div class=\"row\">
#                     <div class=\"col-md-6 mb-3\"><input name=\"ans3\" class=\"form-control\" placeholder=\"Javob 3\" required></div>
#                     <div class=\"col-md-6 mb-3\"><input name=\"ans4\" class=\"form-control\" placeholder=\"Javob 4\" required></div>
#                 </div>
#                 <div class=\"mb-3 mt-2\"><label class=\"form-label\">To\'g\'ri javob raqami (1-4)</label><input name=\"correct\" class=\"form-control\" type=\"number\" min=\"1\" max=\"4\" required></div>
#                 <button class=\"btn btn-primary\">Qo\'shish</button>
#             </form>
#         </div>
#     """
#     return render_with_template(form)


# @app.route('/categories/new', methods=['GET','POST'])
# @require_login
# def categories_new():
#     if request.method == 'POST':
#         category = request.form.get('category', '').strip()
#         if not category:
#             flash('Kategoriya nomi kiritilmadi')
#             return redirect(url_for('categories_new'))
#         path = _questions_file_path(category)
#         if os.path.exists(path):
#             flash('Kategoriya mavjud')
#             return redirect(url_for('questions_index'))
#         try:
#             with open(path, 'w', encoding='utf-8') as f:
#                 json.dump([], f, ensure_ascii=False)
#             flash('Kategoriya yaratildi')
#         except Exception:
#             flash('Xatolik')
#         return redirect(url_for('questions_index'))

#     form = '''
#       <h4>Yangi kategoriya yaratish</h4>
#       <form method='post'>
#         <div class='mb-3'><label>Kategoriya nomi</label><input name='category' class='form-control' required></div>
#         <button class='btn btn-primary'>Yaratish</button>
#       </form>
#     '''
#     return render_with_template(form)

# def _questions_file_path(category):
#     ncat = _normalize_category(category)
#     from config import DATA_DIR
#     return os.path.join(DATA_DIR, 'questions', f"{ncat}.json")

# @app.route('/questions/<category>')
# @require_login
# def questions_view(category):
#     # category may come URL-quoted
#     raw_cat = urllib.parse.unquote(category)
#     qlist = get_questions_by_category(raw_cat)
#     safe_cat = urllib.parse.quote(raw_cat, safe='')

#     content = f'<h4>Kategoriya: {raw_cat} ({len(qlist)} savol)</h4>'
    
#     for q in qlist:
#         answers_html = ''
#         for i, a in enumerate(q.get('answers',[])):
#             is_correct = 'text-success fw-bold' if a.get('correct') else 'text-muted'
#             checkmark = '✔️' if a.get('correct') else ' '
#             answers_html += f"<div><span class='{is_correct}'>{i+1}. {a['text']} {checkmark}</span></div>"
        
#         content += f"""
#         <div class='card p-3'>
#             <p class='mb-2'><b>{q.get('question')}</b></p>
#             <div class='small mt-2 mb-3'>{answers_html}</div>
#             <div class='mt-2'>
#                 <a class='btn btn-sm btn-outline-secondary me-2' href='/questions/{safe_cat}/{q['id']}/edit'>Tahrirlash</a>
#                 <a class='btn btn-sm btn-outline-danger' href='/questions/{safe_cat}/{q['id']}/delete' onclick="return confirm('O\'chirishni tasdiqlaysizmi?')">O\'chirish</a>
#             </div>
#         </div>
#         """
#     content += '<div class="card p-3 mt-3"><a class="btn btn-primary" href="/questions/new">➕ Yangi savol qo\'shish</a></div>'
#     return render_with_template(content)

# @app.route('/questions/<category>/<int:q_id>/edit', methods=['GET', 'POST'])
# @require_login
# def question_edit(category, q_id):
#     raw_cat = urllib.parse.unquote(category)
#     qlist = get_questions_by_category(raw_cat)
#     q = next((x for x in qlist if int(x.get('id'))==q_id), None)
    
#     if not q:
#         flash('Savol topilmadi')
#         return redirect(url_for('questions_view', category=raw_cat))

#     if request.method == 'POST':
#         question = request.form['question'].strip()
#         answers = [request.form[f'ans{i}'].strip() for i in range(1,5)]
#         try:
#             correct = int(request.form['correct']) - 1
#             if correct < 0 or correct >= 4:
#                 raise ValueError()
#         except Exception:
#             flash('To\'g\'ri javob raqamida xatolik')
#             return redirect(url_for('question_edit', category=category, q_id=q_id))
        
#         new_answers = [{'text': a, 'correct': (i==correct)} for i,a in enumerate(answers)]
        
#         # update
#         for i, item in enumerate(qlist):
#             if int(item.get('id'))==q_id:
#                 qlist[i]['question'] = question
#                 qlist[i]['answers'] = new_answers
#                 break
        
#         # save back
#         save_questions({raw_cat: qlist})
#         flash('Savol yangilandi')
#         return redirect(url_for('questions_view', category=category))

#     # render form
#     ans = q.get('answers', [])
#     try:
#         current_correct = next((i+1 for i,a in enumerate(ans) if a.get('correct')), 1)
#     except Exception:
#         current_correct = 1

#     form = f"""
#         <h4>Tahrirlash - {raw_cat} (ID: {q_id})</h4>
#         <div class='card p-4'>
#             <form method='post'>
#                 <div class='mb-3'><label class='form-label'>Savol</label><textarea name='question' class='form-control' rows=3 required>{q.get('question')}</textarea></div>
#                 <div class='row'>
#                     <div class='col-md-6 mb-3'><input name='ans1' class='form-control' placeholder='Javob 1' value='{ans[0]['text'] if len(ans)>0 else ''}' required></div>
#                     <div class='col-md-6 mb-3'><input name='ans2' class='form-control' placeholder='Javob 2' value='{ans[1]['text'] if len(ans)>1 else ''}' required></div>
#                 </div>
#                 <div class='row'>
#                     <div class='col-md-6 mb-3'><input name='ans3' class='form-control' placeholder='Javob 3' value='{ans[2]['text'] if len(ans)>2 else ''}' required></div>
#                     <div class='col-md-6 mb-3'><input name='ans4' class='form-control' placeholder='Javob 4' value='{ans[3]['text'] if len(ans)>3 else ''}' required></div>
#                 </div>
#                 <div class='mb-3 mt-2'><label class='form-label'>To'g'ri javob raqami (1-4)</label><input name='correct' class='form-control' type='number' min='1' max='4' value='{current_correct}' required></div>
#                 <button class='btn btn-primary'>Saqlash</button>
#             </form>
#         </div>
#     """
#     return render_with_template(form)

# @app.route('/questions/<category>/<int:q_id>/delete')
# @require_login
# def question_delete(category, q_id):
#     raw_cat = urllib.parse.unquote(category)
#     qlist = get_questions_by_category(raw_cat)
    
#     qlist = [q for q in qlist if int(q.get('id'))!=q_id]
    
#     # reassign ids
#     for idx, q in enumerate(qlist, start=1):
#         q['id'] = idx
        
#     save_questions({raw_cat: qlist})
#     flash('Savol o\'chirildi')
#     return redirect(url_for('questions_view', category=category))

# @app.route('/users')
# @require_login
# def users_index():
#     users = load_users()
#     content = '<h4>Foydalanuvchilar</h4>'
    
#     for u in users:
#         ban_status = "<span class='badge bg-danger ms-2'>Banned</span>" if u.get('is_banned') else ""
        
#         content += f"""
#         <div class='card p-3'>
#             <div class='d-flex justify-content-between align-items-center'>
#                 <div>
#                     <b>@{u.get('username','-')}</b> ({u.get('id')}) {ban_status}
#                     <div class='small-muted'>QBC: {u.get('qbc',0)} | Umumiy savollar: {u.get('total_questions',0)}</div>
#                 </div>
#                 <div>
#                     <a class='btn btn-sm btn-outline-info me-2' href='/users/{u.get('id')}'>Detail</a>
#                     """
#         # Ban/Unban tugmalari
#         if u.get('is_banned'):
#             content += f"<a class='btn btn-sm btn-success me-2' href='/users/{u.get('id')}/unban'>Unban</a>"
#         else:
#             content += f"<a class='btn btn-sm btn-danger me-2' href='/users/{u.get('id')}/ban'>Ban</a>"
            
#         # Grant QBC only visible to owner
#         if session.get('is_owner'):
#             content += f" <a class='btn btn-sm btn-primary' href='/users/{u.get('id')}/grant'>Grant QBC</a>"
            
#         content += "</div></div></div>"
        
#     return render_with_template(content)

# @app.route('/users_history')
# @require_login
# def users_history_index():
#     users = load_users()
#     content = '<h4>Foydalanuvchilar Historiyasi</h4>'
    
#     for u in users:
#         uname = u.get('username','-')
#         content += f"""
#         <div class='card p-3 d-flex justify-content-between align-items-center'>
#             <div>
#                 <b>@{uname}</b> <div class='small-muted'>{u.get('id')}</div>
#             </div>
#             <a class='btn btn-sm btn-outline-primary' href='/users_history/{u.get('id')}'>Historiyani Ko\'rish</a>
#         </div>
#         """
#     return render_with_template(content)

# @app.route('/users_history/<int:uid>', methods=['GET','POST'])
# @require_login
# def user_history_view(uid):
#     u = get_user(uid)
#     if not u:
#         flash('Foydalanuvchi topilmadi')
#         return redirect(url_for('users_history_index'))
    
#     # Handle owner-only grant from this page
#     if request.method == 'POST':
#         if not session.get('is_owner'):
#             flash('Faqat owner amalga oshirishi mumkin')
#             return redirect(url_for('user_history_view', uid=uid))
#         try:
#             amt = float(request.form.get('amount'))
#         except Exception:
#             flash('Xato miqdor')
#             return redirect(url_for('user_history_view', uid=uid))
        
#         new_qbc = u.get('qbc', 0) + amt
#         update_user(uid, qbc=new_qbc)
#         flash(f'{amt} QBC qo\'shildi')
#         return redirect(url_for('user_history_view', uid=uid))

#     hist = load_history(uid)
#     content = f"<h4>History: @{u.get('username','-')} ({uid})</h4>"
#     content += f"<div class='card p-3 mb-4'><b>QBC:</b> {u.get('qbc',0)} &nbsp; | &nbsp; <b>Total Savollar:</b> {u.get('total_questions',0)}</div>"
    
#     content += "<div class='card p-3'><h5>Chat History (oxirgi 30 kun)</h5>"
#     if not hist:
#         content += "<div class='small-muted'>Hech qanday istoriya yo\'q</div>"
#     else:
#         for h in hist[::-1]:
#             ts = h.get('ts')
#             d = h.get('direction')
#             txt = (h.get('text') or '').replace('<', '&lt;').replace('>', '&gt;')
#             label = 'Foydalanuvchi' if d == 'in' else 'Bot'
#             bg_color = 'bg-light' if d == 'in' else 'bg-secondary-subtle'
            
#             content += f"""
#             <div class='border rounded p-2 mb-2 {bg_color}'>
#                 <small class='text-muted d-block'>{ts} - <b>{label}</b></small>
#                 <div>{txt}</div>
#             </div>
#             """
#     content += "</div>"

#     # Grant form for owner
#     if session.get('is_owner'):
#         content += f"""
#         <div class='card p-3 mt-3'>
#             <h5>QBC Berish (Owner-only)</h5>
#             <form method='post'>
#                 <div class='mb-2'>
#                     <input name='amount' class='form-control' placeholder='Miqdor (masalan, 10.5)' type='number' step='any' required>
#                 </div>
#                 <button class='btn btn-primary'>Yuborish</button>
#             </form>
#         </div>
#         """
#     content += f"<div class='card p-3 mt-3'><a class='btn btn-outline-secondary' href='/users_history'>← Orqaga</a></div>"
#     return render_with_template(content)

# @app.route('/users/<int:uid>')
# @require_login
# def user_detail(uid):
#     u = get_user(uid)
#     if not u:
#         flash('Foydalanuvchi topilmadi')
#         return redirect(url_for('users_index'))

#     # help requests by user
#     reqs = [r for r in load_help_requests() if r.get('user_id') == uid]
    
#     content = f"<h4>Foydalanuvchi: @{u.get('username','-')} ({u.get('id')})</h4>"
#     content += f"""
#     <div class='card p-3 mb-4'>
#         <b>QBC:</b> {u.get('qbc',0)} &nbsp; | &nbsp; 
#         <b>Umumiy Savollar:</b> {u.get('total_questions',0)} &nbsp; | &nbsp; 
#         <b>To'g'ri Javoblar:</b> {u.get('correct_answers',0)}
#     </div>
#     """
    
#     content += "<div class='card p-3'><h5>Urinib ko'rilgan savollar (kategoriya bo'yicha)</h5>"
#     if not u.get('attempted_questions'):
#         content += "<div class='small-muted'>Urinishlar yo'q</div>"
#     else:
#         for cat, lst in u.get('attempted_questions', {}).items():
#             content += f"<div><b>{cat}:</b> {', '.join([str(x) for x in lst])}</div>"
#     content += "</div>"
    
#     # Chat history
#     content += "<div class='card p-3 mt-3'><h5>Chat History (oxirgi 200 ta xabar)</h5>"
#     hist = u.get('chat_history', [])
#     if not hist:
#         content += "<div class='small-muted'>Chat historiyasi yo'q</div>"
#     else:
#         for h in hist[-200:][::-1]:
#             ts = h.get('ts')
#             d = h.get('direction')
#             txt = (h.get('text') or '').replace('<', '&lt;').replace('>', '&gt;')
#             label = 'Foydalanuvchi' if d == 'in' else 'Bot'
#             bg_color = 'bg-light' if d == 'in' else 'bg-secondary-subtle'
            
#             content += f"""
#             <div class='border rounded p-2 mb-2 {bg_color}'>
#                 <small class='text-muted d-block'>{ts} - <b>{label}</b></small>
#                 <div>{txt}</div>
#             </div>
#             """
#     content += "</div>"
    
#     content += "<div class='card p-3 mt-3'><h5>Yordam So'rovlari</h5>"
#     if not reqs:
#         content += "<div class='small-muted'>Yordam so'rovlari yo'q</div>"
    
#     for r in reqs:
#         status_badge = 'bg-success' if r.get('admin_reply') else 'bg-warning text-dark'
#         status_text = 'Javob berilgan' if r.get('admin_reply') else 'Javob kutilmoqda'
        
#         content += f"""
#         <div class='border rounded p-3 mb-3'>
#             <div class='d-flex justify-content-between'>
#                 <b>#{r.get('id')}</b>
#                 <span class='badge {status_badge}'>{status_text}</span>
#             </div>
#             <div class='small-muted mb-2'>{r.get('created_at')}</div>
#             <p>{r.get('text')}</p>
#             """
#         if r.get('admin_reply'):
#             content += f"<div class='alert alert-secondary'>Admin javobi: {r.get('admin_reply')}</div>"
            
#         content += f"<a class='btn btn-sm btn-primary' href='/help/{r.get('id')}/reply'>Javob yozish / Ko'rish</a></div>"
        
#     content += "</div>"
    
#     content += f"<div class='card p-3 mt-3'><a class='btn btn-outline-secondary' href='/users'>← Orqaga</a></div>"
#     return render_with_template(content)

# @app.route('/users/<int:uid>/ban')
# @require_login
# def user_ban(uid):
#     u = get_user(uid)
#     if not u:
#         flash('Foydalanuvchi topilmadi')
#         return redirect(url_for('users_index'))
#     update_user(uid, is_banned=True)
#     flash('Foydalanuvchi banlandi')
#     return redirect(url_for('users_index'))

# @app.route('/users/<int:uid>/unban')
# @require_login
# def user_unban(uid):
#     update_user(uid, is_banned=False)
#     flash('Foydalanuvchi bandan chiqarildi')
#     return redirect(url_for('users_index'))

# @app.route('/users/<int:uid>/grant', methods=['GET','POST'])
# @require_login
# @require_owner
# def user_grant(uid):
#     u = get_user(uid)
#     if not u:
#         flash('Foydalanuvchi topilmadi')
#         return redirect(url_for('users_index'))
    
#     if request.method == 'POST':
#         try:
#             amt = float(request.form.get('amount'))
#         except Exception:
#             flash('Xato miqdor. Raqam kiriting.')
#             return redirect(url_for('user_grant', uid=uid))
        
#         new_qbc = u.get('qbc',0) + amt
#         update_user(uid, qbc=new_qbc)
#         flash(f'{amt} QBC qo\'shildi. Yangi balans: {new_qbc}')
#         return redirect(url_for('users_index'))
    
#     form = f"""
#         <h4>{u.get('username','-')} ga QBC berish</h4>
#         <div class='card p-4'>
#             <form method='post'>
#                 <div class='mb-3'>
#                     <label class='form-label'>Miqdor</label>
#                     <input name='amount' class='form-control' type='number' step='any' placeholder='Masalan, 50.0' required>
#                 </div>
#                 <button class='btn btn-primary'>Yuborish</button>
#             </form>
#         </div>
#     """
#     return render_with_template(form)

# @app.route('/admins', methods=['GET','POST'])
# @require_login
# def admins_index():
#     admins = load_admins()
    
#     if request.method == 'POST':
#         # only owner can add admins via web
#         if not session.get('is_owner'):
#             flash('Faqat owner yangi admin qo\'shishi mumkin')
#             return redirect(url_for('admins_index'))
#         try:
#             new_id = int(request.form.get('user_id'))
#             level = request.form.get('level')
#             add_admin(new_id, level=level)
#             flash('Admin qo\'shildi')
#         except Exception:
#             flash('Xatolik! ID raqam ekanligiga ishonch hosil qiling.')
#         return redirect(url_for('admins_index'))
        
#     content = '<h4>Admins</h4>'
    
#     for a in admins:
#         remove_btn = ''
#         if session.get('is_owner'):
#             remove_btn = f"<a class='btn btn-sm btn-outline-danger ms-2' href='/admins/{a.get('id')}/remove'>O\'chirish</a>"
            
#         content += f"""
#         <div class='card p-3 d-flex justify-content-between align-items-center'>
#             <div><b>{a.get('id')}</b> - {a.get('level')}</div>
#             {remove_btn}
#         </div>
#         """
    
#     if session.get('is_owner'):
#         content += '''
#         <div class='card p-3 mt-3'>
#             <h5>Yangi admin qo\'shish (Owner-only)</h5>
#             <form method='post'>
#                 <div class='mb-2'><input name='user_id' class='form-control' placeholder='User ID' type='number' required></div>
#                 <div class='mb-2'>
#                     <select name='level' class='form-control'>
#                         <option value='question_admin'>Question Admin</option>
#                         <option value='user_admin'>User Admin</option>
#                         <option value='full'>Full Admin</option>
#                     </select>
#                 </div>
#                 <button class='btn btn-primary'>Qo\'shish</button>
#             </form>
#         </div>
#         '''
        
#     return render_with_template(content)

# @app.route('/admins/<int:uid>/remove')
# @require_login
# @require_owner
# def admin_remove(uid):
#     remove_admin(uid)
#     flash('Admin olib tashlandi')
#     return redirect(url_for('admins_index'))

# @app.route('/help')
# @require_login
# def help_index():
#     reqs = load_help_requests()
#     content = '<h4>Yordam So\'rovlari</h4>'
    
#     for r in reqs:
#         status_badge = 'bg-success' if r.get('admin_reply') else 'bg-warning text-dark'
#         status_text = 'Javob berilgan' if r.get('admin_reply') else 'Yangi'
        
#         content += f"""
#         <div class='card p-3'>
#             <div class='d-flex justify-content-between'>
#                 <b>{r.get('id')}. @{r.get('username','-')} ({r.get('user_id')})</b>
#                 <span class='badge {status_badge}'>{status_text}</span>
#             </div>
#             <div class='small-muted mb-2'>{r.get('created_at')}</div>
#             <p>{r.get('text')}</p>
#             """
#         if r.get('admin_reply'):
#             content += f"<div class='alert alert-secondary'>Admin javobi: {r.get('admin_reply')}</div>"
            
#         content += f"<a class='btn btn-sm btn-primary' href='/help/{r.get('id')}/reply'>Javob yozish</a></div>"
        
#     return render_with_template(content)

# @app.route('/help/<int:rid>/reply', methods=['GET','POST'])
# @require_login
# def help_reply(rid):
#     reqs = load_help_requests()
#     req = next((x for x in reqs if x.get('id')==rid), None)
    
#     if not req:
#         flash('So\'rov topilmadi')
#         return redirect(url_for('help_index'))

#     if request.method == 'POST':
#         text = request.form.get('reply')
#         update_help_request(rid, admin_reply=text, status='answered')
        
#         # try to notify user via Telegram
#         try:
#             if BOT_TOKEN:
#                 url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
#                 data = json.dumps({'chat_id': req.get('user_id'), 'text': f"Admin javobi:\n{text}"}).encode('utf-8')
#                 requ = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
#                 urllib.request.urlopen(requ)
#         except Exception:
#             pass
            
#         flash('Javob saqlandi va yuborildi (agar bot ishlayotgan bo\'lsa)')
#         return redirect(url_for('help_index'))

#     form = f"""
#         <h4>Javob yozish - {req.get('username','-')}</h4>
#         <div class='card p-4'>
#             <div class='mb-3'><b>So'rov matni:</b> <p class='alert alert-info'>{req.get('text')}</p></div>
#             <form method='post'>
#                 <div class='mb-3'>
#                     <label class='form-label'>Javobingiz</label>
#                     <textarea name='reply' class='form-control' rows=4 required>{req.get('admin_reply', '')}</textarea>
#                 </div>
#                 <button class='btn btn-primary'>Yuborish</button>
#             </form>
#         </div>
#     """
#     return render_with_template(form)

# @app.route('/broadcast', methods=['GET','POST'])
# @require_login
# def broadcast():
#     if request.method == 'POST':
#         if not session.get('is_owner'):
#             flash('Faqat owner broadcast yuborishi mumkin')
#             return redirect(url_for('index'))
            
#         text = request.form.get('text')
#         users = load_users()
#         sent = 0
        
#         for u in users:
#             try:
#                 if BOT_TOKEN:
#                     url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
#                     data = json.dumps({'chat_id': u.get('id'), 'text': text, 'parse_mode': 'HTML'}).encode('utf-8')
#                     requ = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
#                     urllib.request.urlopen(requ)
#                     sent += 1
#             except Exception:
#                 continue
                
#         flash(f'Broadcast yuborildi: {sent} ta foydalanuvchiga')
#         return redirect(url_for('index'))
        
#     form = '''
#         <h4>Broadcast (Barcha foydalanuvchilarga xabar yuborish)</h4>
#         <div class='card p-4'>
#             <form method='post'>
#                 <div class='mb-3'>
#                     <label class='form-label'>Xabar matni (HTML formatini qo\'llab-quvvatlaydi)</label>
#                     <textarea name='text' class='form-control' rows=4 required></textarea>
#                 </div>
#                 <button class='btn btn-danger'>Yuborish</button>
#             </form>
#         </div>
#     '''
#     return render_with_template(form)

# if __name__ == '__main__':
#     # Bu qism faqat lokal ishga tushirish uchun
#     # Real muhitda gunicorn/uWSGI kabi serverlardan foydalanish tavsiya etiladi
#     app.run(host='127.0.0.1', port=5001, debug=True)




from flask import Flask, request, render_template_string, redirect, url_for, session, flash
# 'utils' va 'config' modullarini import qilish kerak.
# Ishlash uchun ular mavjudligiga va kerakli funksiyalarga ega ekanligiga ishonch hosil qiling.
from utils import add_question, _normalize_category, load_questions, get_questions_by_category, save_questions, load_users, get_user, update_user, load_admins, add_admin, remove_admin, load_help_requests, update_help_request, load_history
from config import ADMIN_WEB_TOKEN, BOT_TOKEN, DATA_DIR # DATA_DIR configdan import qilinishi kerak
import os
import json
import urllib.parse
from datetime import datetime

# Agar DATA_DIR config.py da bo'lmasa, quyidagicha belgilash kerak:
# DATA_DIR = os.path.join(os.path.dirname(__file__), 'data') # Masalan

app = Flask(__name__)
# WEB_ADMIN_SECRET ni o'rnating yoki tasodifiy kalitdan foydalaning
app.secret_key = os.getenv('WEB_ADMIN_SECRET', os.urandom(24))

# === YORDAMCHI FUNKSIYA: Savollar fayl manzilini aniqlash ===
def _questions_file_path(category):
    """Kategoriya nomi asosida savollar fayliga yo'lni qaytaradi."""
    ncat = _normalize_category(category)
    return os.path.join(DATA_DIR, 'questions', f"{ncat}.json")


# === YANGILANGAN BASE_TEMPLATE (Dark Mode, Responsive, Optimallashtirilgan) ===
BASE_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz Admin Panel</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        /* Modern, high-contrast, professional theme */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        :root{
            --primary-color: #5b46e3; /* Kuchi rang: Mor/Ko'k */
            --primary-color-dark: #4a34d0;
            --secondary-color: #6c757d;
            --bg-light: #f4f7f9; /* Eng yorug' fon */
            --bg-surface: #ffffff; /* Kartochkalar foni */
            --text-primary: #1f2937;
            --text-muted: #6b7280;
            --border-color: #e5e7eb;
            --shadow-light: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
            --shadow-hover: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.08);
            --info-light: #d0e8ff;
            --info-dark: #007bff;
            --danger-color: #dc3545;
            --success-color: #28a745;
        }

        html, body {
            height: 100%;
            margin: 0;
        }
        body {
            font-family: 'Poppins', sans-serif;
            background: var(--bg-light);
            color: var(--text-primary);
            transition: background-color 0.3s, color 0.3s;
        }

        /* Header/Topbar */
        .topbar {
            background: var(--primary-color);
            color: #fff;
            padding: 15px 20px;
            border-radius: 0;
            box-shadow: var(--shadow-light);
            margin-bottom: 25px;
        }
        .topbar .brand {
            color: #fff;
            display: flex;
            align-items: center;
            font-size: 1.5rem;
            font-weight: 600;
        }
        .topbar .brand small {
            color: rgba(255, 255, 255, 0.7);
            margin-left: 10px;
            font-weight: 400;
        }
        .topbar .top-actions a {
            color: #fff;
            border-color: rgba(255, 255, 255, 0.3);
            font-weight: 500;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }

        /* Sidebar Navigation */
        .sidebar-container {
            padding-right: 20px;
        }
        .list-group {
            border: none;
            padding-right: 0;
        }
        .list-group-item {
            background: transparent;
            border: none;
            border-radius: 8px;
            padding: 12px 15px;
            color: var(--text-muted);
            font-weight: 500;
            margin-bottom: 5px;
            transition: background-color 0.2s, color 0.2s, box-shadow 0.2s;
        }
        .list-group-item:hover {
            background: #e9ecef; /* Light mode hover */
            color: var(--primary-color-dark);
        }
        .list-group-item.active {
            background: var(--primary-color);
            color: #fff;
            box-shadow: var(--shadow-light);
        }
        .list-group-item.active:hover {
            background: var(--primary-color-dark);
        }

        /* Cards */
        .card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: box-shadow 0.3s, background-color 0.3s, border-color 0.3s;
            box-shadow: var(--shadow-light);
        }
        .card:hover {
            box-shadow: var(--shadow-hover);
        }
        .card-title-link:hover {
            text-decoration: underline;
            color: var(--primary-color);
        }

        h4, h5 {
            color: var(--text-primary);
            font-weight: 600;
            margin-bottom: 15px;
        }
        .small-muted {
            color: var(--text-muted);
        }

        /* Tables */
        .table-responsive {
            border-radius: 8px;
            overflow-x: auto;
            border: 1px solid var(--border-color);
        }
        .table {
            margin-bottom: 0;
        }
        .table thead th {
            background: var(--primary-color);
            color: #fff;
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--primary-color-dark);
        }
        .table tbody tr:last-child td {
            border-bottom: none;
        }
        .table tbody td {
            padding: 12px 15px;
            border-bottom: 1px solid var(--border-color);
            background: var(--bg-surface);
            vertical-align: middle;
        }
        .table-striped tbody tr:nth-of-type(odd) {
            background-color: var(--bg-light);
        }


        /* Forms */
        .form-control {
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 10px 12px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .form-control:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.25rem rgba(91, 70, 227, 0.25); /* Primary rang soya */
        }
        
        /* Utility classes */
        .alert {
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 25px;
        }
        .alert-info {
             background-color: var(--info-light);
             color: var(--info-dark);
             border-color: var(--info-dark);
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border-color: #f5c6cb;
        }
        .alert-secondary {
            background-color: #e2e3e5;
            color: #383d41;
            border-color: #d6d8db;
        }


        /* Responsive Breakpoint */
        @media (max-width: 992px) {
            .container {
                padding: 0 15px;
            }
            .sidebar-container {
                display: none; /* Hide sidebar on mobile/tablet, rely on top nav */
                padding-right: 0;
            }
            .col-md-9 {
                width: 100%;
            }
            .topbar .brand {
                font-size: 1.25rem;
            }
        }
        
        /* === DARK MODE STYLES === */
        body.dark-mode {
            /* Dark Mode Overrides */
            --bg-light: #0d1117; /* Qorong'i fon */
            --bg-surface: #161b22; /* Qorong'i kartochkalar */
            --text-primary: #f0f6fc;
            --text-muted: #8b949e;
            --border-color: #30363d;
            --info-light: #1a253a;
            --info-dark: #90b8f0;
        }

        .dark-mode .topbar {
            background: #010409; /* Eng qorong'i tepa panel */
            box-shadow: none;
        }

        .dark-mode .list-group-item:hover {
            background: #1a1f26;
            color: var(--text-primary);
        }

        .dark-mode .card {
            background: var(--bg-surface);
            border-color: var(--border-color);
            box-shadow: none;
        }
        .dark-mode .card:hover {
            box-shadow: 0 0 10px rgba(91, 70, 227, 0.15); /* Primary rang soya (dark) */
        }
        
        .dark-mode .table thead th {
            background: #010409;
            border-bottom-color: var(--border-color);
        }
        .dark-mode .table tbody td {
            background: var(--bg-surface);
            border-bottom-color: #1f2937;
        }
        .dark-mode .table-striped tbody tr:nth-of-type(odd) {
            background-color: #0d1117;
        }

        .dark-mode .form-control {
            background-color: #0d1117;
            color: var(--text-primary);
            border-color: #30363d;
        }
        .dark-mode .form-control:focus {
            background-color: #161b22;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.25rem rgba(91, 70, 227, 0.35);
        }

        .dark-mode .alert-info {
            background-color: var(--info-light);
            border-color: #2b3954;
            color: var(--info-dark);
        }
        .dark-mode .alert-danger {
            background-color: #32171c;
            color: #dc3545;
            border-color: #581d24;
        }
        .dark-mode .alert-secondary {
            background-color: #1a1f26;
            color: #8b949e;
            border-color: #30363d;
        }
        .dark-mode .bg-light { /* Chat history user message */
            background-color: #30363d !important;
            color: var(--text-primary) !important;
        }
        .dark-mode .bg-secondary-subtle { /* Chat history bot message */
             background-color: #1a1f26 !important;
             color: var(--text-primary) !important;
        }
        .dark-mode .border {
            border-color: #30363d !important;
        }
        
        .dark-mode .text-dark {
             color: var(--text-primary) !important;
        }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Sidebar itemini aktiv qilish
            const path = window.location.pathname;
            const links = document.querySelectorAll('.list-group-item-action');
            links.forEach(link => {
                const linkHref = link.getAttribute('href');
                // Dashboard uchun maxsus tekshirish
                if (linkHref === '/' && path === '/') {
                    link.classList.add('active');
                } 
                // Boshqa barcha sahifalar uchun
                else if (linkHref !== '/' && path.startsWith(linkHref)) {
                    link.classList.add('active');
                }
            });
        });
    </script>
</head>
<body class="{{ 'dark-mode' if session.get('theme')=='dark' else '' }}">
<div class="topbar">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center">
            <div class="brand">
                <span class="material-icons" style="font-size:32px; margin-right: 10px;">quiz</span>
                <span>Quiz Admin</span>
                <small class="small-muted d-none d-md-inline ms-2">Administration Panel</small>
            </div>
            <div class="top-actions d-flex align-items-center">
                <a href="/toggle_theme" class="btn btn-sm btn-outline-light me-2">
                    <span class="material-icons" style="font-size:16px; margin-right: 5px; vertical-align: middle;">{{ 'light_mode' if session.get('theme')=='dark' else 'dark_mode' }}</span> 
                    Theme
                </a>
                <a href="/logout" class="btn btn-sm btn-outline-light">
                    <span class="material-icons" style="font-size:16px; margin-right: 5px; vertical-align: middle;">logout</span> 
                    Logout
                </a>
            </div>
        </div>
    </div>
</div>
<div class="container">
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for m in messages %}
                <div class="alert alert-info">{{ m }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    <div class="row">
        <div class="col-md-3 sidebar-container">
            <div class="list-group">
                <a href="/" class="list-group-item list-group-item-action">Dashboard</a>
                <a href="/questions" class="list-group-item list-group-item-action">Questions</a>
                <a href="/users" class="list-group-item list-group-item-action">Users</a>
                <a href="/admins" class="list-group-item list-group-item-action">Admins</a>
                <a href="/help" class="list-group-item list-group-item-action">Help Requests</a>
                <a href="/users_history" class="list-group-item list-group-item-action">Users History</a>
                <a href="/broadcast" class="list-group-item list-group-item-action">Broadcast</a>
            </div>
        </div>
        <div class="col-md-9">
            {% block content %}{% endblock %}
        </div>
    </div>
    <div class="text-center small-muted mt-5 p-3">Quiz Admin Panel | Optimised for all devices.</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''
# === YANGILANGAN BASE_TEMPLATE TUGADI ===

# === SECURITY FUNKSIYALARI ===
def require_login(func):
    def wrapper(*args, **kwargs):
        # token via query param can log in once
        token = request.args.get('token')
        if token and token == ADMIN_WEB_TOKEN:
            session['logged_in'] = True
            session['is_owner'] = True
        
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__ # Funksiyaning asl nomini saqlash
    return wrapper

def render_with_template(body_html: str):
    """Helper to inject theme CSS and render the base template with body."""
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', body_html))

def require_owner(func):
    def wrapper(*args, **kwargs):
        if not session.get('is_owner'):
            flash('Faqat owner buyrug\'i')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or url_for('index')
    if request.method == 'POST':
        token = request.form.get('token')
        if token == ADMIN_WEB_TOKEN:
            session['logged_in'] = True
            session['is_owner'] = True
            flash('Muvaffaqiyatli kirish!')
            return redirect(next_url)
        flash('Invalid token')
    return render_with_template('''
        <div class="card p-4 mx-auto" style="max-width: 400px;">
            <h4 class="text-center">🔑 Admin Login</h4>
            <form method="post">
                <div class="mb-3">
                    <label class="form-label">Admin Token</label>
                    <input name="token" class="form-control" type="password" required>
                </div>
                <button class="btn btn-primary w-100">Kirish</button>
            </form>
        </div>
    ''')

@app.route('/logout')
def logout():
    session.clear()
    flash('Siz tizimdan chiqdingiz.')
    return redirect(url_for('login'))

@app.route('/toggle_theme')
@require_login
def toggle_theme():
    cur = session.get('theme')
    session['theme'] = None if cur == 'dark' else 'dark'
    # redirect back to referring page or index
    ref = request.headers.get('Referer') or url_for('index')
    return redirect(ref)

# === ASOSIY ROUTING FUNKSIYALARI ===
@app.route('/')
@require_login
def index():
    qs = load_questions()
    users = load_users()
    admins = load_admins()
    
    total_questions = sum(len(qlist) for qlist in qs.values())
    
    content = '''
    <div class="row">
        <div class="col-md-4">
            <div class="card p-4 text-center">
                <h5 class="small-muted">Foydalanuvchilar</h5>
                <h1 class="text-primary">{}</h1>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card p-4 text-center">
                <h5 class="small-muted">Savollar Soni</h5>
                <h1 class="text-primary">{}</h1>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card p-4 text-center">
                <h5 class="small-muted">Adminlar</h5>
                <h1 class="text-primary">{}</h1>
            </div>
        </div>
    </div>
    <div class="card p-4 mt-3">
        <h5>Kategoriyalar</h5>
        <ul class="list-group list-group-flush">
            {}
        </ul>
    </div>
    '''.format(
        len(users), 
        total_questions, 
        len(admins), 
        ''.join([f'<li class="list-group-item d-flex justify-content-between"><span>{cat}</span><span class="badge bg-secondary">{len(qlist)} savol</span></li>' for cat, qlist in qs.items()])
    )
    return render_with_template(content)

@app.route('/questions')
@require_login
def questions_index():
    qs = load_questions()
    items = '<h4>Savollar Kategoriyalari</h4>'

    for cat, qlist in qs.items():
        safe_cat = urllib.parse.quote(cat, safe='')
        items += f"""
        <div class="card p-3 d-flex flex-row justify-content-between align-items-center">
            <div>
                <h5>{cat} <small class="text-muted">({len(qlist)} savol)</small></h5>
            </div>
            <div>
                <a class="btn btn-sm btn-outline-primary me-2" href="/questions/{safe_cat}">Ko'rish</a>
            </div>
        </div>
        """
    # Separate actions: add question (choose existing category) or create new category
    items += '<div class="card p-3"><a class="btn btn-primary me-2" href="/questions/new">➕ Yangi savol</a><a class="btn btn-outline-secondary" href="/categories/new">➕ Yangi kategoriya</a></div>'
    return render_with_template(items)

@app.route('/questions/new', methods=['GET', 'POST'])
@require_login
def questions_new():
    qs = load_questions()
    categories = list(qs.keys())
    if request.method == 'POST':
        selected = request.form.get('category_select')
        if not selected:
            flash('Iltimos, mavjud kategoriyani tanlang yoki yangi kategoriya yarating.')
            return redirect(url_for('questions_new'))
        category = urllib.parse.unquote(selected)
        question = request.form['question'].strip()
        answers = [request.form[f'ans{i}'].strip() for i in range(1,5)]
        try:
            correct = int(request.form['correct']) - 1
            if correct < 0 or correct >= 4:
                raise ValueError()
        except Exception:
            flash('To\'g\'ri javob indeksida xatolik (1-4 bo\'lishi kerak)')
            return redirect(url_for('questions_new'))
        answers_struct = [{'text': a, 'correct': (i==correct)} for i,a in enumerate(answers)]
        add_question(category, question, answers_struct)
        flash(f"Savol '{category}' kategoriyasiga qo'shildi.")
        return redirect(url_for('questions_view', category=urllib.parse.quote(category, safe='')))

    if not categories:
        form = "<div class='card p-3'>Hech qanday kategoriya mavjud emas. Iltimos avval <a href='/categories/new'>kategoriya yarating</a>.</div>"
        return render_with_template(form)

    opts = ''.join([f"<option value=\"{urllib.parse.quote(cat, safe='')}\">{cat}</option>" for cat in categories])
    form = f"""
        <h4>Yangi savol qo'shish</h4>
        <div class="card p-4">
            <form method="post">
                <div class="mb-3"><label class="form-label">Kategoriya</label><select name="category_select" class="form-control" required>{opts}</select></div>
                <div class="mb-3"><label class="form-label">Savol</label><textarea name="question" class="form-control" rows=3 required></textarea></div>
                <div class="row">
                    <div class="col-md-6 mb-3"><input name="ans1" class="form-control" placeholder="Javob 1" required></div>
                    <div class="col-md-6 mb-3"><input name="ans2" class="form-control" placeholder="Javob 2" required></div>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3"><input name="ans3" class="form-control" placeholder="Javob 3" required></div>
                    <div class="col-md-6 mb-3"><input name="ans4" class="form-control" placeholder="Javob 4" required></div>
                </div>
                <div class="mb-3 mt-2"><label class="form-label">To'g'ri javob raqami (1-4)</label><input name="correct" class="form-control" type="number" min="1" max="4" required></div>
                <button class="btn btn-primary">Qo'shish</button>
            </form>
        </div>
    """
    return render_with_template(form)


@app.route('/categories/new', methods=['GET','POST'])
@require_login
def categories_new():
    if request.method == 'POST':
        category = request.form.get('category', '').strip()
        if not category:
            flash('Kategoriya nomi kiritilmadi')
            return redirect(url_for('categories_new'))
        
        try:
            path = _questions_file_path(category)
        except NameError:
             flash('DATA_DIR config faylida topilmadi. Kategoriya yaratilmadi.')
             return redirect(url_for('questions_index'))

        if os.path.exists(path):
            flash('Kategoriya mavjud')
            return redirect(url_for('questions_index'))
        try:
            # Faylni yaratish va bo'sh JSON [] yozish
            with open(path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False)
            flash(f'Kategoriya "{category}" yaratildi.')
        except Exception as e:
            flash(f'Xatolik: {e}')
        return redirect(url_for('questions_index'))

    form = '''
      <h4>Yangi kategoriya yaratish</h4>
      <div class='card p-4'>
          <form method='post'>
              <div class='mb-3'><label class='form-label'>Kategoriya nomi</label><input name='category' class='form-control' required></div>
              <button class='btn btn-primary'>Yaratish</button>
          </form>
      </div>
    '''
    return render_with_template(form)


@app.route('/questions/<category>')
@require_login
def questions_view(category):
    # category may come URL-quoted
    raw_cat = urllib.parse.unquote(category)
    qlist = get_questions_by_category(raw_cat)
    safe_cat = urllib.parse.quote(raw_cat, safe='')

    content = f'<h4>Kategoriya: {raw_cat} ({len(qlist)} savol)</h4>'
    
    for q in qlist:
        answers_html = ''
        for i, a in enumerate(q.get('answers',[])):
            is_correct = 'text-success fw-bold' if a.get('correct') else 'text-muted'
            checkmark = '✔️' if a.get('correct') else ' '
            answers_html += f"<div><span class='{is_correct}'>{i+1}. {a['text']} {checkmark}</span></div>"
        
        content += f"""
        <div class='card p-3'>
            <p class='mb-2'><b>ID {q.get('id')}: {q.get('question')}</b></p>
            <div class='small mt-2 mb-3'>{answers_html}</div>
            <div class='mt-2'>
                <a class='btn btn-sm btn-outline-secondary me-2' href='/questions/{safe_cat}/{q['id']}/edit'>Tahrirlash</a>
                <a class='btn btn-sm btn-danger' href='/questions/{safe_cat}/{q['id']}/delete' onclick="return confirm('O\'chirishni tasdiqlaysizmi?')">O'chirish</a>
            </div>
        </div>
        """
    content += '<div class="card p-3 mt-3"><a class="btn btn-primary" href="/questions/new">➕ Yangi savol qo\'shish</a></div>'
    return render_with_template(content)

@app.route('/questions/<category>/<int:q_id>/edit', methods=['GET', 'POST'])
@require_login
def question_edit(category, q_id):
    raw_cat = urllib.parse.unquote(category)
    qlist = get_questions_by_category(raw_cat)
    q = next((x for x in qlist if int(x.get('id'))==q_id), None)
    
    if not q:
        flash('Savol topilmadi')
        return redirect(url_for('questions_view', category=category))

    if request.method == 'POST':
        question = request.form['question'].strip()
        answers = [request.form[f'ans{i}'].strip() for i in range(1,5)]
        try:
            correct = int(request.form['correct']) - 1
            if correct < 0 or correct >= 4:
                raise ValueError()
        except Exception:
            flash('To\'g\'ri javob raqamida xatolik')
            return redirect(url_for('question_edit', category=category, q_id=q_id))
        
        new_answers = [{'text': a, 'correct': (i==correct)} for i,a in enumerate(answers)]
        
        # update
        for i, item in enumerate(qlist):
            if int(item.get('id'))==q_id:
                qlist[i]['question'] = question
                qlist[i]['answers'] = new_answers
                break
        
        # save back
        save_questions({raw_cat: qlist})
        flash('Savol yangilandi')
        return redirect(url_for('questions_view', category=category))

    # render form
    ans = q.get('answers', [])
    try:
        current_correct = next((i+1 for i,a in enumerate(ans) if a.get('correct')), 1)
    except Exception:
        current_correct = 1

    form = f"""
        <h4>Tahrirlash - {raw_cat} (ID: {q_id})</h4>
        <div class='card p-4'>
            <form method='post'>
                <div class='mb-3'><label class='form-label'>Savol</label><textarea name='question' class='form-control' rows=3 required>{q.get('question')}</textarea></div>
                <div class='row'>
                    <div class='col-md-6 mb-3'><input name='ans1' class='form-control' placeholder='Javob 1' value='{ans[0]['text'] if len(ans)>0 else ''}' required></div>
                    <div class='col-md-6 mb-3'><input name='ans2' class='form-control' placeholder='Javob 2' value='{ans[1]['text'] if len(ans)>1 else ''}' required></div>
                </div>
                <div class='row'>
                    <div class='col-md-6 mb-3'><input name='ans3' class='form-control' placeholder='Javob 3' value='{ans[2]['text'] if len(ans)>2 else ''}' required></div>
                    <div class='col-md-6 mb-3'><input name='ans4' class='form-control' placeholder='Javob 4' value='{ans[3]['text'] if len(ans)>3 else ''}' required></div>
                </div>
                <div class='mb-3 mt-2'><label class='form-label'>To'g'ri javob raqami (1-4)</label><input name='correct' class='form-control' type='number' min='1' max='4' value='{current_correct}' required></div>
                <button class='btn btn-primary'>Saqlash</button>
            </form>
        </div>
    """
    return render_with_template(form)

@app.route('/questions/<category>/<int:q_id>/delete')
@require_login
def question_delete(category, q_id):
    raw_cat = urllib.parse.unquote(category)
    qlist = get_questions_by_category(raw_cat)
    
    initial_count = len(qlist)
    qlist = [q for q in qlist if int(q.get('id'))!=q_id]
    
    if len(qlist) == initial_count:
        flash('Savol topilmadi.', 'error')
        return redirect(url_for('questions_view', category=category))
        
    # reassign ids
    for idx, q in enumerate(qlist, start=1):
        q['id'] = idx
        
    save_questions({raw_cat: qlist})
    flash('Savol o\'chirildi')
    return redirect(url_for('questions_view', category=category))

@app.route('/users')
@require_login
def users_index():
    users = load_users()
    content = '<h4>Foydalanuvchilar</h4>'
    
    for u in users:
        ban_status = "<span class='badge bg-danger ms-2'>Banned</span>" if u.get('is_banned') else ""
        
        content += f"""
        <div class='card p-3'>
            <div class='d-flex justify-content-between align-items-center'>
                <div>
                    <a href='/users/{u.get('id')}' class='card-title-link'><b>@{u.get('username','-')}</b> ({u.get('id')})</a> {ban_status}
                    <div class='small-muted'>QBC: {u.get('qbc',0)} | Umumiy savollar: {u.get('total_questions',0)}</div>
                </div>
                <div class='d-flex flex-wrap gap-2'>
                    """
        # Ban/Unban tugmalari
        if u.get('is_banned'):
            content += f"<a class='btn btn-sm btn-success' href='/users/{u.get('id')}/unban'>Unban</a>"
        else:
            content += f"<a class='btn btn-sm btn-danger' href='/users/{u.get('id')}/ban'>Ban</a>"
            
        # Grant QBC only visible to owner
        if session.get('is_owner'):
            content += f" <a class='btn btn-sm btn-primary ms-2' href='/users/{u.get('id')}/grant'>Grant QBC</a>"
            
        content += "</div></div></div>"
        
    return render_with_template(content)

@app.route('/users_history')
@require_login
def users_history_index():
    users = load_users()
    content = '<h4>Foydalanuvchilar Historiyasi (Chat History)</h4>'
    
    for u in users:
        uname = u.get('username','-')
        content += f"""
        <div class='card p-3 d-flex justify-content-between align-items-center'>
            <div>
                <b>@{uname}</b> <div class='small-muted'>{u.get('id')}</div>
            </div>
            <a class='btn btn-sm btn-outline-primary' href='/users_history/{u.get('id')}'>Historiyani Ko\'rish</a>
        </div>
        """
    return render_with_template(content)

@app.route('/users_history/<int:uid>', methods=['GET','POST'])
@require_login
def user_history_view(uid):
    u = get_user(uid)
    if not u:
        flash('Foydalanuvchi topilmadi')
        return redirect(url_for('users_history_index'))
    
    # Handle owner-only grant from this page (yangi QBC berish maydoni)
    if request.method == 'POST' and session.get('is_owner'):
        try:
            amt = float(request.form.get('amount'))
            if amt <= 0:
                 raise ValueError("Miqdor musbat bo'lishi kerak.")
        except ValueError as e:
            flash(f'Xato miqdor: {e}')
            return redirect(url_for('user_history_view', uid=uid))
        except Exception:
            flash('Xato miqdor')
            return redirect(url_for('user_history_view', uid=uid))
        
        new_qbc = u.get('qbc', 0) + amt
        update_user(uid, qbc=new_qbc)
        flash(f'✅ {amt} QBC qo\'shildi. Yangi QBC: {new_qbc}')
        return redirect(url_for('user_history_view', uid=uid))

    hist = load_history(uid)
    content = f"<h4>History: @{u.get('username','-')} ({uid})</h4>"
    content += f"<div class='card p-3 mb-4'><b>QBC:</b> {u.get('qbc',0)} &nbsp; | &nbsp; <b>Total Savollar:</b> {u.get('total_questions',0)}</div>"
    
    # Grant form for owner
    if session.get('is_owner'):
        content += f"""
        <div class='card p-3 mt-3 mb-4'>
            <h5>QBC Berish (Owner-only)</h5>
            <form method='post'>
                <div class='mb-2'>
                    <input name='amount' class='form-control' placeholder='Miqdor (masalan, 10.5)' type='number' step='any' required>
                </div>
                <button class='btn btn-primary'>Yuborish</button>
            </form>
        </div>
        """
    
    content += "<div class='card p-3'><h5>Chat History (oxirgi 30 kun)</h5>"
    if not hist:
        content += "<div class='small-muted'>Hech qanday istoriya yo\'q</div>"
    else:
        for h in hist[::-1]:
            ts = h.get('ts')
            d = h.get('direction')
            txt = (h.get('text') or '').replace('<', '&lt;').replace('>', '&gt;')
            label = 'Foydalanuvchi' if d == 'in' else 'Bot'
            bg_color = 'bg-light' if d == 'in' else 'bg-secondary-subtle'
            
            content += f"""
            <div class='border rounded p-2 mb-2 {bg_color}'>
                <small class='text-muted d-block'>{ts} - <b>{label}</b></small>
                <div>{txt}</div>
            </div>
            """
    content += "</div>"

    content += f"<div class='card p-3 mt-3'><a class='btn btn-outline-secondary' href='/users_history'>← Orqaga</a></div>"
    return render_with_template(content)

@app.route('/users/<int:uid>')
@require_login
def user_detail(uid):
    u = get_user(uid)
    if not u:
        flash('Foydalanuvchi topilmadi')
        return redirect(url_for('users_index'))

    # help requests by user
    reqs = [r for r in load_help_requests() if r.get('user_id') == uid]
    
    content = f"<h4>Foydalanuvchi: @{u.get('username','-')} ({u.get('id')})</h4>"
    content += f"""
    <div class='card p-3 mb-4'>
        <b>QBC:</b> {u.get('qbc',0)} &nbsp; | &nbsp; 
        <b>Umumiy Savollar:</b> {u.get('total_questions',0)} &nbsp; | &nbsp; 
        <b>To'g'ri Javoblar:</b> {u.get('correct_answers',0)}
    </div>
    """
    
    content += "<div class='card p-3'><h5>Urinib ko'rilgan savollar (kategoriya bo'yicha)</h5>"
    if not u.get('attempted_questions'):
        content += "<div class='small-muted'>Urinishlar yo'q</div>"
    else:
        for cat, lst in u.get('attempted_questions', {}).items():
            content += f"<div><b>{cat}:</b> {', '.join([str(x) for x in lst])}</div>"
    content += "</div>"
    
    # Chat history (oxirgi 200 ta xabar)
    content += "<div class='card p-3 mt-3'><h5>Chat History (oxirgi 200 ta xabar)</h5>"
    hist = u.get('chat_history', [])
    if not hist:
        content += "<div class='small-muted'>Chat historiyasi yo'q</div>"
    else:
        for h in hist[-200:][::-1]:
            ts = h.get('ts')
            d = h.get('direction')
            txt = (h.get('text') or '').replace('<', '&lt;').replace('>', '&gt;')
            label = 'Foydalanuvchi' if d == 'in' else 'Bot'
            bg_color = 'bg-light' if d == 'in' else 'bg-secondary-subtle'
            
            content += f"""
            <div class='border rounded p-2 mb-2 {bg_color}'>
                <small class='text-muted d-block'>{ts} - <b>{label}</b></small>
                <div>{txt}</div>
            </div>
            """
    content += "</div>"
    
    content += "<div class='card p-3 mt-3'><h5>Yordam So'rovlari</h5>"
    if not reqs:
        content += "<div class='small-muted'>Yordam so'rovlari yo'q</div>"
    
    for r in reqs:
        status_badge = 'bg-success' if r.get('admin_reply') else 'bg-warning text-dark'
        status_text = 'Javob berilgan' if r.get('admin_reply') else 'Javob kutilmoqda'
        
        content += f"""
        <div class='border rounded p-3 mb-3'>
            <div class='d-flex justify-content-between'>
                <b>#{r.get('id')}</b>
                <span class='badge {status_badge}'>{status_text}</span>
            </div>
            <div class='small-muted mb-2'>{r.get('created_at')}</div>
            <p>{r.get('text')}</p>
            """
        if r.get('admin_reply'):
            content += f"<div class='alert alert-secondary'>Admin javobi: {r.get('admin_reply')}</div>"
            
        content += f"<a class='btn btn-sm btn-primary' href='/help/{r.get('id')}/reply'>Javob yozish / Ko'rish</a></div>"
        
    content += "</div>"
    
    content += f"<div class='card p-3 mt-3'><a class='btn btn-outline-secondary' href='/users'>← Orqaga</a></div>"
    return render_with_template(content)

@app.route('/users/<int:uid>/ban')
@require_login
def user_ban(uid):
    u = get_user(uid)
    if not u:
        flash('Foydalanuvchi topilmadi')
        return redirect(url_for('users_index'))
    update_user(uid, is_banned=True)
    flash(f'Foydalanuvchi @{u.get("username", uid)} banlandi')
    return redirect(url_for('users_index'))

@app.route('/users/<int:uid>/unban')
@require_login
def user_unban(uid):
    u = get_user(uid)
    if not u:
        flash('Foydalanuvchi topilmadi')
        return redirect(url_for('users_index'))
    update_user(uid, is_banned=False)
    flash(f'Foydalanuvchi @{u.get("username", uid)} bandan chiqarildi')
    return redirect(url_for('users_index'))

@app.route('/users/<int:uid>/grant', methods=['GET','POST'])
@require_login
@require_owner
def user_grant(uid):
    u = get_user(uid)
    if not u:
        flash('Foydalanuvchi topilmadi')
        return redirect(url_for('users_index'))
    
    if request.method == 'POST':
        try:
            amt = float(request.form.get('amount'))
            if amt <= 0:
                 raise ValueError("Miqdor musbat bo'lishi kerak.")
        except ValueError as e:
            flash(f'Xato miqdor: {e}')
            return redirect(url_for('user_grant', uid=uid))
        except Exception:
            flash('Xato miqdor')
            return redirect(url_for('user_grant', uid=uid))

        new_qbc = u.get('qbc', 0) + amt
        update_user(uid, qbc=new_qbc)
        flash(f"✅ {amt} QBC @{u.get('username', 'Nomalum')} ({uid}) ga qoshildi. Yangi QBC: {new_qbc}")
        return redirect(url_for('users_index'))

    content = f"""
        <h4>QBC Berish: @{u.get('username','-')} ({uid})</h4>
        <div class='card p-4'>
            <div class='alert alert-info'>Hozirgi QBC: <b>{u.get('qbc',0)}</b></div>
            <form method='post'>
                <div class='mb-3'>
                    <label class='form-label'>Beriladigan Miqdor (QBC)</label>
                    <input name='amount' class='form-control' placeholder='Masalan, 10.5' type='number' step='any' required>
                </div>
                <button class='btn btn-primary'>Grant QBC</button>
            </form>
            <a class='btn btn-outline-secondary mt-3' href='/users'>← Orqaga</a>
        </div>
    """
    return render_with_template(content)

@app.route('/admins')
@require_login
def admins_index():
    admins = load_admins()
    content = '<h4>Adminlar ro\'yxati</h4>'
    
    if session.get('is_owner'):
        content += '''
        <div class="card p-3 mb-4">
            <form method="post" action="/admins/add" class="d-flex">
                <input name="admin_id" class="form-control me-2" type="number" placeholder="Yangi Admin ID" required>
                <button class="btn btn-success" type="submit">➕ Qo\'shish</button>
            </form>
        </div>
        '''
    
    content += '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>ID</th><th>Username</th><th>Amallar</th></tr></thead><tbody>'
    for admin_id in admins:
        u = get_user(admin_id)
        uname = u.get('username', 'Noma\'lum') if u else 'ID topilmadi'
        
        delete_btn = ''
        if session.get('is_owner'):
             delete_btn = f"<a class='btn btn-sm btn-danger' href='/admins/{admin_id}/remove' onclick=\"return confirm('Haqiqatan ham @{uname} ({admin_id}) ni adminlikdan olib tashlamoqchimisiz?')\">O'chirish</a>"
        
        content += f"<tr><td>{admin_id}</td><td>@{uname}</td><td>{delete_btn}</td></tr>"

    content += '</tbody></table></div>'
    return render_with_template(content)

@app.route('/admins/add', methods=['POST'])
@require_login
@require_owner
def admins_add():
    try:
        admin_id = int(request.form.get('admin_id'))
        if admin_id in load_admins():
            flash('Admin allaqachon mavjud.')
        else:
            add_admin(admin_id)
            flash(f'Admin {admin_id} qo\'shildi.')
    except Exception:
        flash('Yaroqsiz ID formatida.')
    return redirect(url_for('admins_index'))

@app.route('/admins/<int:admin_id>/remove')
@require_login
@require_owner
def admins_remove(admin_id):
    if admin_id in load_admins():
        remove_admin(admin_id)
        flash(f'Admin {admin_id} olib tashlandi.')
    else:
        flash('Admin topilmadi.')
    return redirect(url_for('admins_index'))


@app.route('/help')
@require_login
def help_index():
    reqs = load_help_requests()
    content = '<h4>Yordam So\'rovlari</h4>'
    
    if not reqs:
        content += '<div class="card p-3"><div class="small-muted">Hech qanday so\'rov yo\'q.</div></div>'
        return render_with_template(content)
        
    content += '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>ID</th><th>Foydalanuvchi</th><th>Xabar</th><th>Status</th><th>Amallar</th></tr></thead><tbody>'
    
    for r in reqs:
        user_id = r.get('user_id')
        u = get_user(user_id)
        uname = u.get('username', f'ID: {user_id}') if u else f'ID: {user_id}'
        
        status_badge = 'bg-success' if r.get('admin_reply') else 'bg-warning text-dark'
        status_text = 'Javob berilgan' if r.get('admin_reply') else 'Kutilmoqda'
        
        short_text = (r.get('text', '')[:50] + '...') if len(r.get('text', '')) > 50 else r.get('text', '')
        
        content += f"""
        <tr>
            <td>{r.get('id')}</td>
            <td><a href='/users/{user_id}' class='card-title-link'>@{uname}</a></td>
            <td>{short_text}</td>
            <td><span class='badge {status_badge}'>{status_text}</span></td>
            <td><a class='btn btn-sm btn-primary' href='/help/{r.get('id')}/reply'>Javob</a></td>
        </tr>
        """
        
    content += '</tbody></table></div>'
    return render_with_template(content)


@app.route('/help/<int:req_id>/reply', methods=['GET', 'POST'])
@require_login
def help_reply(req_id):
    reqs = load_help_requests()
    req = next((r for r in reqs if r.get('id') == req_id), None)
    
    if not req:
        flash('So\'rov topilmadi')
        return redirect(url_for('help_index'))
        
    user_id = req.get('user_id')
    u = get_user(user_id)
    uname = u.get('username', f'ID: {user_id}') if u else f'ID: {user_id}'

    if request.method == 'POST':
        reply = request.form.get('reply', '').strip()
        if not reply:
            flash('Javob matni kiritilmadi')
            return redirect(url_for('help_reply', req_id=req_id))
            
        # Update va saqlash
        # Admin nomini olish uchun hozircha "Admin" deb belgilayman. Haqiqiy admin nomi session orqali olinishi kerak
        update_help_request(req_id, reply=reply, admin_name='Admin')
            
        flash('Javob muvaffaqiyatli saqlandi.')
        return redirect(url_for('help_index'))

    reply_form = f"""
        <h4>Yordam So'roviga Javob</h4>
        <div class='card p-4'>
            <h5>Foydalanuvchi: @{uname} ({user_id})</h5>
            <div class='alert alert-secondary'><b>So'rov:</b> {req.get('text')}</div>
            
            <form method='post'>
                <div class='mb-3'>
                    <label class='form-label'>Javob matni</label>
                    <textarea name='reply' class='form-control' rows='5' required>{req.get('admin_reply', '')}</textarea>
                </div>
                <button class='btn btn-primary'>Yuborish va Saqlash</button>
                <a class='btn btn-outline-secondary ms-2' href='/help'>← Orqaga</a>
            </form>
        </div>
    """
    return render_with_template(reply_form)


@app.route('/broadcast', methods=['GET','POST'])
@require_login
@require_owner
def broadcast():
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        if not message:
            flash('Xabar matni kiritilmadi')
            return redirect(url_for('broadcast'))
            
        users = load_users()
        total = len(users)
        success_count = 0
        
        # Bu yerda bot orqali tarqatish mantig'i bo'lishi kerak.
        # Haqiqiy bot yuborish funksiyasi 'utils' da bo'lishi kerak
        # Hozircha faqat simulyatsiya.

        flash(f'Xabar {total} foydalanuvchiga yuborishga harakat qilindi. Muvaffaqiyatli: {success_count} (Simulyatsiya)')
        return redirect(url_for('broadcast'))

    content = '''
        <h4>Xabar Tarqatish (Broadcast)</h4>
        <div class='card p-4'>
            <div class='alert alert-danger'>Diqqat! Bu funksiya barcha foydalanuvchilarga xabar yuboradi. Faqat muhim e'lonlar uchun foydalaning.</div>
            <form method='post'>
                <div class='mb-3'>
                    <label class='form-label'>Tarqatish Xabari</label>
                    <textarea name='message' class='form-control' rows='6' required></textarea>
                </div>
                <button class='btn btn-danger'>Barcha foydalanuvchilarga yuborish</button>
            </form>
        </div>
    '''
    return render_with_template(content)

# Flask ilovasini ishga tushirish (agar bu asosiy fayl bo'lsa)
if __name__ == '__main__':
    # Agar config.py dan DATA_DIR ni import qila olmasangiz, bu yerda uni aniqlang
    # global DATA_DIR 
    # DATA_DIR = os.path.join(os.path.dirname(__file__), 'data') 
    app.run(debug=True)