
const fs = require('fs');
const path = require('path');
const parse = require('csv-parse/lib/sync');
const moment = require('moment');

// Fonction pour charger les données des fichiers CSV
function loadData(filePath) {
    const content = fs.readFileSync(filePath);
    const records = parse(content, {
        columns: true,
        skip_empty_lines: true
    });
    return records;
}

// Fonction pour convertir la chaîne de date en objet Moment
function parseDate(dateString) {
    return moment(dateString, 'DD/MM/YYYY HH:mm');
}

// Fonction modifiée pour être exportée et utilisée par une route API
async function executeScript() {
    try {
        // Charger les données des fichiers
        const horaireConfData = loadData(path.join(__dirname, 'horaire_conf.csv')).map(record => ({
            ...record,
            debut: parseDate(record.debut),
            fin: parseDate(record.fin),
            duree: moment.duration(parseDate(record.fin).diff(parseDate(record.debut)))
        }));
        // ... (reste de la logique du script)

        // Ici tu renverrais le résultat du script
        return horaireConfData; // Exemple de ce que tu pourrais renvoyer
    } catch (error) {
        // Gérer les erreurs éventuelles
        console.error('Erreur lors de l\'exécution du script :', error);
        throw error; // Renvoyer l'erreur pour que l'API puisse y répondre
    }
}

module.exports = executeScript;
