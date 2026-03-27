const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Hello from app");
});

app.get("/api", (req, res) => {
  res.json({ time: new Date() });
});

app.listen(3000, () => console.log("App running on 3000"));
