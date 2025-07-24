@echo off
echo 🚀 Deploying Personality Test to Railway...

REM Check if railway CLI is installed
where railway >nul 2>nul
if %errorlevel% neq 0 (
    echo 📦 Installing Railway CLI...
    npm install -g @railway/cli
)

REM Login to Railway
echo 🔐 Logging into Railway...
railway login

REM Deploy the project
echo 📤 Starting deployment...
railway deploy

echo ✅ Deployment completed!
echo 🌐 Your app should be available at your Railway project URL
echo 🔧 Admin Dashboard: https://your-app.railway.app/admin.html
echo 👤 Admin Login: admin / admin123

pause
