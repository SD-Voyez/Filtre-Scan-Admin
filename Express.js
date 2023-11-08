const express = require('express');
const app = express();
const port = 3000;

// Ici, tu intégreras la fonction du script filtre-scan-admin.js
const filtreScanAdmin = require('./filtre-scan-admin');

app.use(express.static('public')); // pour servir ta page HTML

app.get('/execute-script', async (req, res) => {
    try {
        const result = await filtreScanAdmin();
        res.json({ success: true, result });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(port, () => {
    console.log(`Serveur lancé sur http://localhost:${port}`);
});
