"""
database.py — TriLit AI v5  ·  Complete SQLite Backend
Tables: users, sessions, search_history, bookmarks, collections,
        summaries, screening_sessions, payments, notifications,
        tickets, audit_logs, paper_notes, reading_list,
        projects, project_papers, tasks, ai_chats, research_gaps
"""
import sqlite3, os, json, hashlib, secrets
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "trilit.db")

def _conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA foreign_keys=ON")
    return c

def init_db():
    c = _conn()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        email         TEXT UNIQUE NOT NULL,
        name          TEXT NOT NULL,
        password      TEXT NOT NULL,
        initials      TEXT DEFAULT '',
        avatar_color  TEXT DEFAULT '#7c3aed',
        plan          TEXT DEFAULT 'free',
        credits_used  INTEGER DEFAULT 0,
        credits_limit INTEGER DEFAULT 10,
        api_key       TEXT UNIQUE,
        theme         TEXT DEFAULT 'dark',
        created_at    TEXT DEFAULT (datetime('now')),
        last_login    TEXT,
        is_admin      INTEGER DEFAULT 0,
        is_active     INTEGER DEFAULT 1,
        bio           TEXT DEFAULT '',
        institution   TEXT DEFAULT '',
        field         TEXT DEFAULT '',
        promo_used    TEXT DEFAULT '',
        total_searches INTEGER DEFAULT 0,
        total_summaries INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS sessions (
        token      TEXT PRIMARY KEY,
        user_id    INTEGER NOT NULL,
        expires_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS search_history (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id  INTEGER NOT NULL,
        query    TEXT NOT NULL,
        k        INTEGER DEFAULT 10,
        category TEXT DEFAULT '',
        results  INTEGER DEFAULT 0,
        ts       TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS bookmarks (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        paper_id   TEXT NOT NULL,
        title      TEXT NOT NULL,
        abstract   TEXT DEFAULT '',
        categories TEXT DEFAULT '',
        score      REAL DEFAULT 0,
        note       TEXT DEFAULT '',
        collection TEXT DEFAULT 'Default',
        ts         TEXT DEFAULT (datetime('now')),
        UNIQUE(user_id, paper_id)
    );
    CREATE TABLE IF NOT EXISTS summaries (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        paper_title TEXT DEFAULT '',
        paper_id    TEXT DEFAULT '',
        abstract    TEXT NOT NULL,
        summary     TEXT NOT NULL,
        word_count  INTEGER DEFAULT 0,
        ts          TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS screening_sessions (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id      INTEGER NOT NULL,
        name         TEXT DEFAULT 'Session',
        total        INTEGER DEFAULT 0,
        included     INTEGER DEFAULT 0,
        excluded     INTEGER DEFAULT 0,
        threshold    REAL DEFAULT 0.5,
        results_json TEXT DEFAULT '[]',
        ts           TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS payments (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        amount     REAL NOT NULL,
        currency   TEXT DEFAULT 'USD',
        plan       TEXT NOT NULL,
        status     TEXT DEFAULT 'success',
        stripe_id  TEXT DEFAULT '',
        invoice_no TEXT DEFAULT '',
        ts         TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS notifications (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        msg     TEXT NOT NULL,
        type    TEXT DEFAULT 'info',
        read    INTEGER DEFAULT 0,
        ts      TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS tickets (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        body    TEXT NOT NULL,
        status  TEXT DEFAULT 'open',
        reply   TEXT DEFAULT '',
        ts      TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS audit_logs (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action  TEXT NOT NULL,
        detail  TEXT DEFAULT '',
        ts      TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS paper_notes (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id  INTEGER NOT NULL,
        paper_id TEXT NOT NULL,
        note     TEXT NOT NULL,
        ts       TEXT DEFAULT (datetime('now')),
        UNIQUE(user_id, paper_id)
    );
    CREATE TABLE IF NOT EXISTS reading_list (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id  INTEGER NOT NULL,
        paper_id TEXT NOT NULL,
        title    TEXT NOT NULL,
        status   TEXT DEFAULT 'unread',
        ts       TEXT DEFAULT (datetime('now')),
        UNIQUE(user_id, paper_id)
    );
    CREATE TABLE IF NOT EXISTS projects (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER NOT NULL,
        name        TEXT NOT NULL,
        description TEXT DEFAULT '',
        color       TEXT DEFAULT '#7c3aed',
        status      TEXT DEFAULT 'active',
        deadline    TEXT DEFAULT '',
        ts          TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS project_papers (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        user_id    INTEGER NOT NULL,
        paper_id   TEXT NOT NULL,
        title      TEXT NOT NULL,
        abstract   TEXT DEFAULT '',
        note       TEXT DEFAULT '',
        ts         TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS tasks (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        project_id INTEGER,
        title      TEXT NOT NULL,
        done       INTEGER DEFAULT 0,
        priority   TEXT DEFAULT 'medium',
        due_date   TEXT DEFAULT '',
        ts         TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS ai_chats (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        session_id TEXT NOT NULL,
        role       TEXT NOT NULL,
        content    TEXT NOT NULL,
        ts         TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS research_gaps (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        query      TEXT NOT NULL,
        gaps_json  TEXT DEFAULT '[]',
        ts         TEXT DEFAULT (datetime('now'))
    );
    CREATE TABLE IF NOT EXISTS paper_comparisons (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name    TEXT DEFAULT 'Comparison',
        papers_json TEXT DEFAULT '[]',
        ts      TEXT DEFAULT (datetime('now'))
    );
    """)
    c.commit()
    # Seed admin
    try:
        pw = hashlib.sha256(b"admin123").hexdigest()
        c.execute("""INSERT OR IGNORE INTO users
            (email,name,password,initials,plan,credits_limit,is_admin,api_key,avatar_color)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            ("admin@trilit.ai","Admin User",pw,"AU","university",
             999999,1,secrets.token_hex(20),"#e11d48"))
        c.commit()
    except: pass
    c.close()

# ── Auth ──────────────────────────────────────────────────────────────────────
def register_user(email, name, password, promo=""):
    colors=["#7c3aed","#0ea5e9","#10b981","#f59e0b","#ef4444","#8b5cf6","#06b6d4","#ec4899"]
    color=colors[len(email)%len(colors)]
    initials="".join(w[0].upper() for w in name.split()[:2])
    pw=hashlib.sha256(password.encode()).hexdigest()
    promos={"RESORA2026":"pro","TRILIT2024":"pro","RESEARCH50":"pro","UNIVERSITY2024":"university",
            "STUDENT2024":"pro","FREE2024":"free","PHD2024":"pro","SCHOLAR2024":"pro"}
    plan=promos.get(promo.upper(),"free")
    limit={"free":10,"pro":500,"university":999999}.get(plan,10)
    api=secrets.token_hex(20)
    c=_conn()
    try:
        c.execute("""INSERT INTO users
            (email,name,password,initials,avatar_color,plan,credits_limit,api_key,promo_used)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (email.lower().strip(),name,pw,initials,color,plan,limit,api,promo))
        c.commit()
        uid=c.execute("SELECT id FROM users WHERE email=?",(email.lower(),)).fetchone()[0]
        _notify(uid,f"Welcome to Resora, {name.split()[0]}! Your {plan.capitalize()} plan is active.","success",c)
        c.commit(); return True,"Account created!"
    except sqlite3.IntegrityError: return False,"Email already registered."
    finally: c.close()

def login_user(email, password):
    pw=hashlib.sha256(password.encode()).hexdigest()
    c=_conn()
    row=c.execute("SELECT * FROM users WHERE email=? AND password=? AND is_active=1",
                  (email.lower().strip(),pw)).fetchone()
    if not row: c.close(); return None,"Invalid email or password."
    token=secrets.token_hex(32)
    exp=(datetime.now()+timedelta(days=7)).isoformat()
    c.execute("INSERT OR REPLACE INTO sessions VALUES(?,?,?)",(token,row["id"],exp))
    c.execute("UPDATE users SET last_login=datetime('now') WHERE id=?",(row["id"],))
    c.execute("INSERT INTO audit_logs(user_id,action,detail) VALUES(?,?,?)",
              (row["id"],"login",f"{email} logged in"))
    c.commit(); c.close()
    return dict(row),token

def get_user(uid):
    c=_conn(); r=c.execute("SELECT * FROM users WHERE id=?",(uid,)).fetchone(); c.close()
    return dict(r) if r else None

def get_user_by_email(email):
    c=_conn(); r=c.execute("SELECT * FROM users WHERE email=?",(email.lower(),)).fetchone(); c.close()
    return dict(r) if r else None

def update_user(uid,**kw):
    allowed={"name","plan","credits_limit","credits_used","initials","bio",
             "institution","field","theme","avatar_color","total_searches","total_summaries"}
    sets=", ".join(f"{k}=?" for k in kw if k in allowed)
    vals=[v for k,v in kw.items() if k in allowed]
    if not sets: return
    c=_conn(); c.execute(f"UPDATE users SET {sets} WHERE id=?",vals+[uid]); c.commit(); c.close()

def use_credit(uid):
    c=_conn()
    r=c.execute("SELECT credits_used,credits_limit,plan FROM users WHERE id=?",(uid,)).fetchone()
    if not r: c.close(); return False
    if r["plan"] in ("pro","university") or r["credits_used"]<r["credits_limit"]:
        c.execute("UPDATE users SET credits_used=credits_used+1 WHERE id=?",(uid,))
        c.commit(); c.close(); return True
    c.close(); return False

def upgrade_plan(uid,plan):
    limits={"free":10,"pro":500,"university":999999}
    c=_conn()
    c.execute("UPDATE users SET plan=?,credits_limit=?,credits_used=0 WHERE id=?",
              (plan,limits.get(plan,10),uid))
    c.commit(); c.close()

# ── Notifications ─────────────────────────────────────────────────────────────
def _notify(uid,msg,t="info",conn=None):
    c=conn or _conn()
    c.execute("INSERT INTO notifications(user_id,msg,type) VALUES(?,?,?)",(uid,msg,t))
    if not conn: c.commit(); c.close()

def notify(uid,msg,t="info"): _notify(uid,msg,t)

def get_notifications(uid,unread=False):
    c=_conn()
    q="SELECT * FROM notifications WHERE user_id=?"
    if unread: q+=" AND read=0"
    q+=" ORDER BY ts DESC LIMIT 50"
    rows=c.execute(q,(uid,)).fetchall(); c.close()
    return [dict(r) for r in rows]

def mark_read(uid):
    c=_conn(); c.execute("UPDATE notifications SET read=1 WHERE user_id=?",(uid,)); c.commit(); c.close()

def unread_count(uid):
    c=_conn(); n=c.execute("SELECT COUNT(*) FROM notifications WHERE user_id=? AND read=0",(uid,)).fetchone()[0]; c.close(); return n

# ── Search ────────────────────────────────────────────────────────────────────
def add_search(uid,query,k,cat,count):
    c=_conn()
    c.execute("INSERT INTO search_history(user_id,query,k,category,results) VALUES(?,?,?,?,?)",(uid,query,k,cat,count))
    c.execute("UPDATE users SET total_searches=total_searches+1 WHERE id=?",(uid,))
    c.commit(); c.close()

def get_search_history(uid,limit=30):
    c=_conn(); rows=c.execute("SELECT * FROM search_history WHERE user_id=? ORDER BY ts DESC LIMIT ?",(uid,limit)).fetchall(); c.close()
    return [dict(r) for r in rows]

def delete_search_history(uid):
    c=_conn(); c.execute("DELETE FROM search_history WHERE user_id=?",(uid,)); c.commit(); c.close()

def get_popular_queries(uid,limit=5):
    c=_conn()
    rows=c.execute("SELECT query,COUNT(*) as cnt FROM search_history WHERE user_id=? GROUP BY query ORDER BY cnt DESC LIMIT ?",(uid,limit)).fetchall()
    c.close(); return [dict(r) for r in rows]

# ── Bookmarks ──────────────────────────────────────────────────────────────────
def add_bookmark(uid,paper_id,title,abstract="",cats="",score=0.0,note="",collection="Default"):
    c=_conn()
    try:
        c.execute("INSERT INTO bookmarks(user_id,paper_id,title,abstract,categories,score,note,collection) VALUES(?,?,?,?,?,?,?,?)",
                  (uid,paper_id,title,abstract,cats,score,note,collection))
        c.commit(); c.close(); return True
    except sqlite3.IntegrityError: c.close(); return False

def get_bookmarks(uid,collection=None):
    c=_conn()
    q="SELECT * FROM bookmarks WHERE user_id=?"
    args=[uid]
    if collection: q+=" AND collection=?"; args.append(collection)
    q+=" ORDER BY ts DESC"
    rows=c.execute(q,args).fetchall(); c.close()
    return [dict(r) for r in rows]

def delete_bookmark(uid,bid):
    c=_conn(); c.execute("DELETE FROM bookmarks WHERE id=? AND user_id=?",(bid,uid)); c.commit(); c.close()

def update_bookmark_note(uid,bid,note):
    c=_conn(); c.execute("UPDATE bookmarks SET note=? WHERE id=? AND user_id=?",(note,bid,uid)); c.commit(); c.close()

def get_collections(uid):
    c=_conn(); rows=c.execute("SELECT DISTINCT collection FROM bookmarks WHERE user_id=?",(uid,)).fetchall(); c.close()
    return [r[0] for r in rows] or ["Default"]

# ── Summaries ─────────────────────────────────────────────────────────────────
def add_summary(uid,abstract,summary,title="",paper_id=""):
    wc=len(summary.split())
    c=_conn()
    c.execute("INSERT INTO summaries(user_id,paper_title,paper_id,abstract,summary,word_count) VALUES(?,?,?,?,?,?)",
              (uid,title,paper_id,abstract[:500],summary,wc))
    c.execute("UPDATE users SET total_summaries=total_summaries+1 WHERE id=?",(uid,))
    c.commit(); c.close()

def get_summaries(uid,limit=30):
    c=_conn(); rows=c.execute("SELECT * FROM summaries WHERE user_id=? ORDER BY ts DESC LIMIT ?",(uid,limit)).fetchall(); c.close()
    return [dict(r) for r in rows]

# ── Screening ─────────────────────────────────────────────────────────────────
def save_screening(uid,name,total,included,excluded,thr,results):
    c=_conn()
    c.execute("INSERT INTO screening_sessions(user_id,name,total,included,excluded,threshold,results_json) VALUES(?,?,?,?,?,?,?)",
              (uid,name,total,included,excluded,thr,json.dumps(results)))
    c.commit(); c.close()

def get_screenings(uid):
    c=_conn(); rows=c.execute("SELECT id,name,total,included,excluded,threshold,ts FROM screening_sessions WHERE user_id=? ORDER BY ts DESC",(uid,)).fetchall(); c.close()
    return [dict(r) for r in rows]

# ── Reading list ──────────────────────────────────────────────────────────────
def add_to_reading_list(uid,paper_id,title):
    c=_conn()
    try: c.execute("INSERT INTO reading_list(user_id,paper_id,title) VALUES(?,?,?)",(uid,paper_id,title)); c.commit()
    except: pass
    c.close()

def get_reading_list(uid):
    c=_conn(); rows=c.execute("SELECT * FROM reading_list WHERE user_id=? ORDER BY ts DESC",(uid,)).fetchall(); c.close()
    return [dict(r) for r in rows]

def update_reading_status(uid,paper_id,status):
    c=_conn(); c.execute("UPDATE reading_list SET status=? WHERE user_id=? AND paper_id=?",(status,uid,paper_id)); c.commit(); c.close()

# ── Projects ──────────────────────────────────────────────────────────────────
def create_project(uid,name,description="",color="#7c3aed",deadline=""):
    c=_conn()
    cur=c.cursor()
    cur.execute("INSERT INTO projects(user_id,name,description,color,deadline) VALUES(?,?,?,?,?)",(uid,name,description,color,deadline))
    c.commit(); pid=cur.lastrowid; c.close(); return pid

def get_projects(uid):
    c=_conn(); rows=c.execute("SELECT * FROM projects WHERE user_id=? ORDER BY ts DESC",(uid,)).fetchall(); c.close()
    return [dict(r) for r in rows]

def get_project(pid):
    c=_conn(); r=c.execute("SELECT * FROM projects WHERE id=?",(pid,)).fetchone(); c.close()
    return dict(r) if r else None

def update_project(pid,**kw):
    allowed={"name","description","color","status","deadline"}
    sets=", ".join(f"{k}=?" for k in kw if k in allowed)
    vals=[v for k,v in kw.items() if k in allowed]
    if not sets: return
    c=_conn(); c.execute(f"UPDATE projects SET {sets} WHERE id=?",vals+[pid]); c.commit(); c.close()

def delete_project(pid):
    c=_conn()
    c.execute("DELETE FROM project_papers WHERE project_id=?",(pid,))
    c.execute("DELETE FROM tasks WHERE project_id=?",(pid,))
    c.execute("DELETE FROM projects WHERE id=?",(pid,))
    c.commit(); c.close()

def add_paper_to_project(pid,uid,paper_id,title,abstract="",note=""):
    c=_conn()
    try:
        c.execute("INSERT INTO project_papers(project_id,user_id,paper_id,title,abstract,note) VALUES(?,?,?,?,?,?)",
                  (pid,uid,paper_id,title,abstract,note))
        c.commit()
    except: pass
    c.close()

def get_project_papers(pid):
    c=_conn(); rows=c.execute("SELECT * FROM project_papers WHERE project_id=? ORDER BY ts DESC",(pid,)).fetchall(); c.close()
    return [dict(r) for r in rows]

# ── Tasks ─────────────────────────────────────────────────────────────────────
def add_task(uid,title,project_id=None,priority="medium",due_date=""):
    c=_conn()
    c.execute("INSERT INTO tasks(user_id,project_id,title,priority,due_date) VALUES(?,?,?,?,?)",
              (uid,project_id,title,priority,due_date))
    c.commit(); c.close()

def get_tasks(uid,project_id=None):
    c=_conn()
    q="SELECT * FROM tasks WHERE user_id=?"
    args=[uid]
    if project_id: q+=" AND project_id=?"; args.append(project_id)
    q+=" ORDER BY done,ts DESC"
    rows=c.execute(q,args).fetchall(); c.close()
    return [dict(r) for r in rows]

def toggle_task(tid):
    c=_conn(); c.execute("UPDATE tasks SET done=1-done WHERE id=?",(tid,)); c.commit(); c.close()

def delete_task(tid):
    c=_conn(); c.execute("DELETE FROM tasks WHERE id=?",(tid,)); c.commit(); c.close()

# ── AI Chat ───────────────────────────────────────────────────────────────────
def save_chat_message(uid,session_id,role,content):
    c=_conn()
    c.execute("INSERT INTO ai_chats(user_id,session_id,role,content) VALUES(?,?,?,?)",(uid,session_id,role,content))
    c.commit(); c.close()

def get_chat_history(uid,session_id,limit=50):
    c=_conn()
    rows=c.execute("SELECT role,content,ts FROM ai_chats WHERE user_id=? AND session_id=? ORDER BY ts ASC LIMIT ?",(uid,session_id,limit)).fetchall()
    c.close(); return [dict(r) for r in rows]

def get_chat_sessions(uid):
    c=_conn()
    rows=c.execute("SELECT DISTINCT session_id, MIN(ts) as first_ts FROM ai_chats WHERE user_id=? GROUP BY session_id ORDER BY first_ts DESC LIMIT 20",(uid,)).fetchall()
    c.close(); return [dict(r) for r in rows]

# ── Payments ──────────────────────────────────────────────────────────────────
def add_payment(uid,amount,plan,status="success",stripe_id=""):
    inv=f"TL-{datetime.now().strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"
    c=_conn()
    c.execute("INSERT INTO payments(user_id,amount,plan,status,stripe_id,invoice_no) VALUES(?,?,?,?,?,?)",
              (uid,amount,plan,status,stripe_id,inv))
    c.commit(); c.close(); return inv

def get_payments(uid):
    c=_conn(); rows=c.execute("SELECT * FROM payments WHERE user_id=? ORDER BY ts DESC",(uid,)).fetchall(); c.close()
    return [dict(r) for r in rows]

# ── Support ───────────────────────────────────────────────────────────────────
def add_ticket(uid,subject,body):
    c=_conn(); c.execute("INSERT INTO tickets(user_id,subject,body) VALUES(?,?,?)",(uid,subject,body)); c.commit(); c.close()

def get_tickets(uid):
    c=_conn(); rows=c.execute("SELECT * FROM tickets WHERE user_id=? ORDER BY ts DESC",(uid,)).fetchall(); c.close()
    return [dict(r) for r in rows]

def get_all_tickets():
    c=_conn(); rows=c.execute("SELECT t.*,u.name,u.email FROM tickets t JOIN users u ON t.user_id=u.id ORDER BY t.ts DESC").fetchall(); c.close()
    return [dict(r) for r in rows]

def reply_ticket(tid,reply):
    c=_conn(); c.execute("UPDATE tickets SET reply=?,status='resolved' WHERE id=?",(reply,tid)); c.commit(); c.close()

# ── Admin ─────────────────────────────────────────────────────────────────────
def get_all_users():
    c=_conn(); rows=c.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall(); c.close()
    return [dict(r) for r in rows]

def get_audit_logs(limit=200):
    c=_conn(); rows=c.execute("SELECT l.*,u.name FROM audit_logs l LEFT JOIN users u ON l.user_id=u.id ORDER BY l.ts DESC LIMIT ?",(limit,)).fetchall(); c.close()
    return [dict(r) for r in rows]

def toggle_user_active(uid):
    c=_conn(); c.execute("UPDATE users SET is_active=1-is_active WHERE id=?",(uid,)); c.commit(); c.close()

def get_stats():
    c=_conn()
    s={
        "total_users":  c.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "pro_users":    c.execute("SELECT COUNT(*) FROM users WHERE plan='pro'").fetchone()[0],
        "uni_users":    c.execute("SELECT COUNT(*) FROM users WHERE plan='university'").fetchone()[0],
        "revenue":      c.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='success'").fetchone()[0],
        "searches":     c.execute("SELECT COUNT(*) FROM search_history").fetchone()[0],
        "summaries":    c.execute("SELECT COUNT(*) FROM summaries").fetchone()[0],
        "bookmarks":    c.execute("SELECT COUNT(*) FROM bookmarks").fetchone()[0],
        "tickets_open": c.execute("SELECT COUNT(*) FROM tickets WHERE status='open'").fetchone()[0],
        "projects":     c.execute("SELECT COUNT(*) FROM projects").fetchone()[0],
        "tasks":        c.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
    }
    c.close(); return s

# ── Paper notes ───────────────────────────────────────────────────────────────
def save_note(uid,paper_id,note):
    c=_conn(); c.execute("INSERT OR REPLACE INTO paper_notes(user_id,paper_id,note) VALUES(?,?,?)",(uid,paper_id,note)); c.commit(); c.close()

def get_note(uid,paper_id):
    c=_conn(); r=c.execute("SELECT note FROM paper_notes WHERE user_id=? AND paper_id=?",(uid,paper_id)).fetchone(); c.close()
    return r[0] if r else ""

init_db()
