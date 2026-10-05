import os
import json
import uuid
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import resend

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_SECRET", "dev-secret-key")

os.makedirs("submissions", exist_ok=True)

NOTIFICATION_EMAIL = "goable@goable.com.au"

def get_resend_credentials():
    """Get Resend API key. Checks RESEND_API_KEY secret first, falls back to Replit connector."""
    direct_key = os.environ.get("RESEND_API_KEY")
    if direct_key:
        return direct_key, None

    hostname = os.environ.get("REPLIT_CONNECTORS_HOSTNAME")
    repl_identity = os.environ.get("REPL_IDENTITY")
    web_repl_renewal = os.environ.get("WEB_REPL_RENEWAL")

    if repl_identity:
        x_replit_token = f"repl {repl_identity}"
    elif web_repl_renewal:
        x_replit_token = f"depl {web_repl_renewal}"
    else:
        return None, None

    if not hostname:
        return None, None

    try:
        response = requests.get(
            f"https://{hostname}/api/v2/connection?include_secrets=true&connector_names=resend",
            headers={
                "Accept": "application/json",
                "X-Replit-Token": x_replit_token
            }
        )
        data = response.json()
        connection = data.get("items", [{}])[0]
        settings = connection.get("settings", {})
        return settings.get("api_key"), settings.get("from_email")
    except Exception as e:
        print(f"Error getting Resend credentials: {e}")
        return None, None

def send_notification_email(submission_data):
    """Send email notification for new personalised plan submission."""
    api_key, from_email = get_resend_credentials()
    
    if not api_key or not from_email:
        print("Resend not configured - skipping email notification")
        return False
    
    resend.api_key = api_key
    if not from_email or "gmail.com" in from_email or "yahoo.com" in from_email or "hotmail.com" in from_email:
        from_email = "Hair Extensions Hub <hello@bookings.hairextensions.app>"
    
    html_content = f"""
    <h2>New Personalised Plan Request</h2>
    <p><strong>Client:</strong> {submission_data['client_name']}</p>
    <p><strong>Email:</strong> {submission_data['email']}</p>
    <p><strong>Location:</strong> {submission_data.get('city', 'N/A')}, {submission_data.get('country', 'N/A')}</p>
    <hr>
    <h3>Hair Details</h3>
    <p><strong>Length:</strong> {submission_data['hair_length']}</p>
    <p><strong>Thickness:</strong> {submission_data['hair_thickness']}</p>
    <p><strong>Texture:</strong> {submission_data['hair_texture']}</p>
    <p><strong>Colour:</strong> {submission_data.get('hair_colour', 'N/A')}</p>
    <hr>
    <h3>Lifestyle</h3>
    <p><strong>Wash Frequency:</strong> {submission_data.get('wash_frequency', 'N/A')}</p>
    <p><strong>Heat Styling:</strong> {submission_data.get('heat_styling', 'N/A')}</p>
    <p><strong>Budget:</strong> {submission_data.get('budget', 'N/A')}</p>
    <p><strong>Previous Extensions:</strong> {submission_data.get('had_extensions', 'N/A')}</p>
    <hr>
    <h3>Goals & Concerns</h3>
    <p><strong>Main Goal:</strong> {submission_data['main_goal']}</p>
    <p><strong>Concerns:</strong> {submission_data.get('concerns', 'N/A')}</p>
    <hr>
    <p><em>Submitted: {submission_data['timestamp']}</em></p>
    """
    
    try:
        resend.Emails.send({
            "from": from_email,
            "to": [NOTIFICATION_EMAIL],
            "subject": f"New Personalised Plan Request - {submission_data['client_name']}",
            "html": html_content
        })
        print(f"Email notification sent to {NOTIFICATION_EMAIL}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_weft_booking_email(booking_data):
    """Send email notification for new weft booking request."""
    api_key, from_email = get_resend_credentials()

    if not api_key:
        print("Resend not configured - skipping email notification")
        return False

    resend.api_key = api_key
    if not from_email or any(d in from_email for d in ["gmail.com", "yahoo.com", "hotmail.com"]):
        from_email = "Hair Extensions Hub <hello@bookings.hairextensions.app>"

    name     = booking_data.get('name', '')
    mobile   = booking_data.get('mobile', '')
    email    = booking_data.get('email', '')
    suburb   = booking_data.get('location', '')
    service  = booking_data.get('service', '')
    weft     = booking_data.get('weft_type', '') or 'Not specified'
    length   = booking_data.get('length', '') or 'Not specified'
    grams    = booking_data.get('grams', '') or 'Not specified'
    notes    = booking_data.get('notes', '') or 'None'
    ts       = booking_data.get('timestamp', '')

    html_content = f"""
    <div style="font-family:Georgia,serif;max-width:600px;margin:0 auto;background:#1A1208;color:#FAF6EF;padding:40px 36px;border-radius:4px">
      <div style="border-bottom:1px solid rgba(201,169,110,.25);padding-bottom:20px;margin-bottom:28px">
        <p style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#C9A96E;margin:0 0 8px">Hair Extensions Hub</p>
        <h1 style="font-size:26px;font-weight:300;color:#fff;margin:0;line-height:1.2">New booking request</h1>
      </div>
      <table style="width:100%;border-collapse:collapse;margin-bottom:28px">
        <tr><td style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(201,169,110,.6);padding:8px 0 4px;border-bottom:1px solid rgba(255,255,255,.05)" colspan="2">Client</td></tr>
        <tr><td style="font-size:13px;color:rgba(250,246,239,.5);padding:8px 12px 8px 0;width:120px">Name</td><td style="font-size:14px;color:#FAF6EF;padding:8px 0">{name}</td></tr>
        <tr><td style="font-size:13px;color:rgba(250,246,239,.5);padding:8px 12px 8px 0">Mobile</td><td style="font-size:14px;color:#FAF6EF;padding:8px 0"><a href="tel:{mobile}" style="color:#C9A96E;text-decoration:none">{mobile}</a></td></tr>
        <tr><td style="font-size:13px;color:rgba(250,246,239,.5);padding:8px 12px 8px 0">Email</td><td style="font-size:14px;color:#FAF6EF;padding:8px 0"><a href="mailto:{email}" style="color:#C9A96E;text-decoration:none">{email}</a></td></tr>
        <tr><td style="font-size:13px;color:rgba(250,246,239,.5);padding:8px 12px 8px 0">Suburb</td><td style="font-size:14px;color:#FAF6EF;padding:8px 0">{suburb}</td></tr>
      </table>
      <table style="width:100%;border-collapse:collapse;margin-bottom:28px">
        <tr><td style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(201,169,110,.6);padding:8px 0 4px;border-bottom:1px solid rgba(255,255,255,.05)" colspan="2">Service requested</td></tr>
        <tr><td style="font-size:13px;color:rgba(250,246,239,.5);padding:8px 12px 8px 0;width:120px">Service</td><td style="font-size:14px;color:#FAF6EF;padding:8px 0">{service}</td></tr>
        <tr><td style="font-size:13px;color:rgba(250,246,239,.5);padding:8px 12px 8px 0">Weft type</td><td style="font-size:14px;color:#FAF6EF;padding:8px 0">{weft}</td></tr>
        <tr><td style="font-size:13px;color:rgba(250,246,239,.5);padding:8px 12px 8px 0">Length</td><td style="font-size:14px;color:#FAF6EF;padding:8px 0">{length}</td></tr>
        <tr><td style="font-size:13px;color:rgba(250,246,239,.5);padding:8px 12px 8px 0">Grams</td><td style="font-size:14px;color:#FAF6EF;padding:8px 0">{grams}</td></tr>
      </table>
      <div style="background:rgba(255,255,255,.03);border:1px solid rgba(201,169,110,.1);padding:16px 18px;margin-bottom:28px">
        <p style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:rgba(201,169,110,.6);margin:0 0 8px">Notes from client</p>
        <p style="font-size:14px;color:rgba(250,246,239,.7);margin:0;line-height:1.7;font-style:italic">{notes}</p>
      </div>
      <p style="font-size:11px;color:rgba(250,246,239,.2);margin:0">Submitted {ts} · Hair Extensions Hub · hairextensionshub.com</p>
    </div>
    """

    try:
        resend.Emails.send({
            "from": from_email,
            "to": [NOTIFICATION_EMAIL],
            "subject": f"Booking request — {name} · {service}",
            "html": html_content
        })
        print(f"Weft booking email sent to {NOTIFICATION_EMAIL}")
        return True
    except Exception as e:
        print(f"Error sending weft booking email: {e}")
        return False

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/wefts")
def wefts():
    return render_template("wefts.html")

@app.route("/grams-email", methods=["POST"])
def grams_email():
    data = request.get_json(silent=True) or {}
    email   = data.get("email", "").strip()
    grams   = data.get("grams", "")
    rows    = data.get("rows", "")
    length  = data.get("length", "")
    weft    = data.get("weft", "")
    explain = data.get("explain", "")

    if not email or "@" not in email:
        return jsonify({"ok": False}), 400

    api_key, from_email = get_resend_credentials()
    if api_key:
        resend.api_key = api_key
        if not from_email or any(d in from_email for d in ["gmail.com", "yahoo.com", "hotmail.com"]):
            from_email = "Hair Extensions Hub <hello@bookings.hairextensions.app>"
        row_label = f"{rows} row{'s' if rows != 1 else ''}"
        len_note  = {"18": "Below shoulder", "22": "Mid-back — most popular", "26": "Lower back — luxurious"}.get(str(length), f"{length} inch")
        html_content = f"""
        <div style="font-family:Georgia,serif;max-width:560px;margin:0 auto;background:#1A1208;color:#FAF6EF;padding:40px 36px;border-radius:4px">
          <p style="font-size:11px;letter-spacing:3px;text-transform:uppercase;color:#C9A96E;margin:0 0 8px">Hair Extensions Hub</p>
          <h1 style="font-size:24px;font-weight:300;color:#fff;margin:0 0 6px;line-height:1.2">Your grams recommendation</h1>
          <p style="font-size:13px;color:rgba(250,246,239,.4);margin:0 0 28px">Based on your answers — personalised for your hair.</p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px">
            <div style="background:rgba(201,169,110,.08);border:1px solid rgba(201,169,110,.15);padding:16px">
              <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(201,169,110,.6);margin-bottom:6px">Grams</div>
              <div style="font-size:28px;font-weight:300;color:#fff;line-height:1">{grams}g</div>
              <div style="font-size:11px;color:rgba(250,246,239,.35);margin-top:4px">{row_label}</div>
            </div>
            <div style="background:rgba(201,169,110,.08);border:1px solid rgba(201,169,110,.15);padding:16px">
              <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(201,169,110,.6);margin-bottom:6px">Length</div>
              <div style="font-size:28px;font-weight:300;color:#fff;line-height:1">{length}&Prime;</div>
              <div style="font-size:11px;color:rgba(250,246,239,.35);margin-top:4px">{len_note}</div>
            </div>
          </div>
          <div style="background:rgba(201,169,110,.06);border:1px solid rgba(201,169,110,.1);padding:14px 16px;margin-bottom:20px">
            <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:rgba(201,169,110,.5);margin-bottom:4px">Recommended weft</div>
            <div style="font-size:14px;color:#E8D5B0">{weft}</div>
          </div>
          <p style="font-size:13px;color:rgba(250,246,239,.55);line-height:1.75;font-style:italic;margin-bottom:28px">{explain}</p>
          <div style="border-top:1px solid rgba(201,169,110,.15);padding-top:20px;display:flex;gap:12px;flex-wrap:wrap">
            <a href="https://hairextensions.app/wefts#request" style="font-size:11px;font-weight:500;letter-spacing:2px;text-transform:uppercase;color:#1A1208;background:#C9A96E;padding:12px 20px;text-decoration:none;display:inline-block">Book with Donna →</a>
            <a href="https://stan.store/hairextensionshub" style="font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#C9A96E;border:1px solid rgba(201,169,110,.3);padding:12px 20px;text-decoration:none;display:inline-block">Get the $27 guide</a>
          </div>
          <p style="font-size:11px;color:rgba(250,246,239,.15);margin-top:24px">Hair Extensions Hub · City of Moreton Bay · hairextensions.app</p>
        </div>
        """
        try:
            resend.Emails.send({
                "from": from_email,
                "to": [email],
                "subject": f"Your hair extensions recommendation — {grams}g, {length} inch",
                "html": html_content
            })
            print(f"Grams email sent to {email}")
        except Exception as e:
            print(f"Grams email error: {e}")

    return jsonify({"ok": True})

@app.route("/digital")
def digital():
    return render_template("digital.html", notify_success=False)

@app.route("/digital-notify", methods=["POST"])
def digital_notify():
    name = request.form.get("notify_name", "").strip()
    email = request.form.get("notify_email", "").strip()
    if not email or "@" not in email:
        return redirect(url_for("digital"))
    data = {
        "type": "digital_notify",
        "timestamp": datetime.utcnow().isoformat(),
        "name": name,
        "email": email,
    }
    submission_id = uuid.uuid4().hex[:12]
    filename = f"submissions/{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}_notify_{submission_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return render_template("digital.html", notify_success=True)

@app.route("/weft-booking", methods=["POST"])
def weft_booking():
    name = request.form.get("name", "").strip()
    mobile = request.form.get("mobile", "").strip()
    email = request.form.get("email", "").strip()
    location = request.form.get("suburb", request.form.get("location", "")).strip()
    service = request.form.get("service", "").strip()
    weft_type = request.form.get("weft_type", request.form.get("weftType", "")).strip()
    length = request.form.get("length", "").strip()
    grams = request.form.get("grams", "").strip()
    notes = request.form.get("notes", "").strip()
    
    if not name or not email or not mobile or not service:
        return "Please fill in all required fields.", 400
    
    data = {
        "type": "weft_booking",
        "timestamp": datetime.utcnow().isoformat(),
        "name": name,
        "mobile": mobile,
        "email": email,
        "location": location,
        "service": service,
        "weft_type": weft_type,
        "length": length,
        "grams": grams,
        "notes": notes,
    }
    
    submission_id = uuid.uuid4().hex[:12]
    filename = f"submissions/{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}_weft_{submission_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    send_weft_booking_email(data)
    
    return redirect(url_for("booking_thank_you", name=name))

@app.route("/booking-thank-you")
def booking_thank_you():
    client_name = request.args.get("name", "")
    return render_template("booking_thankyou.html", client_name=client_name)

@app.route("/personalised-plan", methods=["POST"])
def personalised_plan():
    client_name = request.form.get("client_name", "").strip()
    email = request.form.get("email", "").strip()
    hair_length = request.form.get("hair_length", "").strip()
    hair_thickness = request.form.get("hair_thickness", "").strip()
    hair_texture = request.form.get("hair_texture", "").strip()
    main_goal = request.form.get("main_goal", "").strip()
    
    if not client_name or not email or not hair_length or not hair_thickness or not hair_texture or not main_goal:
        return "Please fill in all required fields.", 400
    
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "client_name": client_name,
        "email": email,
        "country": request.form.get("country", "").strip(),
        "city": request.form.get("city", "").strip(),
        "hair_length": hair_length,
        "hair_thickness": hair_thickness,
        "hair_texture": hair_texture,
        "hair_colour": request.form.get("hair_colour", "").strip(),
        "wash_frequency": request.form.get("wash_frequency", "").strip(),
        "heat_styling": request.form.get("heat_styling", "").strip(),
        "budget": request.form.get("budget", "").strip(),
        "had_extensions": request.form.get("had_extensions", "").strip(),
        "main_goal": main_goal,
        "concerns": request.form.get("concerns", "").strip(),
    }
    
    submission_id = uuid.uuid4().hex[:12]
    filename = f"submissions/{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}_{submission_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    send_notification_email(data)
    
    return redirect(url_for("thank_you", name=client_name))

@app.route("/thank-you")
def thank_you():
    client_name = request.args.get("name", "")
    return render_template("thankyou.html", client_name=client_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
