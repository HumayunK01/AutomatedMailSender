# Code Feast 4.0 Automated Email Sender 📧

A comprehensive automated email system for sending certificates and appreciation emails to Code Feast 4.0 participants, winners, and organizers.

## 🎯 Overview

This system automatically sends personalized HTML emails with PDF certificates to:
- **Winners** (3 people) - Congratulatory emails with winner certificates
- **Participants** (27 people) - Appreciation emails with participation certificates  
- **Organizers** (14 people) - Thank you emails with organizer certificates

**Total**: 44 emails with professional HTML templates and PDF attachments.

## 🚀 Features

### ✨ Email Templates
- **Beautiful HTML emails** with responsive design
- **Custom styling** for each recipient type (winners, participants, organizers)
- **Personalized content** with names and achievements
- **Professional branding** with gradients and modern UI

### 📊 Smart Rate Limiting
- **30-second delays** between individual emails
- **60-second breaks** between different groups
- **Safe sending rates** to prevent Gmail blocking
- **Progress tracking** with time estimates

### 🔧 Debug & Monitoring
- **Real-time progress** updates
- **Failed email tracking** with detailed error messages
- **Comprehensive statistics** (success rate, totals)
- **Retry suggestions** for failed sends

### 📁 Certificate Management
- **Organized folder structure** for certificates
- **Automatic PDF attachment** with custom filenames
- **File validation** before sending

## 📋 Prerequisites

1. **Python 3.7+** installed
2. **Gmail account** with App Password enabled
3. **Certificate files** properly organized in folders

### Gmail Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Update the credentials in `CodeFeast.py`

## 📁 Project Structure

```
automatedemailsender/
├── CodeFeast.py              # Main email sender script
├── example_sender.py         # Test script with sample emails
├── README.md                 # This documentation
├── .gitignore               # Git ignore patterns
└── certificates/            # Certificate storage
    ├── winners/             # Winner certificates (3 files)
    ├── participants/        # Participant certificates (27 files)
    └── organizers/          # Organizer certificates (14 files)
```

## 🎨 Email Types & Templates

### 🏆 Winner Emails
- **Subject**: "Code Feast 4.0 - Congratulations on Your Victory! 🏆"
- **Features**: 
  - Medal emoji based on ranking (🥇🥈🥉)
  - Achievement unlocked section
  - Position announcement (1st, 2nd, 3rd Place)
- **Next Steps**: Certificate download, social media sharing

### 🎉 Participant Emails  
- **Subject**: "Code Feast 4.0 - Thank You for Participating! 🎉"
- **Features**:
  - Appreciation message
  - Community contribution acknowledgment
- **Next Steps**: Certificate download, continued learning

### 👥 Organizer Emails
- **Subject**: "Code Feast 4.0 - Thank You for Organizing! 🎉"  
- **Features**:
  - Event statistics dashboard
  - Appreciation message
  - Professional organizer certificate
- **Next Steps**: Documentation, planning improvements

## ⚙️ Configuration

### Environment Variables (.env file)
```bash
# Email Configuration
SENDER_EMAIL=your_sending_email_here
SENDER_PASSWORD=your_gmail_app_password_here
EVENT_NAME=your_event_name_here

# Timing Configuration (in seconds)
DELAY_BETWEEN_EMAILS=30
DELAY_BETWEEN_GROUPS=60

# Email Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

# Debug Settings
DEBUG_MODE=false
```

### Setup Instructions
1. Copy `env.example` to `.env`
2. Replace `your_gmail_app_password_here` with your actual Gmail App Password
3. Adjust timing settings if needed
4. Optionally modify event name and email settings

## 🚀 Usage

### Quick Start
```bash
# Clone the repository
git clone https://github.com/HumayunK01/AutomatedMailSender.git

# Navigate to project directory
cd AutomatedMailSender

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment file
cp env.example .env
# Edit .env file with your Gmail credentials

# Run the main script
python CodeFeast.py
```

### Test Mode
```bash
# Run with sample emails first
python example_sender.py
```

## 📊 Expected Output

### During Execution
```
============================================================
🏆 SENDING WINNER EMAILS (3 emails)
[INFO] Starting batch email send for winners...
[INFO] Total emails to send: 3
[INFO] Estimated time: 90 seconds (1 minutes 30 seconds)

[SUCCESS] Email sent to Aarzoo Nazim Asar (arzoo.232262.co@mhssce.ac.in)
[PROGRESS] 1/3 emails sent successfully
[WAIT] Waiting 30 seconds before next email...
...
```

### Final Summary
```
================================================================================
🎊 [CAMPAIGN COMPLETE] All email campaigns finished!
================================================================================
📧 Total emails processed: 44
✅ Successfully sent: 44
❌ Failed to send: 0
📈 Success rate: 100.0%

🎉 [PERFECT SUCCESS] All 44 emails sent successfully!
🚀 No failed emails - Campaign completed flawlessly!
```

### If Failures Occur
```
🚨 [FAILED EMAILS SUMMARY] 2 emails need attention:
================================================================================
1. Name: John Doe
   Email: john@example.com
   Error: Connection timeout
------------------------------------------------------------
2. Name: Jane Smith  
   Email: jane@example.com
   Error: Invalid email address
------------------------------------------------------------

💡 [RETRY SUGGESTION] You can copy these email addresses and try sending manually or re-run the script.
```

## ⏱️ Timing & Performance

### Estimated Execution Time
- **Winners**: ~3 minutes (3 emails + delays)
- **Break**: 1 minute
- **Participants**: ~14.5 minutes (27 emails + delays)
- **Break**: 1 minute  
- **Organizers**: ~7.5 minutes (14 emails + delays)
- **Total**: ~27 minutes

### Gmail Rate Limits
- **Daily Limit**: 2,000 emails (Google Workspace)
- **Rate Limit**: ~100-150 emails per minute
- **Our Rate**: 2 emails per minute (very safe)

## 🛡️ Safety Features

### Rate Limiting Protection
- Conservative 30-second delays between emails
- 60-second breaks between groups
- Well below Gmail's rate limits

### Error Handling
- Unicode encoding error handling
- Retry mechanism for failed sends
- Detailed error logging
- Graceful failure recovery

### File Validation
- Certificate file existence checks
- Warning messages for missing files
- Detailed attachment logging

## 🔧 Troubleshooting

### Common Issues

#### Authentication Errors
```
[ERROR] Error sending email: Authentication failed
```
**Solution**: Check Gmail App Password and 2FA setup

#### File Not Found
```
[WARNING] Certificate file not found: certificates/winners/example.pdf
```
**Solution**: Verify certificate files exist in correct folders

#### Encoding Errors
```
[ERROR] Encoding error: 'charmap' codec can't encode character
```
**Solution**: Script automatically handles this with UTF-8 fallback

#### Rate Limiting
```
[ERROR] Quota exceeded
```
**Solution**: Wait 24 hours or reduce sending frequency

## 📝 Customization

### Adding New Recipients
1. Add recipient data to appropriate array in `CodeFeast.py`
2. Ensure certificate file exists in correct folder
3. Follow naming convention: `firstname.lastname.pdf`

### Modifying Templates
- Edit `generate_*_content()` methods for email content
- Modify `get_email_config()` for styling and colors
- Update `generate_next_steps()` for action items

### Changing Delays
```python
# In send_batch_emails method
time.sleep(30)  # Change to desired seconds between emails

# In main execution
time.sleep(60)  # Change to desired seconds between groups
```

## 🎯 Best Practices

### Before Running
1. ✅ Test with `example_sender.py` first
2. ✅ Verify all certificate files exist
3. ✅ Check Gmail credentials
4. ✅ Ensure stable internet connection

### During Execution
1. 📱 Monitor console output for errors
2. ⏰ Don't interrupt the process
3. 📊 Note any failed emails for follow-up

### After Completion
1. 📋 Review final statistics
2. 🔄 Retry any failed emails if needed
3. 📧 Verify emails were received
4. 🎉 Celebrate successful campaign!

## 📞 Support

### Contact Information
- **Email**: programmersclub@mhssce.ac.in
- **Event**: Code Feast 4.0
- **Organization**: Programmers Club

### Quick Help
- Check Gmail App Password setup
- Verify certificate file names match code
- Ensure stable internet during sending
- Monitor console output for errors

## 🎖️ Recipients Summary

### 🏆 Winners (3)
1. **Aarzoo Nazim Asar** - 1st Place
2. **Mohammed Anas Nathani** - 2nd Place  
3. **Mohammed Saif Shaikh** - 3rd Place

### 🎉 Participants (27)
Complete list of 27 participants with their certificates

### 👥 Organizers (14)
Complete organizing team including:
- Rahil Khan, Rugved Patil, Ali Ansari
- Humayun Khan, Gulamnabi Mundus, Om Mishra
- Maaz Khan, Hammad Siddique, Adarsh Sharma
- Zehra Shaikh, Hannan Shemle, Faiz Ahmed
- Inshiraah Khan, Fatima Shaikh

---

## 📜 License

This project is created for Code Feast 4.0 event by Programmers Club.

## 🚀 Ready to Send!

Your automated email system is configured and ready to deliver professional certificates to all Code Feast 4.0 participants. Run `python CodeFeast.py` when you're ready to begin the campaign!

**Estimated completion time: 27 minutes**  
**Success rate: Expected 100%**  
**Total impact: 44 happy recipients! 🎉**
