#!/usr/bin/env node
/**
 * Sync Agent Engine configuration from backend to frontend
 * This script reads the backend agent_engine_config.json and updates the frontend .env
 */

const fs = require('fs');
const path = require('path');

function syncAgentConfig() {
  try {
    // Try multiple possible paths for backend configuration
    const possiblePaths = [
      // Cloud Build: copied to frontend directory
      path.join(__dirname, '..', 'backend-config.json'),
      // Local development: frontend/scripts -> backend/
      path.join(__dirname, '..', '..', 'backend', 'agent_engine_config.json'),
      // Cloud Build: might be at root level
      path.join(__dirname, '..', '..', '..', 'backend', 'agent_engine_config.json'),
      // Alternative: relative from frontend directory
      path.join(process.cwd(), '..', 'backend', 'agent_engine_config.json'),
      // Direct relative path
      '../backend/agent_engine_config.json',
      // Current working directory
      path.join(process.cwd(), 'backend', 'agent_engine_config.json')
    ];

    let backendConfigPath = null;

    for (const testPath of possiblePaths) {
      const resolvedPath = path.resolve(testPath);
      console.log(`🔍 Checking for backend config at: ${resolvedPath}`);
      if (fs.existsSync(resolvedPath)) {
        backendConfigPath = resolvedPath;
        console.log(`✅ Found backend config at: ${backendConfigPath}`);
        break;
      }
    }

    if (!backendConfigPath) {
      console.log('⚠️ Backend agent_engine_config.json not found. Using fallback values.');
      console.log('This is normal in Cloud Build if agent config is provided via environment variables.');

      // Create a minimal .env with current environment variables
      const envPath = path.join(__dirname, '..', '.env');
      const fallbackEnv = [
        'VITE_GOOGLE_CLOUD_PROJECT=tiger21-demo',
        'VITE_GOOGLE_CLOUD_LOCATION=us-central1',
        'VITE_AGENT_ENGINE_ID=7562269452029394944'
      ].join('\n');

      fs.writeFileSync(envPath, fallbackEnv);
      console.log('✅ Created .env with fallback values');
      return;
    }

    const backendConfig = JSON.parse(fs.readFileSync(backendConfigPath, 'utf-8'));

    console.log('📖 Found backend config:');
    console.log(`  - Agent Engine ID: ${backendConfig.agent_engine_id}`);
    console.log(`  - Project: ${backendConfig.project_id}`);
    console.log(`  - Location: ${backendConfig.location}`);

    // Update frontend .env file
    const envPath = path.join(__dirname, '..', '.env');
    let envContent = '';

    if (fs.existsSync(envPath)) {
      envContent = fs.readFileSync(envPath, 'utf-8');
    }

    // Update or add environment variables
    const updates = {
      'VITE_GOOGLE_CLOUD_PROJECT': backendConfig.project_id,
      'VITE_GOOGLE_CLOUD_LOCATION': backendConfig.location,
      'VITE_AGENT_ENGINE_ID': backendConfig.agent_engine_id
    };

    let updatedContent = envContent;

    Object.entries(updates).forEach(([key, value]) => {
      const regex = new RegExp(`^${key}=.*$`, 'm');
      const newLine = `${key}=${value}`;

      if (regex.test(updatedContent)) {
        updatedContent = updatedContent.replace(regex, newLine);
        console.log(`✅ Updated ${key}=${value}`);
      } else {
        updatedContent += (updatedContent ? '\n' : '') + newLine;
        console.log(`✅ Added ${key}=${value}`);
      }
    });

    fs.writeFileSync(envPath, updatedContent);

    console.log('🎉 Successfully synced agent configuration!');
    console.log(`📝 Updated ${envPath}`);

  } catch (error) {
    console.error('❌ Error syncing config:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  syncAgentConfig();
}

module.exports = { syncAgentConfig };