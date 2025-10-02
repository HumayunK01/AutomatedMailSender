import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import sys
import time
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple email sender class
class EmailSender:
    def __init__(self):
        # Simple configuration
        self.sender_email = os.getenv('SENDER_EMAIL', 'your_email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'your_gmail_app_password_here')
        self.event_name = os.getenv('EVENT_NAME', 'MERN Workshop')
        self.participants_file = os.getenv('PARTICIPANTS_FILE', 'data/participants.csv')
        self.delay = int(os.getenv('DELAY_BETWEEN_EMAILS', '30'))
        self.organization_name = os.getenv('ORGANIZATION_NAME', 'Programmers Club')
        
    
    def generate_achievement_badge(self):
        """Generate achievement badge section"""
        return """
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 24px; margin: 20px 0; text-align: center;">
          <div style="font-size: 48px; margin-bottom: 8px;">🏆</div>
          <h3 style="color: #ffffff; font-size: 18px; font-weight: 700; margin: 0 0 8px 0;">Achievement Unlocked!</h3>
          <p style="color: #e9d5ff; font-size: 14px; margin: 0;">You've mastered the MERN Stack</p>
        </div>
        """
    
    def generate_stats_section(self):
        """Generate completion stats"""
        return """
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin: 24px 0;">
          <tr>
            <td align="center" style="padding: 16px; background: #f0fdf4; border-radius: 8px; width: 33.33%;">
              <div style="font-size: 24px; font-weight: 700; color: #166534; margin-bottom: 4px;">✓</div>
              <div style="font-size: 12px; color: #166534; font-weight: 600;">Completed</div>
            </td>
            <td style="width: 8px;"></td>
            <td align="center" style="padding: 16px; background: #eff6ff; border-radius: 8px; width: 33.33%;">
              <div style="font-size: 24px; font-weight: 700; color: #1e40af; margin-bottom: 4px;">★</div>
              <div style="font-size: 12px; color: #1e40af; font-weight: 600;">Certified</div>
            </td>
            <td style="width: 8px;"></td>
            <td align="center" style="padding: 16px; background: #fef3c7; border-radius: 8px; width: 33.33%;">
              <div style="font-size: 24px; font-weight: 700; color: #92400e; margin-bottom: 4px;">🚀</div>
              <div style="font-size: 12px; color: #92400e; font-weight: 600;">Ready</div>
            </td>
          </tr>
        </table>
        """    
    def generate_content(self, name):
        """Professional full-width content generation"""
        return f"""
        <div style="width:100%; text-align:center;">
          <h2 style="margin:0 0 12px; font-size:22px; line-height:1.35; color:#1e293b; letter-spacing:-0.2px; font-weight:800;">
            Congratulations {name}! 🎉
          </h2>
          <p style="margin:0 0 12px; color:#475569; font-size:16px; line-height:1.7;">
            You have successfully completed the <strong>{self.event_name}</strong>!
          </p>
          <p style="margin:0 0 12px; color:#475569; font-size:16px; line-height:1.7;">
            Your completion certificate is attached to this email.
          </p>
          <p style="margin:0 0 16px; color:#475569; font-size:16px; line-height:1.7;">
            Keep learning and building amazing projects!
          </p>
          <p style="margin:0; color:#64748b; font-size:14px; line-height:1.6;">
            Best regards,<br>{self.organization_name} Team
          </p>
        </div>
        """
    
    def generate_next_steps(self):
        """Professional full-width next steps"""
        return """
        <div style="width:100%; margin:12px 0 0; text-align:center;">
          <p style="margin:0 0 10px; color:#1e293b; font-weight:700; letter-spacing:.2px;">Next Steps</p>
          <p style="margin:6px 0; color:#475569; font-size:14px;">✅ Download your certificate</p>
          <p style="margin:6px 0; color:#475569; font-size:14px;">🚀 Start building MERN projects</p>
          <p style="margin:6px 0; color:#475569; font-size:14px;">📚 Keep learning!</p>
        </div>
        """
    
    def generate_html_template(self, name):
        """Professional full-width responsive template"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>{self.event_name} - Certificate of Completion</title>
  <!--[if mso]>
  <style type="text/css">
    body, table, td {{font-family: Arial, sans-serif !important;}}
  </style>
  <![endif]-->
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
    
    /* Full width responsive design */
    .email-container {{ width: 100% !important; max-width: 100% !important; }}
    .main-table {{ width: 100% !important; max-width: 100% !important; }}
    
    /* Mobile responsiveness */
    @media only screen and (max-width: 600px) {{
      .outer-pad {{ padding: 8px !important; }}
      .container {{ width: 100% !important; max-width: 100% !important; margin: 0 !important; }}
      .card {{ border-radius: 0 !important; border-left: none !important; border-right: none !important; }}
      .px {{ padding: 20px 16px !important; }}
      .title {{ font-size: 24px !important; line-height: 1.3 !important; }}
      .eyebrow {{ font-size: 11px !important; padding: 6px 12px !important; }}
      .hero-text {{ font-size: 14px !important; }}
      .chips span {{ 
        display: inline-block !important; 
        margin: 3px 4px 3px 0 !important;
        font-size: 11px !important;
        padding: 6px 10px !important;
      }}
      .divider-pad {{ padding: 0 16px !important; }}
      .footer {{ font-size: 11px !important; padding: 16px !important; line-height: 1.5 !important; }}
      .gradient-bar {{ height: 3px !important; }}
      .content-section {{ padding: 20px 16px !important; }}
    }}
    
    /* Tablet responsiveness */
    @media only screen and (max-width: 768px) {{
      .outer-pad {{ padding: 12px !important; }}
      .container {{ width: 100% !important; max-width: 100% !important; }}
      .px {{ padding: 24px 20px !important; }}
      .title {{ font-size: 26px !important; }}
    }}
    
    /* Disable auto-link styling */
    a[x-apple-data-detectors] {{
      color: inherit !important;
      text-decoration: none !important;
      font-size: inherit !important;
      font-family: inherit !important;
      font-weight: inherit !important;
      line-height: inherit !important;
    }}
  </style>
</head>
<body style="margin:0; padding:0; background:#f8fafc; color:#334155; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height:1.6; width:100%;">
  <!-- Preheader text (hidden) -->
  <div style="display:none; max-height:0; overflow:hidden; mso-hide:all;">
    🎉 Congratulations on completing {self.event_name}! Your certificate is ready.
  </div>
  
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f8fafc; width:100%;" class="email-container">
    <tr>
      <td align="center" class="outer-pad" style="padding:16px 8px; width:100%;">
        <!-- Main Container -->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" class="container card main-table" style="width:100%; max-width:100%; background:#ffffff; border-radius:0; border:1px solid #e2e8f0; box-shadow:0 2px 4px rgba(0, 0, 0, 0.1); overflow:hidden; margin:0;">
          
          <!-- Gradient Bar -->
          <tr>
            <td class="gradient-bar" style="padding:0; height:4px; background:linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%); background-size: 200% 100%; width:100%;"></td>
          </tr>
          
          <!-- Header Section -->
          <tr>
            <td class="px" style="padding:32px 24px 16px 24px; text-align:center; width:100%;">
              <div class="eyebrow" style="display:inline-block; padding:8px 16px; border:1px solid #3b82f6; border-radius:999px; font-size:12px; letter-spacing:0.1em; text-transform:uppercase; color:#3b82f6; background:#eff6ff; font-weight:600;">
                ✨ Certificate of Completion
              </div>
              
              <h1 class="title" style="margin:20px 0 12px; font-size:28px; line-height:1.2; color:#1e293b; letter-spacing:-0.5px; font-weight:800;">
                {self.event_name}
              </h1>
              
              <p class="hero-text" style="margin:0 0 20px; color:#64748b; font-size:16px; line-height:1.6;">
                <strong style="color:#1e293b; font-weight:700;">{name}</strong> 👋 — you've successfully completed the {self.event_name}.<br>
                <span style="color:#3b82f6;">Congratulations on your achievement!</span>
              </p>
            </td>
          </tr>
          
          <!-- Divider -->
          <tr>
            <td class="divider-pad" style="padding:0 24px; width:100%;">
              <div style="height:1px; width:100%; background:linear-gradient(90deg, rgba(59,130,246,0) 0%, rgba(59,130,246,0.3) 50%, rgba(59,130,246,0) 100%);"></div>
            </td>
          </tr>
          
          <!-- Content Section -->
          <tr>
            <td class="px content-section" style="padding:24px; width:100%;">
              {self.generate_content(name)}
              
              <!-- Tech Stack Chips -->
              <div class="chips" style="margin:24px 0 12px; text-align:center; line-height:1.8;">
                <span style="display:inline-block; margin:4px 6px 4px 0; padding:8px 14px; border-radius:8px; font-size:12px; font-weight:600; color:#0369a1; background:#e0f2fe; border:1px solid #0ea5e9;">
                  MongoDB
                </span>
                <span style="display:inline-block; margin:4px 6px 4px 0; padding:8px 14px; border-radius:8px; font-size:12px; font-weight:600; color:#7c3aed; background:#f3e8ff; border:1px solid #a855f7;">
                  Express
                </span>
                <span style="display:inline-block; margin:4px 6px 4px 0; padding:8px 14px; border-radius:8px; font-size:12px; font-weight:600; color:#059669; background:#ecfdf5; border:1px solid #10b981;">
                  React
                </span>
                <span style="display:inline-block; margin:4px 6px 4px 0; padding:8px 14px; border-radius:8px; font-size:12px; font-weight:600; color:#dc2626; background:#fef2f2; border:1px solid #ef4444;">
                  Node.js
                </span>
              </div>
              
              <!-- Next Steps Section -->
              <div style="margin-top:24px;">
                {self.generate_next_steps()}
              </div>
            </td>
          </tr>
          
          <!-- Footer -->
          <tr>
            <td class="footer" style="padding:20px 24px; border-top:1px solid #e2e8f0; text-align:center; color:#64748b; font-size:12px; line-height:1.7; background:#f8fafc; width:100%;">
              <div style="margin-bottom:8px; color:#475569;">
                📎 <strong style="color:#1e293b;">Attached:</strong> JPG certificate for {name}
              </div>
              <div style="color:#64748b;">
                If the attachment doesn't work, please contact us for assistance.
              </div>
              <div style="margin-top:12px; padding-top:12px; border-top:1px solid #e2e8f0; color:#64748b;">
                Best regards,<br><strong style="color:#1e293b;">{self.organization_name} Team</strong>
              </div>
            </td>
          </tr>
        </table>
        
        <!-- Spacer for email clients -->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-top:16px; width:100%;">
          <tr>
            <td style="text-align:center; color:#94a3b8; font-size:11px; padding:0 16px; width:100%;">
              This email was sent because you completed {self.event_name}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
    
    def send_email(self, name, email, certificate_path=None):
        """Send simple email"""
        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = f"{self.event_name} - Certificate"
        msg['From'] = f"{self.event_name} <{self.sender_email}>"
        msg['To'] = email

        # Generate HTML content
        html_content = self.generate_html_template(name)
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        # Attach certificate if provided
        if certificate_path and os.path.exists(certificate_path):
            try:
                with open(certificate_path, "rb") as f:
                    file_attachment = MIMEApplication(f.read(), _subtype="jpg")
                    filename = f"{name.replace(' ', '_')}_Certificate.jpg"
                    file_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(file_attachment)
                    print(f"[ATTACH] Certificate: {filename}")
            except Exception as e:
                print(f"[ERROR] Could not attach certificate: {e}")

        try:
            # Send email
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, email, msg.as_string())
            server.quit()
            print(f"[SENT] Email sent to {name} ({email})")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send to {name}: {e}")
            return False
    


    def send_all_emails(self, participants_data):
        """Send emails to all participants"""
        success_count = 0
        total_count = len(participants_data)

        print(f"Sending emails to {total_count} participants...")

        for i, participant in enumerate(participants_data):
            name = participant.get('name', '')
            email = participant.get('email', '')
            certificate_path = participant.get('certificate_path')
            if not email:
                print(f"[SKIP] Missing email for {name}, skipping.")
                continue

            if self.send_email(name, email, certificate_path):
                success_count += 1

            # Delay between emails
            if i < total_count - 1:
                print(f"Waiting {self.delay} seconds...")
                time.sleep(self.delay)

        print(f"\nSent {success_count}/{total_count} emails successfully!")
        return success_count

    def load_participants(self):
        """Load participants from CSV file"""
        if not os.path.exists(self.participants_file):
            print(f"Error: File {self.participants_file} not found!")
            return []

        participants = []
        try:
            with open(self.participants_file, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = (row.get('name') or '').strip()
                    email = (row.get('email') or '').strip()
                    cert_path = (row.get('certificate_path') or '').strip()
                    if name and email:
                        participants.append({
                            'name': name,
                            'email': email,
                            'certificate_path': cert_path
                        })
                    else:
                        print(f"Skipping row with missing name or email: {row}")
            print(f"Loaded {len(participants)} participants from {self.participants_file}")
            return participants
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

# Main execution
if __name__ == "__main__":
    # Create email sender
    sender = EmailSender()

    # Load participants
    participants = sender.load_participants()

    if not participants:
        print("No participants to send emails to. Exiting.")
        sys.exit(1)

    # Send emails
    sender.send_all_emails(participants)
