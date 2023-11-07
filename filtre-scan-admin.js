
const fs = require('fs');
const path = require('path');
const parse = require('csv-parse/lib/sync');
const moment = require('moment');

// Function to load data from CSV files
function loadData(filePath) {
    const content = fs.readFileSync(filePath);
    const records = parse(content, {
        columns: true,
        skip_empty_lines: true
    });
    return records;
}

// Function to convert date string to Moment object
function parseDate(dateString) {
    return moment(dateString, 'DD/MM/YYYY HH:mm');
}

// Modified function to be exported and used by an API route
async function executeScript() {
    try {
        // Load the data from the files
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

        // Prepare intervals for each participant
        const participantsIntervals = export1Data.reduce((acc, { Prenom, Date }) => {
            if (!acc[Prenom]) {
                acc[Prenom] = [];
            }
            acc[Prenom].push(Date);
            return acc;
        }, {});

        // Transform lists of dates into tuples (entry, exit)
        for (const [prenom, dates] of Object.entries(participantsIntervals)) {
            participantsIntervals[prenom] = [];
            for (let i = 0; i < dates.length; i += 2) {
                participantsIntervals[prenom].push({ entree: dates[i], sortie: dates[i + 1] });
            }
        }

        // Calculate presence for each participant and each conference
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

                // Check if the participant attended at least 50% of the conference
                if (tempsPresence.asMilliseconds() >= conf.duree.asMilliseconds() * 0.5) {
                    resultats.push({ Conference: conf.Conference, Nom: participant });
                }
            }
        }

        // Return the results
        return resultats;
    } catch (error) {
        // Handle possible errors
        console.error('Error executing the script:', error);
        throw error; // Throw the error so the API can respond to it
    }
}

module.exports = executeScript;
