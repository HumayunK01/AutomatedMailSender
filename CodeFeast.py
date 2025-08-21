import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from enum import Enum
import sys
import time  # Added for delays
import json
import csv
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
        
        # Load dynamic event statistics from environment
        self.total_participants = int(os.getenv('TOTAL_PARTICIPANTS', '30'))
        self.problems_solved = int(os.getenv('PROBLEMS_SOLVED', '23'))
        self.completion_rate = os.getenv('COMPLETION_RATE', '80%')
        
        # Load data file paths
        self.winners_data_file = os.getenv('WINNERS_DATA_FILE', '')
        self.participants_data_file = os.getenv('PARTICIPANTS_DATA_FILE', '')
        self.organizers_data_file = os.getenv('ORGANIZERS_DATA_FILE', '')
        
        # Certificate path configuration
        self.certificate_base_path = os.getenv('CERTIFICATE_BASE_PATH', 'certificates')
        self.winners_cert_folder = os.getenv('WINNERS_CERT_FOLDER', 'winners')
        self.participants_cert_folder = os.getenv('PARTICIPANTS_CERT_FOLDER', 'participants')
        self.organizers_cert_folder = os.getenv('ORGANIZERS_CERT_FOLDER', 'organizers')
        
        # Email template customization
        self.organization_name = os.getenv('ORGANIZATION_NAME', 'Programmers Club')
        self.organization_tagline = os.getenv('ORGANIZATION_TAGLINE', 'Making coding accessible to everyone')
        self.copyright_year = os.getenv('COPYRIGHT_YEAR', '2025')
        
        # Batch processing options
        self.max_batch_size = int(os.getenv('MAX_BATCH_SIZE', '100'))
        self.retry_failed_emails = os.getenv('RETRY_FAILED_EMAILS', 'true').lower() == 'true'
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.dry_run_mode = os.getenv('DRY_RUN_MODE', 'false').lower() == 'true'
        
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
                    <div style="font-size: 24px; font-weight: bold; color: #6b21a8;">{stats.get('total_participants', self.total_participants)}</div>
                    <div style="color: #6b21a8; font-size: 14px;">Total Participants</div>
                </div>
                <div class="stats-item" style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #6b21a8;">{stats.get('problems_solved', self.problems_solved)}</div>
                    <div style="color: #6b21a8; font-size: 14px;">Problems Solved</div>
                </div>
                <div class="stats-item" style="background: white; padding: 15px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 24px; font-weight: bold; color: #6b21a8;">{stats.get('completion_rate', self.completion_rate)}</div>
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
                            <p style="margin: 0 0 5px; color: #6b7280; font-size: 14px; font-weight: 600;">{self.organization_name}</p>
                            <p style="margin: 10px 0 0; color: #9ca3af; font-size: 12px;">{self.organization_tagline}</p>
                        </div>
                    </div>
                    
                    <!-- Footer -->
                    <div class="footer-section" style="background: #f9fafb; padding: 20px 30px; border-top: 1px solid #e5e7eb; text-align: center;">
                        <p style="margin: 0; color: #6b7280; font-size: 12px; line-height: 1.4;">
                            This email was sent by {self.event_name} Team. If you have any questions, please contact us.<br>
                            © {self.copyright_year} {self.organization_name}. All rights reserved.
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
        # Dry run mode - just log what would be sent
        if self.dry_run_mode:
            print(f"[DRY RUN] Would send {email_type.value} email to {recipient_data['name']} ({recipient_data['email']})")
            if attachment_path:
                print(f"[DRY RUN] Would attach certificate: {attachment_path}")
            return True
            
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
        # Split into batches if max_batch_size is set
        if len(recipients_data) > self.max_batch_size:
            print(f"[INFO] Splitting {len(recipients_data)} emails into batches of {self.max_batch_size}")
            all_success = 0
            all_failed = []
            
            for i in range(0, len(recipients_data), self.max_batch_size):
                batch = recipients_data[i:i + self.max_batch_size]
                batch_num = (i // self.max_batch_size) + 1
                total_batches = (len(recipients_data) + self.max_batch_size - 1) // self.max_batch_size
                
                print(f"\n[BATCH {batch_num}/{total_batches}] Processing {len(batch)} emails...")
                success_count, failed_emails = self._send_batch_chunk(email_type, batch)
                all_success += success_count
                all_failed.extend(failed_emails)
                
                # Delay between batches (except for the last batch)
                if i + self.max_batch_size < len(recipients_data):
                    print(f"[WAIT] Waiting {self.delay_between_groups} seconds between batches...")
                    time.sleep(self.delay_between_groups)
            
            return all_success, all_failed
        else:
            return self._send_batch_chunk(email_type, recipients_data)
    
    def _send_batch_chunk(self, email_type, recipients_data):
        """Send a chunk of emails with individual delays"""
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

    def load_data_from_file(self, file_path, data_type):
        """Load recipient data from JSON or CSV file"""
        if not file_path or not os.path.exists(file_path):
            return []
        
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            
            elif file_extension == '.csv':
                data = []
                with open(file_path, 'r', encoding='utf-8', newline='') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Build certificate path dynamically
                        cert_folder = getattr(self, f"{data_type}_cert_folder")
                        cert_filename = self.generate_certificate_filename(row['name'])
                        row['certificate_path'] = os.path.join(self.certificate_base_path, cert_folder, cert_filename)
                        
                        # Add event stats for organizers if not present
                        if data_type == 'organizers' and 'event_stats' not in row:
                            row['event_stats'] = {
                                'total_participants': self.total_participants,
                                'problems_solved': self.problems_solved,
                                'completion_rate': self.completion_rate
                            }
                        data.append(row)
                return data
            
        except Exception as e:
            print(f"[ERROR] Failed to load data from {file_path}: {e}")
            return []
        
        return []
    
    def generate_certificate_filename(self, name):
        """Generate certificate filename from person's name"""
        # Remove spaces, convert to lowercase, and add .pdf extension
        filename = name.lower().replace(' ', '').replace('.', '') + '.pdf'
        return filename

    def get_recipients_data(self):
        """Get all recipient data from files only - no hardcoded fallbacks"""
        winners = self.load_data_from_file(self.winners_data_file, 'winners')
        participants = self.load_data_from_file(self.participants_data_file, 'participants')
        organizers = self.load_data_from_file(self.organizers_data_file, 'organizers')
        
        # Validate that all required files are loaded
        if not winners and self.winners_data_file:
            print(f"[WARNING] No winners data loaded from {self.winners_data_file}")
        if not participants and self.participants_data_file:
            print(f"[WARNING] No participants data loaded from {self.participants_data_file}")
        if not organizers and self.organizers_data_file:
            print(f"[WARNING] No organizers data loaded from {self.organizers_data_file}")
            
        # Show data file usage status
        print(f"[INFO] Data loaded: {len(winners)} winners, {len(participants)} participants, {len(organizers)} organizers")
        if not any([winners, participants, organizers]):
            print("[ERROR] No data files specified or loaded! Please check your .env configuration.")
            print("[INFO] Required environment variables:")
            print("  - WINNERS_DATA_FILE=data/winners.csv")
            print("  - PARTICIPANTS_DATA_FILE=data/participants.csv") 
            print("  - ORGANIZERS_DATA_FILE=data/organizers.json")
            
        return winners, participants, organizers



# Example usage
if __name__ == "__main__":
    # Initialize email sender (loads configuration from .env file)
    sender = CodeFeastEmailSender()
    
    # Load recipient data dynamically (from files or fallback to defaults)
    winners_data, participants_data, organizers_data = sender.get_recipients_data()
    
    # Track all failed emails across all groups
    all_failed_emails = []
    total_success = 0
    total_emails = len(winners_data) + len(participants_data) + len(organizers_data)
    
    # Validate we have data to send
    if total_emails == 0:
        print("\n❌ [ERROR] No email data loaded! Cannot proceed with campaign.")
        print("[INFO] Please ensure data files are properly configured in your .env file:")
        print("   WINNERS_DATA_FILE=data/winners.csv")
        print("   PARTICIPANTS_DATA_FILE=data/participants.csv")
        print("   ORGANIZERS_DATA_FILE=data/organizers.json")
        exit(1)
    
    # Send emails to different groups with breaks between them
    groups_to_send = []
    if len(winners_data) > 0:
        groups_to_send.append(("🏆 WINNERS", EmailType.WINNER, winners_data))
    if len(participants_data) > 0:
        groups_to_send.append(("🎉 PARTICIPANTS", EmailType.PARTICIPANT, participants_data))
    if len(organizers_data) > 0:
        groups_to_send.append(("👥 ORGANIZERS", EmailType.ORGANIZER, organizers_data))
    
    # Send emails for each group
    for i, (group_name, email_type, data) in enumerate(groups_to_send):
        if i > 0:  # Add break between groups (not before first group)
            print("\n" + "=" * 60)
            print(f"⏰ BREAK: Waiting {sender.delay_between_groups} seconds between groups...")
            time.sleep(sender.delay_between_groups)
        
        print("\n" + "=" * 60)
        print(f"{group_name} EMAILS ({len(data)} emails)")
        success_count, failed_emails = sender.send_batch_emails(email_type, data)
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
