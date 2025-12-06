const sqlite3 = require("sqlite3").verbose();
const path = require("path");

const dbPath = path.resolve(__dirname, "app.db");
const db = new sqlite3.Database(dbPath);

db.serialize(() => {
    // Stores user's code snapshots
    db.run(`
        CREATE TABLE IF NOT EXISTS code_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            language TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    `);

    // Stores AI chat messages (explain, full fix, etc.)
    db.run(`
        CREATE TABLE IF NOT EXISTS ai_chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            ai_response TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    `);

    // User’s saved projects (multiple files)
    db.run(`
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT,
            code TEXT,
            language TEXT,
            is_favorite INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    `);

    // Store full fix versions for history view
    db.run(`
        CREATE TABLE IF NOT EXISTS full_fix_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_code TEXT,
            fixed_code TEXT,
            language TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    `);
});

module.exports = db;
