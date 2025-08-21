import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from enum import Enum
import sys
import time  # Added for delays
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set UTF-8 encoding for Windows console
if sys.platform.startswith('win'):
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        # Fallback: set console to UTF-8
        os.system('chcp 65001 >nul 2>&1')

class EmailType(Enum):
    WINNER = "winner"
    PARTICIPANT = "participant"
    ORGANIZER = "organizer"

class CodeFeastEmailSender:
    def __init__(self, sender_email=None, sender_password=None, event_name=None):
        # Load from environment variables or use provided values
        self.sender_email = sender_email or os.getenv('SENDER_EMAIL', 'programmersclub@mhssce.ac.in')
        self.sender_password = sender_password or os.getenv('SENDER_PASSWORD', 'your_gmail_app_password_here')
        self.event_name = event_name or os.getenv('EVENT_NAME', 'Code Feast 4.0')
        
        # Load timing configuration from environment
        self.delay_between_emails = int(os.getenv('DELAY_BETWEEN_EMAILS', '30'))
        self.delay_between_groups = int(os.getenv('DELAY_BETWEEN_GROUPS', '60'))
        
        # Load email server configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '465'))
        
        # Debug mode
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        
    def get_email_config(self, email_type):
        """Get email configuration based on type"""
        configs = {
            EmailType.WINNER: {
                "subject_emoji": "🏆",
                "subject_text": "Congratulations on Your Victory!",
                "header_title": "Winner Announcement",
                "header_subtitle": "Congratulations on your exceptional achievement!",
                "primary_color": "#1e40af",
                "secondary_color": "#0ea5e9",
                "accent_color": "#f0f9ff"
            },
            EmailType.PARTICIPANT: {
                "subject_emoji": "🎉",
                "subject_text": "Thank You for Participating!",
                "header_title": "Participation Certificate",
                "header_subtitle": "Your contribution made this event amazing!",
                "primary_color": "#059669",
                "secondary_color": "#10b981",
                "accent_color": "#f0fdf4"
            },
            EmailType.ORGANIZER: {
                "subject_emoji": "🎉",
                "subject_text": "Thank You for Organizing!",
                "header_title": "Organizer Certificate",
                "header_subtitle": "Appreciation for your hard work and dedication",
                "primary_color": "#7c3aed",
                "secondary_color": "#8b5cf6",
                "accent_color": "#faf5ff"
            }
        }
        return configs.get(email_type, configs[EmailType.PARTICIPANT])
    
    def generate_winner_content(self, data):
        """Generate content specific to winners"""
        rank_section = ""
        if data.get('rank_position'):
            medal_emoji = "🥇" if "1st" in str(data['rank_position']) else "🥈" if "2nd" in str(data['rank_position']) else "🥉"
            rank_section = f"""
            <div class="content-section" style="background: #fef3c7; padding: 25px; border-radius: 12px; margin: 25px 0; border-left: 5px solid #f59e0b; text-align: center;">
                <div class="achievement-medal" style="font-size: 48px; margin-bottom: 15px;">{medal_emoji}</div>
                <h3 style="color: #92400e; margin: 0 0 10px; font-size: 24px; font-weight: bold;">Achievement Unlocked!</h3>
                <p style="color: #92400e; margin: 0; font-size: 18px; font-weight: 600;">Position: {data['rank_position']}</p>
                <p style="color: #92400e; margin: 8px 0 0; font-size: 16px;">Competition: {self.event_name}</p>
            </div>"""
        
        return f"""
        <p style="margin: 0 0 25px; line-height: 1.6; color: #4b5563; font-size: 16px;">
            We are <strong>thrilled</strong> to announce that you have emerged as a <span style="color: #1e40af; font-weight: bold;">winner</span> in {self.event_name}! 
            Your outstanding performance demonstrated exceptional technical skills and innovative problem-solving abilities.
        </p>
        {rank_section}
        <div class="content-section" style="background: #f0f9ff; padding: 25px; border-radius: 12px; margin: 25px 0; text-align: center; border: 2px solid #0ea5e9;">
            <h3 style="color: #0c4a6e; margin: 0 0 15px; font-size: 22px;">📜 Your Winner Certificate</h3>
            <p style="color: #0c4a6e; margin: 0 0 20px; font-size: 16px; line-height: 1.5;">
                Your official {self.event_name} winner certificate has been attached to this email. 
                Display it with pride!
            </p>
        </div>
        """
    
    def generate_participant_content(self, data):
        """Generate content specific to participants"""
        return f"""
        <p style="margin: 0 0 25px; line-height: 1.6; color: #4b5563; font-size: 16px;">
            Thank you for being part of {self.event_name}! Your participation and enthusiasm contributed to making this event a tremendous success. 
            Every line of code you wrote and every problem you tackled brought value to our programming community.
        </p>
        <div class="content-section" style="background: #f0fdf4; padding: 25px; border-radius: 12px; margin: 25px 0; text-align: center; border: 2px solid #10b981;">
            <h3 style="color: #047857; margin: 0 0 15px; font-size: 22px;">📜 Your Participation Certificate</h3>
            <p style="color: #047857; margin: 0 0 20px; font-size: 16px; line-height: 1.5;">
                Your official {self.event_name} participation certificate has been attached to this email. 
                Keep coding and keep growing!
            </p>
        </div>
        """
    
    def generate_organizer_content(self, data):
        """Generate content specific to organizers"""
        stats = data.get('event_stats', {})
        return f"""
        <p style="margin: 0 0 25px; line-height: 1.6; color: #4b5563; font-size: 16px;">
            Here's a comprehensive summary of {self.event_name}. Thank you for your dedication in making this event successful!
        </p>
        <div class="content-section" style="background: #faf5ff; padding: 25px; border-radius: 12px; margin: 25px 0; border: 2px solid #8b5cf6;">
            <h3 style="color: #6b21a8; margin: 0 0 20px; font-size: 22px;">📊 Event Statistics</h3>
            <div class="stats-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div class="stats-item" style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #6b21a8;">{stats.get('total_participants', 'N/A')}</div>
                    <div style="color: #6b21a8; font-size: 14px;">Total Participants</div>
                </div>
                <div class="stats-item" style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #6b21a8;">{stats.get('problems_solved', 'N/A')}</div>
                    <div style="color: #6b21a8; font-size: 14px;">Problems Solved</div>
                </div>
                <div class="stats-item" style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #6b21a8;">{stats.get('completion_rate', 'N/A')}</div>
                    <div style="color: #6b21a8; font-size: 14px;">Completion Rate</div>
                </div>
            </div>
        </div>
        <div class="content-section" style="background: #f0f4ff; padding: 25px; border-radius: 12px; margin: 25px 0; text-align: center; border: 2px solid #8b5cf6;">
            <h3 style="color: #6b21a8; margin: 0 0 15px; font-size: 22px;">📜 Your Organizer Certificate</h3>
            <p style="color: #6b21a8; margin: 0 0 20px; font-size: 16px; line-height: 1.5;">
                Your official {self.event_name} organizer certificate has been attached to this email. 
                Thank you for your leadership and dedication!
            </p>
        </div>
        """
    
    def generate_next_steps(self, email_type, data):
        """Generate next steps based on email type"""
        steps = {
            EmailType.WINNER: [
                "🏆 Download and save your winner certificate",
                "📱 Share your achievement on LinkedIn and social media",
                "🏷️ Tag @Programmers Club in your posts",
                "📌 Use hashtags: #CodeFeast4.0 #Programming #Winner"
            ],
            EmailType.PARTICIPANT: [
                "📜 Download your participation certificate",
                "📚 Continue practicing on coding platforms",
                "🌟 Follow us for upcoming events and workshops",
                "📱 Share your coding journey on social media"
            ],
            EmailType.ORGANIZER: [
                "📜 Download your organizer certificate",
                "📧 Send follow-up communications to winners",
                "📋 Document lessons learned for future events",
                "🎯 Plan improvements for the next iteration",
                "🤝 Coordinate with sponsors and partners"
            ]
        }
        
        step_list = steps.get(email_type, steps[EmailType.PARTICIPANT])
        step_html = "".join([f'<p style="color: #374151; margin: 0 0 12px; font-size: 16px; line-height: 1.5;">{step}</p>' for step in step_list])
        
        return f"""
        <div style="background: #f8fafc; padding: 25px; border-radius: 12px; margin: 25px 0; border: 1px solid #e2e8f0;">
            <h3 style="color: #1f2937; margin: 0 0 20px; font-size: 20px;">🚀 Next Steps</h3>
            {step_html}
        </div>
        """
    
    def generate_html_template(self, email_type, data):
        """Generate complete HTML template based on email type and data"""
        config = self.get_email_config(email_type)
        
        # Generate type-specific content
        content_generators = {
            EmailType.WINNER: self.generate_winner_content,
            EmailType.PARTICIPANT: self.generate_participant_content,
            EmailType.ORGANIZER: self.generate_organizer_content
        }
        
        main_content = content_generators[email_type](data)
        next_steps = self.generate_next_steps(email_type, data)
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="format-detection" content="telephone=no">
            <meta name="x-apple-disable-message-reformatting">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <title>{self.event_name} - {config['header_title']}</title>
            <!--[if mso]>
            <noscript>
                <xml>
                    <o:OfficeDocumentSettings>
                        <o:PixelsPerInch>96</o:PixelsPerInch>
                    </o:OfficeDocumentSettings>
                </xml>
            </noscript>
            <![endif]-->
            <style type="text/css">
                /* Reset styles */
                body, table, td, p, a, li, blockquote {{
                    -webkit-text-size-adjust: 100%;
                    -ms-text-size-adjust: 100%;
                }}
                table, td {{
                    mso-table-lspace: 0pt;
                    mso-table-rspace: 0pt;
                }}
                img {{
                    -ms-interpolation-mode: bicubic;
                    max-width: 100%;
                    height: auto;
                }}
                
                /* Responsive styles */
                @media screen and (max-width: 600px) {{
                    .email-container {{
                        width: 100% !important;
                        margin: 0 !important;
                        border-radius: 0 !important;
                    }}
                    .header-section {{
                        padding: 30px 20px !important;
                    }}
                    .header-title {{
                        font-size: 24px !important;
                        line-height: 1.2 !important;
                    }}
                    .header-subtitle {{
                        font-size: 16px !important;
                    }}
                    .header-description {{
                        font-size: 14px !important;
                    }}
                    .main-content {{
                        padding: 25px 20px !important;
                    }}
                    .greeting-title {{
                        font-size: 20px !important;
                        line-height: 1.3 !important;
                    }}
                    .content-section {{
                        padding: 20px !important;
                        margin: 20px 0 !important;
                    }}
                    .stats-grid {{
                        display: block !important;
                    }}
                    .stats-item {{
                        margin-bottom: 15px !important;
                        display: block !important;
                    }}
                    .cta-button {{
                        padding: 14px 20px !important;
                        font-size: 16px !important;
                        display: block !important;
                        width: 80% !important;
                        max-width: 200px !important;
                        margin: 20px auto !important;
                    }}
                    .footer-section {{
                        padding: 15px 20px !important;
                    }}
                    .date-badge {{
                        position: static !important;
                        margin: 0 auto 15px !important;
                        display: inline-block !important;
                    }}
                    .achievement-medal {{
                        font-size: 40px !important;
                    }}
                    .signature-section {{
                        padding-top: 25px !important;
                        margin-top: 30px !important;
                    }}
                }}
                
                @media screen and (max-width: 480px) {{
                    .email-container {{
                        margin: 5px !important;
                    }}
                    .header-section {{
                        padding: 25px 15px !important;
                    }}
                    .main-content {{
                        padding: 20px 15px !important;
                    }}
                    .content-section {{
                        padding: 15px !important;
                    }}
                    .header-title {{
                        font-size: 22px !important;
                    }}
                    .achievement-medal {{
                        font-size: 36px !important;
                    }}
                }}
                
                /* Dark mode support */
                @media (prefers-color-scheme: dark) {{
                    .email-bg {{
                        background: #1f2937 !important;
                    }}
                    .email-container {{
                        background: #374151 !important;
                    }}
                    .main-content {{
                        color: #f9fafb !important;
                    }}
                }}
            </style>
        </head>
        <body class="email-bg" style="margin: 0; padding: 0; font-family: 'Arial', 'Helvetica', sans-serif; line-height: 1.6; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;">
            <div style="padding: 10px;">
                <div class="email-container" style="max-width: 650px; margin: 10px auto; background: #ffffff; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); overflow: hidden;">
                    
                    <!-- Header Section -->
                    <div class="header-section" style="background: linear-gradient(135deg, {config['primary_color']} 0%, {config['secondary_color']} 100%); padding: 40px 30px; text-align: center; position: relative;">
                        <h1 class="header-title" style="color: #ffffff; margin: 0 0 10px; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.1); line-height: 1.2;">{self.event_name}</h1>
                        <p class="header-subtitle" style="color: #e2e8f0; margin: 0 0 15px; font-size: 18px; font-weight: 600;">{config['header_title']}</p>
                        <p class="header-description" style="color: #cbd5e1; margin: 0; font-size: 15px; line-height: 1.5; max-width: 400px; margin: 0 auto;">{config['header_subtitle']}</p>
                    </div>
                    
                    <!-- Main Content -->
                    <div class="main-content" style="padding: 35px 30px; color: #333333;">
                        <!-- Personalized Greeting -->
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h2 class="greeting-title" style="color: #1f2937; font-weight: 700; font-size: 22px; margin: 0 0 10px; line-height: 1.3;">Hello {data.get('name', 'Participant')}! 👋</h2>
                            <div style="width: 60px; height: 4px; background: {config['secondary_color']}; margin: 0 auto; border-radius: 2px;"></div>
                        </div>
                        
                        {main_content}
                        {next_steps}
                        
                        <!-- Signature -->
                        <div class="signature-section" style="margin-top: 35px; padding-top: 30px; border-top: 2px solid #e5e7eb; text-align: center;">
                            <p style="margin: 0 0 5px; color: #1f2937; font-weight: 600; font-size: 16px;">With appreciation,</p>
                            <p style="margin: 0 0 5px; color: {config['primary_color']}; font-weight: 800; font-size: 20px;">{self.event_name} Team</p>
                            <p style="margin: 0 0 5px; color: #6b7280; font-size: 14px; font-weight: 600;">Programmers Club</p>
                            <p style="margin: 10px 0 0; color: #9ca3af; font-size: 12px;">Making coding accessible to everyone</p>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div class="footer-section" style="background: #f9fafb; padding: 20px 30px; border-top: 1px solid #e5e7eb; text-align: center;">
                        <p style="margin: 0; color: #6b7280; font-size: 12px; line-height: 1.4;">
                            This email was sent by {self.event_name} Team. If you have any questions, please contact us.<br>
                            © 2025 Programmers Club. All rights reserved.
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_template
    
    def send_email(self, email_type, recipient_data, attachment_path=None):
        """Send email based on type and recipient data"""
        config = self.get_email_config(email_type)
        
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"{self.event_name} - {config['subject_text']} {config['subject_emoji']}"
        msg['From'] = f"{self.event_name} Team <{self.sender_email}>"
        msg['To'] = recipient_data['email']
        
        # Generate HTML content
        html_content = self.generate_html_template(email_type, recipient_data)
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Attach file if provided
        if attachment_path and os.path.exists(attachment_path):
            try:
                with open(attachment_path, "rb") as f:
                    file_attachment = MIMEApplication(f.read(), _subtype="pdf")
                    filename = f"{recipient_data['name'].replace(' ', '_')}_{self.event_name.replace(' ', '_')}_Certificate.pdf"
                    file_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(file_attachment)
                    print(f"[SUCCESS] Certificate attached: {filename}")
            except Exception as e:
                print(f"[ERROR] Error attaching certificate: {e}")
        elif attachment_path:
            print(f"[WARNING] Certificate file not found: {attachment_path}")
        
        try:
            # Create secure connection and send email
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient_data['email'], msg.as_string())
            server.quit()
            print(f"[SUCCESS] Email sent to {recipient_data['name']} ({recipient_data['email']})")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error sending email to {recipient_data['name']}: {e}")
            return False
    


    def send_batch_emails(self, email_type, recipients_data):
        """Send batch emails of specified type with delays to prevent rate limiting"""
        success_count = 0
        failed_emails = []  # Track failed emails
        total_count = len(recipients_data)
        
        print(f"\n[INFO] Starting batch email send for {email_type.value}s...")
        print(f"[INFO] Total emails to send: {total_count}")
        print(f"[INFO] Estimated time: {total_count * self.delay_between_emails} seconds ({total_count * self.delay_between_emails // 60} minutes {total_count * self.delay_between_emails % 60} seconds)\n")
        
        for i, recipient in enumerate(recipients_data):
            email_sent = False
            try:
                success = self.send_email(
                    email_type,
                    recipient,
                    recipient.get('certificate_path')
                )
                if success:
                    success_count += 1
                    email_sent = True
                    print(f"[PROGRESS] {i+1}/{total_count} emails sent successfully")
                    
                    # Add delay between emails (except for the last one)
                    if i < total_count - 1:
                        print(f"[WAIT] Waiting {self.delay_between_emails} seconds before next email...")
                        time.sleep(self.delay_between_emails)
                        
            except UnicodeEncodeError as e:
                print(f"[ERROR] Encoding error for {recipient['name']}: {str(e)}")
                # Try to send without emoji in subject
                try:
                    config = self.get_email_config(email_type)
                    config['subject_emoji'] = ''  # Remove emoji
                    success = self.send_email(
                        email_type,
                        recipient,
                        recipient.get('certificate_path')
                    )
                    if success:
                        success_count += 1
                        email_sent = True
                        print(f"[PROGRESS] {i+1}/{total_count} emails sent successfully (retry)")
                        
                        # Add delay between emails (except for the last one)
                        if i < total_count - 1:
                            print(f"[WAIT] Waiting {self.delay_between_emails} seconds before next email...")
                            time.sleep(self.delay_between_emails)
                            
                except Exception as e2:
                    failed_emails.append({
                        "name": recipient['name'],
                        "email": recipient['email'],
                        "error": f"Encoding retry failed: {e2}"
                    })
                    print(f"[ERROR] Failed to send to {recipient['name']} (retry): {e2}")
            except Exception as e:
                failed_emails.append({
                    "name": recipient['name'],
                    "email": recipient['email'],
                    "error": str(e)
                })
                print(f"[ERROR] Failed to send to {recipient['name']}: {e}")
            
            # If email wasn't sent through any method, add to failed list
            if not email_sent:
                # Check if already added to avoid duplicates
                if not any(f['email'] == recipient['email'] for f in failed_emails):
                    failed_emails.append({
                        "name": recipient['name'],
                        "email": recipient['email'],
                        "error": "Unknown error - email not sent"
                    })
        
        print(f"\n[SUMMARY] {success_count}/{total_count} emails sent successfully!")
        
        # Display failed emails if any
        if failed_emails:
            print(f"\n[FAILED EMAILS DEBUG] {len(failed_emails)} emails failed to send:")
            print("=" * 80)
            for i, failed in enumerate(failed_emails, 1):
                print(f"{i}. Name: {failed['name']}")
                print(f"   Email: {failed['email']}")
                print(f"   Error: {failed['error']}")
                print("-" * 60)
        else:
            print(f"\n[SUCCESS] All {email_type.value} emails sent successfully! 🎉")
        
        return success_count, failed_emails

# Example usage
if __name__ == "__main__":
    # Initialize email sender (loads configuration from .env file)
    sender = CodeFeastEmailSender()
    
    # Winners data (Top 3)
    winners_data = [
        {
            "email": "arzoo.232262.co@mhssce.ac.in",
            "name": "Aarzoo Nazim Asar",
            "certificate_path": "certificates/winners/aarzoonazimasar.pdf",
            "rank_position": "1st Place"
        },
        {
            "email": "mohammedanasnathani0123@gmail.com",
            "name": "Mohammed Anas Nathani",
            "certificate_path": "certificates/winners/mohammedanasnathani.pdf",
            "rank_position": "2nd Place"
        },
        {
            "email": "mohammedsaif.s@somaiya.edu",
            "name": "Mohammed Saif Shaikh",
            "certificate_path": "certificates/winners/mohammedsaifshaikh.pdf",
            "rank_position": "3rd Place"
        }
    ]
    
    # Participants data
    participants_data = [
        {
            "email": "makardwaj.231838.ci@mhssce.ac.in",
            "name": "Makardwaj Parab",
            "certificate_path": "certificates/participants/makardwajparab.pdf"
        },
        {
            "email": "sahil.241708.cs@mhssce.ac.in",
            "name": "Sahil Ansari",
            "certificate_path": "certificates/participants/sahilansari.pdf"
        },
        {
            "email": "zoha251284@gmail.com",
            "name": "Ansari Zoha Najmul Kalam",
            "certificate_path": "certificates/participants/ansarizohanajmulkalam.pdf"
        },
        {
            "email": "saif.231824.ci@mhssce.ac.in",
            "name": "Khan Mohammad Saif",
            "certificate_path": "certificates/participants/khanmohammadsaif.pdf"
        },
        {
            "email": "ramsha.231807.ci@mhssce.ac.in",
            "name": "Ansari Ramsha",
            "certificate_path": "certificates/participants/ansariramshashakil.pdf"
        },
        {
            "email": "hashir.231825.ci@mhssce.ac.in",
            "name": "Khan Mohd Hashir",
            "certificate_path": "certificates/participants/khanmohdhashir.pdf"
        },
        {
            "email": "laaibah.231820.ci@mhssce.ac.in",
            "name": "Khan Laaibah",
            "certificate_path": "certificates/participants/khanlaaibah.pdf"
        },
        {
            "email": "abdullah.221829.ci@mhssce.ac.in",
            "name": "Abdullah Mewawala",
            "certificate_path": "certificates/participants/abdullahmewawala.pdf"
        },
        {
            "email": "maaz.221842.ci@mhssce.ac.in",
            "name": "Shaikh Maaz",
            "certificate_path": "certificates/participants/shaikhmaaz.pdf"
        },
        {
            "email": "afjal.221246.co@mhssce.ac.in",
            "name": "Shaikh Mohammed Afjal",
            "certificate_path": "certificates/participants/shaikhmohammedafjal.pdf"
        },
        {
            "email": "ayaanshaikh9421@gmail.com",
            "name": "Ayaan Shaikh",
            "certificate_path": "certificates/participants/ayaanshaikh.pdf"
        },
        {
            "email": "umar.221208.co@mhssce.ac.in",
            "name": "Ansari Umar Farooque",
            "certificate_path": "certificates/participants/ansariumarfarooque.pdf"
        },
        {
            "email": "baria.221212.co@mhssce.ac.in",
            "name": "Shams Baria",
            "certificate_path": "certificates/participants/shamsbaria.pdf"
        },
        {
            "email": "kaif.221459.it@mhssce.ac.in",
            "name": "Ansari Mohd Kaif",
            "certificate_path": "certificates/participants/ansarimohdkaif.pdf"
        },
        {
            "email": "aparajita2419@gmail.com",
            "name": "Aparajita Singh",
            "certificate_path": "certificates/participants/aparajitasingh.pdf"
        },
        {
            "email": "aadnanq22comp@student.mes.ac.in",
            "name": "Adnan Ansar",
            "certificate_path": "certificates/participants/adnanansar.pdf"
        },
        {
            "email": "hujaifa.221444.it@mhssce.ac.in",
            "name": "Shaikh Hujaifa",
            "certificate_path": "certificates/participants/shaikhhujaifajaved.pdf"
        },
        {
            "email": "hendrejatinpay@gmail.com",
            "name": "Jatin Nitin Hendre",
            "certificate_path": "certificates/participants/jatinnitinhendre.pdf"
        },
        {
            "email": "vatdpatel@gmail.com",
            "name": "Vatsal Patel",
            "certificate_path": "certificates/participants/vatsalpatel.pdf"
        },
        {
            "email": "ayushmohite0811@gmail.com",
            "name": "Ayush Mohite",
            "certificate_path": "certificates/participants/ayushmohite.pdf"
        },
        {
            "email": "swayambhoir579@gmail.com",
            "name": "Swayam Kabir Bhoir",
            "certificate_path": "certificates/participants/swayamkabirbhoir.pdf"
        },
        {
            "email": "223vedant0059@dbit.in",
            "name": "Vedant Apraj",
            "certificate_path": "certificates/participants/vedantapraj.pdf"
        },
        {
            "email": "aroratejjan7@gmail.com",
            "name": "Tejjan Arora",
            "certificate_path": "certificates/participants/tejjanarora.pdf"
        },
        {
            "email": "farhan.241259.co@mhssce.ac.in",
            "name": "Siddiqui Mohd Farhan",
            "certificate_path": "certificates/participants/siddiquimohdfarhan.pdf"
        },
        {
            "email": "mr.rajbhadrabhanushali@gmail.com",
            "name": "Raj Bhanushali",
            "certificate_path": "certificates/participants/rajbhanushali.pdf"
        },
        {
            "email": "kvijay2a3v@gmail.com",
            "name": "Aniket Kamble",
            "certificate_path": "certificates/participants/aniketkamble.pdf"
        },
        {
            "email": "anujmishra200421@gmail.com",
            "name": "Anuj Mishra",
            "certificate_path": "certificates/participants/anujmishra.pdf"
        }
    ]
    
    # Organizers data
    organizers_data = [
        {
            "email": "rahil.232870.ci@mhssce.ac.in",
            "name": "Rahil Khan",
            "certificate_path": "certificates/organizers/rahilkhan.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "rugved.221235.co@mhssce.ac.in",
            "name": "Rugved Patil",
            "certificate_path": "certificates/organizers/rugvedpatil.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "ali.221204.co@mhssce.ac.in",
            "name": "Ali Ansari",
            "certificate_path": "certificates/organizers/aliansari.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "humayun.232863.ci@mhssce.ac.in",
            "name": "Humayun Khan",
            "certificate_path": "certificates/organizers/humayunkhan.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "gulamnabi.232865.ci@mhssce.ac.in",
            "name": "Gulamnabi Mundus",
            "certificate_path": "certificates/organizers/gulamnabimundus.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "om.231830.ci@mhssce.ac.in",
            "name": "Om Mishra",
            "certificate_path": "certificates/organizers/ommishra.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "maaz.242267.co@mhssce.ac.in",
            "name": "Maaz Khan",
            "certificate_path": "certificates/organizers/maazkhan.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "hammad.241257.co@mhssce.ac.in",
            "name": "Hammad Siddique",
            "certificate_path": "certificates/organizers/hammadsiddique.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "adarsh.241855.ci@mhssce.ac.in",
            "name": "Adarsh Sharma",
            "certificate_path": "certificates/organizers/aadarshsharma.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "zehra.231757.cs@mhssce.ac.in",
            "name": "Zehra Shaikh",
            "certificate_path": "certificates/organizers/zehrashaikh.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "hannan.231211.co@mhssce.ac.in",
            "name": "Hannan Shemle",
            "certificate_path": "certificates/organizers/hannanshemle.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "faiz.221231.co@mhssce.ac.in",
            "name": "Faiz Ahmed",
            "certificate_path": "certificates/organizers/faizahmed.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "inshiraah.232263.co@mhssce.ac.in",
            "name": "Inshiraah Khan",
            "certificate_path": "certificates/organizers/inshiraahkhan.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        },
        {
            "email": "fatima.241844.ci@mhssce.ac.in",
            "name": "Fatima Shaikh",
            "certificate_path": "certificates/organizers/fatimashaikh.pdf",
            "event_stats": {
                "total_participants": 30,
                "problems_solved": 23,
                "completion_rate": "80%"
            }
        }
    ]
    
    # Track all failed emails across all groups
    all_failed_emails = []
    total_success = 0
    total_emails = 44
    
    # Send emails to different groups with 1-minute breaks
    print("=" * 60)
    print("🏆 SENDING WINNER EMAILS (3 emails)")
    success_count, failed_emails = sender.send_batch_emails(EmailType.WINNER, winners_data)
    total_success += success_count
    all_failed_emails.extend(failed_emails)
    
    print("\n" + "=" * 60)
    print(f"⏰ BREAK: Waiting {sender.delay_between_groups} seconds between groups...")
    time.sleep(sender.delay_between_groups)
    
    print("\n" + "=" * 60)
    print("🎉 SENDING PARTICIPANT EMAILS (27 emails)")
    success_count, failed_emails = sender.send_batch_emails(EmailType.PARTICIPANT, participants_data)
    total_success += success_count
    all_failed_emails.extend(failed_emails)
    
    print("\n" + "=" * 60)
    print(f"⏰ BREAK: Waiting {sender.delay_between_groups} seconds between groups...")
    time.sleep(sender.delay_between_groups)
    
    print("\n" + "=" * 60)
    print("👥 SENDING ORGANIZER EMAILS (14 emails)")
    success_count, failed_emails = sender.send_batch_emails(EmailType.ORGANIZER, organizers_data)
    total_success += success_count
    all_failed_emails.extend(failed_emails)
    
    print("\n" + "=" * 80)
    print("🎊 [CAMPAIGN COMPLETE] All email campaigns finished!")
    print("=" * 80)
    print(f"📧 Total emails processed: {total_emails}")
    print(f"✅ Successfully sent: {total_success}")
    print(f"❌ Failed to send: {len(all_failed_emails)}")
    print(f"📈 Success rate: {(total_success/total_emails)*100:.1f}%")
    
    # Display comprehensive failed emails summary
    if all_failed_emails:
        print(f"\n🚨 [FAILED EMAILS SUMMARY] {len(all_failed_emails)} emails need attention:")
        print("=" * 80)
        for i, failed in enumerate(all_failed_emails, 1):
            print(f"{i}. Name: {failed['name']}")
            print(f"   Email: {failed['email']}")
            print(f"   Error: {failed['error']}")
            print("-" * 60)
        print("\n💡 [RETRY SUGGESTION] You can copy these email addresses and try sending manually or re-run the script.")
    else:
        print(f"\n🎉 [PERFECT SUCCESS] All {total_emails} emails sent successfully!")
        print("🚀 No failed emails - Campaign completed flawlessly!")
    
    print("\n⏰ Campaign execution completed!")
