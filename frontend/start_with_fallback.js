#!/usr/bin/env node
/**
 * Start Frontend with Fallback
 * Script untuk menjalankan frontend dengan error handling yang lebih baik
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Starting PT. Sanghiang Perkasa Frontend with Enhanced Error Handling');
console.log('=' * 60);

// Check if package.json exists
const packageJsonPath = path.join(__dirname, 'package.json');
if (!fs.existsSync(packageJsonPath)) {
  console.error('❌ package.json not found in frontend directory');
  process.exit(1);
}

// Check if node_modules exists
const nodeModulesPath = path.join(__dirname, 'node_modules');
if (!fs.existsSync(nodeModulesPath)) {
  console.log('📦 Installing dependencies...');
  const install = spawn('npm', ['install'], { 
    stdio: 'inherit',
    cwd: __dirname 
  });
  
  install.on('close', (code) => {
    if (code === 0) {
      console.log('✅ Dependencies installed successfully');
      startReactApp();
    } else {
      console.error('❌ Failed to install dependencies');
      process.exit(1);
    }
  });
} else {
  startReactApp();
}

function startReactApp() {
  console.log('🎯 Starting React development server...');
  console.log('📊 Dashboard will be available at: http://localhost:3000');
  console.log('🔧 Enhanced error handling enabled');
  console.log('⚠️  Fallback data will be used if API is unavailable');
  console.log('');
  
  const reactApp = spawn('npm', ['start'], { 
    stdio: 'inherit',
    cwd: __dirname 
  });
  
  reactApp.on('error', (error) => {
    console.error('❌ Error starting React app:', error.message);
    console.log('');
    console.log('🔧 Troubleshooting:');
    console.log('1. Make sure Node.js is installed');
    console.log('2. Check if port 3000 is available');
    console.log('3. Try: npm install && npm start');
    process.exit(1);
  });
  
  reactApp.on('close', (code) => {
    if (code !== 0) {
      console.error(`❌ React app exited with code ${code}`);
    }
  });
  
  // Handle process termination
  process.on('SIGINT', () => {
    console.log('\n🛑 Stopping React development server...');
    reactApp.kill('SIGINT');
    process.exit(0);
  });
  
  process.on('SIGTERM', () => {
    console.log('\n🛑 Stopping React development server...');
    reactApp.kill('SIGTERM');
    process.exit(0);
  });
}

// Show helpful information
console.log('💡 Tips:');
console.log('- If you see "Gagal memuat data PT. Sanghiang Perkasa", the app will use fallback data');
console.log('- Check browser console (F12) for detailed error information');
console.log('- API endpoints will be tried in order: 8000, 8001, test-route');
console.log('- Dashboard will always be functional with fallback data');
console.log(''); 