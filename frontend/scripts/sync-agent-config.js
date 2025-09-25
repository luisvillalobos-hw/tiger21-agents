#!/usr/bin/env node
/**
 * Sync Agent Engine configuration from backend to frontend
 * This script reads the backend agent_engine_config.json and updates the frontend .env
 */

const fs = require('fs');
const path = require('path');

function syncAgentConfig() {
  try {
    // Read backend configuration
    const backendConfigPath = path.join(__dirname, '..', '..', 'backend', 'agent_engine_config.json');

    if (!fs.existsSync(backendConfigPath)) {
      console.error('❌ Backend agent_engine_config.json not found at:', backendConfigPath);
      process.exit(1);
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