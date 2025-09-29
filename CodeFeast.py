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
        
    
    def generate_content(self, name):
        """Simple content generation (centered layout with improved typography)"""
        return f"""
        <div style="max-width:520px; margin:0 auto; text-align:center;">
          <h2 style="margin:0 0 12px; font-size:22px; line-height:1.35; color:#ffffff; letter-spacing:-0.2px; font-weight:800;">
            Congratulations {name}! 🎉
          </h2>
          <p style="margin:0 0 12px; color:#cbd5e1; font-size:16px; line-height:1.7;">
            You have successfully completed the <strong>{self.event_name}</strong>!
          </p>
          <p style="margin:0 0 12px; color:#cbd5e1; font-size:16px; line-height:1.7;">
            Your completion certificate is attached to this email.
          </p>
          <p style="margin:0 0 16px; color:#cbd5e1; font-size:16px; line-height:1.7;">
            Keep learning and building amazing projects!
          </p>
          <p style="margin:0; color:#94a3b8; font-size:14px; line-height:1.6;">
            Best regards,<br>{self.organization_name} Team
          </p>
        </div>
        """
    
    def generate_next_steps(self):
        """Simple next steps (centered block, readable on mobile)"""
        return """
        <div style="max-width:520px; margin:12px auto 0; text-align:center;">
          <p style="margin:0 0 10px; color:#e2e8f0; font-weight:700; letter-spacing:.2px;">Next Steps</p>
          <p style="margin:6px 0; color:#cbd5e1; font-size:14px;">✅ Download your certificate</p>
          <p style="margin:6px 0; color:#cbd5e1; font-size:14px;">🚀 Start building MERN projects</p>
          <p style="margin:6px 0; color:#cbd5e1; font-size:14px;">📚 Keep learning!</p>
        </div>
        """
    
    def generate_html_template(self, name):
        """User-specified Web3 template (fully responsive and centered)"""
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
    
    /* Mobile responsiveness */
    @media only screen and (max-width: 600px) {{
      .outer-pad {{ padding: 12px !important; }}
      .container {{ width: 100% !important; max-width: 100% !important; }}
      .card {{ border-radius: 12px !important; }}
      .px {{ padding: 24px 20px !important; }}
      .title {{ font-size: 22px !important; line-height: 1.3 !important; }}
      .eyebrow {{ font-size: 11px !important; padding: 5px 11px !important; }}
      .hero-text {{ font-size: 13px !important; }}
      .chips span {{ 
        display: inline-block !important; 
        margin: 4px 5px 4px 0 !important;
        font-size: 11px !important;
        padding: 5px 9px !important;
      }}
      .divider-pad {{ padding: 0 20px !important; }}
      .footer {{ font-size: 11px !important; padding: 16px 20px !important; line-height: 1.5 !important; }}
      .gradient-bar {{ height: 3px !important; }}
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
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {{
      .dark-mode-bg {{ background: #0b0f1a !important; }}
      .dark-mode-card {{ background: #0e1320 !important; }}
    }}
  </style>
</head>
<body style="margin:0; padding:0; background:#0b0f1a; color:#e5e7eb; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height:1.6;">
  <!-- Preheader text (hidden) -->
  <div style="display:none; max-height:0; overflow:hidden; mso-hide:all;">
    🎉 Congratulations on completing {self.event_name}! Your certificate is ready.
  </div>
  
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#0b0f1a;" class="dark-mode-bg">
    <tr>
      <td align="center" class="outer-pad" style="padding:32px 24px;">
        <!-- Main Container -->
        <table role="presentation" width="640" align="center" cellspacing="0" cellpadding="0" border="0" class="container card" style="width:100%; max-width:640px; background:#0e1320; border-radius:20px; border:1px solid rgba(124,58,237,0.4); box-shadow:0 0 0 1px rgba(0,229,255,0.08), 0 20px 40px -12px rgba(124,58,237,0.3), 0 8px 20px -8px rgba(0,0,0,0.4); overflow:hidden; margin:0 auto;">
          
          <!-- Gradient Bar -->
          <tr>
            <td class="gradient-bar" style="padding:0; height:4px; background:linear-gradient(90deg, #00e5ff 0%, #7c3aed 50%, #00e5ff 100%); background-size: 200% 100%;"></td>
          </tr>
          
          <!-- Header Section -->
          <tr>
            <td class="px" style="padding:36px 32px 12px 32px; text-align:center;">
              <div class="eyebrow" style="display:inline-block; padding:7px 14px; border:1px solid rgba(0,229,255,0.4); border-radius:999px; font-size:12px; letter-spacing:0.1em; text-transform:uppercase; color:#a5f3fc; background:rgba(2,6,23,0.7); font-weight:600; box-shadow:0 0 20px rgba(0,229,255,0.15);">
                ✨ Certificate of Completion
              </div>
              
              <h1 class="title" style="margin:20px 0 10px; font-size:28px; line-height:1.2; color:#ffffff; letter-spacing:-0.5px; font-weight:800; text-shadow:0 2px 10px rgba(124,58,237,0.3);">
                {self.event_name}
              </h1>
              
              <p class="hero-text" style="margin:0 0 20px; color:#94a3b8; font-size:15px; line-height:1.6;">
                <strong style="color:#e5e7eb; font-weight:700;">{name}</strong> 👋 — you've officially completed the {self.event_name}.<br>
                <span style="color:#a5f3fc;">Welcome to the builders.</span>
              </p>
            </td>
          </tr>
          
          <!-- Divider -->
          <tr>
            <td class="divider-pad" style="padding:0 32px;">
              <div style="height:1px; width:100%; background:linear-gradient(90deg, rgba(0,229,255,0) 0%, rgba(0,229,255,0.6) 50%, rgba(0,229,255,0) 100%);"></div>
            </td>
          </tr>
          
          <!-- Content Section -->
          <tr>
            <td class="px" style="padding:28px 32px 8px 32px;">
              {self.generate_content(name)}
              
              <!-- Tech Stack Chips -->
              <div class="chips" style="margin:22px 0 8px; text-align:center; line-height:1.8;">
                <span style="display:inline-block; margin:4px 6px 4px 0; padding:7px 12px; border-radius:10px; font-size:12px; font-weight:600; color:#a5f3fc; background:rgba(3,105,161,0.12); border:1px solid rgba(3,105,161,0.4); box-shadow:0 2px 8px rgba(3,105,161,0.15); transition:all 0.3s;">
                  MongoDB
                </span>
                <span style="display:inline-block; margin:4px 6px 4px 0; padding:7px 12px; border-radius:10px; font-size:12px; font-weight:600; color:#c7d2fe; background:rgba(67,56,202,0.15); border:1px solid rgba(67,56,202,0.4); box-shadow:0 2px 8px rgba(67,56,202,0.15); transition:all 0.3s;">
                  Express
                </span>
                <span style="display:inline-block; margin:4px 6px 4px 0; padding:7px 12px; border-radius:10px; font-size:12px; font-weight:600; color:#6ee7b7; background:rgba(6,78,59,0.15); border:1px solid rgba(6,78,59,0.4); box-shadow:0 2px 8px rgba(6,78,59,0.15); transition:all 0.3s;">
                  React
                </span>
                <span style="display:inline-block; margin:4px 6px 4px 0; padding:7px 12px; border-radius:10px; font-size:12px; font-weight:600; color:#fca5a5; background:rgba(127,29,29,0.15); border:1px solid rgba(127,29,29,0.4); box-shadow:0 2px 8px rgba(127,29,29,0.15); transition:all 0.3s;">
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
            <td class="footer" style="padding:20px 28px; border-top:1px solid rgba(148,163,184,0.15); text-align:center; color:#94a3b8; font-size:12px; line-height:1.7; background:rgba(2,6,23,0.4);">
              <div style="margin-bottom:8px; color:#cbd5e1;">
                📎 <strong style="color:#e5e7eb;">Attached:</strong> PDF certificate for {name}
              </div>
              <div style="color:#64748b;">
                If the button doesn't work, open the attachment directly.
              </div>
              <div style="margin-top:12px; padding-top:12px; border-top:1px solid rgba(148,163,184,0.1); color:#64748b;">
                Built with <span style="color:#f87171;">❤️</span> by <strong style="color:#94a3b8;">{self.organization_name}</strong>
              </div>
            </td>
          </tr>
        </table>
        
        <!-- Spacer for email clients -->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-top:16px;">
          <tr>
            <td style="text-align:center; color:#64748b; font-size:11px; padding:0 20px;">
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
        msg['From'] = self.sender_email
        msg['To'] = email

        # Generate HTML content
        html_content = self.generate_html_template(name)
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))

        # Attach certificate if provided
        if certificate_path and os.path.exists(certificate_path):
            try:
                with open(certificate_path, "rb") as f:
                    file_attachment = MIMEApplication(f.read(), _subtype="pdf")
                    filename = f"{name.replace(' ', '_')}_Certificate.pdf"
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
