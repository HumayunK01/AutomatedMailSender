import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import sys
import time
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email sender class for organizers
class OrganizerEmailSender:
    def __init__(self):
        # Configuration
        self.sender_email = os.getenv('SENDER_EMAIL', 'your_email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'your_gmail_app_password_here')
        self.event_name = os.getenv('EVENT_NAME', 'MERN Workshop')
        self.organizers_file = os.getenv('ORGANIZERS_FILE', 'data/organizers.json')
        self.delay = int(os.getenv('DELAY_BETWEEN_EMAILS', '30'))
        self.organization_name = os.getenv('ORGANIZATION_NAME', 'Programmers Club')
        
    
    def generate_organizer_content(self, name):
        """Special content for organizers"""
        return f"""
        <div style="width:100%; text-align:center;">
          <h2 style="margin:0 0 16px; font-size:24px; line-height:1.35; color:#1e293b; letter-spacing:-0.3px; font-weight:800;">
            Thank You for Your Dedication! 🙏
          </h2>
          <p style="margin:0 0 16px; color:#475569; font-size:17px; line-height:1.7;">
            Dear <strong>{name}</strong>,
          </p>
          <p style="margin:0 0 16px; color:#475569; font-size:17px; line-height:1.7;">
            Your tireless efforts and commitment made the <strong>{self.event_name}</strong> a tremendous success. As an organizer, you went above and beyond to create an exceptional learning experience for all participants.
          </p>
          <p style="margin:0 0 16px; color:#475569; font-size:17px; line-height:1.7;">
            Your certificate of appreciation is attached to this email as a token of our gratitude.
          </p>
          <p style="margin:0 0 20px; color:#475569; font-size:17px; line-height:1.7;">
            We couldn't have done it without you!
          </p>
        </div>
        """
    
    def generate_organizer_impact(self):
        """Impact section for organizers"""
        return """
        <div style="background:#fef3c7; padding:24px; margin:24px 0; border-left:4px solid #f59e0b;">
          <p style="margin:0 0 12px; color:#92400e; font-size:15px; font-weight:700;">
            Your Impact as an Organizer
          </p>
          <p style="margin:0; color:#92400e; font-size:15px; line-height:1.6;">
            You helped shape the future of aspiring developers by creating a welcoming learning environment and ensuring the event ran smoothly from start to finish.
          </p>
        </div>
        """
    
    def generate_html_template(self, name):
        """Professional organizer template with distinct design"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>{self.event_name} - Certificate of Appreciation</title>
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
      .title {{ font-size: 26px !important; line-height: 1.3 !important; }}
      .badge {{ font-size: 11px !important; padding: 6px 12px !important; }}
      .hero-text {{ font-size: 15px !important; }}
      .content-section {{ padding: 20px 16px !important; }}
    }}
    
    /* Tablet responsiveness */
    @media only screen and (max-width: 768px) {{
      .outer-pad {{ padding: 12px !important; }}
      .container {{ width: 100% !important; max-width: 100% !important; }}
      .px {{ padding: 24px 20px !important; }}
      .title {{ font-size: 28px !important; }}
    }}
  </style>
</head>
<body style="margin:0; padding:0; background:#fafafa; color:#334155; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height:1.6; width:100%;">
  <!-- Preheader text (hidden) -->
  <div style="display:none; max-height:0; overflow:hidden; mso-hide:all;">
    Thank you for organizing {self.event_name}! Your certificate of appreciation is ready.
  </div>
  
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#fafafa; width:100%;" class="email-container">
    <tr>
      <td align="center" class="outer-pad" style="padding:16px 8px; width:100%;">
        <!-- Main Container -->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" class="container card main-table" style="width:100%; max-width:100%; background:#ffffff; border-radius:0; border:1px solid #e5e7eb; box-shadow:0 2px 4px rgba(0, 0, 0, 0.08); overflow:hidden; margin:0;">
          
          <!-- Header Bar - Gold/Amber for organizers -->
          <tr>
            <td style="padding:0; height:5px; background:linear-gradient(90deg, #f59e0b 0%, #d97706 50%, #f59e0b 100%); width:100%;"></td>
          </tr>
          
          <!-- Header Section -->
          <tr>
            <td class="px" style="padding:40px 32px 20px 32px; text-align:center; width:100%; background:linear-gradient(180deg, #fffbeb 0%, #ffffff 100%);">
              <div class="badge" style="display:inline-block; padding:8px 18px; border:2px solid #f59e0b; border-radius:999px; font-size:12px; letter-spacing:0.1em; text-transform:uppercase; color:#d97706; background:#ffffff; font-weight:700; margin-bottom:20px;">
                ⭐ Certificate of Appreciation
              </div>
              
              <h1 class="title" style="margin:0 0 16px 0; font-size:32px; line-height:1.2; color:#1e293b; letter-spacing:-0.5px; font-weight:800;">
                {self.event_name}
              </h1>
              
              <p class="hero-text" style="margin:0; color:#64748b; font-size:17px; line-height:1.6;">
                In recognition of <strong style="color:#1e293b; font-weight:700;">{name}</strong>'s outstanding contribution<br>as an event organizer
              </p>
            </td>
          </tr>
          
          <!-- Divider -->
          <tr>
            <td style="padding:0 32px; width:100%;">
              <div style="height:1px; width:100%; background:linear-gradient(90deg, rgba(245,158,11,0) 0%, rgba(245,158,11,0.3) 50%, rgba(245,158,11,0) 100%);"></div>
            </td>
          </tr>
          
          <!-- Content Section -->
          <tr>
            <td class="px content-section" style="padding:32px; width:100%;">
              {self.generate_organizer_content(name)}
              
              <!-- Impact Section -->
              {self.generate_organizer_impact()}
              
              <!-- Closing Message -->
              <div style="text-align:center; margin:32px 0 20px 0;">
                <p style="margin:0 0 12px 0; color:#475569; font-size:17px; line-height:1.7;">
                  We look forward to working with you on future events!
                </p>
                <p style="margin:0 0 8px 0; color:#1e293b; font-size:18px; font-weight:600;">
                  With Gratitude,
                </p>
                <p style="margin:0; color:#1e293b; font-size:18px; font-weight:600;">
                  {self.organization_name} Team
                </p>
              </div>
              
            </td>
          </tr>
          
          <!-- Footer -->
          <tr>
            <td style="padding:24px 32px; border-top:1px solid #e5e7eb; text-align:center; color:#64748b; font-size:12px; line-height:1.7; background:#fafafa; width:100%;">
              <div style="margin-bottom:8px; color:#475569;">
                📎 <strong style="color:#1e293b;">Attached:</strong> Certificate of Appreciation for {name}
              </div>
              <div style="color:#64748b;">
                Your certificate recognizes your valuable contribution as an organizer
              </div>
              <div style="margin-top:16px; padding-top:16px; border-top:1px solid #e5e7eb; color:#9ca3af; font-size:11px;">
                {self.organization_name} | {self.event_name}
              </div>
            </td>
          </tr>
        </table>
        
        <!-- Spacer -->
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin-top:16px; width:100%;">
          <tr>
            <td style="text-align:center; color:#9ca3af; font-size:11px; padding:0 16px; width:100%;">
              This email was sent to recognize your contribution as an organizer of {self.event_name}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  
</body>
</html>"""
    
    def send_email(self, name, email, certificate_path=None):
        """Send email to organizer"""
        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = f"{self.event_name} - Certificate of Appreciation"
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
                    filename = f"{name.replace(' ', '_')}_Organizer_Certificate.jpg"
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
    

    def send_all_emails(self, organizers_data):
        """Send emails to all organizers"""
        success_count = 0
        total_count = len(organizers_data)

        print(f"Sending emails to {total_count} organizers...")

        for i, organizer in enumerate(organizers_data):
            name = organizer.get('name', '')
            email = organizer.get('email', '')
            certificate_path = organizer.get('certificate_path')
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

    def load_organizers(self):
        """Load organizers from JSON file"""
        if not os.path.exists(self.organizers_file):
            print(f"Error: File {self.organizers_file} not found!")
            return []

        try:
            with open(self.organizers_file, 'r', encoding='utf-8') as f:
                organizers = json.load(f)
                print(f"Loaded {len(organizers)} organizers from {self.organizers_file}")
                return organizers
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

# Main execution
if __name__ == "__main__":
    # Create email sender
    sender = OrganizerEmailSender()

    # Load organizers
    organizers = sender.load_organizers()

    if not organizers:
        print("No organizers to send emails to. Exiting.")
        sys.exit(1)

    # Send emails
    sender.send_all_emails(organizers)

