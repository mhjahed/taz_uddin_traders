# Deployment Guide for TAZ UDDIN TRADERS

## Pre-deployment Checklist
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up email configuration
- [ ] Configure media file storage
- [ ] Run security checks
- [ ] Create database backups
- [ ] Test with production settings

## Environment Variables Required
- SECRET_KEY
- DATABASE_URL
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

## Post-deployment Steps
1. Run migrations
2. Collect static files
3. Create superuser
4. Load initial data
5. Test all features