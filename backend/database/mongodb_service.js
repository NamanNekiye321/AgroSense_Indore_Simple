// ============================================================
// FILE: mongodb_service.js
// WHO MADE THIS: Naman
// WHAT IT DOES: Handles connecting to MongoDB database.
//               Features a resilient architecture:
//               - Real MongoDB Mongoose ODM when server is reachable
//               - Graceful In-Memory buffer fallback if DB is offline
//               - Zero-downtime farmer consultations
// ============================================================

const mongoose = require('mongoose');
const Recommendation = require('./models/Recommendation');

// MongoDB URI from environment or default local port 27017
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/agrosense_indore';

let isConnected = false;
const inMemoryHistory = []; // Fallback circular buffer for offline resilience

// --- CONNECT TO MONGODB ---
async function connectDB() {
    try {
        await mongoose.connect(MONGODB_URI, {
            serverSelectionTimeoutMS: 4000 // Fast 4-second timeout if daemon not active
        });
        isConnected = true;
        console.log('✅ Connected to MongoDB successfully (Database: agrosense_indore)!');
    } catch (error) {
        isConnected = false;
        console.warn('⚠️  Could not connect to MongoDB. Running in resilient In-Memory Fallback mode.');
        console.warn('   Start mongod locally or set MONGODB_URI in your .env file.');
    }
}

// Track disconnection / reconnection events
mongoose.connection.on('connected', () => { isConnected = true; });
mongoose.connection.on('disconnected', () => { isConnected = false; });

// --- SAVE A NEW RECOMMENDATION ---
async function saveRecommendation(data) {
    if (isConnected) {
        try {
            const newRecord = new Recommendation(data);
            const saved = await newRecord.save();
            console.log('💾 Saved recommendation to MongoDB. ID:', saved._id);
            return saved;
        } catch (error) {
            console.error('Could not save to MongoDB, saving to memory buffer:', error.message);
        }
    }

    // Resilient fallback storage:
    const fallbackRecord = {
        _id: 'mem_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 4),
        ...data,
        created_at: new Date()
    };
    inMemoryHistory.unshift(fallbackRecord);
    if (inMemoryHistory.length > 50) inMemoryHistory.pop(); // Cap at 50 records
    console.log('💾 Saved recommendation to resilient In-Memory ledger. ID:', fallbackRecord._id);
    return fallbackRecord;
}

// --- GET RECENT RECOMMENDATIONS ---
async function getHistory(limit = 20) {
    if (isConnected) {
        try {
            const records = await Recommendation
                .find()
                .sort({ created_at: -1 })
                .limit(limit);
            if (records && records.length > 0) return records;
        } catch (error) {
            console.error('Could not read from MongoDB, falling back to memory buffer:', error.message);
        }
    }
    return inMemoryHistory.slice(0, limit);
}

// --- GET DATABASE STATUS ---
function getStatus() {
    return {
        connected: isConnected,
        engine: isConnected ? 'MongoDB (Active)' : 'In-Memory Fallback Mode',
        uri: isConnected ? MONGODB_URI : 'Local Memory Buffer'
    };
}

module.exports = { connectDB, saveRecommendation, getHistory, getStatus };
