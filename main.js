
document.getElementById('executeButton').addEventListener('click', function() {
    fetch('/execute-script')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Résultat du script :', data.result);
                // You can display the results on the page as needed.
                alert('Le script a été exécuté avec succès. Vérifiez la console pour les résultats.');
            } else {
                console.error('Erreur dans le script :', data.error);
            }
        })
        .catch(error => {
            console.error('Erreur dans la requête API :', error);
            alert('Une erreur est survenue lors de exécution du script.');
        });
});
