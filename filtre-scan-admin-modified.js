
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
        
        // Fonction principale
async function main() {
    // Charger les données des fichiers
    const horaireConfData = loadData(path.join(__dirname, 'horaire_conf.csv')).map(record => ({
        ...record,
        debut: parseDate(record.debut),
        fin: parseDate(record.fin),
        duree: moment.duration(parseDate(record.fin).diff(parseDate(record.debut)))
    }));
    const export1Data = loadData(path.join(__dirname, 'export1.csv')).map(record => ({
        ...record,
        Date: parseDate(record.Date)
    }));

    // Préparer les intervalles pour chaque participant
    const participantsIntervals = export1Data.reduce((acc, { Prenom, Date }) => {
        if (!acc[Prenom]) {
            acc[Prenom] = [];
        }
        acc[Prenom].push(Date);
        return acc;
    }, {});

    // Transformer les listes de dates en tuples (entrée, sortie)
    for (const [prenom, dates] of Object.entries(participantsIntervals)) {
        participantsIntervals[prenom] = [];
        for (let i = 0; i < dates.length; i += 2) {
            participantsIntervals[prenom].push({ entree: dates[i], sortie: dates[i + 1] });
        }
    }

    // Calculer la présence pour chaque participant et chaque conférence
    const resultats = [];

    for (const conf of horaireConfData) {
        for (const [participant, intervals] of Object.entries(participantsIntervals)) {
            let tempsPresence = moment.duration();

            for (const { entree, sortie } of intervals) {
                const debut = moment.max(entree, conf.debut);
                const fin = moment.min(sortie, conf.fin);
                const temps = moment.duration(fin.diff(debut));
                tempsPresence.add(temps);
            }

            // Vérifier si le participant a assisté à au moins 50% de la conférence
            if (tempsPresence.asMilliseconds() >= conf.duree.asMilliseconds() * 0.5) {
                resultats.push({ Conference: conf.Conference, Nom: participant });
            }
        }
    }

    // Afficher les résultats
    console.log('Resultats :', resultats);
}

main();
        // Ici tu renverrais le résultat du script
        return horaireConfData; // Exemple de ce que tu pourrais renvoyer
    } catch (error) {
        // Gérer les erreurs éventuelles
        console.error('Erreur lors de l\'exécution du script :', error);
        throw error; // Renvoyer l'erreur pour que l'API puisse y répondre
    }
}

module.exports = executeScript;
