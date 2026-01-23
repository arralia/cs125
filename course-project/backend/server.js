
// this is some template code for a node.js server genereated with gemini ai
// just to use as a starting point for our backend

import express from "express";
import cors from "cors";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json()); // Parses incoming JSON requests

// Health check route
app.get("/health", (req, res) => {
    res.status(200).json({ status: "ok", message: "Server is running smoothly" });
});

// Sample API route
app.get("/api", (req, res) => {
    res.json({ message: "Welcome to the API!" });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: "Something went wrong!" });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});

