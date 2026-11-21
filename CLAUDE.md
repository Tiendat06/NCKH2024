# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read the knowledge base first — mandatory

Before starting ANY task in this repo (feature, bug fix, refactor, review, or answering a question about the code), read the knowledge base in `../swt-xray-knowledge-base/` before reading or editing application code. Do this at the start of every task, not once per session.

The KB routing engine below is imported into every session. Follow its steps to decide which KB files the task needs:

1. STEP 0 — load the relevant slice of `../swt-xray-knowledge-base/_meta/manifest.yml` (line numbers come from `_meta/anchors.md`).
2. STEP 1 — read the entrypoint files in order (`03-conventions.md`, `services/xray-webapp.md`, ...).
3. STEP 2 — load the files the task-routing table lists for this kind of task, including the matching playbook in `playbooks/`.

Paths inside the routing engine are relative to `../swt-xray-knowledge-base/`. Say in one line which KB files you read before starting the work. If the KB and the code disagree, the code wins — fix the KB as part of the task.

@../swt-xray-knowledge-base/CLAUDE.local.md

## What this is

A Flask monolith for chest X-ray abnormality detection: a custom-trained YOLOv6 model (14 VinBigData classes) plus torchxrayvision segmentation (cardio-thoracic ratio, organ contours), wrapped in a clinic workflow — staff accounts, patients, medical records, and real-time doctor↔patient chat. UI strings and many code comments are Vietnamese.

The repo is a fork of the upstream YOLOv6 project with the web app layered on top. `yolov6/`, `configs/`, `hubconf.py`, `utils/deploy/`, `utils/tools/`, `utils/docs/` and the notebooks are vendored upstream code — leave them alone unless the task is about the model itself. The web app is everything else.

## Commands

```bash
# Backing services (only MongoDB and Redis are containerised)
docker-compose up -d mongodb redis

# Dependencies (Python 3.8 virtualenv; the existing .venv was created with uv)
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt        # everything the app imports, pinned
.venv/Scripts/pip install -r requirements-dev.txt    # optional: YOLOv6 train/eval/export tools
# Reproducible install (all transitive versions pinned): uv pip sync requirements-lock-windows.txt
# (Docker/Linux: requirements-lock-linux.txt; regenerate both with uv pip compile when requirements.txt changes)

# Run (Flask + SocketIO on http://127.0.0.1:5000)
python __init__.py
```

- Run from the repo root: imports (`routes`, `events`, `app.*`, `database`, `my_yolov6`) and the `static/img/...` output paths are all relative to it.
- The entry point is the root `__init__.py`, not `flask run` — it must go through `socketio.run(app, debug=True)` for chat to work.
- `requirements.txt` targets Python 3.8 and pins every runtime import (Flask 2.2.2, torch 2.4.1, torchxrayvision 1.5.5, ...); keep it in sync with `.venv` when adding a package.
- The `Dockerfile` and the `app` service in `docker-compose.yml` are fully commented out; the app runs on the host.
- There is no test suite, linter config, or CI. `.pre-commit-config.yaml` only runs whitespace/EOF/YAML/large-file hooks.

### Required local setup

- `.env` (gitignored; an older `app/.env` is still in pushed git history — TD-003): `MONGO_URI`, `DATABASE_NAME`, `SECRET_KEY`, `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_TLS`, `MAIL_SSL`.
- `routes/apis/client_secret.json` (gitignored) — Google OAuth client secrets, loaded by `routes/log.py`. The redirect URI is hardcoded to `http://127.0.0.1:5000/callback`.
- Redis host is hardcoded to `host.docker.internal:6379` in `events/chat.py`.
- MongoDB and Redis must be up before the app starts; there is no retry logic.
- `database/data/test.*.json` are exports of the `account`, `body_target`, `disease`, `medical_record`, `patient`, `role`, `user` collections for seeding a fresh database (`mongoimport --jsonArray --drop`). `body_target_id` values are the PSPNet target indices `"0"`–`"13"`: the UI posts them back and the controller uses them as mask indices.
- Model weights live in `app/controllers/weights/best_ckpt.pt` with class names in `app/controllers/data/vinbigdata.yaml`. Inference runs on CPU.

## Architecture

### Request path

```
routes/<domain>.py  (Blueprint, URL only)
  → [app/middlewares/<Domain>MiddleWare.py]   chat & patient only; plain pass-through, no auth logic
  → app/controllers/<Domain>Controller.py     business logic, session, render_template / jsonify
  → [app/services/<Domain>Service.py]         chat & patient only
  → app/models/<Entity>.py                    raw pymongo queries
  → database/__init__.py  DataBaseUtils       MongoClient wrapper, .get_collection(name)
```

Blueprints are registered in `routes/__init__.py`. A new endpoint needs a route function there that instantiates the controller per request (`return XController().method()`). `XrayController()` is created per request, but the models are process-wide singletons: `get_yolov6()` (XrayController.py) and `get_pspnet()` (BodyTarget.py) load YOLOv6 and one PSPNet on first use and reuse them afterwards.

`routes/error.py` registers a catch-all `app_errorhandler(Exception)`, so any unhandled exception renders `templates/error/error.html` instead of a traceback — check the console output when debugging.

### Models

Each `app/models/<Entity>.py` holds two classes: a plain entity (`Account`, with name-mangled fields exposed through `_field` properties, e.g. `user._name`, `account._role_id`) and an `<Entity>Model(DataBaseUtils)` holding the queries via `self.__conn.get_collection(...)`. There is no ORM. `Patient` is constructed through `app/models/builder/BuilderPatient.py`.

Business IDs are generated by `AUTO_<X>_ID()` methods: find the max existing ID, increment, and format as a 3-letter prefix + 7 zero-padded digits (`ACC0000001`, `ROL0000003`). Entities reference each other by these IDs, not by Mongo `_id`.

Collections: `account`, `role`, `user`, `patient`, `disease`, `medical_record`, `body_target`, `chat`.

### Templates

Nearly every page renders `templates/index.html`, which switches on two variables: `content` (`'home'` for the public landing page, `'index'` for the staff dashboard shell) and `page` (`'index'`, `'xray'`, `'account'`, `'user'`, `'user_profile'`, `'patient'`, `'chat'`) to pick the partial to include. Adding a dashboard page means adding a `page` branch there and passing `content='index', page='<name>'` from the controller. AJAX endpoints either return `jsonify(...)` (shape varies per endpoint) or render an HTML fragment (e.g. `xray/change_range.html`, `home/home_patient_record.html`) that `static/js/main.js` injects into the page. All frontend JS is in `static/js/main.js`.

### Auth and roles

Session-cookie auth (Flask's default signed client-side cookie — `SESSION_TYPE='filesystem'` is set but `Session(app)` is never called, so Flask-Session is inert), two login paths that set the same session keys (`account`, `google_id`, `user_name`, `user_img`, `user_id`, `acc_id`): Google OAuth (`/log/login_gmail` → `/callback`) and email/password (`POST /log/login`). The only route-level guard is `login_is_required` on `/`, keyed on `session['google_id']` (the password login sets it to a dummy value); controllers otherwise check `'account' in session` themselves. Patients are not accounts — they identify with just their `PID` on the public home page.

Known quirks to be aware of rather than copy:
- Passwords are stored and compared in plaintext; "reset password" sets it to the account's email.
- `ROL0000003` is both the default role at registration (pending email confirmation → `ROL0000002`) and the "banned" role rejected at login.
- `PatientModel.delete_patient` is a stub although `/patient/delete` is routed.
- Cloudinary credentials are hardcoded in `__init__.py`.

### X-ray pipeline

`my_yolov6.py` wraps the vendored `yolov6/` package; `infer()` returns the annotated frame plus detection count, labels, confidences, Vietnamese/English disease names and colors. `XrayController.load_data` (`/xray`) saves the upload under `static/img/`, runs inference at `conf_thres=0.3`, writes a resized copy to `static/img/data/`, uploads the annotated image to Cloudinary, and stashes the paths in the session. `/xray/ajax/changeRange` re-runs inference on the session's saved file with a new confidence threshold — it depends on that session state. The body-target, ratio and contour endpoints use torchxrayvision's PSPNet and write to `static/img/{body_target,new_body_target,ratio,upload_ratio,contours,upload_contours}/`; those folders and `static/img/data/` are gitignored (kept with `.gitkeep`; the 4 images referenced by `database/data/test.medical_record.json` stay tracked). The raw upload that `/xray` saves to `static/img/<filename>` is not ignored and shows up as untracked.

### Chat

`events/chat.py` registers the SocketIO handlers. Staff connect with `?user_type=admin` and join `admin_room`; patients emit `user_login` with their `PID`, and Redis stores `PID → socket sid` so staff replies can be routed to the right socket (Redis is used for nothing else). Messages persist to the `chat` collection through `ChatMiddleware → ChatController → ChatService → ChatModel`. Client sides are in `templates/chat/chat.html` (staff) and `templates/home/home.html` (patient).

## Knowledge base

`../swt-xray-knowledge-base/` (a sibling directory of this repo, not inside it) is a separate documentation set about this app with its own `CLAUDE.md` and maintenance scripts. It has the full route table (`01-architecture.md`), per-route detail (`services/xray-webapp.md`), the tech-debt list (`_meta/manifest.yml`) and step-by-step playbooks (`playbooks/`). Its rule: code is the source of truth — when they disagree, fix the KB, and follow that directory's `CLAUDE.md` when editing it.
