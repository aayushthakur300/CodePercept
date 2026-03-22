// db.js
const { Sequelize, DataTypes } = require("sequelize");
const path = require("path");

const sequelize = new Sequelize({
  dialect: "sqlite",
  storage: path.join(__dirname, "codesense.db"),
  logging: false,
});

const User = sequelize.define("User", {
  provider: { type: DataTypes.STRING },
  providerId: { type: DataTypes.STRING },
  email: { type: DataTypes.STRING },
  name: { type: DataTypes.STRING },
  avatar: { type: DataTypes.STRING },
});

const CodeHistory = sequelize.define("CodeHistory", {
  userId: { type: DataTypes.INTEGER },
  code: { type: DataTypes.TEXT },
  language: { type: DataTypes.STRING },
  result_json: { type: DataTypes.TEXT }, // store AI output
});

const ChatMessage = sequelize.define("ChatMessage", {
  userId: { type: DataTypes.INTEGER },
  sender: { type: DataTypes.STRING },
  message: { type: DataTypes.TEXT },
  timestamp: { type: DataTypes.DATE, defaultValue: DataTypes.NOW },
});

User.hasMany(CodeHistory, { foreignKey: "userId" });
User.hasMany(ChatMessage, { foreignKey: "userId" });
CodeHistory.belongsTo(User, { foreignKey: "userId" });
ChatMessage.belongsTo(User, { foreignKey: "userId" });

async function initDB() {
  await sequelize.sync();
}

module.exports = {
  sequelize,
  initDB,
  User,
  CodeHistory,
  ChatMessage,
};
