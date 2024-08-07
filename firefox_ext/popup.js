let mapsEmbedApiKey = "AIzaSyCZwWelCX40BErYG34NLnUEeL2jOYEJyWo";
let mapsEmbedEndpoint = "https://www.google.com/maps/embed/v1/place";
let crackingGeoGuessrApi = 'http://127.0.0.1:5000'
let crackingGeoGuessrApiEndpoint =  `${crackingGeoGuessrApi}/cracking-geoguessr/get-recommendation`;

console.log(mapsEmbedApiKey);

document.addEventListener("DOMContentLoaded", function() {
  const captureButton = document.getElementById('capture-button');
  const recommendationP = document.getElementById('recommendation');
  const recommendationT = document.getElementById('recommendationText')
  
  captureButton.addEventListener("click", function() {
    browser.tabs.captureVisibleTab(function(screenshotDataUrl) {
      console.log(screenshotDataUrl);
      captureButton.disabled = true;
      captureButton.textContent = 'Cracking GeoGuessr...';
      recommendationP.style.display = 'none';

      let image = screenshotDataUrl.replace(/^.+,/, '');

      fetch(crackingGeoGuessrApiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'image' : image })
      })
      .then(response => {
          if (!response.ok) {
              throw new Error(`HTTP error indicated in response! Status code: ${response.status}.`);
          }
          return response.text();
      })
      .then(data => {
        let recommendation = data;

        let embeddedMap = document.getElementById("embedded-map-frame");
        embeddedMap.src = `${mapsEmbedEndpoint}?key=${mapsEmbedApiKey}&q=${recommendation}`;

        captureButton.textContent = 'Crack GeoGuessr'; 
        captureButton.disabled = false;
        recommendationT.textContent = recommendation;
        recommendationP.style.display = 'block';
      })
      .catch(error => {
          console.error('There has been a problem with your fetch operation:', error); 
      });
    });
  });
});